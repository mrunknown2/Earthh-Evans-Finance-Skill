---
description: "คำนวณ Cost of Capital → เส้นทาง WACC (current → sector-stable)"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Bash
model: opus
---

# /deep-o-stock-analyst:wacc

**Cost of Capital** สไตล์ Damodaran — จาก WACC ปัจจุบันสู่ระดับเสถียร

## Input ที่ต้องการ

- **ticker หุ้น** + (ถ้ามี) ผล `/livecheck` ล่าสุด

## สิ่งที่ทำ

1. **หาข้อมูลจริง:** Risk-free (สกุลที่รายงาน) · ERP/CRP (Damodaran Online) · **Beta** (bottom-up/sector ไม่ใช่ regression ดิบ) · pre-tax cost of debt (rating/synthetic) · market-value weights ของ equity/debt · tax
2. **รัน engine** หา WACC (ห้ามคูณเอง) — mode `wacc`:
   ```bash
   echo '{"mode":"wacc","rf":0.04,"beta":1.2,"erp":0.05,"crp":0.0,"equity_mv":<E>,"debt_mv":<D>,"pre_tax_cost_of_debt":0.05,"tax":0.25}' \
     | python3 "${CLAUDE_PLUGIN_ROOT}/skills/deep-o-stock-analyst/scripts/valuation_engine.py"
   ```
   คืน `cost_of_equity` (rf + β·(ERP+CRP)), `cost_of_debt_after_tax`, `weight_equity/debt`, `wacc`
3. **เส้นทาง WACC:** อธิบายว่าปรับไปสู่ระดับ sector/stable ที่เท่าไหร่ ทำไม (beta → 1, debt ratio → target) — รัน engine ซ้ำด้วยพารามิเตอร์ stable เพื่อได้ WACC∞

## ตัวอย่างสั่ง

```
/wacc NVDA
```

## Discipline

ทุกตัวเลข/ข้อเท็จจริงสำคัญ **ใส่ลิงก์อ้างอิง** (รวม Damodaran Online ERP/Beta) · ระบุ **as-of date** (YYYY-MM-DD) · ห้ามกุข้อมูล (ไม่พบให้เขียน "ไม่พบข้อมูล") · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
