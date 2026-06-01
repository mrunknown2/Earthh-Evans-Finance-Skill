---
description: "efficient frontier + จุดพอร์ตปัจจุบัน + จุดหลังปรับ"
allowed-tools:
  - Read
  - Write
model: opus
---

# /portfolio-risk-architect:frontier

**Efficient Frontier** — วางพอร์ตบนแผนที่ risk-return

## Input ที่ต้องการ

- รายชื่อสินทรัพย์ + **μ, σ, ρ** ของแต่ละตัว

## สิ่งที่ทำ

- วาด **efficient frontier**
- ปักจุด **พอร์ตปัจจุบัน** เทียบกับ frontier (อยู่ใต้เส้น = ไม่ efficient)
- ปักจุด **พอร์ตหลังปรับ** (ตามข้อเสนอ) ให้เห็นการขยับ

## Discipline (สำคัญมากสำหรับ command นี้)

frontier ไวต่อ input **μ, σ, ρ** มาก — เป็น **ช่วงความเป็นไปได้ภายใต้สมมติฐาน ไม่ใช่พยากรณ์** · ระบุสมมติฐานทุกครั้ง · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
