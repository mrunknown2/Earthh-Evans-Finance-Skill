"""Known-answer + determinism tests for portfolio_engine.
Standalone runner (PEP 668 blocks pytest on the dev box): python3 test_portfolio_engine.py
Every numeric assertion below is hand-computed so a wrong port of a formula fails."""
import json, subprocess, sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "portfolio_engine.py")
sys.path.insert(0, HERE)
import portfolio_engine as E


def approx(a, b, tol=1e-4):
    return abs(a - b) <= tol


# ---- cov matrix + portfolio vol (hand-computed) ----

def test_cov_matrix():
    cov = E.cov_matrix([0.2, 0.5], [[1.0, 0.0], [0.0, 1.0]])
    assert approx(cov[0][0], 0.04), cov
    assert approx(cov[1][1], 0.25), cov
    assert approx(cov[0][1], 0.0), cov


def test_cov_matrix_with_correlation():
    # 0.2 * 0.5 * 0.8 = 0.08
    cov = E.cov_matrix([0.2, 0.5], [[1.0, 0.8], [0.8, 1.0]])
    assert approx(cov[0][1], 0.08), cov[0][1]


def test_port_vol_uncorrelated_equal():
    # w=.5/.5, vol .2/.2, rho 0 -> sigma_p = sqrt(0.02) = 0.141421
    cov = E.cov_matrix([0.2, 0.2], [[1, 0], [0, 1]])
    assert approx(E.port_vol([0.5, 0.5], cov), 0.1414214), E.port_vol([0.5, 0.5], cov)


def test_port_vol_correlation_raises_vol():
    cov = E.cov_matrix([0.2, 0.2], [[1, 0.8], [0.8, 1]])
    # sigma_p^2 = 0.02 + 2*0.25*0.032 = 0.036 -> 0.1897367
    assert approx(E.port_vol([0.5, 0.5], cov), 0.1897367), E.port_vol([0.5, 0.5], cov)


# ---- risk contribution (the plugin's core) ----

def test_risk_contribution_sums_to_sigma():
    cov = E.cov_matrix([0.1, 0.5], [[1, 0], [0, 1]])
    rc = E.risk_contributions([0.7, 0.3], cov)
    sig = E.port_vol([0.7, 0.3], cov)
    assert approx(sum(x["rc"] for x in rc), sig), (sum(x["rc"] for x in rc), sig)
    assert approx(sum(x["rc_pct"] for x in rc), 1.0), sum(x["rc_pct"] for x in rc)


def test_risk_contribution_concentration_thesis():
    # 30% capital in a 5x-vol asset carries the majority of risk
    cov = E.cov_matrix([0.1, 0.5], [[1, 0], [0, 1]])
    rc = E.risk_contributions([0.7, 0.3], cov)
    # hand: sigma_p=sqrt(0.0274)=0.1655295; RC2=0.3*(0.25*0.3/sig)=0.135930; pct=0.82117
    assert approx(rc[1]["rc_pct"], 0.82117, tol=1e-3), rc[1]["rc_pct"]
    assert rc[1]["rc_pct"] > rc[1]["weight"], "risk share must exceed capital share"


# ---- diversification ratio / effective holdings / ENB / HHI ----

def test_diversification_ratio():
    cov = E.cov_matrix([0.2, 0.2], [[1, 0], [0, 1]])
    # DR = (0.5*0.2+0.5*0.2)/0.1414214 = 1.414214
    assert approx(E.diversification_ratio([0.5, 0.5], [0.2, 0.2], cov), 1.414214), \
        E.diversification_ratio([0.5, 0.5], [0.2, 0.2], cov)


def test_effective_holdings():
    assert approx(E.effective_holdings([0.5, 0.5]), 2.0)
    assert approx(E.effective_holdings([0.7, 0.3]), 1.0 / (0.49 + 0.09))  # 1.7241


def test_hhi():
    assert approx(E.hhi([0.5, 0.5]), 0.5)
    assert approx(E.hhi([1.0]), 1.0)


def test_enb_equals_inverse_herfindahl_of_risk_shares():
    # two equal risk shares -> ENB = 1/(0.25+0.25) = 2
    assert approx(E.enb([0.5, 0.5]), 2.0)
    assert approx(E.enb([0.82117, 0.17883]), 1.0 / (0.82117**2 + 0.17883**2), tol=1e-3)


def test_normalize_weights_from_dollars():
    w = E.normalize_weights([3000, 3000, 3000, 1000])
    assert approx(w[0], 0.3) and approx(w[3], 0.1), w


# ---- stress (exact) ----

def test_stress_return_exact():
    r = E.stress_return([0.6, 0.4], [-0.5, -0.2])
    assert approx(r, -0.38), r


def test_stress_null_shock_treated_as_na_flat():
    # BTC didn't exist in 2008 -> shock null -> treated as 0 (flat), flagged N/A,
    # must NOT crash on w*None.
    payload = {
        "mode": "stress",
        "assets": [{"name": "VOO", "weight": 0.5}, {"name": "BTC", "weight": 0.5}],
        "scenarios": [{"name": "GFC 2008", "shocks": {"VOO": -0.5, "BTC": None}}],
    }
    p = subprocess.run([sys.executable, SCRIPT], input=json.dumps(payload),
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    s = json.loads(p.stdout)["stress"][0]
    assert approx(s["portfolio_return"], 0.5 * -0.5 + 0.5 * 0.0), s  # -0.25
    assert s["na_assets"] == ["BTC"], s


# ---- Monte Carlo: DETERMINISM is the whole point ----

def test_monte_carlo_is_reproducible():
    cov = E.cov_matrix([0.2, 0.6], [[1, 0.3], [0.3, 1]])
    args = dict(w=[0.6, 0.4], vols=[0.2, 0.6], mus=[0.08, 0.20], cov=cov,
                horizon_days=252, n_paths=300, seed=42)
    a = E.monte_carlo(**args)
    b = E.monte_carlo(**args)
    assert a["p50"] == b["p50"], (a["p50"], b["p50"])
    assert a["var95"] == b["var95"], (a["var95"], b["var95"])
    assert a["expected_max_dd"] == b["expected_max_dd"]


def test_monte_carlo_seed_changes_result():
    cov = E.cov_matrix([0.2], [[1]])
    base = dict(w=[1.0], vols=[0.2], mus=[0.10], cov=cov, horizon_days=252, n_paths=300)
    a = E.monte_carlo(seed=1, **base)
    b = E.monte_carlo(seed=2, **base)
    assert a["p50"] != b["p50"], "different seeds should give different draws"


def test_monte_carlo_single_asset_median_sane():
    # GBM median gross return ~ exp(mu - 0.5 sigma^2) - 1 = exp(0.08)-1 = 0.0833
    cov = E.cov_matrix([0.2], [[1]])
    r = E.monte_carlo(w=[1.0], vols=[0.2], mus=[0.10], cov=cov,
                      horizon_days=252, n_paths=4000, seed=7)
    assert approx(r["p50"], 0.0833, tol=0.04), r["p50"]
    assert 0.0 <= r["prob_loss"] <= 1.0


# ---- frontier: deterministic random-weight envelope ----

def test_frontier_reproducible_and_minvol_le_current():
    cov = E.cov_matrix([0.15, 0.6], [[1, 0.2], [0.2, 1]])
    args = dict(vols=[0.15, 0.6], mus=[0.07, 0.20], cov=cov, n_samples=500, seed=11,
                current_w=[0.5, 0.5])
    a = E.frontier(**args)
    b = E.frontier(**args)
    assert a["min_vol"]["vol"] == b["min_vol"]["vol"], "frontier must be reproducible"
    assert a["min_vol"]["vol"] <= a["current"]["vol"] + 1e-9, \
        (a["min_vol"]["vol"], a["current"]["vol"])


# ---- CLI smoke (stdin JSON -> stdout JSON), mode=all ----

def test_cli_all_modes():
    payload = {
        "mode": "all", "seed": 42, "horizon_days": 252, "n_paths": 200, "n_samples": 200,
        "assets": [
            {"name": "VOO", "weight": 0.30, "vol": 0.16, "mu": 0.08},
            {"name": "QQQ", "weight": 0.30, "vol": 0.22, "mu": 0.10},
            {"name": "BTC", "weight": 0.30, "vol": 0.60, "mu": 0.20},
            {"name": "Cash", "weight": 0.10, "vol": 0.00, "mu": 0.04},
        ],
        "correlation": [[1, 0.85, 0.4, 0], [0.85, 1, 0.45, 0], [0.4, 0.45, 1, 0], [0, 0, 0, 1]],
        "scenarios": [{"name": "GFC 2008", "shocks": {"VOO": -0.51, "QQQ": -0.53, "BTC": -0.6, "Cash": 0.0}}],
        "rf": 0.04,
    }
    p = subprocess.run([sys.executable, SCRIPT], input=json.dumps(payload),
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    r = json.loads(p.stdout)
    # BTC (30% capital, 60% vol) must dominate risk
    btc = [x for x in r["risk"]["assets"] if x["name"] == "BTC"][0]
    assert btc["rc_pct"] > 0.5, btc["rc_pct"]
    assert r["risk"]["diversification_ratio"] > 1.0
    assert "p50" in r["montecarlo"] and "var95" in r["montecarlo"]
    assert approx(r["stress"][0]["portfolio_return"],
                  0.30*-0.51 + 0.30*-0.53 + 0.30*-0.6 + 0.10*0.0), r["stress"]
    assert "min_vol" in r["frontier"] and "max_sharpe" in r["frontier"]


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
