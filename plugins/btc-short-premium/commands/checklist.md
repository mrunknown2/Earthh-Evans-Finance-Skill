---
description: "Pre-Trade Gate — 8-Check Framework + No-Trade Rules ทีละข้อ → pass/fail"
allowed-tools:
  - Read
  - WebSearch
model: opus
---

# /btc-short-premium:checklist

**Pre-Trade Gate** — เดิน 8-Check + No-Trade Rules 7 ข้อทีละข้อ → สรุป pass/fail พร้อมค่าจริงจากรูป

## Input ที่ต้องการ

- **(1) CoinGlass Derivatives BTC row** — Liquidation Heatmap / Funding Rate / OI
- **(2) Bybit Option Chain expiry วันนี้** — IV, HV, delta, premium
- **(3) TradingView Daily** — trend, key S/R
- **(4) TradingView 4H** — momentum, ATR
- **(5) TradingView 1H** — micro-structure
- หรือพิมพ์ **ตัวเลขดิบ** แทนรูป (Liq, Funding, IV, HV, ATR ฯลฯ)

## สิ่งที่ทำ

**MANDATORY MACRO CHECK ก่อนทุกครั้ง (= Check #1):**
- WebSearch `"economic calendar today FOMC CPI NFP"` — ถ้ามี print ก่อน 08:00 UTC → ❌ Force SKIP (No-Trade Rule #1) หยุดทันที ไม่เดิน check ต่อ
- WebSearch `"BTC price now"` — sanity-check ราคาในรูปว่าไม่ใช่รูปเก่า

**เดิน 8-Check Framework ทีละข้อ** (ดู `8-CHECK FRAMEWORK` ใน agent) แสดง ✅/❌ + ค่าจริง:

| # | Check | เกณฑ์ผ่าน | ค่าจริง | ผล |
|---|-------|-----------|---------|-----|
| 1 | Macro Event | ไม่มี FOMC/CPI/NFP ก่อน settle | — | ✅/❌ |
| 2 | IV/HV Ratio | ≥ 1.15 (ideal > 1.5) | — | ✅/❌ |
| 3 | SD Distance | Strike > 1.5 SD จาก spot | — | ✅/❌ |
| 4 | Funding Rate | Neutral zone (±0.01%) | — | ✅/❌ |
| 5 | Delta | 0.13–0.15 (sweet spot) | — | ✅/❌ |
| 6 | Resistance/Support | Strike confluence กับ MA/level | — | ✅/❌ |
| 7 | ATR Filter | Strike > 1.5× ATR 4H | — | ✅/❌ |
| 8 | Combination Read | ไม่ติด pattern อันตราย | — | ✅/❌ |

**เดิน No-Trade Rules 7 ข้อ** (ดู `NO-TRADE RULES` ใน agent) flag ข้อที่ติด:

1. FOMC/CPI/NFP day → SKIP
2. IV < HV (ratio < 1.0) → SKIP
3. BTC rallied 5%+ วันก่อน → SKIP
4. ขาดทุน 3 ครั้งติด → หยุด 2–3 วัน
5. Active liquidation > $200M → SKIP
6. Funding < −0.03% → SKIP Short Call
7. Gut uncertainty → SKIP

**สรุป pass/fail gate:**
- ผ่านทั้ง 8-Check และ 7 No-Trade Rules → **PASS — เดิน /full ต่อได้**
- ขาด 8-Check 1 ข้อ → **ลด size หรือ skip**
- ติด No-Trade Rule ข้อใดข้อหนึ่ง → **FAIL — SKIP วันนี้**

อ้างกฎและ threshold จาก `agents/btc-short-premium.md` — ไม่ redefine ตัวเลขเอง

## ตัวอย่างสั่ง

```
/checklist
[แนบ 5 รูป: CoinGlass, OptionChain, Daily, 4H, 1H]
```

## Discipline

อ้างค่าจริงจากรูปทุก check · ห้าม approximate หรือกุข้อมูลแทนรูป · ถ้า Liq > $200M = FAIL ทันที (ดู `CRITICAL RULES` ใน agent) · สรุป pass/fail commit ทิศทาง ห้าม "it depends" · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
