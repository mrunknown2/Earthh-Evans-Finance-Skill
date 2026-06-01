---
description: "Option-Adjusted Valuation — ตัว O ใน DEEP+O (inventory, stage, window, milestones)"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
model: opus
---

# /deep-o-stock-analyst:options

**Option-Adjusted Valuation** — ตัว **O** ของ DEEP+O: มูลค่าแฝงที่ DCF แกนหลักจับไม่ได้

## Input ที่ต้องการ

- **ticker หุ้น** + EV_core จาก `/valuation` หรือ `/reversedcf`

## สิ่งที่ทำ

- **Inventory ของ optionality:** real options, ธุรกิจ/ตลาดใหม่, platform extension, milestones (เช่น drug pipeline, AI compute, new geography)
- ประเมินแต่ละ option: stage · window (เวลาที่ยังเปิด) · economics@scale · ความน่าจะเป็น
- รวม: `EV_core (Reverse DCF/DCF) + ΣEV(options) → EV_total`
- **ชี้ว่าตลาดใส่มูลค่า optionality อะไรไปแล้ว** — กำลังจ่ายล่วงหน้าให้ option ที่ยังไม่เกิดหรือไม่

## ตัวอย่างสั่ง

```
/options TSLA
```

## Discipline

ทุกตัวเลข/ข้อเท็จจริงสำคัญ **ใส่ลิงก์อ้างอิง** · ระบุ **as-of date** (YYYY-MM-DD) · แยก fact / judgment ของแต่ละ option · ห้ามกุข้อมูล · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
