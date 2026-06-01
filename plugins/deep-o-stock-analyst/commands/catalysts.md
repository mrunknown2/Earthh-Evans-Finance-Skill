---
description: "Catalysts Map 12–24 เดือน — วัน/ไตรมาส + owner metric + แหล่งอ้างอิง"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
model: opus
---

# /deep-o-stock-analyst:catalysts

**Catalysts Map** — เหตุการณ์ใน 12–24 เดือนที่จะขยับมูลค่า/ราคา

## Input ที่ต้องการ

- **ticker หุ้น**

## สิ่งที่ทำ

- ตาราง catalyst เรียงตามไทม์ไลน์ **12–24 เดือน** แต่ละแถวมี:
  - **วัน/ไตรมาส** (เช่น Q3 2026, วันประกาศงบ, วันตัดสินคดี)
  - **Event** — earnings, product launch, regulatory decision, capacity online, contract renewal
  - **Owner metric** — ตัวเลขที่ต้องจับตา (เช่น data-center revenue, gross margin, design wins)
  - **แหล่งอ้างอิง** — ลิงก์ IR calendar / filing / press
- ระบุว่าแต่ละ catalyst เอียงไป bull หรือ bear

## ตัวอย่างสั่ง

```
/catalysts NVDA
```

## Discipline

ทุกตัวเลข/ข้อเท็จจริงสำคัญ **ใส่ลิงก์อ้างอิง** · ระบุ **as-of date** (YYYY-MM-DD) · ห้ามกุข้อมูล (ไม่พบกำหนดการให้เขียน "ไม่พบข้อมูล") · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
