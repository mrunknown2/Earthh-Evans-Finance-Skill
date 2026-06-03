---
description: "Pipeline — analyze → verify → zones → append screener จบในคำสั่งเดียว"
allowed-tools:
  - Read
  - Write
  - Bash
  - WebSearch
  - WebFetch
model: opus
---

# /reverse-dcf-screener:full

**Full Pipeline** — รับ ticker ตัวเดียวแล้วเดินครบ: analyze → verify → zones → append screener จบในคำสั่งเดียว

## Input ที่ต้องการ

- **ticker หุ้น** — บังคับ
- **(ถ้ามี)** สมมติฐานที่นายท่านอยากกำหนดเอง (terminal margin / N / TAM / WACC override)

## สิ่งที่ทำ

1. **analyze** — ดึงงบจริงตาม `${CLAUDE_PLUGIN_ROOT}/skills/reverse-dcf-screener/references/prompt.md` → ประกอบ JSON → รัน engine สร้าง `analyses/<TICKER>_<date>.xlsx`:
   ```
   echo '<JSON>' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/reverse-dcf-screener/scripts/fill_engine.py"
   ```
2. **verify** — ไล่เช็คทุกตัวเลขจากงบล่าสุด**อีกรอบ** (discipline บังคับ 2 รอบ) → แก้ค่าที่เพี้ยน → rerun engine ทับไฟล์เดิม
3. **zones** — แปลผลเป็นโซนราคา 4 ระดับ (🟢 Strong Buy / 🟢 Fair / ⚠️ Caution / 🔴 Red Flag) + ปักหมุดราคาปัจจุบัน
4. **append screener** — รัน engine โหมด screener (pipe payload เดิม + `"screener_file":"analyses/screener.xlsx"`) → engine append แถว + คืน `screener_row/screener_globals` ตาม `/reverse-dcf-screener:screener` เพื่อเทียบกับตัวอื่น (ไม่ต้องเขียน python เอง)
5. **สรุปจบ** — verdict สุดท้าย · Implied/Plausible/Gap · โซนราคา · path ไฟล์ที่สร้าง

## ตัวอย่างสั่ง

```
/reverse-dcf-screener:full IREN
```

## Discipline

อ้างงบจริงตามลำดับแหล่ง + as-of date ทุกตัวเลข · verify 2 รอบบังคับ ห้ามข้าม · ห้ามกุข้อมูล · ห้ามแตะช่องสูตร เขียนเฉพาะ input cells · TAM squishy ที่สุด · เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล
