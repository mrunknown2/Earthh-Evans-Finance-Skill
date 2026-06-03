"""Known-answer tests for btc_calc. Standalone runner (PEP 668):
python3 test_btc_calc.py
Numbers hand-computed; the deterministic numeric gates of the desk (SD distance,
IV/HV gate, position sizing, pin distance) must not drift."""
import json, subprocess, sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "btc_calc.py")
sys.path.insert(0, HERE)
import btc_calc as C


def approx(a, b, tol=0.5):
    return abs(a - b) <= tol


def test_daily_sd_matches_desk_example():
    # Spot 74000, IV 30% -> SD ~ $1,162 (the agent's worked example)
    assert approx(C.daily_sd(74000, 0.30, 1), 1162.0), C.daily_sd(74000, 0.30, 1)


def test_sd_distance_pass_fail():
    near = C.sd_distance(spot=74000, strike=75500, iv=0.30, days=1)
    far = C.sd_distance(spot=74000, strike=76000, iv=0.30, days=1)
    assert approx(near["sd"], 1.29, tol=0.02), near
    assert near["passes_1_5"] is False
    assert approx(far["sd"], 1.72, tol=0.02), far
    assert far["passes_1_5"] is True


def test_iv_hv_gate_zones():
    assert C.iv_hv_gate(0.18, 0.20)["zone"] == "skip"        # 0.90 < 1.0
    assert C.iv_hv_gate(0.20, 0.20)["zone"] == "borderline"  # 1.00
    assert C.iv_hv_gate(0.23, 0.20)["zone"] == "ok"          # 1.15
    assert C.iv_hv_gate(0.40, 0.20)["zone"] == "sweet"       # 2.00 > 1.5
    assert C.iv_hv_gate(0.30, 0.20)["zone"] == "ok"          # 1.50 boundary -> ok
    assert approx(C.iv_hv_gate(0.30, 0.20)["ratio"], 1.5, tol=1e-6)


def test_iv_hv_gate_zero_hv():
    r = C.iv_hv_gate(0.30, 0.0)
    assert r["zone"] == "skip" or r["ratio"] is None  # undefined -> conservative


def test_position_size_margin_at_risk():
    # equity 10k, risk 1% -> $100 margin-at-risk; assume max loss 3x premium($50)=150/contract
    r = C.position_size(equity=10000, risk_pct=0.01, premium_per_contract=50,
                        max_loss_mult=3)
    assert approx(r["margin_at_risk"], 100.0, tol=1e-6), r
    assert approx(r["max_loss_per_contract"], 150.0, tol=1e-6), r
    assert approx(r["max_contracts"], 100.0 / 150.0, tol=1e-6), r


def test_position_size_caps_default_band():
    # risk_pct above the 0.5-1% default band -> flagged
    r = C.position_size(equity=10000, risk_pct=0.03, premium_per_contract=50,
                        max_loss_mult=3)
    assert r["above_default_band"] is True, r


def test_pin_distance_close_triggers():
    # within 0.3 SD of strike at decision time -> close now
    close = C.pin_distance(spot=74050, strike=74000, iv=0.30, days=1)  # 50 / ~1162 = 0.043 SD
    assert close["sd"] < 0.3 and close["close_now"] is True, close
    farr = C.pin_distance(spot=74600, strike=74000, iv=0.30, days=1)  # 600/1162 = 0.516
    assert farr["sd"] >= 0.3 and farr["close_now"] is False, farr


def test_cli_modes():
    for payload, key in [
        ({"mode": "sd", "spot": 74000, "strike": 76000, "iv": 0.30, "days": 1}, "sd"),
        ({"mode": "iv_hv", "iv": 0.30, "hv": 0.20}, "zone"),
        ({"mode": "size", "equity": 10000, "risk_pct": 0.01,
          "premium_per_contract": 50, "max_loss_mult": 3}, "margin_at_risk"),
        ({"mode": "pin", "spot": 74050, "strike": 74000, "iv": 0.30, "days": 1}, "close_now"),
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
            t(); print(f"PASS  {t.__name__}"); passed += 1
        except Exception as e:
            print(f"FAIL  {t.__name__}: {e}"); traceback.print_exc(); failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
