---
description: "วิเคราะห์หมวด [8–10] Earnings Quality + Management Quality + Ownership Structure — FCF Conversion, Accrual Ratio, DSO, Insider Ownership, Compensation Alignment; Earnings Quality เป็น Critical Category"
allowed-tools:
  - Read
  - Bash
  - WebSearch
  - WebFetch
model: opus
---

# /fundamental-checklist:quality

**Earnings Quality + Management Quality + Ownership Structure** — ตรวจว่า Earnings เป็นเงินสดจริงหรือ Accounting Engineering ผู้บริหาร Aligned กับผู้ถือหุ้นหรือไม่ และใครอยู่เบื้องหลังบริษัท ตรงกับ Checklist หมวด [8–10]

## Input ที่ต้องการ

- **ticker หุ้น**
- งบล่าสุด: FCF, Net Income, Operating Cash Flow, Accounts Receivable, Revenue (Trend)
- Proxy Statement (DEF 14A): Compensation Structure, Insider Ownership
- SEC Form 4: Insider Transactions ย้อนหลัง 12 เดือน
- 13F Filings: Top Institutional Holders

## สิ่งที่ทำ

### หมวด [8] Earnings Quality

- **8a. Three Quality Tests:**
  - Cash Conversion: `FCF / Net Income` — 80–110%: Healthy · < 70% ต่อเนื่อง 2 ปี: ต้องสอบสวน
  - Accrual Ratio: `(Net Income − FCF) / Avg Assets` — ใกล้ 0 หรือติดลบ = ดี · เพิ่มขึ้นเรื่อย ๆ = Earnings ฝัง Accounting มากขึ้น
  - Revenue Quality: DSO Trend — คงที่หรือลดลง = ดี · DSO ขยาย + Revenue โต = อาจ Channel Stuffing
  - Recurring Mix: % Recurring / Total Revenue — > 60% สำหรับ Tech = ดี
  - Customer Concentration: Top 3 / Revenue — < 30% = ดี · > 40% = ลูกค้าออก 1 ราย = Risk Event
- **8b. Red Flags ที่ระวัง:**
  - Net Income โต YoY แต่ Operating CF แบนหรือลด
  - Accounts Receivable โตเร็วกว่า Revenue มาก
  - Revenue Spike ปลายไตรมาส + Inventory Build ที่ Distributor
  - Goodwill Impairment บ่อยและขนาดใหญ่
- กำหนด verdict: `pass` / `caution` / `red`

> **CRITICAL:** Earnings Quality เป็น Critical Category — ถ้า verdict = `red` → สรุป AVOID ทันที

### หมวด [9] Management Quality

| หัวข้อ | สิ่งที่ประเมิน | แหล่งข้อมูล |
|--------|--------------|------------|
| Skin in the Game | % Insider Ownership + Trend | SEC Form 4, Proxy |
| Capital Allocation Track Record | ผลลัพธ์ M&A, Buyback Timing, Dividend Sustainability | 10-K, IR |
| Guidance Credibility | ประวัติ Beat/Miss vs Guidance | Earnings Transcripts |
| Communication Quality | พูดถึงความเสี่ยงตรงไหม? ยอมรับข้อผิดพลาด? | Earnings Calls |
| Compensation Alignment | Incentive ผูกกับ ROIC/FCF หรือแค่ EPS/Revenue? | Proxy DEF 14A |

- กำหนด verdict: `pass` / `caution` / `red`

### หมวด [10] Ownership Structure

| สัญญาณ | บวก | ลบ |
|--------|----|----|
| Insider Ownership | > 10% คงตัวหรือเพิ่มขึ้น | สูงแต่ขายออกต่อเนื่องหลัง Lockup |
| Institutional Quality | Long-only Value Fund เป็น Top Holder | ส่วนใหญ่เป็น Short-term Momentum Fund |
| Insider Transaction | Open-market Buy ช่วงตลาดปรับฐาน | ขายเร็งขึ้นเมื่อราคาพุ่ง |
| Float Size | Float เพียงพอสำหรับ Liquidity | Float น้อยมาก + Short Interest สูง |

- แหล่งข้อมูล: Yahoo Finance Holders · Finviz · Dataroma · Whalewisdom/Fintel (13F)
- กำหนด verdict: `pass` / `caution` / `red`

## References ที่ใช้

- `references/checklist-15.md` หมวด [8], [9], [10] — Benchmark + Red Flag List + แหล่งข้อมูลฟรี

## ตัวอย่างสั่ง

```
/quality NVDA
/quality META
/quality PTON
```

## Discipline

ข้อมูลจริงก่อนเสมอ (Form 4, Proxy, 10-K) · Earnings Quality = red → หยุด ไม่ดำเนินการต่อ · DSO ต้อง contextualize ตาม Sector ก่อนตัดสิน · ระบุ as-of date + source ทุกตัวเลข · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
