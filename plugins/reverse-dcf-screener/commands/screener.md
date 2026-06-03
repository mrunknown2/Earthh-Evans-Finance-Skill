---
description: "append หุ้นลง master screener + แสดงตารางเทียบแพง/ถูกหลายตัว (sheet Screener)"
allowed-tools:
  - Read
  - Write
  - Bash
model: opus
---

# /reverse-dcf-screener:screener

**Master Screener** — เพิ่มหุ้นลงตาราง master screener แล้วแสดงตารางเทียบแพง/ถูกหลายตัวพร้อมกัน

## Input ที่ต้องการ

- **(ไม่บังคับ)** ticker — ถ้าไม่ระบุ ใช้ไฟล์ล่าสุดใน `analyses/`
- ต้องผ่าน `/reverse-dcf-screener:analyze` (+ `verify`) มาก่อน เพื่อมีค่าที่ verify แล้ว

## สิ่งที่ทำ

1. **ประกอบ JSON ของหุ้น** — ใช้ค่าที่ verify แล้วของหุ้นล่าสุด (payload เดียวกับ `/analyze`) แล้ว**เพิ่ม key** `"screener_file"` ชี้ไฟล์ master:
   ```
   echo '{...payload หุ้น..., "screener_file": "analyses/screener.xlsx"}' \
     | python3 "${CLAUDE_PLUGIN_ROOT}/skills/reverse-dcf-screener/scripts/fill_engine.py"
   ```
   > มี `"screener_file"` (หรือ `"mode":"screener"`) → engine สลับเป็นโหมด screener: **append เท่านั้น ไม่เขียนไฟล์ per-stock**
2. **engine จัดการ append ให้** — ไม่ต้องเขียน python เอง · engine จะ:
   - หาแถวว่างถัดไป (เริ่ม row 10) แล้วเขียน**เฉพาะ input cols**: A Ticker · B Sector · D Rev R0 · E EV · F margin · G g · H ROIC · I N · J Hist CAGR · K TAM · Q WACC override
   - **ไม่แตะ formula cols** C/L/M/N/O/P (Excel recalc ตอนเปิด) · ถ้า append เกินบล็อกสูตรเดิมจะ translate สูตรให้แถวใหม่อัตโนมัติ
   - เซ็ต **globals S3-S7** (tax/fade/max_pen/abs_ceiling/buffer) ครั้งแรกถ้ายังว่าง แล้ว reuse ค่าเดิมทุกแถว (Gap จึงเทียบกันได้บนสมมติฐานเดียว) — ถ้าไฟล์มีค่า globals อยู่แล้ว **จะไม่ทับ**
   - คืน JSON: `screener_file`, `screener_row`, `screener_globals` + `implied_cagr/plausible_cagr/gap/verdict` (คำนวณด้วย **globals ของไฟล์** → ตรงกับที่ Excel recalc เป๊ะ)
3. **แสดงตารางเทียบใน chat** — โหลด/อ่านทุกหุ้นใน screener เรียงตาม Gap: Ticker · Implied CAGR · Plausible CAGR · Gap · Verdict (แพง/Fair/ถูก) → เห็นว่าตัวไหนถูก/แพงสุดในตะกร้า

## ตัวอย่างสั่ง

```
/reverse-dcf-screener:screener IREN
```

## Discipline

append เท่านั้น ไม่ทับแถวเดิม · เขียนเฉพาะ input cols ห้ามแตะช่องสูตร · ค่าที่ลงตารางต้องผ่าน verify แล้ว · Gap เทียบกันได้เฉพาะเมื่อ assumptions ฐานเดียวกัน · เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล
