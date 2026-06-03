---
description: "จำลอง 10,000 เส้นทาง (GBM) → distribution ผลตอบแทน & max drawdown"
allowed-tools:
  - Read
  - Bash
model: opus
---

# /portfolio-risk-architect:montecarlo

**Monte Carlo Simulation** — จำลองหลายเส้นทางเพื่อดูช่วงผลลัพธ์ที่เป็นไปได้

## Input ที่ต้องการ

- holdings + น้ำหนัก
- **μ, σ, ρ** ของสินทรัพย์ + **horizon**

## สิ่งที่ทำ

1. **รัน engine** (ห้ามจำลองในหัว) — mode `montecarlo`, `seed` คงที่ → reproducible:
   ```bash
   echo '{"mode":"montecarlo","seed":42,"horizon_days":252,"n_paths":10000,"assets":[{"name":"VOO","weight":0.3,"vol":0.16,"mu":0.08}, ...],"correlation":[[1,...],...]}' \
     | python3 "${CLAUDE_PLUGIN_ROOT}/skills/portfolio-risk-architect/scripts/portfolio_engine.py"
   ```
   engine จำลอง **correlated GBM 10,000 เส้นทาง** (Cholesky + Box–Muller, seeded) → คืน `p5/p50/p95`, `prob_loss`, `var95/var99`, `cvar95/cvar99`, `expected_max_dd`, `worst_max_dd`
2. **เล่าผล** percentile + prob loss + E[max DD] ที่ engine คืน · ระบุ **seed + n_paths + μ/σ/ρ/horizon** ที่ใช้ (เพื่อให้ reproduce ได้)

## Discipline (สำคัญมากสำหรับ command นี้)

**ตัวเลขมาจาก engine เท่านั้น ห้ามปั้น percentile เอง** · ผลลัพธ์ = **"ช่วงความเป็นไปได้ภายใต้สมมติฐาน" ไม่ใช่การพยากรณ์** · **ระบุสมมติฐานทุกครั้ง** (μ, σ, ρ, horizon, seed) · **GBM ไม่จับ fat tail / regime change** — p5/CVaR มองโลกในแง่ดีเกินจริงในวิกฤต → เสริม `/stress` historical เสมอ · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
