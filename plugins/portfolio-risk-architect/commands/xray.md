---
description: "แตก look-through holdings เป็นหุ้นรายตัวจริง + treemap น้ำหนัก sector/single-name"
allowed-tools:
  - Read
  - Write
model: opus
---

# /portfolio-risk-architect:xray

**Portfolio X-Ray (Look-Through)** — แตกทุก ETF/กองทุนลงเป็น exposure หุ้นรายตัวจริง

## Input ที่ต้องการ

- holdings + น้ำหนัก ของพอร์ต
- holdings ของแต่ละ ETF (ถ้าไม่รู้ → ใช้ค่า approximate ที่ระบุชัดว่าต้อง verify)

## สิ่งที่ทำ

- แตก ETF เป็นหุ้นจริง รวม exposure ที่ซ้ำกัน (เช่น VOO + QQQ → AAPL/MSFT/NVDA/AMZN/GOOGL/META/AVGO ทับซ้อน)
- แสดง **top-10 single-name** ของทั้งพอร์ต
- treemap น้ำหนักแยกตาม **Sector (GICS) / ประเทศ / สกุลเงิน / asset class**
- ชี้จุดที่น้ำหนักจริงต่อหุ้นกลุ่มเดียวสูงกว่าที่เจ้าของคิด

## Discipline

น้ำหนัก ETF ที่ไม่ชัวร์ = **approximate, verify** · ระบุ as-of date · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
