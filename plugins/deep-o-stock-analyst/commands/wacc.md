---
description: "คำนวณ Cost of Capital → เส้นทาง WACC (current → sector-stable)"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
model: opus
---

# /deep-o-stock-analyst:wacc

**Cost of Capital** สไตล์ Damodaran — จาก WACC ปัจจุบันสู่ระดับเสถียร

## Input ที่ต้องการ

- **ticker หุ้น** + (ถ้ามี) ผล `/livecheck` ล่าสุด

## สิ่งที่ทำ

- **Cost of Equity:** Risk-free (สกุลที่รายงาน) + ERP/CRP + **Beta** (bottom-up/sector ไม่ใช่ regression ดิบ)
- **Cost of Debt:** pre-tax + spread (จาก rating/synthetic rating)
- **Weights:** target capital structure แบบ **market value** (ไม่ใช่ book)
- → **WACC ตอนเริ่ม**
- **เส้นทาง WACC:** อธิบายว่าปรับไปสู่ระดับ sector/stable ที่เท่าไหร่ ทำไม (beta → 1, debt ratio → target)

## ตัวอย่างสั่ง

```
/wacc NVDA
```

## Discipline

ทุกตัวเลข/ข้อเท็จจริงสำคัญ **ใส่ลิงก์อ้างอิง** (รวม Damodaran Online ERP/Beta) · ระบุ **as-of date** (YYYY-MM-DD) · ห้ามกุข้อมูล (ไม่พบให้เขียน "ไม่พบข้อมูล") · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
