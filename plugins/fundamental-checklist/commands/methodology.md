---
description: "อธิบายที่มาของสูตร Companion Variable ครบ 6 ตัว + Scorecard Logic (STRONG/REVIEW/AVOID) + ข้อยกเว้น FCF/Banks + 10 Closing Principles — เชิงการศึกษา"
allowed-tools:
  - Read
  - Bash
  - WebSearch
  - WebFetch
model: opus
---

# /fundamental-checklist:methodology

**Methodology Deep Dive** — ที่มาของสูตร Companion Variable ทุกตัว Logic Scorecard และ 10 หลักการปิดท้าย · เชิงการศึกษา

## สิ่งที่แสดง

### Part 1 — Companion Variable Formulas (ทั้ง 6)

อ้างอิง `references/companion-variables.md`:

**CV-1 | P/E — Companion: EPS Growth Rate**
```
PEG = P/E ÷ EPS Growth Rate (5Y CAGR)
Justified P/E = (Payout Ratio × (1+g)) / (Cost of Equity − g)
```
- PEG < 1.0: Undervalued เทียบ Growth · 1.0–2.0: Fair Value · > 2.0: Overvalued
- PEG Trap: Growth Spike 1 ปี ≠ Sustainable Growth · ต้องใช้คู่ Earnings Quality

**CV-2 | EV/Sales — Companion: After-Tax Operating Margin**
```
After-Tax Op Margin = EBIT × (1−Tax Rate) / Revenue
Justified EV/Sales = After-Tax Op Margin × (1−Reinvestment Rate) / (WACC−g)
```
- Red Flag: EV/Sales สูง + Margin กำลังหด

**CV-3 | EV/EBITDA — Companion: CapEx Intensity + ROIC**
```
EV / (EBITDA − Maintenance CapEx)  ← แม่นกว่าสำหรับ Capital-Intensive
ROIC > WACC → Premium EV/EBITDA สมเหตุสมผล
ROIC < WACC → ทำลายมูลค่าทุกบาทที่ลงทุน
```

**CV-4 | P/B — Companion: ROE**
```
Justified P/B = (ROE − g) / (Cost of Equity − g)
ROE = CoE → P/B = 1.0x  |  ROE > CoE → P/B > 1 Justified  |  ROE < CoE → P/B < 1 Fair
```
- DuPont Decompose ROE ก่อนเสมอ: ROE ที่มาจาก Leverage ≠ คุณภาพธุรกิจ

**CV-5 | FCF Yield / EV/FCF — Companion: FCF Growth + Reinvestment Rate**
```
FCF Yield = FCFF / EV
Owner Earnings = Net Income + D&A − Maintenance CapEx − Working Capital Changes
```
- FCF Yield > 10Y Bond Yield = Equity มี Positive Risk Premium
- Maintenance CapEx ≠ CapEx ทั้งหมด — ต้อง Estimate เอง

**CV-6 | PEG — Companion: Growth Quality & Sustainability**
- ดูรายละเอียดใน CV-1 ด้านบน + PEG Trap 4 ข้อ

---

### Part 2 — Scorecard Logic

อ้างอิง `references/scorecard.md` + engine `scorecard` mode:

**Verdict ต่อหมวด:** `pass` / `caution` / `red`

**Overall Read Logic (match engine verbatim):**
```python
if critical_red or red_count >= 3:      → AVOID
elif (red_count == 0
      and screen_passed >= 0.8 × screen_total
      and red_flag_total == 0
      and caution_count <= 1):           → STRONG
else:                                   → REVIEW
```

**Critical Categories (Red = AVOID ทันที):**
```python
CRITICAL_CATEGORIES = {"Moat", "Financial Strength", "Earnings Quality"}
```

**Quick Screen Gate (หมวด 14):**
- ปกติ: total = 10 ต้องผ่าน ≥ 8
- `fcf_exempt=True`: total = 9 ต้องผ่าน ≥ 8/9
- `is_financial=True`: total = 8 ต้องผ่าน ≥ 7/8

**3 คำถามสุดท้าย (หมวด 15):**
1. "ธุรกิจนี้จะใหญ่กว่าและทำกำไรได้มากกว่าใน 5–10 ปี?" — ถ้าไม่ = หยุด
2. "ถ้าหุ้นตก 30% จะซื้อเพิ่มไหม?" — ถ้าไม่ = Position ใหญ่เกินไป
3. "บอกได้ชัดเจนไหมว่าทำไมตลาดถึง Misprice?" — ถ้าไม่ = รอก่อน

---

### Part 3 — 10 Closing Principles (จาก `references/scorecard.md` + `case-studies.md`)

1. **ทุก Multiple คือ DCF ที่ถูกย่อรูปมา** — Decompress ด้วย Companion Variable ก่อน
2. **ROIC > WACC ต่อเนื่อง 5 ปีขึ้นไป = พิสูจน์ Moat แล้ว** — ทุกอย่างอื่น = Hypothesis
3. **FCF คือความจริง** — Net Income ถูกจัดการได้ Cash ไม่ได้
4. **Trajectory ของ Margin สำคัญกว่าระดับปัจจุบัน** — Direction > Level
5. **Operating Leverage คือพลังที่ทรงพลังที่สุด** — Revenue Growth โต Structural กว่า Cost
6. **Reverse DCF บังคับความซื่อสัตย์ทางปัญญา** — ถาม "ราคานี้ Assume อะไร?" ก่อน
7. **Insider ขายที่ Stock Highs + Fundamental แย่ลงพร้อมกัน = Exit Signal** — อย่างใดอย่างหนึ่งไม่พอ
8. **Capital Allocation คือจุดที่ Alpha ถูกสร้างและทำลาย** — ธุรกิจดีที่บริหารเงินทุนแย่ Underperform เสมอ
9. **ก่อนบอกว่า Misprice ต้องหา Variant View ที่ชัดก่อน** — ตลาดไม่ได้ผิดเสมอไป
10. **Narrative ไม่มี Number ไม่ใช่การวิเคราะห์ · Number ไม่มี Narrative พลาด Context**

---

## References ที่ใช้

- `references/companion-variables.md` — สูตร Justified Multiple ทั้ง 6 + Master Summary Table
- `references/scorecard.md` — Logic STRONG/REVIEW/AVOID + Critical Categories + 10 Principles
- `references/checklist-15.md` หมวด [14] — ข้อยกเว้น FCF/Banks

## ตัวอย่างสั่ง

```
/methodology
```

## Discipline

เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล · สูตรทุกตัว port ตรงเข้า `checklist_engine.py` — ตัวเลขที่ engine คำนวณ = ตัวเลขที่ได้จากสูตรนี้
