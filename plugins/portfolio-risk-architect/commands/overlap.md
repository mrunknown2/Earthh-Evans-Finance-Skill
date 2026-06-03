---
description: "heatmap ความซ้ำซ้อนระหว่างกอง — ชี้ที่ 'ซื้อซ้ำ'"
allowed-tools:
  - Read
model: opus
---

# /portfolio-risk-architect:overlap

**Overlap Analysis** — วัดความซ้ำซ้อนของ holdings ระหว่างกองที่ถือ

## Input ที่ต้องการ

- top holdings ของแต่ละกอง/ETF ในพอร์ต

## สิ่งที่ทำ

- คำนวณ **weighted holdings overlap %** ระหว่างกองแต่ละคู่
- แสดงเป็น heatmap ความซ้ำซ้อน
- ชี้ส่วนที่เป็น **"ซื้อของซ้ำ"** (เงินที่จ่ายเพื่อ exposure เดียวกันสองรอบ) — เช่น VOO กับ QQQ ทับซ้อนกลุ่ม mega-cap tech

## Discipline

ค่า holdings ที่ไม่ชัวร์ = **approximate, verify** · ระบุ as-of date · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
