---
description: "drawdown ของพอร์ตในวิกฤตจริง (GFC2008/COVID2020/2022/Yen2024)"
allowed-tools:
  - Read
  - Bash
model: opus
---

# /portfolio-risk-architect:stress

**Tail Risk & Stress Test** — จำลองพอร์ตในเหตุการณ์วิกฤตจริง

## Input ที่ต้องการ

- holdings + น้ำหนัก
- per-asset return ของแต่ละสินทรัพย์ในแต่ละวิกฤต (ใช้ **peak-to-trough จริงในช่วงเหตุการณ์**; ถ้าสินทรัพย์ไม่มีประวัติ ณ ตอนนั้น เช่น BTC ปี 2008 → mark N/A หรือ proxy แล้วระบุ)

## สิ่งที่ทำ

1. **รัน engine** (ห้ามรวมเลขในหัว) — mode `stress`, ใส่ shock per-asset ต่อ scenario:
   ```bash
   echo '{"mode":"stress","assets":[{"name":"VOO","weight":0.3},{"name":"QQQ","weight":0.3},{"name":"BTC","weight":0.3},{"name":"Cash","weight":0.1}],
     "scenarios":[
       {"name":"GFC 2008","shocks":{"VOO":-0.51,"QQQ":-0.53,"BTC":null}},
       {"name":"COVID 2020","shocks":{"VOO":-0.34,"QQQ":-0.28,"BTC":-0.50}},
       {"name":"2022 Rate Shock","shocks":{"VOO":-0.18,"QQQ":-0.33,"BTC":-0.64}},
       {"name":"Aug 2024 Yen Unwind","shocks":{"VOO":-0.06,"QQQ":-0.10,"BTC":-0.18}}]}' \
     | python3 "${CLAUDE_PLUGIN_ROOT}/skills/portfolio-risk-architect/scripts/portfolio_engine.py"
   ```
   engine คืน `portfolio_return` ต่อ scenario = `Σ(wᵢ·shockᵢ)` (สินทรัพย์ที่ไม่ใส่ shock = 0)
2. **เล่าผล** est. max drawdown ต่อเหตุการณ์ + เสริม time-to-recover (เชิงคุณภาพ) · จะดู VaR/CVaR เชิงสถิติให้รัน `/montecarlo` คู่กัน

## Discipline

**ตัวเลขรวมพอร์ตมาจาก engine** · ผลเป็น **est. ภายใต้สมมติฐาน shock** ไม่ใช่ตัวเลขที่จะเกิดซ้ำแน่นอน · ระบุ as-of date + ที่มาของ per-asset shock (peak-to-trough จริง) · BTC/สินทรัพย์ที่ยังไม่เกิด ณ วิกฤตนั้น → mark N/A อย่า proxy เงียบๆ · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
