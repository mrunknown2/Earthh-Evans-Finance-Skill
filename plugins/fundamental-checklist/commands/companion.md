---
description: "คำนวณ Justified Multiple ทั้ง 6 ตัวจาก Damodaran Companion Variables (P/E, EV/Sales, EV/EBITDA, P/B, PEG, FCF Yield) — verdict ต่อ multiple: P/E·EV/Sales·P/B → cheap/fair/expensive (EV/Sales → speculation ถ้า margin ≤ 0) · PEG → undervalued/fair/overvalued · EV/EBITDA·FCF Yield → context"
allowed-tools:
  - Read
  - Bash
  - WebSearch
  - WebFetch
model: opus
---

# /fundamental-checklist:companion

**Companion Variable Analysis** — คำนวณ Justified Multiple ครบ 6 ตัวจาก Damodaran Framework · รัน engine `companion` mode ทีละ Multiple

## Input ที่ต้องการ

- **ticker หุ้น** + งบล่าสุด (Revenue, EBIT, EBITDA, Net Income, CapEx, FCF, Equity, Debt, Cash)
- WACC และ Cost of Equity (ดึงจาก Damodaran หรือ bottom-up)
- Payout Ratio, ROE, growth assumptions (g) ล่าสุด

## สิ่งที่ทำ

ดึงข้อมูลจริง → รัน engine `companion` mode **ทีละ Multiple** (6 calls) → สรุปตารางเปรียบเทียบ Actual vs Justified per Multiple

| Multiple | Companion Variable | สูตร Justified |
|----------|--------------------|----------------|
| PEG | EPS Growth Rate | P/E ÷ EPS Growth (5Y CAGR) |
| P/E | EPS Growth + Payout | `(Payout × (1+g)) / (CoE − g)` |
| EV/Sales | After-Tax Op Margin | `Margin × (1−Reinv) / (WACC−g)` |
| EV/EBITDA | CapEx Intensity + ROIC | `EV / (EBITDA − MaintCapEx)` พร้อม ROIC vs WACC |
| P/B | Return on Equity (ROE) | `(ROE − g) / (CoE − g)` |
| FCF Yield | FCF Growth + Capital Intensity | `FCFF / EV` พร้อม Owner Earnings |

## Engine Calls (ทีละ Multiple)

```bash
# CV-1a: PEG
echo '{"mode":"companion","multiple":"peg","pe":35,"eps_growth_5y":35}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"

# CV-1b: Justified P/E
echo '{"mode":"companion","multiple":"pe","payout":0.3,"g":0.08,"coe":0.10,"actual_pe":35}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"

# CV-2: Justified EV/Sales
echo '{"mode":"companion","multiple":"ev_sales","ebit":32.7e9,"tax":0.21,"revenue":60.9e9,"reinv_rate":0.05,"wacc":0.09,"g":0.05,"actual_ev_sales":22}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"

# CV-3: EV/(EBITDA-MaintCapEx) + ROIC
echo '{"mode":"companion","multiple":"ev_ebitda","ebitda":40e9,"maint_capex":3e9,"ev":600e9,"roic":1.0,"wacc":0.09}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"

# CV-4: Justified P/B
echo '{"mode":"companion","multiple":"pb","roe":0.30,"g":0.08,"coe":0.10,"actual_pb":11}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"

# CV-5: FCF Yield + Owner Earnings
echo '{"mode":"companion","multiple":"fcf_yield","fcff":27e9,"ev":1200e9,"ni":29.8e9,"da":3.4e9,"maint_capex":2e9,"wc_change":1e9}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```

Output keys per call: `multiple`, `justified`, `actual`, `verdict`, `gap`, `note`
Verdict ต่อ multiple: P/E·EV/Sales·P/B → `cheap`/`fair`/`expensive` (EV/Sales → `speculation` ถ้า margin ≤ 0) · PEG → `undervalued`/`fair`/`overvalued` · EV/EBITDA·FCF Yield → `context` (อ่านคู่ ROIC-vs-WACC / bond yield, `justified` = null)

## Output Format

**ตัวอย่าง output จริงจาก engine** (จาก JSON ด้านบน):

| Multiple | Justified | Actual | Verdict | Gap | Companion Variable |
|----------|-----------|--------|---------|-----|-------------------|
| PEG | — | 1.0 | fair | — | EPS Growth 5Y (pe=35, g=35%) |
| P/E | 16.2x | 35x | expensive | +18.8x | Payout 30%, g 8%, CoE 10% |
| EV/Sales | 10.07x | 22x | expensive | +11.93x | After-Tax Margin 42.4% |
| EV/EBITDA | — | 16.2x | context | — | ROIC 100% vs WACC 9% (value-creating) |
| P/B | 11.0x | 11x | fair | ~0 | ROE 30%, g 8%, CoE 10% |
| FCF Yield | — | 2.25% | context | — | FCFF $27B / EV $1,200B |

พร้อม context ว่าทำไม Multiple ถึงอยู่ที่ระดับนั้น

## References ที่ใช้

- `references/companion-variables.md` — สูตร Justified Multiple ทั้ง 6 + Benchmark Table + PEG Trap + DuPont ROE + Owner Earnings

## ตัวอย่างสั่ง

```
/companion NVDA
/companion META
```

## Discipline

ดึงข้อมูลจริง ไม่ estimate ในหัว · ระบุ as-of date + source ทุกตัวเลข · WACC ดึงจาก Damodaran หรือ bottom-up ไม่ใช้ค่าเดาสุ่ม · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
