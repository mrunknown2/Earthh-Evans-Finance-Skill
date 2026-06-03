---
description: "efficient frontier + จุดพอร์ตปัจจุบัน + จุดหลังปรับ"
allowed-tools:
  - Read
  - Bash
model: opus
---

# /portfolio-risk-architect:frontier

**Efficient Frontier** — วางพอร์ตบนแผนที่ risk-return

## Input ที่ต้องการ

- รายชื่อสินทรัพย์ + **μ, σ, ρ** ของแต่ละตัว + น้ำหนักพอร์ตปัจจุบัน

## สิ่งที่ทำ

1. **รัน engine** (ห้ามวาดเส้นจากการเดา) — mode `frontier`, seeded:
   ```bash
   echo '{"mode":"frontier","seed":42,"n_samples":20000,"rf":0.04,"assets":[{"name":"VOO","weight":0.3,"vol":0.16,"mu":0.08}, ...],"correlation":[[1,...],...]}' \
     | python3 "${CLAUDE_PLUGIN_ROOT}/skills/portfolio-risk-architect/scripts/portfolio_engine.py"
   ```
   engine สุ่ม long-only weights 20,000 ชุด (seeded) → คืน `min_vol`, `max_sharpe`, `current` (จุดพอร์ตปัจจุบัน), `cloud` (สำหรับ plot)
2. **วาด** cloud + ปักจุด `current` (อยู่ในกลุ่ม/ใต้ envelope = ยังไม่ efficient) เทียบ `max_sharpe` / `min_vol`
3. ถ้ามีพอร์ตหลังปรับ → รันซ้ำใส่ `current_w` ใหม่เพื่อปักจุดเทียบการขยับ

## Discipline (สำคัญมากสำหรับ command นี้)

**จุด/เส้นมาจาก engine เท่านั้น** · เป็น **random-weight approximation** (ไม่ใช่ QP-exact) แต่ reproducible ด้วย seed · frontier ไวต่อ **μ, σ, ρ** มาก — เป็น **ช่วงความเป็นไปได้ภายใต้สมมติฐาน ไม่ใช่พยากรณ์** · ระบุสมมติฐาน + seed ทุกครั้ง · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
