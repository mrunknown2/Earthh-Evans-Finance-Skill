#!/usr/bin/env python3
"""Fundamental Checklist engine — deterministic, stdlib-only.

Reads a JSON payload from stdin, prints a JSON result to stdout. Every number is
COMPUTED here, not LLM-estimated — money math must be reproducible. The agent
gathers real inputs (financials, multiples), runs a mode, then interprets.

Modes: "companion" | "screen" | "scorecard".
เรียบเรียงจาก Ultimate Fundamental Stock Checklist — Earthh Evans · Invest Hub.

No third-party deps (portable across IDEs/providers). Pure Python.
"""
import sys, json

INF = float("inf")


def _verdict_vs(actual, justified, tol=0.05):
    """เทียบ actual กับ justified multiple → ถูก/fair/แพง (tol = สัดส่วนคลาด)."""
    if justified in (None, INF) or justified <= 0:
        return "speculation"
    gap = (actual - justified) / justified
    if gap < -tol:
        return "cheap"
    if gap > tol:
        return "expensive"
    return "fair"


# ---------- Companion Variables (justified multiples, Damodaran CV-1..CV-5) ----------

def companion(multiple, **kw):
    """Justified value of a multiple from its companion variable + verdict vs actual."""
    m = multiple

    if m == "peg":
        # CV-1: PEG = P/E ÷ EPS Growth(5Y CAGR). <1 undervalued, >2 overvalued.
        pe, growth = kw["pe"], kw["eps_growth_5y"]
        peg = pe / growth if growth else INF
        verdict = ("undervalued" if peg < 1.0
                   else "overvalued" if peg > 2.0 else "fair")
        return {"multiple": "peg", "justified": None, "actual": peg,
                "verdict": verdict, "gap": None,
                "note": "PEG = P/E ÷ EPS Growth(5Y). <1 undervalued, >2 overvalued. "
                        "ระวัง: growth ต้อง sustainable ไม่ใช่ EPS จาก buyback."}

    if m == "pe":
        # CV-1: Justified P/E = (Payout × (1+g)) / (CoE − g)
        payout, g, coe, actual = kw["payout"], kw["g"], kw["coe"], kw["actual_pe"]
        just = payout * (1.0 + g) / (coe - g) if (coe - g) > 0 else INF
        return {"multiple": "pe", "justified": just, "actual": actual,
                "verdict": _verdict_vs(actual, just),
                "gap": (actual - just) if just not in (None, INF) else None,
                "note": "Justified P/E = Payout×(1+g)/(CoE−g). companion = EPS Growth."}

    if m == "ev_sales":
        # CV-2: Justified EV/Sales = AfterTaxOpMargin × (1−Reinv) / (WACC − g)
        ebit, tax, rev = kw["ebit"], kw["tax"], kw["revenue"]
        reinv, wacc, g = kw["reinv_rate"], kw["wacc"], kw["g"]
        actual = kw["actual_ev_sales"]
        atom = ebit * (1.0 - tax) / rev if rev else 0.0
        if atom <= 0:
            return {"multiple": "ev_sales", "justified": None, "actual": actual,
                    "verdict": "speculation", "gap": None,
                    "note": "After-Tax Op Margin ≤ 0 → Justified EV/Sales ไม่มีความหมาย "
                            "= Speculation (เคส Peloton). Multiple ต่ำไม่ได้แปลว่าถูก."}
        just = atom * (1.0 - reinv) / (wacc - g) if (wacc - g) > 0 else INF
        return {"multiple": "ev_sales", "justified": just, "actual": actual,
                "verdict": _verdict_vs(actual, just),
                "gap": (actual - just) if just != INF else None,
                "note": f"After-Tax Op Margin = {atom:.3f}. Justified EV/Sales = "
                        "Margin×(1−Reinv)/(WACC−g). EV/Sales สูง+Margin กำลังหด = อันตราย."}

    if m == "pb":
        # CV-4: Justified P/B = (ROE − g) / (CoE − g)
        roe, g, coe, actual = kw["roe"], kw["g"], kw["coe"], kw["actual_pb"]
        just = (roe - g) / (coe - g) if (coe - g) > 0 else INF
        return {"multiple": "pb", "justified": just, "actual": actual,
                "verdict": _verdict_vs(actual, just),
                "gap": (actual - just) if just != INF else None,
                "note": "Justified P/B = (ROE−g)/(CoE−g). ROE>CoE → P/B>1 justified. "
                        "ต้อง DuPont ROE ก่อน — ROE สูงจาก leverage ≠ moat."}

    if m == "ev_ebitda":
        # CV-3: EV/(EBITDA − Maintenance CapEx) + ROIC vs WACC context
        ebitda, maint, ev = kw["ebitda"], kw["maint_capex"], kw["ev"]
        roic, wacc = kw["roic"], kw["wacc"]
        adj = ebitda - maint
        ratio = ev / adj if adj else INF
        context = "value-creating" if roic > wacc else "value-destroying"
        return {"multiple": "ev_ebitda", "justified": None, "actual": ratio,
                "verdict": "context", "gap": None,
                "note": f"EV/(EBITDA−MaintCapEx) = {ratio:.1f}x. ROIC {roic:.0%} vs "
                        f"WACC {wacc:.0%} → {context}. EBITDA ตัด CapEx ออกหลอกได้."}

    if m == "fcf_yield":
        # CV-5: FCF Yield = FCFF / EV (+ Owner Earnings option)
        fcff, ev = kw["fcff"], kw["ev"]
        fy = fcff / ev if ev else 0.0
        owner = None
        if all(k in kw for k in ("ni", "da", "maint_capex", "wc_change")):
            owner = kw["ni"] + kw["da"] - kw["maint_capex"] - kw["wc_change"]
        return {"multiple": "fcf_yield", "justified": None, "actual": fy,
                "verdict": "context", "gap": None, "owner_earnings": owner,
                "note": "FCF Yield = FCFF/EV. > yield พันธบัตร 10 ปี = Equity Premium มี. "
                        "Owner Earnings = NI + D&A − MaintCapEx − ΔWC (Buffett)."}

    raise ValueError(f"unknown multiple: {multiple!r} "
                     "(peg|pe|ev_sales|pb|ev_ebitda|fcf_yield)")


# ---------- Quick Screen 60 วิ (10 เกณฑ์ gate, threshold จากเอกสารหน้า 19-20) ----------

def screen(criteria, is_financial=False, fcf_exempt=False):
    """นับ pass/fail ของ 10 เกณฑ์ screen → gate verdict.

    banks (is_financial): ข้ามเกณฑ์ 2 (FCF conv) + 3 (Net Debt/EBITDA) — ใช้ CET1/NIM แทน.
    fcf_exempt: ธุรกิจ infra buildout — FCF conv ต่ำชั่วคราวจาก growth capex ไม่นับ fail.
    """
    failed = []
    c = criteria

    def chk(key, ok):
        if not ok:
            failed.append(key)

    chk("roic_gt_wacc_3y", c.get("roic_gt_wacc_3y", False))
    if not is_financial and not fcf_exempt:
        chk("fcf_conversion", c.get("fcf_conversion", 0) > 0.80)
    if not is_financial:
        chk("net_debt_ebitda", c.get("net_debt_ebitda", INF) < 2.5)
    chk("gross_margin_stable_3y", c.get("gross_margin_stable_3y", False))
    chk("revenue_quality", c.get("revenue_quality", False))
    chk("ev_sales_justified", c.get("ev_sales_justified", False))
    chk("peg", c.get("peg", INF) < 1.5)
    chk("insider_no_selling", c.get("insider_no_selling", False))
    chk("macro_aligned", c.get("macro_aligned", False))
    chk("capital_allocation_ok", c.get("capital_allocation_ok", False))

    total = 10 - (2 if is_financial else (1 if fcf_exempt else 0))
    passed = total - len(failed)
    if len(failed) == 0:
        gate = "strong"
    elif len(failed) <= 2:
        gate = "review"
    else:
        gate = "avoid"
    return {"passed": passed, "failed": len(failed), "total": total,
            "gate_verdict": gate, "failed_list": failed,
            "note": "Quick Screen 60 วิ — รันก่อน deep dive. banks ใช้ CET1/NIM แทนเกณฑ์ 2,3."}


# ---------- Scorecard aggregate (15 หมวด → overall read, ไม่ปั้น weight/0-100) ----------

CRITICAL_CATEGORIES = {"Moat", "Financial Strength", "Earnings Quality"}


def scorecard(categories, red_flags=None, screen_result=None):
    """รวม verdict 15 หมวด + red flags + screen → overall read (STRONG/REVIEW/AVOID).

    Derive ตรงจากเอกสาร: นับ pass/caution/red ต่อหมวด + red flag รวม + screen gate.
    ไม่มี 0-100, ไม่ปั้น weight. critical_red = red ในหมวด Moat/Financial/EarningsQuality.
    """
    red_flags = red_flags or []
    screen_result = screen_result or {"passed": 0, "total": 10}
    pass_c = sum(1 for c in categories if c["verdict"] == "pass")
    caution_c = sum(1 for c in categories if c["verdict"] == "caution")
    red_c = sum(1 for c in categories if c["verdict"] == "red")
    critical_red = any(c["verdict"] == "red" and c["name"] in CRITICAL_CATEGORIES
                       for c in categories)
    screen_passed = screen_result.get("passed", 0)
    screen_total = screen_result.get("total", 10)

    if critical_red or red_c >= 3:
        read = "AVOID"
    elif (red_c == 0 and screen_passed >= 0.8 * screen_total
          and len(red_flags) == 0 and caution_c <= 1):
        read = "STRONG"
    else:
        read = "REVIEW"

    return {"pass_count": pass_c, "caution_count": caution_c, "red_count": red_c,
            "red_flag_total": len(red_flags), "screen_passed": screen_passed,
            "screen_total": screen_total, "critical_red": critical_red,
            "overall_read": read,
            "note": "STRONG/REVIEW/AVOID เป็น framework signal ไม่ใช่ score. "
                    "ปิดท้ายด้วย 3 คำถามสุดท้ายก่อนกดซื้อ (qualitative)."}


# ---------- dispatch ----------

def analyze(d):
    mode = d.get("mode")
    if mode == "companion":
        kw = {k: v for k, v in d.items() if k not in ("mode", "multiple")}
        return companion(d["multiple"], **kw)
    if mode == "screen":
        return screen(d["criteria"], d.get("is_financial", False),
                      d.get("fcf_exempt", False))
    if mode == "scorecard":
        return scorecard(d["categories"], d.get("red_flags"),
                         d.get("screen_result"))
    raise ValueError(f"unknown mode: {mode!r} (companion|screen|scorecard)")


def main():
    d = json.load(sys.stdin)
    print(json.dumps(analyze(d), ensure_ascii=False))


if __name__ == "__main__":
    main()
