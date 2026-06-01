---
description: "Risk Map (Regulation/Execution/GeoFX/ESG) + Bull/Base/Bear + thesis killers"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
model: opus
---

# /deep-o-stock-analyst:risk

**Risk Map + Scenarios** — อะไรทำให้ thesis พังได้บ้าง และพังแล้วราคาไปไหน

## Input ที่ต้องการ

- **ticker หุ้น** + thesis หลัก (จาก `/full` หรือผู้ใช้)

## สิ่งที่ทำ

- **Risk Map 4 ด้าน** (+ ลิงก์หน่วยงาน/แหล่งอ้างอิง):
  - **Regulation** — คดี/ใบอนุญาต/สอบสวน + ไทม์ไลน์/เพดานโทษ
  - **Execution** — guidance miss, margin, supply chain (foundry/hyperscalers/ลูกค้าใหญ่)
  - **GeoFX** — ภูมิรัฐศาสตร์, สกุลเงิน, tariff
  - **ESG** — governance/SBC/related-party
- **Bull / Base / Bear** — 3 ฉาก พร้อมตัวเลขเป้าหมายคร่าวๆ
- **Triggers & Thesis Killers** — สัญญาณอะไรที่ถ้าเกิดแล้วต้องเปลี่ยนคำตัดสินทันที

## ตัวอย่างสั่ง

```
/risk NVDA
```

## Discipline

ทุกตัวเลข/ข้อเท็จจริงสำคัญ **ใส่ลิงก์อ้างอิง** (หน่วยงานกำกับ) · ระบุ **as-of date** (YYYY-MM-DD) · ห้ามกุข้อมูล · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
