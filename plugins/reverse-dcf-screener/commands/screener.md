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

1. **อ่านค่า** — ดึง input + ผลของหุ้นล่าสุด (re-run engine โหมด `no_write:true` เพื่อได้ `implied_cagr/plausible_cagr/gap/verdict`)
2. **append แถวใหม่** ลง sheet **Screener** ในไฟล์ master (`analyses/screener.xlsx` หรือ master ที่นายท่านกำหนด) — เขียนเฉพาะ input cols:
   - A Ticker · B Sector · D Revenue R0 · E EV · F Term margin · G g · H ROIC · I N · J Hist CAGR · K TAM · Q WACC override
   - **ห้ามแตะ formula cols:** C WACC · L Reinv · M Implied · N Plausible · O Gap · P Verdict (Excel recalc ตอนเปิด)
   - Global assumptions (ถ้ายังว่าง): S3 tax · S4 fade · S5 max_pen · S6 abs_ceiling · S7 buffer
3. **แสดงตารางเทียบใน chat** — ทุกหุ้นใน screener เรียงตาม Gap: Ticker · Implied CAGR · Plausible CAGR · Gap · Verdict (แพง/Fair/ถูก) → เห็นว่าตัวไหนถูก/แพงสุดในตะกร้า

## ตัวอย่างสั่ง

```
/reverse-dcf-screener:screener IREN
```

## Discipline

append เท่านั้น ไม่ทับแถวเดิม · เขียนเฉพาะ input cols ห้ามแตะช่องสูตร · ค่าที่ลงตารางต้องผ่าน verify แล้ว · Gap เทียบกันได้เฉพาะเมื่อ assumptions ฐานเดียวกัน · เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล
