---
description: "Pin Risk Decision — ใกล้ 13:30 TH ปิดหรือถือ"
allowed-tools:
  - Read
model: opus
---

# /btc-short-premium:pin

**Pin Risk Decision** — รับ position + spot + distance + เวลา TH → ตัดสิน ปิดทันที / hold ถึง 13:30 TH / hold ถึง settle

## Input ที่ต้องการ

- **Position** — strategy (Short Call / Short Put), strike, entry premium
- **Spot price (BTC)** ตอนนี้ + **distance from strike** (USD)
- **Premium ตอนนี้** (Ask Price)
- **Entry premium** (ราคาที่ขาย)
- **TradingView 1H** — candle + momentum ล่าสุด
- **เวลาปัจจุบัน (TH)** — เช่น "13:00 TH"

## สิ่งที่ทำ

- ประเมิน **gamma squeeze risk** ใน TWAP settlement window (14:30–15:00 TH):
  - gamma สูงสุดเมื่อ option ใกล้ ATM + ใกล้ expiry → premium เคลื่อนเร็วมาก
  - ยิ่งใกล้ 15:00 TH (settle) + BTC ใกล้ strike → risk สูงขึ้น exponential
- ตรวจ **Pin Rule** จาก framework:
  - ถ้า BTC ห่าง strike **< $200** เมื่อถึง **13:30 TH** → **ปิด position ทันที** (90 นาทีก่อน settle 15:00 TH)
  - ถ้า BTC ห่าง strike ≥ $200 + premium decay ตามแผน → อาจ hold ต่อได้
- ตัดสิน **1 ใน 3:** ปิดทันที / hold ถึง 13:30 TH แล้วประเมินใหม่ / hold ถึง settle
- ระบุ trigger — ถ้า BTC ขยับอีก X USD → ต้องปิดทันที

Pin Rule อ้างจาก `agents/btc-short-premium.md` — ไม่ redefine threshold เอง

## ตัวอย่างสั่ง

```
/pin
Short Call 78000 | entry premium 450 | premium ตอนนี้ 180
BTC spot: 77850 | distance: 150
เวลา: 13:00 TH
[แนบรูป 1H]
```

## Discipline

อ้างตัวเลขจริงจากรูปเท่านั้น · เคารพ Critical Rules ตาม framework · SL = Index Price · Pin Rule 13:30 TH / distance < $200 / settle 15:00 TH อ้างจาก framework · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
