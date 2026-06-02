---
description: "Position Check — position เปิดอยู่ → hold/close/adjust + TP zone"
allowed-tools:
  - Read
model: opus
---

# /btc-short-premium:position

**Position Check** — รับ position ปัจจุบัน + option chain + 1H → ตัดสิน hold / ปิดกำไร / ปิดขาดทุน / adjust พร้อม TP zone

## Input ที่ต้องการ

- **Position ปัจจุบัน** — strategy (Short Call / Short Put), strike, entry premium, spot ตอนเปิด, time to expiry
- **Bybit Option Chain expiry วันนี้** — premium bid/ask, IV, delta ของ strike ที่ถืออยู่
- **TradingView 1H** — candle + volume context ล่าสุด

## สิ่งที่ทำ

- ประเมิน **safe zone vs danger zone** จาก option chain + 1H:
  - safe zone — premium decay ตามแผน, BTC ห่าง strike ปลอดภัย, IV ไม่ขยาย
  - danger zone — BTC เข้าใกล้ strike, IV spike, หรือ premium ย้อนกลับ > 50% จาก entry
- ตัดสิน **1 ใน 4 action:** hold ต่อ / ปิดกำไร (TP) / ปิดขาดทุน (SL) / adjust (roll/hedge)
- บอก **trigger ที่ต้องระวัง** — เช่น ถ้า BTC ขึ้น/ลงถึง X → exit ทันที
- ระบุ **TP zone** — premium เหลือ % เท่าไรของ entry premium ควรปิด (ดู threshold จาก agent framework)
- อ้าง SL method จาก agent framework — SL = Index Price ไม่ใช่ Mark Price

อ้างกฎและ threshold จาก `agents/btc-short-premium.md` — ไม่ redefine ตัวเลขเอง

## ตัวอย่างสั่ง

```
/position
Short Call 78000 | entry premium 450 | spot 76200 | 4h to expiry
[แนบรูป Bybit Option Chain + 1H]
```

## Discipline

อ้างตัวเลขจริงจากรูปเท่านั้น · เคารพ Critical Rules ตาม framework · SL = Index Price · TP zone อ้างจาก framework ไม่กุเอง · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
