---
description: "Reverse DCF — ราคาปัจจุบันฝัง expectation อะไร + reality check"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Bash
model: opus
---

# /deep-o-stock-analyst:reversedcf

**Reverse DCF** — ถอดความคาดหวังที่ตลาดฝังในราคาวันนี้ออกมา แล้วเช็กว่าสมจริงไหม

## Input ที่ต้องการ

- **ticker หุ้น** + EV ปัจจุบัน + revenue ฐาน (R0) + WACC + g∞ + terminal margin + terminal ROIC + tax + horizon N

## สิ่งที่ทำ

1. **รัน engine** (terminal-anchored — ห้ามใช้สูตรลัด) — mode `reverse_dcf`:
   ```bash
   echo '{"mode":"reverse_dcf","ev":<EV>,"revenue0":<R0>,"wacc":<W>,"g_terminal":<g∞>,"terminal_margin":<m>,"terminal_roic":<ROIC∞>,"tax":<tax>,"horizon_n":<N>}' \
     | python3 "${CLAUDE_PLUGIN_ROOT}/skills/deep-o-stock-analyst/scripts/valuation_engine.py"
   ```
   engine anchor บน terminal value (ไม่สับสน EV กับ TV): `TV=EV·(1+W)^N → FCFF=TV·(W−g) → R*=FCFF/[m·(1−tax)·(1−g/ROIC)] → ImpliedCAGR=(R*/R0)^(1/(N+1))−1` แล้วคืน `implied_cagr`, `implied_terminal_revenue`, `revenue_multiple_required`
   > ❌ **ห้ามใช้** `Implied Revenue = EV × (WACC − g∞) / margin` — สูตรนั้นสับสน EV ปัจจุบันกับ terminal value + ทิ้ง tax/reinvestment → understate ความคาดหวังเชิงระบบ
2. **Reality check:** `implied_cagr` ที่ตลาดฝัง สมจริงไหมเทียบ TAM + track record (เทียบ historical CAGR + forward consensus) — หรือ price-in ความสมบูรณ์แบบไปแล้ว
3. เทียบ PEG / EV-Sales sanity ถ้าเกี่ยวข้อง

## ตัวอย่างสั่ง

```
/reversedcf NVDA
```

## Discipline

**ตัวเลขมาจาก engine เท่านั้น** · ทุกตัวเลข/ข้อเท็จจริงสำคัญ **ใส่ลิงก์อ้างอิง** · ระบุ **as-of date** (YYYY-MM-DD) + สมมติฐาน (WACC, g∞, margin, ROIC∞, N) · ห้ามกุข้อมูล · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
