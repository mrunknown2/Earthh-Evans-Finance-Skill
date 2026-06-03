---
description: "วิเคราะห์หมวด [6–7] Capital Allocation + Valuation — Buyback Quality, M&A Track Record, Justified Multiple ครบ 6 ตัว; cross-ref deep-o-stock-analyst (intrinsic) + reverse-dcf-screener (implied CAGR) ไม่ทำ DCF เอง"
allowed-tools:
  - Read
  - Bash
  - WebSearch
  - WebFetch
model: opus
---

# /fundamental-checklist:capital

**Capital Allocation + Valuation** — ตรวจว่าผู้บริหารจัดสรรเงินทุนอย่างไร และ Multiple ปัจจุบันยืนยันได้ด้วย Fundamental จริงหรือไม่ ตรงกับ Checklist หมวด [6–7]

## Input ที่ต้องการ

- **ticker หุ้น** + ประวัติ M&A 5–7 ปี, Share Count Trend, CapEx ย้อนหลัง
- งบล่าสุดสำหรับ Companion Variables ทั้ง 6 ตัว: Revenue, EBIT, EBITDA, Net Income, CapEx, FCF, Book Value, ROE, Payout Ratio, EV, Price, WACC, CoE, growth assumptions

## สิ่งที่ทำ

### หมวด [6] Capital Allocation

- **Capital Allocation Hierarchy** (Damodaran) — จัดลำดับความเหมาะสมของ 4 ทาง:
  1. Reinvest ใน Core Business (เหมาะเมื่อ Incremental ROIC > WACC)
  2. Strategic M&A (Synergy ชัด ราคาไม่แพง)
  3. Share Buyback (หุ้นต่ำกว่า Intrinsic Value จริง ๆ)
  4. Dividend (ไม่มี High-ROIC Project เหลือ)
- **6a. Buyback Quality Test** — ดูประวัติ 5 ปี: Share Count ลดลงมีนัยสำคัญ? Timing ใกล้ Low ไหม? Buyback หนักแต่ ROIC ลดลง = Red Flag
- **6b. M&A Track Record** — ROIC ดีขึ้นหรือลงหลัง Acquisition 3 ปี? Goodwill > 40% of Total Assets = ซื้อแพงต่อเนื่อง
- **6c. CapEx Decomposition** — `True Owner Earnings = Net Income + D&A − Maintenance CapEx − WC Changes`
- กำหนด verdict: `pass` / `caution` / `red`

### หมวด [7] Valuation

- รัน engine `companion` mode ครบ **6 Multiple** (peg, pe, ev_sales, ev_ebitda, pb, fcf_yield) — ดู engine calls ใน `/companion`
- สรุปตาราง Actual vs Justified per Multiple + Verdict (cheap/fair/expensive/speculation)
- **Reverse DCF cross-check:**
  - สำหรับ **Intrinsic Value (Target Price)** → ส่งต่อ plugin **`deep-o-stock-analyst`** (ไม่ทำ DCF เอง)
  - สำหรับ **Implied CAGR ที่ตลาดต้องการ ณ ราคาปัจจุบัน** → ส่งต่อ plugin **`reverse-dcf-screener`** (ไม่ทำ Full Reverse DCF เอง)
  - ถาม: "ตลาด Imply Growth Rate เท่าไร? ทำได้จริงไหม?" เป็น framing คำถาม
- กำหนด verdict: `pass` / `caution` / `red`

## Engine Calls (Companion — ทีละ Multiple)

```bash
# PEG
echo '{"mode":"companion","multiple":"peg","pe":35,"eps_growth_5y":35}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"

# Justified P/E
echo '{"mode":"companion","multiple":"pe","payout":0.3,"g":0.08,"coe":0.10,"actual_pe":35}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"

# Justified EV/Sales
echo '{"mode":"companion","multiple":"ev_sales","ebit":32.7e9,"tax":0.21,"revenue":60.9e9,"reinv_rate":0.05,"wacc":0.09,"g":0.05,"actual_ev_sales":22}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"

# EV/EBITDA + ROIC
echo '{"mode":"companion","multiple":"ev_ebitda","ebitda":40e9,"maint_capex":3e9,"ev":600e9,"roic":1.0,"wacc":0.09}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"

# Justified P/B
echo '{"mode":"companion","multiple":"pb","roe":0.30,"g":0.08,"coe":0.10,"actual_pb":11}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"

# FCF Yield + Owner Earnings
echo '{"mode":"companion","multiple":"fcf_yield","fcff":27e9,"ev":1200e9,"ni":29.8e9,"da":3.4e9,"maint_capex":2e9,"wc_change":1e9}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```

## Cross-reference Plugin

> **Capital command ไม่ทำ Full DCF เอง** — ส่งต่อ:
> - **Intrinsic Value / Target Price** → `deep-o-stock-analyst` (plugin แยก)
> - **Market-Implied CAGR / Expectation Analysis** → `reverse-dcf-screener` (plugin แยก)

## References ที่ใช้

- `references/checklist-15.md` หมวด [6], [7] — Capital Allocation Hierarchy + Valuation Summary Table
- `references/companion-variables.md` — สูตร Justified Multiple ทั้ง 6

## ตัวอย่างสั่ง

```
/capital NVDA
/capital AAPL
/capital META
```

## Discipline

Companion Variable ประกอบทุก Multiple บังคับ · Engine คำนวณ ไม่ estimate Multiple ในหัว · DCF/Intrinsic Value ส่งต่อ plugin พี่ที่เชี่ยวชาญ · ระบุ as-of date + source ทุกตัวเลข · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
