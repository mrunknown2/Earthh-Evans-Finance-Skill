---
description: "Reverse DCF — ราคาปัจจุบันฝัง expectation อะไร + reality check"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
model: opus
---

# /deep-o-stock-analyst:reversedcf

**Reverse DCF** — ถอดความคาดหวังที่ตลาดฝังในราคาวันนี้ออกมา แล้วเช็กว่าสมจริงไหม

## Input ที่ต้องการ

- **ticker หุ้น** + EV/Market Cap ปัจจุบัน + WACC

## สิ่งที่ทำ

- จาก **WACC, g∞, FCFF margin** (พร้อมเหตุผลแต่ละตัว) → คำนวณ:
  ```
  Implied steady-state Revenue = EV × (WACC − g∞) / margin
  ```
- **Reality check:** ตลาดกำลังคาดหวังให้รายได้/มาร์จิ้นโตไปถึงระดับไหน เทียบกับ TAM และ track record — สมจริง หรือ price-in ความสมบูรณ์แบบไปแล้ว
- เทียบ PEG / EV-Sales sanity ถ้าเกี่ยวข้อง

## ตัวอย่างสั่ง

```
/reversedcf NVDA
```

## Discipline

ทุกตัวเลข/ข้อเท็จจริงสำคัญ **ใส่ลิงก์อ้างอิง** · ระบุ **as-of date** (YYYY-MM-DD) · ระบุสมมติฐาน (WACC, g∞, margin) · ห้ามกุข้อมูล · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
