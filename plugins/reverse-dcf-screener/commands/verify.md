---
description: "Step 2 — อย่าเพิ่งเชื่อรอบแรก: ไล่เช็คทุกตัวเลขจากงบล่าสุดอีกรอบ → rerun engine"
allowed-tools:
  - Read
  - Write
  - Bash
  - WebSearch
  - WebFetch
model: opus
---

# /reverse-dcf-screener:verify

**Step 2 — "อย่าเพิ่งเชื่อรอบแรก"** — ไล่เช็คทุกตัวเลขจากงบล่าสุด**อีกรอบ** แก้ค่าที่เพี้ยน แล้ว rerun engine กับไฟล์ล่าสุดใน `analyses/`

## Input ที่ต้องการ

- **(ไม่บังคับ)** ticker — ถ้าไม่ระบุ ใช้ไฟล์ล่าสุดใน `analyses/` (`ls -t analyses/*.xlsx | head -1`)
- ต้องมีผล `/reverse-dcf-screener:analyze` มาก่อน

## สิ่งที่ทำ

1. **อ่านค่าที่กรอกไปแล้ว** — เปิดไฟล์ล่าสุดใน `analyses/` อ่าน input cells (C4–C50) ที่ analyze เขียนไว้
2. **ไล่เช็คอีกรอบจากงบล่าสุด** (discipline บังคับ verify 2 รอบ) — WebSearch/WebFetch งบ/earnings ฉบับล่าสุดซ้ำ ทีละตัว:
   - `revenue_r0` ตรง LTM/FY ล่าสุดไหม · `ev` = mktcap + net debt ปัจจุบันไหม · `net_debt` sign ถูกไหม (cash net → ติดลบ)
   - `shares_m` diluted ล่าสุด · `consensus_fy1` มาจากแหล่งจริง · `terminal_margin/roic/tax` สมเหตุสมผลกับ business
   - `sector` สะกดตรง WACC table · `tam` squishy — ตั้งคำถามหนักสุด
3. **แก้ค่าที่เพี้ยน** — ปรับ JSON ให้ถูก พร้อมโน้ตว่าตัวไหนแก้ + แหล่งอ้างอิง
4. **rerun engine** — pipe JSON ที่แก้แล้วเข้า `fill_engine.py` (เขียนทับไฟล์ของ ticker เดิม):
   ```
   echo '<JSON-แก้แล้ว>' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/reverse-dcf-screener/scripts/fill_engine.py"
   ```
5. **รายงาน diff** — ก่อน/หลัง: `implied_cagr` · `plausible_cagr` · `gap` · `verdict` เปลี่ยนไหม + เหตุผล

## ตัวอย่างสั่ง

```
/reverse-dcf-screener:verify IREN
```

## Discipline

ตั้งสมมติฐานว่ารอบแรกอาจพลาด — เช็คใหม่จริงจัง · ทุกการแก้ต้องมีแหล่งอ้างอิง + as-of date · ห้ามกุข้อมูล · ห้ามแตะช่องสูตร เขียนเฉพาะ input cells · เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล
