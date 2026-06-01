---
description: "drawdown ของพอร์ตในวิกฤตจริง (GFC2008/COVID2020/2022/Yen2024)"
allowed-tools:
  - Read
  - Write
model: opus
---

# /portfolio-risk-architect:stress

**Tail Risk & Stress Test** — จำลองพอร์ตในเหตุการณ์วิกฤตจริง

## Input ที่ต้องการ

- holdings + น้ำหนัก
- beta/sensitivity ของแต่ละสินทรัพย์ต่อแต่ละ shock (ถ้าไม่มี → approximate, verify)

## สิ่งที่ทำ

จำลอง drawdown ของพอร์ตในวิกฤตจริง:
- **GFC 2008** · **COVID 2020** · **2022 Rate Shock** · **Aug 2024 Yen Carry Unwind**

รายงานต่อเหตุการณ์: **est. max drawdown**, **time-to-recover**, **VaR & CVaR (95/99%)**

## Discipline

ผลเป็น **est. ภายใต้สมมติฐาน** ไม่ใช่ตัวเลขที่จะเกิดซ้ำแน่นอน · ระบุ as-of date + สมมติฐาน beta · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
