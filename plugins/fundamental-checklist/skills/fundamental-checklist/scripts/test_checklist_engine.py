"""Known-answer tests for checklist_engine. Standalone runner (PEP 668 blocks
pytest on the dev box): python3 test_checklist_engine.py
ตัวเลข hand-computed + อิง case study จาก Earthh Evans Ultimate Fundamental Checklist."""
import json, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "checklist_engine.py")
sys.path.insert(0, HERE)
import checklist_engine as E


def approx(a, b, tol=1e-3):
    return abs(a - b) <= tol


# ---- companion: PEG (exact — เอกสารให้ครบ) ----

def test_peg_nvidia_undervalued():
    # NVDA FY2024: P/E ~35 ที่ EPS โต 100%+ -> PEG ~0.35 (เอกสาร CV-1 + case study 1)
    r = E.companion("peg", pe=35, eps_growth_5y=100)
    assert approx(r["actual"], 0.35), r
    assert r["verdict"] == "undervalued", r


def test_peg_consumer_staple_expensive():
    # P/E 25 ที่ growth 12% -> PEG 2.1 -> overvalued (เอกสาร CV-1 ตาราง)
    r = E.companion("peg", pe=25, eps_growth_5y=12)
    assert approx(r["actual"], 2.083, tol=1e-2), r
    assert r["verdict"] == "overvalued", r


# ---- companion: EV/Sales (directional + guard PTON) ----

def test_ev_sales_peloton_speculation():
    # PTON peak 2021: After-Tax Op Margin ติดลบ -> justified EV/Sales ไม่มีความหมาย
    r = E.companion("ev_sales", ebit=-571, tax=0.0, revenue=4000,
                    reinv_rate=0.5, wacc=0.10, g=0.04, actual_ev_sales=6.0)
    assert r["verdict"] == "speculation", r
    assert r["justified"] is None, r


def test_ev_sales_high_margin_justifies_premium():
    # margin ดี → justified ~4.15x แต่ actual 5.0x ยังเกิน → expensive (margin ดีไม่ได้แปลว่าไม่แพง)
    r = E.companion("ev_sales", ebit=450, tax=0.21, revenue=1000,
                    reinv_rate=0.3, wacc=0.10, g=0.04, actual_ev_sales=5.0)
    # atom = 450*0.79/1000 = 0.3555 ; just = 0.3555*0.7/0.06 = 4.1475
    assert approx(r["justified"], 4.1475, tol=1e-2), r
    assert r["verdict"] == "expensive", r  # actual 5.0 > justified 4.15


# ---- companion: P/B (Justified = (ROE-g)/(CoE-g)) ----

def test_pb_quality_compounder():
    # ROE 30%, g 8%, CoE 10% -> justified P/B = 0.22/0.02 = 11.0 (เอกสาร CV-4 ตาราง)
    r = E.companion("pb", roe=0.30, g=0.08, coe=0.10, actual_pb=8.0)
    assert approx(r["justified"], 11.0, tol=1e-2), r
    assert r["verdict"] == "cheap", r  # actual 8 < justified 11


def test_pb_meta_trough_justified():
    # META trough: ROE 15%, g 4%, CoE 10% -> justified P/B = 0.11/0.06 = 1.833 ; actual ~2 = fair-ish
    r = E.companion("pb", roe=0.15, g=0.04, coe=0.10, actual_pb=2.0)
    assert approx(r["justified"], 1.833, tol=1e-2), r


# ---- companion: P/E justified ----

def test_pe_justified_formula():
    # payout 0.5, g 0.04, coe 0.10 -> (0.5*1.04)/0.06 = 8.667
    r = E.companion("pe", payout=0.5, g=0.04, coe=0.10, actual_pe=12)
    assert approx(r["justified"], 8.667, tol=1e-2), r
    assert r["verdict"] == "expensive", r


# ---- companion: EV/EBITDA (CapEx-adjusted + ROIC context) ----

def test_ev_ebitda_capex_adjusted():
    # EBITDA 100, maint capex 20 -> EV/(80) ; ev 800 -> 10.0 ; roic>wacc -> value-creating
    r = E.companion("ev_ebitda", ebitda=100, maint_capex=20, ev=800,
                    roic=0.18, wacc=0.10)
    assert approx(r["actual"], 10.0, tol=1e-2), r
    assert "value-creating" in r["note"], r


# ---- companion: FCF Yield ----

def test_fcf_yield_basic():
    # fcff 50, ev 1000 -> 5%
    r = E.companion("fcf_yield", fcff=50, ev=1000)
    assert approx(r["actual"], 0.05, tol=1e-4), r


# ---- screen: Quick Screen 60 วิ (10 เกณฑ์ gate) ----

SCREEN_PASS_ALL = {
    "roic_gt_wacc_3y": True, "fcf_conversion": 0.90, "net_debt_ebitda": 1.0,
    "gross_margin_stable_3y": True, "revenue_quality": True,
    "ev_sales_justified": True, "peg": 1.0, "insider_no_selling": True,
    "macro_aligned": True, "capital_allocation_ok": True,
}


def test_screen_all_pass():
    r = E.screen(SCREEN_PASS_ALL)
    assert r["passed"] == 10, r
    assert r["failed"] == 0, r
    assert r["gate_verdict"] == "strong", r


def test_screen_peloton_fails_most():
    # PTON peak: FCF conv ติดลบ, EV/Sales ไม่ justified, insider ขาย, PEG N/A
    crit = dict(SCREEN_PASS_ALL)
    crit.update({"roic_gt_wacc_3y": False, "fcf_conversion": -0.5,
                 "ev_sales_justified": False, "insider_no_selling": False,
                 "peg": 5.0, "gross_margin_stable_3y": False})
    r = E.screen(crit)
    # 6 fails: roic, fcf_conversion, gross_margin, ev_sales, peg(5.0≥1.5), insider
    assert r["failed"] == 6, r
    assert r["gate_verdict"] == "avoid", r
    assert "fcf_conversion" in r["failed_list"], r


def test_screen_bank_override_skips_net_debt():
    # banks: net_debt_ebitda ไม่ใช้ -> ไม่นับ fail แม้ค่าสูง
    crit = dict(SCREEN_PASS_ALL); crit["net_debt_ebitda"] = 8.0
    r = E.screen(crit, is_financial=True)
    assert "net_debt_ebitda" not in r["failed_list"], r
    assert "fcf_conversion" not in r["failed_list"], r  # ก็ skip ด้วย (เกณฑ์ 2)


def test_screen_infra_buildout_fcf_exempt():
    # FCF conv ต่ำชั่วคราวจาก growth capex -> flag ไม่นับ fail ถ้า exempt
    crit = dict(SCREEN_PASS_ALL); crit["fcf_conversion"] = 0.3
    r = E.screen(crit, fcf_exempt=True)
    assert "fcf_conversion" not in r["failed_list"], r


# ---- scorecard: aggregate 15 หมวด (derive จากเอกสาร — ไม่มี 0-100) ----


def _cats(verdict_map):
    """สร้าง 15 หมวด default pass แล้ว override ตาม verdict_map."""
    names = ["Business", "Moat", "Financial Strength", "Profitability",
             "Growth Quality", "Capital Allocation", "Valuation",
             "Earnings Quality", "Management", "Ownership", "Risk", "Macro",
             "Technical", "Quick Screen", "Final Questions"]
    return [{"name": n, "verdict": verdict_map.get(n, "pass")} for n in names]


def test_scorecard_nvidia_strong():
    r = E.scorecard(_cats({}), red_flags=[],
                    screen_result={"passed": 10, "total": 10})
    assert r["pass_count"] == 15, r
    assert r["overall_read"] == "STRONG", r
    assert r["critical_red"] is False, r


def test_scorecard_peloton_avoid():
    # critical red (Moat + Earnings Quality) + red flags เพียบ
    cats = _cats({"Moat": "red", "Earnings Quality": "red",
                  "Profitability": "red", "Growth Quality": "red"})
    r = E.scorecard(cats, red_flags=["EV/Sales test พัง", "FCF ติดลบ peak",
                    "insider ขาย", "inventory build", "churn เพิ่ม"],
                    screen_result={"passed": 2, "total": 10})
    assert r["critical_red"] is True, r
    assert r["overall_read"] == "AVOID", r
    assert r["red_flag_total"] == 5, r


def test_scorecard_meta_review():
    # fundamental ดี แต่ screen mixed + 2 caution (ราคา/recovery) -> REVIEW
    cats = _cats({"Macro": "caution", "Risk": "caution"})
    r = E.scorecard(cats, red_flags=[],
                    screen_result={"passed": 7, "total": 10})
    assert r["overall_read"] == "REVIEW", r
    assert r["critical_red"] is False, r


# ---- CLI smoke (ทั้ง 3 modes) ----

def test_cli_modes():
    for payload, key in [
        ({"mode": "companion", "multiple": "peg", "pe": 35, "eps_growth_5y": 100}, "verdict"),
        ({"mode": "screen", "criteria": SCREEN_PASS_ALL}, "gate_verdict"),
        ({"mode": "scorecard", "categories": _cats({}), "red_flags": [],
          "screen_result": {"passed": 10, "total": 10}}, "overall_read"),
    ]:
        p = subprocess.run([sys.executable, SCRIPT], input=json.dumps(payload),
                           capture_output=True, text=True)
        assert p.returncode == 0, p.stderr
        assert key in json.loads(p.stdout), (payload["mode"], p.stdout)


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
