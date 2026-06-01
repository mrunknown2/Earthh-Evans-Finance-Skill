---
description: "bar chart เทียบ Capital Weight vs Risk Contribution — ภาพที่ทรงพลังสุด"
allowed-tools:
  - Read
  - Write
model: opus
---

# /portfolio-risk-architect:risk

**Risk Contribution** — หัวใจของการวินิจฉัย: ใครคือตัวแบกความเสี่ยงจริง

## Input ที่ต้องการ

- holdings + น้ำหนัก
- vol ของแต่ละสินทรัพย์ + correlation (ถ้าไม่มี → ใช้ค่า approximate ที่ระบุว่าต้อง verify)

## สิ่งที่ทำ

- คำนวณ **Marginal Contribution to Risk (MCR)** + **% Risk Contribution** ของแต่ละสินทรัพย์
- แสดง **bar chart เทียบ Capital Weight (น้ำเงิน) vs Risk Contribution (ทอง)** — ภาพที่เผยว่า "30% ของเงิน" อาจเป็น "60–70% ของความเสี่ยง"
- เทียบกับ **risk parity** เป็น benchmark

## ตัวอย่างที่ source แสดง (illustrative)

VOO/QQQ/BTC/Cash ที่ลงคนละ 30/30/30/10 → risk contribution ราว VOO 13% · QQQ 18% · BTC 68% (σ BTC ~3–4 เท่าของหุ้น)

## Discipline

vol/correlation ที่ไม่ชัวร์ = **approximate, verify** · ระบุ as-of date · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
