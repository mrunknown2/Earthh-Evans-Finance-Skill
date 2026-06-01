---
description: "Damodaran DCF เต็ม (drivers + clean-ups + stable guardrails + triangulation) → intrinsic value"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
model: opus
---

# /deep-o-stock-analyst:valuation

**Intrinsic Valuation** สไตล์ Damodaran — story → numbers → value แบบเต็มระบบ

## Input ที่ต้องการ

- **ticker หุ้น** + (ถ้ามี) ผล `/livecheck` และ `/wacc`

## สิ่งที่ทำ

**B) Operating Drivers (Stage 1–3):**
- Revenue growth: ปีถัดไป + เฉลี่ยปี 2–5, 6–10 (อธิบายตัวขับ)
- Margin path: operating margin → เป้าเสถียร
- Tax: effective → marginal
- Reinvestment (Sales-to-Capital): `Reinvestment_t = ΔRevenue_t / (S/C_t)` (ระบุ S/C ปี 1–5, 6–10)

**C) Clean-ups:** excess cash · debt (book→MV) · cross-holdings · minority interests · **ESOP** Black-Scholes หักจาก equity · **NOLs** · **Failure risk** `p_failure × recovery` (บังคับถ้า early/fragile)

**D) Stable Guardrails:** `g∞ ≤ nominal GDP` · `ROIC∞ → industry/WACC` · `Terminal reinvestment = g∞/ROIC∞` (โชว์ค่า)

**E) Triangulation:** CFROI vs WACC · FCFE yield vs CoE · Reverse DCF cross-check

→ **Intrinsic value / share** + ส่วนต่างจากราคาตลาด

## ตัวอย่างสั่ง

```
/valuation NVDA
```

## Discipline

ทุกตัวเลข/ข้อเท็จจริงสำคัญ **ใส่ลิงก์อ้างอิง** · ระบุ **as-of date** (YYYY-MM-DD) · ระบุสมมติฐาน (WACC, g∞, margin, S/C) ทุกตัว · ห้ามกุข้อมูล · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
