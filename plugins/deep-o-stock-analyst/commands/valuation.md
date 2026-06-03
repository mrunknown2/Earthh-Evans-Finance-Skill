---
description: "Damodaran DCF เต็ม (drivers + clean-ups + stable guardrails + triangulation) → intrinsic value"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Bash
model: opus
---

# /deep-o-stock-analyst:valuation

**Intrinsic Valuation** สไตล์ Damodaran — story → numbers → value แบบเต็มระบบ

## Input ที่ต้องการ

- **ticker หุ้น** + (ถ้ามี) ผล `/livecheck` และ `/wacc`

## สิ่งที่ทำ

**B) Operating Drivers (Stage 1–3):** กำหนด path ของ revenue growth / operating margin / tax / Sales-to-Capital (`Reinvestmentₜ = ΔRevenueₜ / (S/C)ₜ`) ต่อปี

**C) Clean-ups:** excess cash · debt (book→MV) · cross-holdings · minority interests · **ESOP** Black-Scholes หักจาก equity · **NOLs** · **Failure risk** — รวมเป็น `cleanups` (net adjustment) ส่งเข้า engine · failure-risk adjust: `EV_adj = (1−p)·EV + p·(recovery·EV)` (อย่าลืม `(1−p)` ตัวหน้า)

**D) รัน engine** หา intrinsic value (ห้าม discount เอง) — mode `dcf` รับ array ต่อปี:
```bash
echo '{"mode":"dcf","revenue0":<R0>,"growths":[..N..],"margins":[..N..],"sales_to_capital":[..N..],
  "tax":<t>,"wacc":<W>,"g_terminal":<g∞>,"roic_terminal":<ROIC∞>,"terminal_margin":<m∞>,
  "net_debt":<ND>,"shares":<sh>,"cleanups":<adj>}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/deep-o-stock-analyst/scripts/valuation_engine.py"
```
engine คืน `firm_value`, `equity_value`, `value_per_share`, `terminal_value`, `terminal_reinvestment_rate` (= g∞/ROIC∞), `fcff_explicit[]`
> **Guardrails ก่อนส่ง:** `g∞ ≤` nominal GDP / risk-free · `ROIC∞ →` industry/WACC · ถ้า pre-profit/cyclical/financial → DCF ใช้ไม่ได้ตรงๆ (ดู SKILL.md discipline #7)

**E) Triangulation:** CFROI vs WACC · FCFE yield vs CoE · **Reverse DCF** (`/reversedcf`) cross-check · เทียบ `value_per_share` กับราคาตลาด → ส่วนต่าง

## ตัวอย่างสั่ง

```
/valuation NVDA
```

## Discipline

**ตัวเลข intrinsic value มาจาก engine** · ทุกตัวเลข/ข้อเท็จจริงสำคัญ **ใส่ลิงก์อ้างอิง** · ระบุ **as-of date** (YYYY-MM-DD) + สมมติฐาน (WACC, g∞, margin, S/C, ROIC∞) ทุกตัว + รายงานเป็น**ช่วง** (sensitivity WACC×g∞) ไม่ใช่จุดเดียว · ห้ามกุข้อมูล · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
