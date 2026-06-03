---
description: "ตาราง Implied CAGR ตาม WACC×Terminal Margin และ WACC×Price"
allowed-tools:
  - Read
  - Bash
model: opus
---

# /reverse-dcf-screener:sensitivity

**Sensitivity Tables** — แสดงว่า Market-Implied CAGR ขยับแค่ไหนเมื่อสมมติฐานหลักเปลี่ยน — กริด WACC×Terminal Margin และ WACC×Price

## Input ที่ต้องการ

- **(ไม่บังคับ)** ticker — ถ้าไม่ระบุ ใช้ไฟล์ล่าสุดใน `analyses/`
- ต้องผ่าน `/reverse-dcf-screener:analyze` (+ `verify`) มาก่อน

## สิ่งที่ทำ

1. **อ่าน base case** — ดึง input cells ของหุ้นล่าสุดเป็นจุดกลาง (WACC, terminal margin, price ฯลฯ)
2. **กริด 1 — WACC × Terminal Margin** — กวาด WACC รอบค่าฐาน (เช่น ±2%) × terminal margin (เช่น ±5pp) แล้วรัน engine ซ้ำแต่ละช่อง (โหมด `no_write:true`):
   ```
   echo '<JSON+ค่าที่ปรับ+"no_write":true>' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/reverse-dcf-screener/scripts/fill_engine.py"
   ```
   → ตาราง Implied CAGR แต่ละช่อง
3. **กริด 2 — WACC × Price** — กวาด WACC × ราคาหุ้น (เช่น ±20%) → ดูว่าราคาที่เปลี่ยนดัน Implied CAGR ขึ้นแค่ไหน (ราคาขึ้น = ตลาดบังคับโตเร็วขึ้น)
4. **อ่านผล** — ชี้ว่า assumption ตัวไหนกระทบ Implied CAGR มากสุด + ที่ราคาปัจจุบันต้องโตเท่าไหร่เทียบ Plausible

## ตัวอย่างสั่ง

```
/reverse-dcf-screener:sensitivity IREN
```

## Discipline

sensitivity คือกรอบ what-if ไม่ใช่การพยากรณ์ · WACC ฐานเป็น placeholder — ระวังตีความช่วง · ทุกตัวเลขมาจาก engine ไม่ปัดเอง · เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล
