---
description: "correlation matrix heatmap (ปกติ vs regime วิกฤต)"
allowed-tools:
  - Read
  - Bash
model: opus
---

# /portfolio-risk-architect:corr

**Correlation & True Diversification** — วัดการกระจายจริง ไม่ใช่จำนวน ticker

## Input ที่ต้องการ

- return series ของสินทรัพย์ หรือค่า correlation อ้างอิง (ถ้าไม่มี → approximate, verify) + σ + น้ำหนัก

## สิ่งที่ทำ

1. **สร้าง correlation matrix heatmap** — แสดง 2 regime: **ตลาดปกติ vs วิกฤต** (ดัน ρ ขึ้นเข้าหา 1)
2. **รัน engine** หา DR + ENB (ห้ามคำนวณเอง) — mode `risk` คืน `diversification_ratio` + `enb` ทั้งสอง regime:
   ```bash
   # normal regime
   echo '{"mode":"risk","assets":[...with vol...],"correlation":[[...normal...]]}' \
     | python3 "${CLAUDE_PLUGIN_ROOT}/skills/portfolio-risk-architect/scripts/portfolio_engine.py"
   # crisis regime: rerun ด้วย correlation ที่ดันเข้าหา 1 → ดู DR/ENB ยุบลงเท่าไร
   ```
   เทียบ `diversification_ratio` / `enb` ระหว่าง 2 regime → เห็นว่าการกระจาย "หาย" ตอนวิกฤตเท่าไร
3. ย้ำหลักคิด: ในวิกฤต correlation วิ่งเข้าหา 1 — การกระจายที่ดูดีตอนปกติมักหายตอนต้องใช้

## Discipline

**DR/ENB มาจาก engine** · ค่า correlation ที่ไม่ชัวร์ = **approximate, verify** + ระบุ as-of date · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
