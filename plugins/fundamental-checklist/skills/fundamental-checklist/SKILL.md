---
name: fundamental-checklist
description: >
  ใช้เมื่ออยากตรวจสุขภาพหุ้นครบทุกมิติ — Damodaran Companion Variables (ทุก Multiple
  มีตัวขับเคลื่อนที่ทำให้ถูก/แพง), Quick Screen 60 วิ, Red Flag system, 15-category
  due diligence. justified P/E, EV/Sales, EV/EBITDA, P/B, PEG, FCF Yield, ROIC vs WACC,
  moat verification. scorecard บอกผ่านกี่มิติ/ติด red flag ตรงไหน. เชิงการศึกษา ไม่ใช่คำแนะนำ.
---

# Fundamental Checklist

ระบบ **15-Category Fundamental Due Diligence** — ไม่ใช่แค่ดู P/E ว่าถูกหรือแพง แต่**ตรวจทุกมิติของธุรกิจ** ตั้งแต่ Business Model → Moat → Financial Strength → Valuation → Management → Risk → Macro → สรุปออกมาเป็น **STRONG / REVIEW / AVOID** พร้อม Red Flag ที่แม่นยำ

> เรียบเรียงจาก **Earthh Evans · Invest Hub** — Ultimate Fundamental Stock Checklist 2025

---

## Positioning ในครอบครัว Plugin

| Plugin | จุดแข็ง | ใช้เมื่อ |
|--------|--------|---------|
| **`fundamental-checklist`** (ตัวนี้) | **Breadth** — 15 มิติ due diligence + Companion Variables | อยากตรวจสุขภาพหุ้นแบบรอบด้าน ก่อนตัดสินใจ |
| `deep-o-stock-analyst` | **Depth** — Intrinsic Value DCF ลึก | อยากได้ Target Price / มูลค่าที่แท้จริง |
| `reverse-dcf-screener` | **Expectation** — Market-Implied CAGR | อยากรู้ว่าตลาด Price In อะไรไว้ ณ ราคาปัจจุบัน |

---

## Philosophy — ทุก Multiple คือ DCF ที่ถูกย่อรูปมา

> ก่อนจะใช้ Ratio ตัวไหน ต้องเข้าใจก่อนว่าอะไรคือ **Companion Variable** ที่ขับเคลื่อนมันอยู่เบื้องหลัง

| Multiple | Companion Variable | Red Flag ถ้าขาด |
|----------|-------------------|----------------|
| P/E | EPS Growth Rate | EPS โตเพราะ Buyback ไม่ใช่ Operations |
| EV/Sales | After-Tax Operating Margin | EV/Sales สูง + Margin กำลังหด |
| EV/EBITDA | CapEx Intensity + ROIC | ROIC < WACC — ทำลายมูลค่าทุกบาทที่ลงทุน |
| P/B | Return on Equity (ROE) | ROE < CoE = P/B < 1 คือ Fair ไม่ใช่ถูก |
| PEG | Growth Quality & Sustainability | Growth Spike ปีเดียว ไม่ Sustainable |
| FCF Yield | FCF Growth + Capital Intensity | FCF พองเพราะตัด Maintenance CapEx ออก |

**กฎเหล็ก:** อย่าดู Multiple คนเดียว — `companion` mode ใน engine คำนวณ Justified Multiple จากปัจจัยพื้นฐาน ไม่ใช่เทียบ Peer แบบ Gut-feel

---

## Routing — สถานการณ์ → Command

| สถานการณ์ | Command |
|-----------|---------|
| ตรวจสุขภาพหุ้นครบทุกมิติในคำสั่งเดียว — Screen + 15 หมวด + Scorecard | `/full` |
| Quick Screen 10 เกณฑ์ 60 วินาที ก่อน Deep Dive | `/screen` |
| คำนวณ Justified Multiple จาก Companion Variable (P/E, EV/Sales, P/B, EV/EBITDA, PEG, FCF Yield) | `/companion` |
| วิเคราะห์หมวด [1–2] Business Overview / Moat | `/business` |
| วิเคราะห์หมวด [3–5] Financial Strength / Profitability / Growth Quality | `/financials` |
| วิเคราะห์หมวด [6–7] Capital Allocation + Valuation + Companion Variables ครบ 6 Multiple | `/capital` |
| วิเคราะห์หมวด [8–10] Earnings Quality / Management Quality / Ownership | `/quality` |
| วิเคราะห์หมวด [11–13] Risk Assessment / Macro / Technical | `/risk` |
| ดูตัวอย่างจริง NVDA · META · PTON เพื่อเทียบ Framework กับของจริง | `/casestudy` |
| อยากเข้าใจที่มาของสูตร Justified Multiple / Logic Scorecard / ข้อยกเว้น FCF/Banks | `/methodology` |

---

## Critical Rules — AI ห้าม override

กฎเหล่านี้บังคับทุก command ไม่มีข้อยกเว้น:

- **ข้อมูลจริงก่อนเสมอ** — Search / WebFetch ก่อน Memory · ไม่พบให้เขียน "ไม่พบข้อมูล" + บอกแหล่งที่หาแล้ว
- **Companion thinking บังคับ** — อย่าดู Multiple คนเดียว ต้องหา Companion Variable คู่กันทุกครั้ง
- **Engine deterministic** — เลขที่ได้จาก engine ไม่กุ ไม่ estimate ทับผล engine
- **as-of date + source ทุกตัวเลข** — ระบุ `YYYY-MM-DD` + สกุลเงิน + แหล่งที่มา (10-K / 10-Q / IR)
- **Scorecard ไม่ใช่ score ดิบ** — STRONG/REVIEW/AVOID คือ framework signal ไม่ใช่คำแนะนำซื้อขาย
- **Critical Categories = AVOID ทันที** — ถ้า `Moat`, `Financial Strength`, หรือ `Earnings Quality` ได้ verdict = `red` → `overall_read = "AVOID"` ไม่ว่าหมวดอื่นจะ pass กี่หมวด

---

## Engine — `checklist_engine.py` (4 Modes)

skill package นี้ **portable** — `SKILL.md` + `references/` + `scripts/checklist_engine.py` ชุดเดียว ใช้ได้ทั้ง Claude Code / Claude Desktop / Codex / Antigravity · ไม่ต้อง `pip install` ใด ๆ — **stdlib Python 3 ล้วน** · ติดตั้งต่อ platform ดู **`INSTALL.md`**

**เรียก engine โดยตรง** — ส่ง JSON ทาง stdin:

```bash
echo '<JSON>' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
# หรือเรียกด้วย full path (engine ไม่พึ่ง CWD)
python3 /path/to/skills/fundamental-checklist/scripts/checklist_engine.py <<< '<JSON>'
```

### Mode 0: `derive` — Raw Financials → Derived Metrics (deterministic)

**รันก่อน companion/screen เสมอ** — แทนการคำนวณ multiple/ratio **ในหัว** (money math ต้อง reproducible ข้าม platform). รับ raw financials (ทุก field optional) → คืน 13 derived metrics · field ที่ขาด → `null` + เข้า `missing` · หารศูนย์ → `null` · ไม่ throw

```bash
echo '{"mode":"derive","market_cap":4360000,"total_debt":59291,"cash_and_investments":126843,"revenue":402836,"ebit":129039,"ebitda":150175,"tax_rate":0.176,"net_income":132170,"ocf":164713,"fcf":73266,"equity":415265,"eps_start":5.61,"eps_end":10.82,"eps_years":4,"dividends":10049,"buybacks":45709}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```

Output → ป้อนต่อเข้า mode อื่น (เลิกคำนวณในหัว):

| derived key | feed → | หมายเหตุ |
|-------------|--------|---------|
| `net_debt_ebitda` | screen `net_debt_ebitda` | net cash = ติดลบ |
| `fcf_conversion` (FCF/NI) | screen `fcf_conversion` | **≠** `cash_conversion` (OCF/NI) |
| `eps_cagr` | companion peg `eps_growth_5y` (×100) | |
| `ev`, `ev_sales` | companion ev_sales `ev` / `actual_ev_sales` | |
| `ev_ebitda` | companion ev_ebitda | |
| `pb` | companion pb `actual_pb` | |
| `pe` | companion pe `actual_pe` | mktcap÷NI — เลือก period NI ให้ตรง multiple ที่ต้องการ |
| `total_payout_ratio` | companion pe `payout` | รวม buyback (low-dividend reinvestor) |
| `after_tax_op_margin` · `cash_conversion` · `fcf_yield` | context / cross-check | |

Output keys: 13 metrics ข้างบน + `missing` (list field ที่ขาด) + `note`

---

### Mode 1: `companion` — Justified Multiple จาก Companion Variable

คำนวณ Justified Multiple เทียบกับ actual → verdict ต่อ multiple: P/E·EV/Sales·P/B → `cheap`/`fair`/`expensive` (EV/Sales → `speculation` ถ้า margin ≤ 0) · PEG → `undervalued`/`fair`/`overvalued` · EV/EBITDA·FCF Yield → `context` (อ่านคู่ ROIC-vs-WACC / bond yield, `justified` = null)

**CV-1 PEG** (P/E ÷ EPS Growth):
```bash
echo '{"mode":"companion","multiple":"peg","pe":35,"eps_growth_5y":35}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```

**CV-1 Justified P/E** (Payout × (1+g) / (CoE − g)):
```bash
echo '{"mode":"companion","multiple":"pe","payout":0.3,"g":0.08,"coe":0.10,"actual_pe":35}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```

**CV-2 Justified EV/Sales** (After-Tax Op Margin × (1−Reinv) / (WACC − g)):
```bash
echo '{"mode":"companion","multiple":"ev_sales","ebit":32.7e9,"tax":0.21,"revenue":60.9e9,"reinv_rate":0.05,"wacc":0.09,"g":0.05,"actual_ev_sales":22}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```

**CV-3 EV/(EBITDA−MaintCapEx) + ROIC context**:
```bash
echo '{"mode":"companion","multiple":"ev_ebitda","ebitda":40e9,"maint_capex":3e9,"ev":600e9,"roic":1.0,"wacc":0.09}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```

**CV-4 Justified P/B** ((ROE − g) / (CoE − g)):
```bash
echo '{"mode":"companion","multiple":"pb","roe":0.30,"g":0.08,"coe":0.10,"actual_pb":11}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```

**CV-5 FCF Yield + Owner Earnings (Buffett)**:
```bash
echo '{"mode":"companion","multiple":"fcf_yield","fcff":27e9,"ev":1200e9,"ni":29.8e9,"da":3.4e9,"maint_capex":2e9,"wc_change":1e9}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```

Output keys: `multiple`, `justified`, `actual`, `verdict`, `gap`, `note` (+ `owner_earnings` สำหรับ fcf_yield)

---

### Mode 2: `screen` — Quick Screen 60 วินาที (10 เกณฑ์ gate)

นับ pass/fail ของ 10 เกณฑ์ → gate verdict: `strong` (0 fail) / `review` (1–2 fail) / `avoid` (3+ fail)

**ตัวอย่างมาตรฐาน (บริษัททั่วไป):**
```bash
echo '{
  "mode":"screen",
  "criteria":{
    "roic_gt_wacc_3y":true,
    "fcf_conversion":0.92,
    "net_debt_ebitda":1.2,
    "gross_margin_stable_3y":true,
    "revenue_quality":true,
    "ev_sales_justified":true,
    "peg":0.9,
    "insider_no_selling":true,
    "macro_aligned":true,
    "capital_allocation_ok":true
  }
}' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```

**ตัวอย่างธนาคาร** (ข้ามเกณฑ์ FCF + Net Debt/EBITDA → ใช้ CET1/NIM แทน):
```bash
echo '{"mode":"screen","criteria":{"roic_gt_wacc_3y":true,"gross_margin_stable_3y":true,"revenue_quality":true,"ev_sales_justified":false,"peg":1.3,"insider_no_selling":true,"macro_aligned":true,"capital_allocation_ok":true},"is_financial":true}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```

**ตัวอย่าง Infrastructure Buildout** (ข้ามเกณฑ์ FCF Conversion ชั่วคราว):
```bash
echo '{"mode":"screen","criteria":{"roic_gt_wacc_3y":true,"net_debt_ebitda":2.1,"gross_margin_stable_3y":true,"revenue_quality":true,"ev_sales_justified":true,"peg":1.2,"insider_no_selling":true,"macro_aligned":true,"capital_allocation_ok":true},"fcf_exempt":true}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```

Output keys: `passed`, `failed`, `total`, `gate_verdict`, `failed_list`, `note`

---

### Mode 3: `scorecard` — Aggregate 15 หมวด → Overall Read

รับ verdict (`pass` / `caution` / `red`) ของ 15 หมวด + red_flags + screen_result → สรุป STRONG / REVIEW / AVOID

**Logic สรุป:**
- `critical_red = True` (Moat / Financial Strength / Earnings Quality เป็น `red`) → **AVOID**
- `red_count >= 3` → **AVOID**
- `red_count == 0` AND `screen_passed >= 80%` AND `red_flags == []` AND `caution_count <= 1` → **STRONG**
- ทุกกรณีอื่น → **REVIEW**

```bash
echo '{
  "mode":"scorecard",
  "categories":[
    {"name":"Business Overview",   "verdict":"pass"},
    {"name":"Moat",                "verdict":"pass"},
    {"name":"Financial Strength",  "verdict":"pass"},
    {"name":"Profitability",       "verdict":"pass"},
    {"name":"Growth Quality",      "verdict":"pass"},
    {"name":"Capital Allocation",  "verdict":"pass"},
    {"name":"Valuation",           "verdict":"caution"},
    {"name":"Earnings Quality",    "verdict":"pass"},
    {"name":"Management Quality",  "verdict":"pass"},
    {"name":"Ownership Structure", "verdict":"pass"},
    {"name":"Risk Assessment",     "verdict":"pass"},
    {"name":"Macro Alignment",     "verdict":"pass"},
    {"name":"Technical Context",   "verdict":"pass"},
    {"name":"Quick Screen",        "verdict":"pass"},
    {"name":"3 Final Questions",   "verdict":"pass"}
  ],
  "red_flags":[],
  "screen_result":{"passed":9,"total":10}
}' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```

Output keys: `pass_count`, `caution_count`, `red_count`, `red_flag_total`, `screen_passed`, `screen_total`, `critical_red`, `overall_read`, `note`

> **หมายเหตุ:** `categories[].name` ต้อง case-sensitive ตรงกับ Critical Categories: `"Moat"`, `"Financial Strength"`, `"Earnings Quality"`

---

## Workflow (เมื่อไม่มี subagent / slash command)

บน platform ที่ไม่มี subagent ของ Claude Code ให้ทำ 5 สเต็ปนี้ในเซสชันเดียว:

1. **Derive** — ดึง raw financials (10-K / 10-Q / IR) → รัน mode `derive` → ได้ EV, EV/Sales, EV/EBITDA, P/B, P/E, FCF/Cash Conversion, eps_cagr, total_payout ฯลฯ · **ห้ามคำนวณ multiple/ratio ในหัว** (deterministic ข้าม platform)
2. **Screen** — กรอก 10 เกณฑ์ (ใช้ค่าจาก derive: `net_debt_ebitda`, `fcf_conversion` ฯลฯ) → รัน mode `screen` → gate verdict + failed_list
3. **Companion** — ป้อนค่าจาก derive (ev, ev_sales, pb, pe, eps_cagr→eps_growth_5y, total_payout→payout) เข้า mode `companion` ทีละ multiple → เทียบ actual vs justified
4. **15 Categories** — เดิน 15 หมวดตาม `references/checklist-15.md` → กำหนด verdict (`pass` / `caution` / `red`) ทีละหมวด พร้อมเหตุผล + as-of date + source · ระบุ red_flags ที่พบ
5. **Scorecard** — ส่ง verdicts ทั้ง 15 หมวด + red_flags + screen_result เข้า mode `scorecard` → อ่าน overall_read → ปิดท้ายด้วย 3 คำถามสุดท้าย (หมวด [15]) ก่อนสรุป

> ข้อบังคับ: ไม่กุข้อมูล · **ตัวเลขคำนวณจาก `derive` ไม่คำนวณในหัว** · Companion Variable ประกอบทุก Multiple · source + as-of date ทุกตัวเลข · verdict หมวด = pass/caution/red เท่านั้น · AVOID = ไม่ดำเนินการต่อ

---

## ดู INSTALL.md

สำหรับการตั้งค่าต่อ IDE (Claude Code, Antigravity, Codex) รวมถึงการ zip สำหรับ Claude Desktop Chat ดู **`INSTALL.md`** ที่ root ของ plugin

---

## Disclaimer

เครื่องมือนี้เป็นกรอบวิเคราะห์พื้นฐานเชิงการศึกษา **ไม่ใช่คำแนะนำการลงทุนรายบุคคล** · STRONG/REVIEW/AVOID เป็น **framework signal** จาก 15-category fundamental checklist ไม่ใช่คำสั่งซื้อขาย · ตัวเลขอิงข้อมูลที่ระบุใน as-of date และสมมติฐานของผู้ใช้ (WACC, growth rate, margin) · ผู้ใช้ต้อง verify เอกสารทางการล่าสุด (10-K / 10-Q / IR) และพิจารณาบริบทของตนเองก่อนตัดสินใจทุกครั้ง
