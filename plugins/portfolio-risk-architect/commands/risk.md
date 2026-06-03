---
description: "bar chart เทียบ Capital Weight vs Risk Contribution — ภาพที่ทรงพลังสุด"
allowed-tools:
  - Read
  - Bash
model: opus
---

# /portfolio-risk-architect:risk

**Risk Contribution** — หัวใจของการวินิจฉัย: ใครคือตัวแบกความเสี่ยงจริง

## Input ที่ต้องการ

- holdings + น้ำหนัก
- vol ของแต่ละสินทรัพย์ + correlation (ถ้าไม่มี → ใช้ค่า approximate ที่ระบุว่าต้อง verify)

## สิ่งที่ทำ

1. **รัน engine** (ห้ามคำนวณเอง) — ประกอบ JSON แล้ว pipe เข้า `portfolio_engine.py` mode `risk`:
   ```bash
   echo '{"mode":"risk","assets":[{"name":"VOO","weight":0.30,"vol":0.16},{"name":"QQQ","weight":0.30,"vol":0.22},{"name":"BTC","weight":0.30,"vol":0.60},{"name":"Cash","weight":0.10,"vol":0.0}],"correlation":[[1,0.9,0.4,0],[0.9,1,0.45,0],[0.4,0.45,1,0],[0,0,0,1]]}' \
     | python3 "${CLAUDE_PLUGIN_ROOT}/skills/portfolio-risk-architect/scripts/portfolio_engine.py"
   ```
   engine คืน `portfolio_vol`, `diversification_ratio`, `enb`, `effective_holdings`, `hhi` และต่อสินทรัพย์ `weight` (=%capital) เทียบ `rc_pct` (=%risk) + `mcr`
2. **แสดง bar chart เทียบ Capital Weight (น้ำเงิน) vs Risk Contribution (ทอง)** จากค่า `weight` vs `rc_pct` ที่ engine คืน — เผยว่า "30% ของเงิน" อาจเป็น "60–70% ของความเสี่ยง"
3. เทียบกับ **risk parity** (เป้าหมาย: %risk เท่ากันทุกตัว) เป็น benchmark

## ตัวอย่าง (รันจริงจาก engine, ไม่ใช่เดา)

พอร์ต 30/30/30/10 (σ VOO .16 / QQQ .22 / BTC .60, ρ เทค-เทค .9 / เทค-BTC ~.4) → engine คืน risk contribution ≈ **VOO 14% · QQQ 20% · BTC 66% · Cash 0%** (ตัวเลขเปลี่ยนตาม σ/ρ ที่ใส่ — รันใหม่ทุกครั้งด้วยค่าจริง)

## Discipline

**ตัวเลขมาจาก engine เท่านั้น ห้ามประเมินในหัว** · vol/correlation ที่ไม่ชัวร์ = **approximate, verify** + ระบุ as-of date · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
