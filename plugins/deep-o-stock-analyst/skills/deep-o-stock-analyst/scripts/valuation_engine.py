#!/usr/bin/env python3
"""Deep-O valuation engine — deterministic, stdlib-only.

Reads a JSON payload from stdin, prints a JSON result to stdout. Every number is
COMPUTED here, not LLM-estimated — money math must be reproducible. The agent's
job is to gather real inputs (financials, rf/beta/ERP, price), run a mode, then
interpret. It does NOT do the arithmetic in its head.

Modes: "wacc" | "dcf" | "reverse_dcf" | "deep".

No numpy (portable across IDEs/providers). Pure Python.
"""
import sys, json


# ---------- WACC (CAPM + market-value weights, Damodaran-style) ----------

def wacc(rf, beta, erp, equity_mv, debt_mv, pre_tax_cost_of_debt, tax, crp=0.0):
    """Cost of Equity = rf + beta*(ERP + CRP); WACC on MARKET-value weights."""
    coe = rf + beta * (erp + crp)
    cod_at = pre_tax_cost_of_debt * (1.0 - tax)
    total = equity_mv + debt_mv
    we = equity_mv / total if total else 1.0
    wd = debt_mv / total if total else 0.0
    return {
        "cost_of_equity": coe,
        "cost_of_debt_after_tax": cod_at,
        "weight_equity": we, "weight_debt": wd,
        "wacc": we * coe + wd * cod_at,
    }


# ---------- DCF (Damodaran FCFF, Sales-to-Capital reinvestment) ----------

def dcf(revenue0, growths, margins, tax, sales_to_capital, wacc, g_terminal,
        roic_terminal, net_debt, shares, terminal_margin=None, wacc_terminal=None,
        cleanups=0.0):
    """Stage-by-stage FCFF DCF.

      FCFFₜ      = Revenueₜ·marginₜ·(1−tax) − ΔRevenueₜ / (S/C)ₜ
      TV         = FCFF_{N+1} / (WACC∞ − g∞),  reinv_∞ = g∞/ROIC∞
      firm_value = Σ PV(FCFFₜ) + PV(TV)
      equity     = firm_value − net_debt + cleanups   (excess cash +, ESOP/minority −)
    """
    n = len(growths)
    wacc_T = wacc_terminal if wacc_terminal is not None else wacc
    term_margin = terminal_margin if terminal_margin is not None else margins[-1]

    rev_prev = revenue0
    pv_fcff = 0.0
    fcff_list = []
    for t in range(1, n + 1):
        g = growths[t - 1]
        rev = rev_prev * (1.0 + g)
        nopat = rev * margins[t - 1] * (1.0 - tax)
        d_rev = rev - rev_prev
        sc = sales_to_capital[t - 1]
        reinv = (d_rev / sc) if sc else 0.0
        fcff = nopat - reinv
        pv_fcff += fcff / (1.0 + wacc) ** t
        fcff_list.append(fcff)
        rev_prev = rev

    # terminal (year N+1)
    rev_term = rev_prev * (1.0 + g_terminal)
    nopat_term = rev_term * term_margin * (1.0 - tax)
    reinv_rate_term = (g_terminal / roic_terminal) if roic_terminal else 0.0
    fcff_term = nopat_term * (1.0 - reinv_rate_term)
    tv = fcff_term / (wacc_T - g_terminal) if (wacc_T - g_terminal) > 0 else float("inf")
    pv_tv = tv / (1.0 + wacc) ** n

    firm_value = pv_fcff + pv_tv
    equity_value = firm_value - net_debt + cleanups
    return {
        "pv_explicit_fcff": pv_fcff,
        "terminal_value": tv,
        "pv_terminal_value": pv_tv,
        "terminal_reinvestment_rate": reinv_rate_term,
        "firm_value": firm_value,
        "equity_value": equity_value,
        "value_per_share": equity_value / shares if shares else 0.0,
        "fcff_explicit": fcff_list,
    }


# ---------- Reverse DCF (terminal-anchored — same math as reverse-dcf-screener) ----------

def reverse_dcf(ev, revenue0, wacc, g_terminal, terminal_margin, terminal_roic,
                tax, horizon_n):
    """Back out the steady-state revenue (and implied revenue CAGR) the CURRENT EV
    requires. Anchors on terminal value — does NOT conflate EV with TV:

      TV         = EV·(1+WACC)^N
      FCFF_term  = TV·(WACC − g∞)
      conversion = margin·(1−tax)·(1 − g∞/ROIC∞)
      R*         = FCFF_term / conversion
      ImpliedCAGR= (R*/R0)^(1/(N+1)) − 1
    """
    tv = ev * (1.0 + wacc) ** horizon_n
    fcff_term = tv * (wacc - g_terminal)
    reinv = g_terminal / terminal_roic if terminal_roic else 0.0
    conversion = terminal_margin * (1.0 - tax) * (1.0 - reinv)
    r_star = fcff_term / conversion if conversion else float("inf")
    implied_cagr = (r_star / revenue0) ** (1.0 / (horizon_n + 1)) - 1.0
    return {
        "terminal_value": tv,
        "fcff_terminal": fcff_term,
        "conversion": conversion,
        "implied_terminal_revenue": r_star,
        "implied_cagr": implied_cagr,
        "revenue_multiple_required": r_star / revenue0,
    }


# ---------- DEEP score (0-5 per dim, weighted -> 0-100, normalized) ----------

DEEP_WEIGHTS = {"demand": 25, "execution": 20, "economics": 20, "price": 20, "optionality": 15}


def deep_score(scores, weights=None):
    """total = Σ (scoreᵢ/5) × weightᵢ  → 0-100  (NOT scoreᵢ×weightᵢ, which maxes at 500)."""
    w = weights or DEEP_WEIGHTS
    contrib = {}
    total = 0.0
    for k, wt in w.items():
        s = scores.get(k, 0)
        c = (s / 5.0) * wt
        contrib[k] = c
        total += c
    if total >= 80:
        band, signal = ">=80", "🟢 ซื้อเพิ่ม"
    elif total >= 60:
        band, signal = "60-79", "🟡 ถือ / สะสมระวัง"
    elif total >= 40:
        band, signal = "40-59", "🟠 ลดน้ำหนัก"
    else:
        band, signal = "<40", "🔴 ขาย"
    return {"total": total, "max_possible": float(sum(w.values())),
            "contributions": contrib, "verdict_band": band, "signal": signal}


# ---------- dispatch ----------

def analyze(d):
    mode = d.get("mode")
    if mode == "wacc":
        return wacc(d["rf"], d["beta"], d["erp"], d["equity_mv"], d["debt_mv"],
                    d["pre_tax_cost_of_debt"], d["tax"], d.get("crp", 0.0))
    if mode == "dcf":
        return dcf(d["revenue0"], d["growths"], d["margins"], d["tax"],
                   d["sales_to_capital"], d["wacc"], d["g_terminal"],
                   d["roic_terminal"], d["net_debt"], d["shares"],
                   d.get("terminal_margin"), d.get("wacc_terminal"),
                   d.get("cleanups", 0.0))
    if mode == "reverse_dcf":
        return reverse_dcf(d["ev"], d["revenue0"], d["wacc"], d["g_terminal"],
                           d["terminal_margin"], d["terminal_roic"], d["tax"],
                           d["horizon_n"])
    if mode == "deep":
        return deep_score(d["scores"], d.get("weights"))
    raise ValueError(f"unknown mode: {mode!r} (wacc|dcf|reverse_dcf|deep)")


def main():
    d = json.load(sys.stdin)
    print(json.dumps(analyze(d), ensure_ascii=False))


if __name__ == "__main__":
    main()
