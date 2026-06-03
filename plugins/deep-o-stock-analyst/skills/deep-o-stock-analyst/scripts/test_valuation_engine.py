"""Known-answer tests for valuation_engine. Standalone runner (PEP 668 blocks
pytest on the dev box): python3 test_valuation_engine.py
Every number is hand-computed so a wrong port of a formula fails."""
import json, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "valuation_engine.py")
sys.path.insert(0, HERE)
import valuation_engine as V


def approx(a, b, tol=1e-3):
    return abs(a - b) <= tol


# ---- WACC (CAPM + market-value weights) ----

def test_wacc_capm():
    # coe = 0.04 + 1.2*0.05 = 0.10 ; cod_at = 0.05*0.75 = 0.0375
    # wacc = 0.8*0.10 + 0.2*0.0375 = 0.0875
    r = V.wacc(rf=0.04, beta=1.2, erp=0.05, equity_mv=800, debt_mv=200,
              pre_tax_cost_of_debt=0.05, tax=0.25)
    assert approx(r["wacc"], 0.0875), r
    assert approx(r["cost_of_equity"], 0.10), r
    assert approx(r["cost_of_debt_after_tax"], 0.0375), r


def test_wacc_with_country_risk_premium():
    r = V.wacc(rf=0.04, beta=1.0, erp=0.05, equity_mv=100, debt_mv=0,
              pre_tax_cost_of_debt=0.06, tax=0.25, crp=0.02)
    # all equity: coe = 0.04 + 1.0*(0.05+0.02) = 0.11 ; wacc = coe
    assert approx(r["wacc"], 0.11), r


# ---- DEEP score: 0-5 weighted -> 0-100 (the H2 fix) ----

def test_deep_score_normalized():
    s = {"demand": 4, "execution": 3, "economics": 5, "price": 2, "optionality": 4}
    # (4/5*25)+(3/5*20)+(5/5*20)+(2/5*20)+(4/5*15) = 20+12+20+8+12 = 72
    r = V.deep_score(s)
    assert approx(r["total"], 72.0), r
    assert r["verdict_band"] == "60-79", r


def test_deep_score_all_fives_is_100():
    s = {"demand": 5, "execution": 5, "economics": 5, "price": 5, "optionality": 5}
    r = V.deep_score(s)
    assert approx(r["total"], 100.0), r["total"]  # NOT 500 — normalization present
    assert r["verdict_band"] == ">=80", r


def test_deep_score_all_zeros_is_zero():
    s = {"demand": 0, "execution": 0, "economics": 0, "price": 0, "optionality": 0}
    assert approx(V.deep_score(s)["total"], 0.0)


def test_deep_score_verdict_bands():
    assert V.deep_score({"demand": 5, "execution": 5, "economics": 5, "price": 5, "optionality": 5})["verdict_band"] == ">=80"
    assert V.deep_score({"demand": 3, "execution": 3, "economics": 3, "price": 3, "optionality": 3})["verdict_band"] == "60-79"  # 60
    assert V.deep_score({"demand": 2, "execution": 2, "economics": 2, "price": 3, "optionality": 2})["verdict_band"] == "40-59"
    assert V.deep_score({"demand": 1, "execution": 1, "economics": 1, "price": 1, "optionality": 1})["verdict_band"] == "<40"  # 20


# ---- Reverse DCF: terminal-anchored (the H3 fix) ----

def test_reverse_dcf_terminal_anchored_matches_sibling():
    # Same math as the reverse-dcf-screener plugin; IREN golden -> implied CAGR ~0.320.
    r = V.reverse_dcf(ev=22.6, revenue0=0.757, wacc=0.095, g_terminal=0.04,
                      terminal_margin=0.35, terminal_roic=0.15, tax=0.25, horizon_n=10)
    assert approx(r["implied_cagr"], 0.320, tol=2e-3), r["implied_cagr"]
    assert r["implied_terminal_revenue"] > 0


def test_reverse_dcf_not_naive_ev_formula():
    # Guard against the old bug: implied revenue must NOT equal EV*(WACC-g)/margin.
    ev, w, g, m = 22.6, 0.095, 0.04, 0.35
    naive = ev * (w - g) / m
    r = V.reverse_dcf(ev=ev, revenue0=0.757, wacc=w, g_terminal=g,
                      terminal_margin=m, terminal_roic=0.15, tax=0.25, horizon_n=10)
    assert abs(r["implied_terminal_revenue"] - naive) > 1.0, \
        (r["implied_terminal_revenue"], naive)


# ---- DCF intrinsic value ----

def test_dcf_zero_growth_perpetuity():
    # Flat revenue 100, margin 20% -> NOPAT 15/yr; g=0 -> no reinvestment.
    # 5 explicit yrs at WACC 10%, terminal g 0 -> firm value = 15/0.10 = 150.
    r = V.dcf(revenue0=100.0, growths=[0, 0, 0, 0, 0], margins=[0.20] * 5,
              tax=0.25, sales_to_capital=[2.0] * 5, wacc=0.10,
              g_terminal=0.0, roic_terminal=0.10, net_debt=0.0, shares=10.0)
    assert approx(r["firm_value"], 150.0, tol=1e-2), r["firm_value"]
    assert approx(r["value_per_share"], 15.0, tol=1e-2), r["value_per_share"]


def test_dcf_net_debt_reduces_equity():
    r = V.dcf(revenue0=100.0, growths=[0]*5, margins=[0.20]*5, tax=0.25,
              sales_to_capital=[2.0]*5, wacc=0.10, g_terminal=0.0,
              roic_terminal=0.10, net_debt=50.0, shares=10.0)
    # equity = 150 - 50 = 100 -> 10/share
    assert approx(r["equity_value"], 100.0, tol=1e-2), r["equity_value"]
    assert approx(r["value_per_share"], 10.0, tol=1e-2), r["value_per_share"]


def test_dcf_reinvestment_drag():
    # With growth but low Sales-to-Capital, reinvestment eats FCFF -> firm value
    # lower than the same growth with no reinvestment need.
    hi_reinv = V.dcf(revenue0=100.0, growths=[0.10]*5, margins=[0.20]*5, tax=0.25,
                     sales_to_capital=[1.0]*5, wacc=0.10, g_terminal=0.02,
                     roic_terminal=0.12, net_debt=0.0, shares=10.0)
    lo_reinv = V.dcf(revenue0=100.0, growths=[0.10]*5, margins=[0.20]*5, tax=0.25,
                     sales_to_capital=[5.0]*5, wacc=0.10, g_terminal=0.02,
                     roic_terminal=0.12, net_debt=0.0, shares=10.0)
    assert hi_reinv["firm_value"] < lo_reinv["firm_value"], \
        (hi_reinv["firm_value"], lo_reinv["firm_value"])


# ---- CLI smoke ----

def test_cli_modes():
    for payload, key in [
        ({"mode": "wacc", "rf": 0.04, "beta": 1.2, "erp": 0.05, "equity_mv": 800,
          "debt_mv": 200, "pre_tax_cost_of_debt": 0.05, "tax": 0.25}, "wacc"),
        ({"mode": "deep", "scores": {"demand": 4, "execution": 3, "economics": 5,
          "price": 2, "optionality": 4}}, "total"),
        ({"mode": "reverse_dcf", "ev": 22.6, "revenue0": 0.757, "wacc": 0.095,
          "g_terminal": 0.04, "terminal_margin": 0.35, "terminal_roic": 0.15,
          "tax": 0.25, "horizon_n": 10}, "implied_cagr"),
    ]:
        p = subprocess.run([sys.executable, SCRIPT], input=json.dumps(payload),
                           capture_output=True, text=True)
        assert p.returncode == 0, p.stderr
        assert key in json.loads(p.stdout), (payload["mode"], json.loads(p.stdout))


if __name__ == "__main__":
    import traceback
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"FAIL  {t.__name__}: {e}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
