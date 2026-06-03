---
description: "เช็คเร็ว — เหมาะ Terminal-Anchored ไหม (มูลค่าอยู่ปลายทาง?) + EV/Sales sanity ก่อนวิเคราะห์เต็ม"
allowed-tools:
  - Read
  - WebSearch
  - WebFetch
model: opus
---

# /reverse-dcf-screener:quick

**Quick Fit-Check** — ตรวจเร็วว่าหุ้นตัวนี้เหมาะกับ Terminal-Anchored Reverse DCF ไหม ก่อนลงทุนเวลาวิเคราะห์เต็ม

## Input ที่ต้องการ

- **ticker หุ้น** — บังคับ

## สิ่งที่ทำ

- WebSearch/WebFetch ดึงเร็วๆ: ราคา/mktcap ปัจจุบัน, revenue ล่าสุด, ลักษณะธุรกิจ (ระบุ as-of date)
- **Terminal-Anchored fit-check** — มูลค่าของบริษัทอยู่ "ปลายทาง" หรือยัง:
  - 🟢 **เหมาะ** — growth/pre-profit/high-multiple ที่มูลค่าส่วนใหญ่อยู่ใน terminal value (กำไรจริงยังน้อย ราคาฝันถึงอนาคต) → เครื่องมือนี้มีประโยชน์สูง
  - ⚠️ **ระวัง** — cyclical (margin แกว่ง) หรือ mature ที่ Hist CAGR จะ overstate Plausible → ใช้ได้แต่ต้องจูน assumptions หนัก
  - 🔴 **ไม่ค่อยเหมาะ** — ธุรกิจที่มูลค่าอยู่ที่ asset/book มากกว่า terminal earnings (เช่น financial/holding) → เครื่องมือนี้บอกได้น้อย
- **EV/Sales sanity** — คำนวณ EV/Sales คร่าวๆ: ถ้าสูงผิดปกติ = ตลาดฝันยาว (เข้าทาง Terminal-Anchored) ถ้าต่ำมาก = มูลค่าอาจไม่ได้อยู่ปลายทาง
- **สรุป** — ควรเดิน `/reverse-dcf-screener:full` ต่อ หรือเครื่องมืออื่นเหมาะกว่า + เหตุผล 1-2 บรรทัด

## ตัวอย่างสั่ง

```
/reverse-dcf-screener:quick IREN
```

## Discipline

ใส่ลิงก์อ้างอิง + as-of date ทุกตัวเลข · ห้ามกุข้อมูล (ไม่พบ → "ไม่พบข้อมูล") · นี่คือ fit-check ไม่ใช่ verdict — verdict ต้องผ่าน analyze/verify · เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล
