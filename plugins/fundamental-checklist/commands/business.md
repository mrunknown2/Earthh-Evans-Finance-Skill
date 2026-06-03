---
description: "วิเคราะห์หมวด [1–2] Business Overview + Moat — Revenue Model, TAM, Recurring vs Cyclical, ROIC>WACC Moat Verification; Moat เป็น Critical Category (red = AVOID)"
allowed-tools:
  - Read
  - Bash
  - WebSearch
  - WebFetch
model: opus
---

# /fundamental-checklist:business

**Business Overview + Moat** — ตรวจสอบว่าธุรกิจทำเงินได้อย่างไร และมีข้อได้เปรียบเชิงโครงสร้างที่ยั่งยืนหรือไม่ ตรงกับ Checklist หมวด [1–2]

## Input ที่ต้องการ

- **ticker หุ้น** พร้อม Sector
- งบล่าสุด (Revenue breakdown, Gross Margin trend, ROIC ย้อนหลัง 5 ปี, WACC)

## สิ่งที่ทำ

### หมวด [1] Business Overview

- **1a. Core Business Model** — Recurring vs Cyclical? Cross-check: Recurring → Gross Margin คงตัวหรือขยายตัว 3 ปีขึ้นไป
- **1b. Revenue Model** — จำแนกประเภท (Subscription/SaaS, Usage-Based, Transaction, One-Time/Hardware, Contract/Backlog, Commodity/Cyclical) + Metric สำคัญต่อประเภท
- **1c. TAM / SAM / SOM** — TAM ใหญ่พอสำหรับ Thesis 10 ปีไหม? ถ้า Market Share > 30% แล้ว Growth ต้องมาจากไหน?
  - Red Flag: อ้าง TAM ใหญ่มากแต่ไม่อธิบาย Capture Path

### หมวด [2] Moat

- ระบุประเภท Moat: Network Effect / Switching Cost / Cost Advantage / Brand+Intangible / Efficient Scale / IP+Patent
- **Moat Verification Test (Damodaran):**
  - ROIC > WACC ต่อเนื่อง 5 ปีขึ้นไป = พิสูจน์ Moat แล้ว
  - ROIC > WACC แค่ 1–2 ปี = อาจ Cyclical Benefit ไม่ใช่ Structural Advantage
  - Incremental ROIC > Average ROIC = Moat กำลังขยาย
  - Gross Margin คงตัวหรือขยายตัวช่วงเงินเฟ้อ = Pricing Power พิสูจน์ตัวเองแล้ว
- กำหนด verdict: `pass` / `caution` / `red`

> **CRITICAL:** Moat เป็น Critical Category — ถ้า verdict = `red` → สรุป AVOID ทันที ไม่ดำเนินการต่อ

## References ที่ใช้

- `references/checklist-15.md` หมวด [1] และ [2] — Revenue Model Table + Moat Type + Verification Test

## Output Format

สรุปสองหมวด:
1. Business Overview — ประเภทธุรกิจ + Revenue Model + TAM Assessment + Red Flags (ถ้ามี)
2. Moat — ประเภท Moat + Verification Results + ROIC vs WACC ย้อนหลัง 5 ปี (as-of date + source) + verdict

## ตัวอย่างสั่ง

```
/business NVDA
/business KO
/business PTON
```

## Discipline

ข้อมูลจริงก่อนเสมอ (Search > Memory) · ROIC ต้องคำนวณจาก 10-K ล่าสุด ไม่ใช้จาก Memory · ระบุ as-of date + source ทุกตัวเลข · Moat = red → หยุด ไม่ดำเนินการต่อ · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
