# valuation_engine.py — deterministic compute reference

ตัวเลข valuation ทุกตัว (WACC, DCF intrinsic value, reverse DCF, DEEP score) **ต้องมาจาก
engine นี้ ห้ามให้โมเดลบวก/คูณ/discount เอง** — เรื่องเงินต้อง deterministic + reproducible.
engine เป็น **Python 3 stdlib ล้วน** (ไม่ต้อง `pip install` · portable ข้าม IDE/provider).

โมเดลมีหน้าที่: ดึงข้อมูลจริง (งบ, rf/beta/ERP, ราคา/EV) + ใส่ลิงก์ → ประกอบ JSON → รัน engine →
**เล่าผล** + as-of date + sensitivity range + disclaimer. โมเดล**ไม่ทำเลขเอง**.

## วิธีเรียก

```bash
echo '<JSON>' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/deep-o-stock-analyst/scripts/valuation_engine.py"
```

## Modes

### `wacc` — Cost of Capital (CAPM + market-value weights)
```jsonc
{"mode":"wacc","rf":0.04,"beta":1.2,"erp":0.05,"crp":0.0,
 "equity_mv":800,"debt_mv":200,"pre_tax_cost_of_debt":0.05,"tax":0.25}
```
→ `cost_of_equity` = rf + β·(ERP+CRP) · `cost_of_debt_after_tax` = cod·(1−tax) · `weight_equity/debt` (MV) · `wacc`

### `dcf` — Intrinsic value (FCFF + Sales-to-Capital reinvestment)
```jsonc
{"mode":"dcf","revenue0":100,"growths":[..N..],"margins":[..N..],"sales_to_capital":[..N..],
 "tax":0.25,"wacc":0.10,"g_terminal":0.025,"roic_terminal":0.12,"terminal_margin":0.20,
 "net_debt":50,"shares":10,"cleanups":0,"wacc_terminal":null}
```
- `growths/margins/sales_to_capital` = array ความยาว N (จำนวนปี explicit)
- `FCFFₜ = Revenueₜ·marginₜ·(1−tax) − ΔRevenueₜ/(S/C)ₜ` · `TV = FCFF_{N+1}/(WACC∞−g∞)`, terminal reinv = g∞/ROIC∞
- `cleanups` = net adjustment (excess cash +, ESOP/minority −) · failure-risk ทำนอก engine: `(1−p)·EV + p·recovery·EV`
- → `firm_value`, `equity_value` (=firm − net_debt + cleanups), `value_per_share`, `terminal_value`, `pv_explicit_fcff`, `terminal_reinvestment_rate`, `fcff_explicit[]`

### `reverse_dcf` — terminal-anchored implied CAGR (เหมือน reverse-dcf-screener)
```jsonc
{"mode":"reverse_dcf","ev":22.6,"revenue0":0.757,"wacc":0.095,"g_terminal":0.04,
 "terminal_margin":0.35,"terminal_roic":0.15,"tax":0.25,"horizon_n":10}
```
- `TV=EV·(1+W)^N → FCFF=TV·(W−g) → R*=FCFF/[m·(1−tax)·(1−g/ROIC)] → ImpliedCAGR=(R*/R0)^(1/(N+1))−1`
- → `implied_cagr`, `implied_terminal_revenue`, `revenue_multiple_required`, `conversion`
- ⚠️ **ห้ามใช้สูตรลัด `EV×(WACC−g)/margin`** — สับสน EV ปัจจุบันกับ terminal value + ทิ้ง tax/reinvestment → understate

### `deep` — DEEP score 0–5 → 0–100 (normalized)
```jsonc
{"mode":"deep","scores":{"demand":4,"execution":3,"economics":5,"price":2,"optionality":4}}
```
- `total = Σ (scoreᵢ/5)·weightᵢ` (น้ำหนัก D25/E20/E20/P20/O15 รวม 100) — **ไม่ใช่** scoreᵢ·weightᵢ (จะเต็ม 500)
- → `total` (0–100), `contributions{}`, `verdict_band` (>=80 / 60-79 / 40-59 / <40), `signal`
- **tie-break:** ถ้า `price` (P) ต่ำ แม้ D/E/O สูง → verdict ห้ามเขียว ("ธุรกิจดีแต่ราคาแพง")

## ข้อควรระวัง (เล่าให้ผู้ใช้)

- DCF ใช้ไม่ได้กับ: pre-profit/FCF ติดลบ (→ revenue multiple), cyclical (→ normalize ทั้งวัฏจักร), ธนาคาร/ประกัน (→ FCFE/excess-return/DDM)
- `g∞ ≤` nominal GDP / risk-free · `ROIC∞ →` industry/WACC (guardrail ก่อนส่งเข้า engine)
- รายงานเป็น **ช่วง** (sensitivity WACC×g∞×margin) ไม่ใช่จุดเดียว — valuation ไวต่อ input มาก

> เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล · เรียบเรียงจาก **Earthh Evans · Invest Hub**
