---
description: "Mark Price Anomaly — Unrealized Loss แปลกๆ จริงหรือ noise"
allowed-tools:
  - Read
model: opus
---

# /btc-short-premium:anomaly

**Mark Price Anomaly** — รับ position + Mark Price + Unrealized Loss → อธิบายว่าเป็น noise หรือ loss จริง + สรุป hold/close

## Input ที่ต้องการ

- **Position** — strategy (Short Call / Short Put), strike, entry premium
- **Mark Price** ตอนนี้ + **Unrealized Loss %** ที่เห็นบน Bybit
- **Spot price (BTC)** ตอนนี้
- **Bybit Option Chain** — bid/ask ของ strike ที่ถืออยู่

## สิ่งที่ทำ

อธิบายกลไก Mark Price + ให้ภาพจริง:

1. **Mark Price คำนวณจาก IV model** — Bybit ใช้ theoretical IV pricing อาจ inflate สูงกว่าราคาตลาดจริง โดยเฉพาะตอน IV spike หรือ bid-ask กว้าง → Unrealized Loss ที่เห็นอาจ "ของปลอม" (อ้าง Field-Note Guardrail #1 จาก framework)
2. **ดู Ask Price แทน Mark** — ราคาที่จะปิด position ได้จริงคือ Ask Price ไม่ใช่ Mark Price; ถ้า Ask << Mark → loss จริงน้อยกว่าที่เห็น
3. **ดู Index Price** — ตรวจว่า option อยู่ใน-the-money (ITM) จริงไหม; ถ้า BTC ยังห่าง strike ใน safe zone → option ยังไม่ intrinsic value
4. **สรุป hold / close** — ถ้า Ask Price ยังรับได้และ BTC ยังอยู่ safe zone → hold; ถ้า ITM + Ask Price สูง → พิจารณาปิด

อ้างกฎและ threshold จาก `agents/btc-short-premium.md` — ไม่ redefine ตัวเลขเอง

## ตัวอย่างสั่ง

```
/anomaly
Short Call 78000 | entry premium 450
Mark Price: 820 | Unrealized Loss: -82%
BTC spot: 76500
[แนบรูป Bybit Option Chain]
```

## Discipline

อ้างตัวเลขจริงจากรูปเท่านั้น · Mark Price ≠ ราคาปิดจริง ดู Ask Price เสมอ · SL = Index Price · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
