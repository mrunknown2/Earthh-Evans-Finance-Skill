---
description: "เปรียบเทียบ before–after risk metrics หลังทำตามข้อเสนอ"
allowed-tools:
  - Read
  - Write
model: opus
---

# /portfolio-risk-architect:rebalance

**Rebalance Before–After** — วัดผลของข้อเสนอปรับพอร์ตเป็นตัวเลข

## Input ที่ต้องการ

- น้ำหนักเดิม + **น้ำหนักใหม่ที่เสนอ** (จาก Recommendation Framework)

## สิ่งที่ทำ

เปรียบเทียบ **before vs after** ในเมตริกความเสี่ยงหลัก:
- portfolio vol · Effective Number of Bets (ENB) · Diversification Ratio
- Risk Contribution breakdown (ตัวแบกความเสี่ยงเปลี่ยนไปยังไง)
- est. max drawdown ในวิกฤตอ้างอิง

แสดงให้เห็นว่าข้อเสนอ "ลดความเสี่ยงกระจุก" ได้จริงแค่ไหน + แลกกับอะไร (trade-off)

## Discipline

ค่าเมตริกที่ไม่ชัวร์ = **approximate, verify** · ระบุ as-of date + สมมติฐาน · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
