---
description: "AI Signal Verification — ตรวจ signal จาก bot/AI อื่นกับ framework เรา"
allowed-tools:
  - Read
  - WebSearch
model: opus
---

# /btc-short-premium:verify

**AI Signal Verification** — รับ signal จาก bot/AI อื่น → เทียบกับ 8-Check + No-Trade + Combination Read → ตาม signal หรือ override

## Input ที่ต้องการ

- **Signal จาก [bot/AI ชื่อ]** — strike, direction, เหตุผลที่ bot ให้
- **5 รูป** — CoinGlass, Bybit Option Chain, Daily, 4H, 1H

## สิ่งที่ทำ

- WebSearch `"economic calendar today FOMC CPI NFP"` + `"BTC price now"` — macro check + sanity ก่อนทุกครั้ง
- เทียบ signal กับ **8-Check Framework** (ดู `agents/btc-short-premium.md`) ทีละข้อ — แสดง ✅/❌ + ค่าจริงจากรูป
- กรอง **No-Trade Rules** — ถ้า signal ติดกฎข้อใดข้อหนึ่ง → override บังคับ (ห้าม override กฎนี้แม้ signal ดูดี)
- อ่าน **Combination Read** จากรูป option chain — ถ้า call/put side ไม่ support direction ของ signal → flag
- ตัดสิน: **"ตาม signal"** หรือ **"override"** พร้อมเหตุผล 3 บรรทัดจากข้อมูลจริง

**บทเรียนสำคัญ (อ้างจาก framework Field-Note Guardrail #2):**
indicator/AI signal เดี่ยวๆ แพ้ Combination Read — pattern ทั้ง 5 มิติชนะ signal เดี่ยวเสมอ; ถ้า signal ขัด Combination Read → override signal

อ้างกฎและ threshold จาก `agents/btc-short-premium.md` — ไม่ redefine ตัวเลขเอง

## ตัวอย่างสั่ง

```
/verify
signal: "Short Call 80000 จาก bot X" (เหตุผล: RSI overbought)
[แนบรูป 5 ภาพ: CoinGlass, OptionChain, Daily, 4H, 1H]
```

## Discipline

อ้างตัวเลขจริงจากรูปเท่านั้น · เคารพ Critical Rules ตาม framework · SL = Index Price · Combination Read > AI signal เดี่ยว · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
