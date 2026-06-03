#!/usr/bin/env python3
"""Reverse DCF (Terminal-Anchored) engine — fill input cells + compute in parallel.
Reads JSON from stdin, prints JSON result to stdout. Keeps Excel formulas intact
so the file recalculates when opened in Excel."""
import sys, json, os, shutil, datetime, warnings
warnings.filterwarnings("ignore")

TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "reverse_dcf_screener.xlsx")

# field -> Engine input cell (yellow). DO NOT touch formula cells.
ENGINE_CELLS = {
    "ticker":"C4","revenue_r0":"C5","ev":"C6","sector":"C7","wacc_override":"C9",
    "terminal_margin":"C11","terminal_g":"C12","terminal_roic":"C13","tax":"C14",
    "horizon_n":"C15","hist_cagr":"C18","fade":"C19","tam":"C20","max_pen":"C21",
    "abs_ceiling":"C22","buffer":"C40","price":"C43","shares_m":"C44","net_debt":"C45",
    "analyst_target":"C48","analyst_range":"C49","consensus_fy1":"C50",
}

def compute(d):
    R0=d["revenue_r0"]; EV=d["ev"]; W=d["wacc"]; m=d["terminal_margin"]
    g=d["terminal_g"]; roic=d["terminal_roic"]; tax=d["tax"]; N=d["horizon_n"]
    hist=d["hist_cagr"]; fade=d["fade"]; tam=d.get("tam",0); maxpen=d["max_pen"]
    absc=d["abs_ceiling"]; buf=d["buffer"]; nd=d["net_debt"]; sh=d["shares_m"]
    fwd = (d["consensus_fy1"]/R0 - 1) if d.get("consensus_fy1") else 0
    reinv = g/roic
    tv = EV*(1+W)**N
    fcff = tv*(W-g)
    conv = m*(1-tax)*(1-reinv)
    rstar = fcff/conv
    implied = (rstar/R0)**(1/(N+1)) - 1
    capA = max(hist, fwd)*fade
    capB = 999 if tam in (0,None) else (maxpen*tam/R0)**(1/(N+1)) - 1
    capC = absc
    plausible = min(capA, capB, capC)
    gap = implied - plausible
    if gap > buf: verdict = "แพง — Priced for Perfection"
    elif gap < -buf: verdict = "ถูก — Low Expectations"
    else: verdict = "Fair — สมเหตุสมผล"
    def price_at(cagr):
        return ((R0*(1+cagr)**(N+1)*conv/(W-g)/(1+W)**N) - nd)*1000/sh
    zones = {
        "strong_buy": price_at(max(plausible-0.05,0)),
        "fair_value": price_at(plausible),
        "caution_low": price_at(plausible+0.05),
        "caution_high": price_at(plausible+0.10),
        "red_flag": price_at(plausible+0.10),
    }
    return {
        "ticker": d.get("ticker"), "reinvestment": reinv, "terminal_value": tv,
        "fcff_n1": fcff, "conversion": conv, "implied_terminal_revenue": rstar,
        "implied_cagr": implied, "cap_a": capA, "cap_b": capB, "cap_c": capC,
        "plausible_cagr": plausible, "gap": gap, "verdict": verdict,
        "ev_sales": EV/R0, "current_price": d.get("price"), "zones": zones,
    }

def write_xlsx(d, out_path):
    import openpyxl
    shutil.copy(TEMPLATE, out_path)
    wb = openpyxl.load_workbook(out_path)
    eng = wb["Engine"]
    eng["C7"] = d.get("sector")
    if "wacc" in d:
        eng["C9"] = d["wacc"]   # put WACC as override (guard against placeholder sector lookup)
    for f, cell in ENGINE_CELLS.items():
        if f in ("sector","wacc_override"): continue
        if f in d and d[f] is not None:
            eng[cell] = d[f]
    wb.save(out_path)
    return out_path

def main():
    d = json.load(sys.stdin)
    res = compute(d)
    if not d.get("no_write"):
        os.makedirs("analyses", exist_ok=True)
        stamp = d.get("date") or datetime.date.today().isoformat()
        out = os.path.join("analyses", f"{d.get('ticker','STOCK')}_{stamp}.xlsx")
        res["file"] = write_xlsx(d, out)
    print(json.dumps(res, ensure_ascii=False))

if __name__ == "__main__":
    main()
