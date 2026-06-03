---
description: "lookup WACC sector + พยายามดึงค่าจริงจาก Damodaran (WebFetch) + เตือน placeholder"
allowed-tools:
  - Read
  - WebSearch
  - WebFetch
model: opus
---

# /reverse-dcf-screener:wacc

**WACC Lookup** — หาค่า WACC ของ sector จากตารางในชุด แล้วพยายามดึงค่าจริงจาก Damodaran มาเทียบ

## Input ที่ต้องการ

- **sector** (ตามชื่อใน WACC table เช่น `Software (System/Application)`) หรือ **ticker** ที่ map เป็น sector ได้

## สิ่งที่ทำ

1. **lookup ตารางในชุด** — อ่าน `${CLAUDE_PLUGIN_ROOT}/skills/reverse-dcf-screener/references/wacc-damodaran.md` หา sector ที่ตรง → คืนค่า WACC placeholder + เตือนว่าเป็น snapshot เก่า
2. **ดึงค่าจริงจาก Damodaran** — WebFetch หน้า cost of capital by sector ของ Damodaran (`https://pages.stern.nyu.edu/~adamodar`) → เทียบค่ากับตาราง ถ้าต่างเยอะให้แจ้ง
3. **แนะนำค่าที่ควรใช้** — บอกค่า WACC ที่เหมาะ + เหตุผล (ถ้า business risk ต่าง sector ค่าเฉลี่ย ให้ปรับ) เพื่อใส่เป็น **WACC override (C9)** ตอนรัน engine
4. **เตือน sector spelling** — ย้ำว่า sector ต้องสะกดตรง WACC table ไม่งั้น VLOOKUP ในไฟล์ Excel จะดึงไม่ติด

## ตัวอย่างสั่ง

```
/reverse-dcf-screener:wacc Software (System/Application)
```

## Discipline

⚠️ WACC ในตารางเป็น **placeholder** (snapshot ม.ค. ของปีที่ทำ) — ต้อง cross-check Damodaran ก่อนใช้ · ใส่ลิงก์ + as-of date · ห้ามกุข้อมูล (ดึงไม่ได้ → บอกตรงๆ ว่าใช้ค่าตารางและเป็น placeholder) · เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล
