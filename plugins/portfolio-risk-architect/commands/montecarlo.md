---
description: "จำลอง 10,000 เส้นทาง (GBM) → distribution ผลตอบแทน & max drawdown"
allowed-tools:
  - Read
  - Write
model: opus
---

# /portfolio-risk-architect:montecarlo

**Monte Carlo Simulation** — จำลองหลายเส้นทางเพื่อดูช่วงผลลัพธ์ที่เป็นไปได้

## Input ที่ต้องการ

- holdings + น้ำหนัก
- **μ, σ, ρ** ของสินทรัพย์ + **horizon**

## สิ่งที่ทำ

- จำลอง **10,000 เส้นทาง (GBM)** → **distribution ของผลตอบแทน & max drawdown**
- แสดง percentile (เช่น p5/p50/p95), prob. of loss, expected max DD

## Discipline (สำคัญมากสำหรับ command นี้)

ผลลัพธ์ = **"ช่วงความเป็นไปได้ภายใต้สมมติฐาน" ไม่ใช่การพยากรณ์** · **ระบุสมมติฐานทุกครั้ง** (μ, σ, ρ, horizon) · GBM ไม่จับ fat tail / regime change ได้ครบ — เตือนผู้ใช้ · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
