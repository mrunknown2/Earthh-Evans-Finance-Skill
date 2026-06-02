---
description: "Quick Morning Check ~2 นาที — regime (quiet/recovery/cascade) → ควร full ต่อ หรือ skip"
allowed-tools:
  - Read
  - WebSearch
model: opus
---

# /btc-short-premium:quick

**Quick Morning Check ~2 นาที** — อ่าน regime จาก CoinGlass + 1H → บอกว่าควรเปิด `/full` หรือ skip

## Input ที่ต้องการ

- **CoinGlass Derivatives BTC row** — Liquidation, Funding Rate, OI (แคปเดียว)
- **TradingView 1H** — candle + volume context

## สิ่งที่ทำ

- WebSearch `"economic calendar today FOMC CPI NFP"` — sanity macro วันนี้; ถ้ามี event ใหญ่ → แจ้งทันที
- อ่าน **regime** จาก Liquidation + Funding ในรูป CoinGlass:
  - **quiet** — Liq ต่ำ, Funding ใกล้ศูนย์ → edge ดี, แนะนำ `/full`
  - **recovery** — Liq เพิ่งพีค, Funding rebounding → รอ settle ก่อน
  - **cascade** — Liq > $200M หรือ Funding spike ผิดปกติ → **SKIP ทันที** ไม่ต้องแคปครบ 5 รูป
- บอก regime ปัจจุบัน + เหตุผล 1-2 บรรทัดจากตัวเลขในรูป
- สรุป: **ควรเปิด `/full` ต่อ** หรือ **skip วันนี้**

threshold cascade (`Liq > $200M`) อ้างจาก agent framework — ไม่ redefine เอง

## ตัวอย่างสั่ง

```
/quick
[แนบรูป CoinGlass + 1H]
```

## Discipline

อ้างตัวเลขจริงจากรูปเท่านั้น · เคารพ Critical Rules ตาม framework · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
