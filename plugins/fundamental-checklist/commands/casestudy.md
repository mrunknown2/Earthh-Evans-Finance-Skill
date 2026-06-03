---
description: "แสดงตัวอย่างจริง NVDA / META / PTON — เทียบ Framework กับของจริง สรุปบทเรียน Companion Variable และ Red Flag ที่มองเห็นได้ก่อน Collapse"
allowed-tools:
  - Read
  - Bash
  - WebSearch
  - WebFetch
model: opus
---

# /fundamental-checklist:casestudy

**Case Studies — NVDA · META · PTON** — เรียนรู้จากตัวอย่างจริงว่า Framework นี้ใช้งานอย่างไร · ข้อมูลจาก `references/case-studies.md`

## Input ที่ต้องการ

- ชื่อ Case Study (ถ้าไม่ระบุ จะแสดงทั้ง 3): `nvda`, `meta`, `pton` หรือชื่อเต็ม
- ถ้าต้องการเปรียบเทียบ 2 บริษัท ระบุได้ เช่น `/casestudy nvda pton`

## สิ่งที่ทำ

อ่านและนำเสนอ Case Study จาก `references/case-studies.md`:

### Case Study 1 — NVIDIA (FY2024) | "Premium Justified"
- EV/Sales 20–25x + After-Tax Op Margin 55%+ → Companion Variable Test ผ่านชัด
- ROIC > 100% + Net Cash + CUDA Ecosystem Moat
- PEG < 0.5x ที่ Peak — ไม่ใช่แพง เป็น Priced for Extraordinary Growth ที่เกิดขึ้นจริง
- **4 บทเรียน:** Operating Leverage + EV/Sales ต้องดูคู่ Margin + Incremental ROIC + ROIC Compounding

### Case Study 2 — META Platforms (Trough 2022 → Recovery 2023) | "Trough Misprice"
- EV/EBITDA 7–8x ที่ Trough สำหรับธุรกิจ Network Effect + Cash-Generative = Mispricing ชัด
- P/B ~2x + ROE 15%+ ใน Earnings Trough → Justified P/B Formula ให้ 2–3x แม้ Pessimistic
- "Year of Efficiency" → Fixed Cost Reset → Operating Leverage ทำงานทันที → +320% ใน 14 เดือน
- **4 บทเรียน:** Margin ปัจจุบัน ≠ Permanent · FCF คือตัวบอกความจริง · P/B + ROE · Structural Cost Reset

### Case Study 3 — Peloton (Peak 2021 → Collapse 2022) | "Speculation ล้วนๆ"
- EV/Sales 6x + After-Tax Op Margin ติดลบ → Justified EV/Sales = ติดลบ = ไม่มีทางสมเหตุสมผล
- FCF ติดลบที่ Revenue Peak = Unit Economics พัง
- **Red Flag Checklist** (ทุกข้อมองเห็นได้ก่อน Crash -95%): EV/Sales Test พัง + FCF ติดลบที่ Peak + Insider ขายที่ High + One-time Demand ถูก Price In เป็น Secular + CAC เร่งขึ้น + NRR ลดลง + Inventory Build
- **5 บทเรียน:** Companion Variable Test Objective + FCF ที่ Peak Demand + Insider Signal ต้องรวมกับ Fundamental + COVID Demand Fade + Narrative vs Reality

### ตารางเปรียบเทียบ 3 บริษัท

| Dimension | NVIDIA FY2024 | Meta Trough 2022 | Peloton Peak 2021 |
|-----------|---------------|-----------------|-----------------|
| ROIC vs WACC | >> WACC | > WACC | < WACC |
| EV/Sales ถูก Justify? | ใช่ (Margin 50%+) | ใช่ (Recovery) | ไม่ (Margin ติดลบ) |
| FCF Conversion | ~44% Margin | $19–43B FCF | ติดลบอย่างมาก |
| Operating Leverage | Extreme | ฟื้นตัว DOL>3 | Negative |
| Insider Activity | Neutral | Mixed | ขายที่ Peak |
| สรุป | BUY | BUY | AVOID |

## References ที่ใช้

- `references/case-studies.md` — ตัวเลขและบทเรียนครบทั้ง 3 Case

## ตัวอย่างสั่ง

```
/casestudy
/casestudy nvda
/casestudy pton
/casestudy meta pton
```

## Discipline

ตัวเลขใน Case Studies เป็นข้อมูลประวัติศาสตร์ ณ ช่วงที่ระบุ — ไม่สะท้อนสถานะปัจจุบันของบริษัท · ใช้เพื่อ Calibrate Framework ไม่ใช่เป็น Stock Recommendation ปัจจุบัน · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
