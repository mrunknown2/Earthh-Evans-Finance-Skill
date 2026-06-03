import json, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "fill_engine.py")

IREN = {
    "ticker": "IREN", "revenue_r0": 0.757, "ev": 22.6, "sector": "Software (System/Application)",
    "wacc": 0.095, "terminal_margin": 0.35, "terminal_g": 0.04, "terminal_roic": 0.15,
    "tax": 0.25, "horizon_n": 10, "hist_cagr": 0.60, "fade": 0.70, "tam": 150.0,
    "max_pen": 0.25, "abs_ceiling": 0.45, "buffer": 0.05, "price": 65.33,
    "shares_m": 357.38, "net_debt": -0.7, "consensus_fy1": 1.09,
    "analyst_target": 79.04, "analyst_range": "$29 - $100+", "no_write": True
}

def run(payload):
    p = subprocess.run([sys.executable, SCRIPT], input=json.dumps(payload),
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    return json.loads(p.stdout)

def approx(a, b, tol=0.005): return abs(a-b) <= tol

def test_iren_golden():
    r = run(IREN)
    assert approx(r["implied_cagr"], 0.320), r["implied_cagr"]
    assert approx(r["plausible_cagr"], 0.420), r["plausible_cagr"]
    assert approx(r["gap"], -0.100), r["gap"]
    assert "ถูก" in r["verdict"], r["verdict"]
    assert approx(r["zones"]["fair_value"], 143.56, tol=0.6), r["zones"]["fair_value"]
    assert approx(r["zones"]["strong_buy"], 97.42, tol=0.6), r["zones"]["strong_buy"]
    assert approx(r["zones"]["red_flag"], 301.30, tol=1.0), r["zones"]["red_flag"]

def test_tam_zero_uses_other_caps():
    payload = dict(IREN); payload["tam"] = 0
    r = run(payload)
    assert approx(r["plausible_cagr"], 0.420), r["plausible_cagr"]

def test_expensive_verdict():
    payload = dict(IREN); payload["price"] = 250.0; payload["ev"] = 90.0
    r = run(payload)
    assert "แพง" in r["verdict"], (r["verdict"], r["implied_cagr"])


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
