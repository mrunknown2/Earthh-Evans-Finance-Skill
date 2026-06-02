---
description: "Full Daily Analysis 6 ขั้นจากรูป 5 ภาพ → TRADE/SKIP/WAIT + strike/size/entry/SL 🟢🟡🔴"
allowed-tools:
  - Read
  - WebSearch
  - WebFetch
model: opus
---

# /btc-short-premium:full

**Full Daily Analysis 6 ขั้น** — รับรูป 5 ภาพ → ออก TRADE/SKIP/WAIT พร้อม strike/size/entry/SL

## Input ที่ต้องการ

- **(1) CoinGlass Derivatives BTC row** — Liquidation Heatmap / Funding Rate / OI
- **(2) Bybit Option Chain expiry วันนี้** — IV, HV, premium bid/ask, delta ทุก strike
- **(3) TradingView Daily** — trend, key S/R, candle context
- **(4) TradingView 4H** — momentum, structure, volume
- **(5) TradingView 1H** — entry timing, micro-structure
- **Macro view** — bearish / bullish / neutral (ความเห็นนายท่าน)
- **Portfolio size** — ขนาด port เป็น USD (สำหรับคำนวณ size)

## สิ่งที่ทำ

**MANDATORY MACRO CHECK ก่อนทุกครั้ง:**
- WebSearch `"economic calendar today FOMC CPI NFP"` — ถ้ามี print ก่อน 08:00 UTC → force SKIP (No-Trade Rule #1) หยุดทันที
- WebSearch `"BTC price now"` — sanity-check ราคาในรูปว่าไม่ใช่รูปเก่า

**เดิน 6-step ตาม agent framework:**
1. **Snapshot** — อ่านตัวเลขดิบจากรูปทั้ง 5 (OI, Funding, Liq, IV/HV ratio, trend direction)
2. **8-Check** — ตรวจ 8 เงื่อนไขตาม framework (ดู `agents/btc-short-premium.md`)
3. **No-Trade Rules** — ผ่านกรอง Critical Rules ทุกข้อก่อน; ติดข้อใดข้อหนึ่ง → SKIP
4. **Combination Read** — อ่าน Call/Put side เทียบกัน → เลือก leg ที่ edge ดีกว่า
5. **Verdict** — TRADE / SKIP / WAIT (commit เสมอ ห้าม "it depends")
6. **Action** — ถ้า TRADE: ระบุ strike / size (% port) / entry premium / SL ที่ Index Price ตาม framework

อ้างกฎและ threshold จาก agent framework — ไม่ redefine ตัวเลขเอง

## ตัวอย่างสั่ง

```
/full
[แนบรูป 5 ภาพ: CoinGlass, OptionChain, Daily, 4H, 1H]
macro view: bearish, portfolio $8K
```

## Discipline

อ้างตัวเลขจริงจากรูปเท่านั้น · ห้าม approximate หรือกุข้อมูลแทนรูป · เคารพ Critical Rules ทุกข้อ · SL = Index Price ตาม framework · verdict ต้อง commit ทิศทาง · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
