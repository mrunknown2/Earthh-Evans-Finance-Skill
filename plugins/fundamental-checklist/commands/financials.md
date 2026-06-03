---
description: "วิเคราะห์หมวด [3–5] Financial Strength + Profitability + Growth Quality — Net Debt/EBITDA, FCF Conversion, ROIC vs WACC, Operating Leverage; Financial Strength เป็น Critical Category"
allowed-tools:
  - Read
  - Bash
  - WebSearch
  - WebFetch
model: opus
---

# /fundamental-checklist:financials

**Financial Strength + Profitability + Growth Quality** — ตรวจความแข็งแกร่งงบดุล ประสิทธิภาพการดำเนินงาน และคุณภาพการเติบโต ตรงกับ Checklist หมวด [3–5]

## Input ที่ต้องการ

- **ticker หุ้น** + Sector
- งบล่าสุด: Net Debt, EBITDA, EBIT, Interest Expense, FCF, Net Income, Operating Cash Flow
- Revenue + Operating Income ย้อนหลัง 3–5 ปี (สำหรับ Trend + Operating Leverage)
- ROIC ย้อนหลัง 3 ปี + WACC ปัจจุบัน
- EBITDA, Maintenance CapEx (สำหรับ engine `companion` ev_ebitda mode)

## สิ่งที่ทำ

### หมวด [3] Financial Strength

- **3a. Net Debt / EBITDA** — benchmark: Net Cash = ดีที่สุด · < 1.5x ปลอดภัย · 1.5–2.5x รับได้ · 2.5–3.5x เริ่มสูง · > 3.5x ความเสี่ยงสูง
- **3b. Interest Coverage** (EBIT / Interest Expense) — > 5x: ปลอดภัยมาก · 3–5x: รับได้ · < 1.5x ช่วงดอกเบี้ยสูง: เสี่ยง Distress
- **3c. FCF Conversion** (Operating CF / Net Income) — > 100%: คุณภาพสูง · 80–100%: ปกติ · < 70% ต่อเนื่อง: ต้องสอบสวน
- กำหนด verdict: `pass` / `caution` / `red`

> **CRITICAL:** Financial Strength เป็น Critical Category — ถ้า verdict = `red` → สรุป AVOID ทันที

### หมวด [4] Profitability

- **4a. Gross Margin Trend** — Trend สำคัญกว่าระดับ · GM ขยายตัวช่วงเงินเฟ้อ = Pricing Power พิสูจน์แล้ว
- **4b. ROIC vs WACC** — `ROIC = NOPAT / Invested Capital` — เปรียบเทียบ ROIC vs WACC ต่อเนื่อง 3–5 ปี
  - Incremental ROIC vs Average ROIC — ถ้า Incremental ROIC ลดลงเรื่อย ๆ = Moat กำลังหดตัว
- รัน engine `companion` mode สำหรับ `ev_ebitda` เพื่อ ROIC context:
```bash
echo '{"mode":"companion","multiple":"ev_ebitda","ebitda":<EBITDA>,"maint_capex":<MaintCapEx>,"ev":<EV>,"roic":<ROIC_decimal>,"wacc":<WACC_decimal>}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```
- กำหนด verdict: `pass` / `caution` / `red`

### หมวด [5] Growth Quality

- **5a. Growth Test 3 มิติ** — Revenue CAGR 3–5 ปี · EPS Growth (Operations vs Buyback?) · FCF Growth (ยืนยัน EPS จริง)
- **5b. Operating Leverage Test** — `DOL = % Change in Operating Income / % Change in Revenue`
  - DOL > 1.5 = Leverage ดี · DOL > 2.0 = ยอดเยี่ยม · DOL < 1.0 = Cost โตเร็วกว่า Revenue (คำเตือน)
  - ตัวอย่าง Meta 2023: Revenue +16%, Operating Income +62% = DOL 3.9 — ยอดเยี่ยม
- กำหนด verdict: `pass` / `caution` / `red`

## References ที่ใช้

- `references/checklist-15.md` หมวด [3], [4], [5] — Benchmark Table ต่อ Sector + FCF Margin Benchmark
- `references/companion-variables.md` CV-3 — EV/EBITDA + ROIC Context

## ตัวอย่างสั่ง

```
/financials NVDA
/financials META
/financials T
```

## Discipline

ข้อมูลจริงก่อนเสมอ · Financial Strength = red → หยุด ไม่ดำเนินการต่อ · ROIC ต้องคำนวณจากงบจริง ระบุว่า Goodwill/SBC/Operating Lease ถูกปรับหรือไม่ · ระบุ as-of date + source ทุกตัวเลข · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
