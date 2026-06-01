---
description: "correlation matrix heatmap (ปกติ vs regime วิกฤต)"
allowed-tools:
  - Read
  - Write
model: opus
---

# /portfolio-risk-architect:corr

**Correlation & True Diversification** — วัดการกระจายจริง ไม่ใช่จำนวน ticker

## Input ที่ต้องการ

- return series ของสินทรัพย์ หรือค่า correlation อ้างอิง (ถ้าไม่มี → approximate, verify)

## สิ่งที่ทำ

- สร้าง **pairwise correlation matrix heatmap** — แสดง 2 regime: **ตลาดปกติ vs วิกฤต**
- คำนวณ **Diversification Ratio = Σ(wᵢσᵢ)/σ_port** และ **Effective Number of Bets (ENB)**
- ย้ำหลักคิด: ในวิกฤต correlation วิ่งเข้าหา 1 — การกระจายที่ดูดีตอนปกติมักหายตอนต้องใช้

## Discipline

ค่า correlation ที่ไม่ชัวร์ = **approximate, verify** · ระบุ as-of date · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
