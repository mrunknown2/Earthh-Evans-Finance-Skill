---
description: "เปรียบเทียบ before–after risk metrics หลังทำตามข้อเสนอ"
allowed-tools:
  - Read
  - Bash
model: opus
---

# /portfolio-risk-architect:rebalance

**Rebalance Before–After** — วัดผลของข้อเสนอปรับพอร์ตเป็นตัวเลข

## Input ที่ต้องการ

- น้ำหนักเดิม + **น้ำหนักใหม่ที่เสนอ** (จาก Recommendation Framework) + σ/ρ/μ เดียวกันทั้งสองชุด

## สิ่งที่ทำ

1. **รัน engine 2 รอบ** (ห้ามเทียบเลขในหัว) — mode `all`, **σ/ρ/seed เดียวกัน** ต่างแค่ `weight`:
   ```bash
   # before
   echo '{"mode":"all","seed":42,"assets":[{"name":"BTC","weight":0.30,"vol":0.60,"mu":0.20}, ...],"correlation":[[...]], "scenarios":[...]}' \
     | python3 "${CLAUDE_PLUGIN_ROOT}/skills/portfolio-risk-architect/scripts/portfolio_engine.py"
   # after — น้ำหนักใหม่ (เช่นลด BTC, เพิ่ม bond/gold) σ/ρ คงเดิม
   echo '{"mode":"all","seed":42,"assets":[{"name":"BTC","weight":0.15,...}, ...], ...}' \
     | python3 "${CLAUDE_PLUGIN_ROOT}/skills/portfolio-risk-architect/scripts/portfolio_engine.py"
   ```
2. **เทียบ before vs after** จากค่า engine: `portfolio_vol` · `enb` · `diversification_ratio` · `rc_pct` ต่อสินทรัพย์ (ตัวแบกความเสี่ยงเปลี่ยนยังไง) · `expected_max_dd` + stress `portfolio_return`
3. สรุปว่าข้อเสนอ "ลดความเสี่ยงกระจุก" ได้จริงแค่ไหน (Δ ตัวเลข) + แลกกับอะไร (Δ expected return, cost, tax)

## Discipline

**ทุกเมตริก before/after มาจาก engine ด้วย σ/ρ/seed เดียวกัน** (เทียบกันได้แฟร์) · ค่าที่ไม่ชัวร์ = approximate, verify + as-of date · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
