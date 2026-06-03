#!/usr/bin/env python3
"""BTC short-premium desk calculator — deterministic numeric gates only.

Reads JSON from stdin, prints JSON to stdout. Covers the QUANTITATIVE parts of the
desk that must not be eyeballed: SD distance, IV/HV gate, position sizing
(margin-at-risk), pin distance. Chart reading + the TRADE/SKIP/WAIT decision stay
with the vision model — this only does the arithmetic, deterministically.

stdlib only (no pip). Modes: "sd" | "iv_hv" | "size" | "pin".
NOT financial advice — short crypto options carry uncapped tail risk.
"""
import sys, json, math

DAY_FRACTION = 1.0 / 365.0


def daily_sd(spot, iv, days=1):
    """1-sigma move over `days` days: Spot · IV · √(days/365)."""
    return spot * iv * math.sqrt(days * DAY_FRACTION)


def sd_distance(spot, strike, iv, days=1):
    """How many SDs the strike sits from spot. Desk gate: must be > 1.5 SD."""
    sd = daily_sd(spot, iv, days)
    dist = abs(strike - spot)
    n = dist / sd if sd > 0 else float("inf")
    return {"daily_sd": sd, "distance_usd": dist, "sd": n, "passes_1_5": n > 1.5}


def iv_hv_gate(iv, hv):
    """IV/HV edge gate. <1.0 skip(no edge) · 1.0-1.15 borderline · 1.15-1.5 ok · >1.5 sweet."""
    if hv <= 0:
        return {"ratio": None, "zone": "skip", "note": "HV<=0 undefined -> conservative skip"}
    r = iv / hv
    if r < 1.0:
        zone = "skip"
    elif r < 1.15:
        zone = "borderline"
    elif r <= 1.5:
        zone = "ok"
    else:
        zone = "sweet"
    return {"ratio": r, "zone": zone, "tradeable": r >= 1.15}


def position_size(equity, risk_pct, premium_per_contract, max_loss_mult=3.0):
    """Margin-at-risk sizing. risk_pct is a fraction of equity (default band 0.5-1%).
    Short options are NOT capped at premium — size on an assumed max loss of
    max_loss_mult × premium per contract (>=2-3x to absorb an IV/gap spike)."""
    mar = equity * risk_pct
    max_loss_per_contract = max_loss_mult * premium_per_contract
    max_contracts = mar / max_loss_per_contract if max_loss_per_contract > 0 else 0.0
    return {
        "margin_at_risk": mar,
        "max_loss_per_contract": max_loss_per_contract,
        "max_contracts": max_contracts,
        "suggested_contracts": math.floor(max_contracts),
        "above_default_band": risk_pct > 0.01,  # 0.5-1% default until track record
        "note": "loss assumed > premium (uncapped tail); start 0.5-1% until proven",
    }


def pin_distance(spot, strike, iv, days=1, threshold_sd=0.3):
    """Pin-risk proximity at decision time. < threshold SD of strike -> close now
    (gamma squeeze in the TWAP settle window). Scales with IV, unlike a fixed $."""
    sd = daily_sd(spot, iv, days)
    dist = abs(strike - spot)
    n = dist / sd if sd > 0 else float("inf")
    return {"daily_sd": sd, "distance_usd": dist, "sd": n,
            "threshold_sd": threshold_sd, "close_now": n < threshold_sd}


def analyze(d):
    mode = d.get("mode")
    if mode == "sd":
        return sd_distance(d["spot"], d["strike"], d["iv"], d.get("days", 1))
    if mode == "iv_hv":
        return iv_hv_gate(d["iv"], d["hv"])
    if mode == "size":
        return position_size(d["equity"], d["risk_pct"], d["premium_per_contract"],
                             d.get("max_loss_mult", 3.0))
    if mode == "pin":
        return pin_distance(d["spot"], d["strike"], d["iv"], d.get("days", 1),
                            d.get("threshold_sd", 0.3))
    raise ValueError(f"unknown mode: {mode!r} (sd|iv_hv|size|pin)")


def main():
    print(json.dumps(analyze(json.load(sys.stdin)), ensure_ascii=False))


if __name__ == "__main__":
    main()
