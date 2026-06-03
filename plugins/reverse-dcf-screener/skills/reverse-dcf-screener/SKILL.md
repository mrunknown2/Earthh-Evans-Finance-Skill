---
name: reverse-dcf-screener
description: >
  ใช้เมื่ออยากรู้ว่าหุ้น "ถูกหรือแพง" ด้วยมุมความคาดหวัง — ราคาตอนนี้บังคับให้บริษัท
  โตปีละกี่ % แล้วทำได้จริงไหม. Terminal-Anchored Reverse DCF, Market-Implied CAGR,
  Plausible CAGR, expectation investing, โซนราคาน่าสะสม. เชิงการศึกษา ไม่ใช่คำแนะนำ.
---

# Reverse DCF Screener

ระบบ **Terminal-Anchored Reverse DCF** — ไม่ทำนายว่าหุ้นจะขึ้นหรือลง แต่**ถอดความคาดหวังที่ราคาฝังไว้** ออกมาเป็นตัวเลข: ราคา/EV วันนี้บังคับให้รายได้ต้องโตปีละกี่ % (**Market-Implied CAGR**) แล้วเทียบกับ **Plausible CAGR** (เพดานที่ทำได้จริงตามประวัติ/TAM/เพดานสัมบูรณ์) → ออก verdict **ถูก / Fair / แพง** + **โซนราคาน่าสะสม 4 ระดับ** agent ชื่อ `reverse-dcf-screener` ดึงงบจริง → verify 2 รอบ → กรอก Engine ลง Excel (`fill_engine.py`) → สรุป chat

> เรียบเรียงจาก **Earthh Evans · Invest Hub**

---

## Routing — สถานการณ์ → Command

| สถานการณ์ | Command |
|-----------|---------|
| อยากรู้หุ้นถูก/แพง ครบจบในคำสั่งเดียว | `/full` |
| เช็คเร็วก่อนลงลึก (เหมาะ Terminal-Anchored ไหม + EV/Sales sanity) | `/quick` |
| วิเคราะห์ทีละสเต็ป — กรอก Engine ลง Excel | `/analyze` → `/verify` → `/zones` |
| ไล่เช็คตัวเลขจากงบอีกรอบ (discipline บังคับ) | `/verify` |
| อยากรู้โซนราคาน่าสะสม | `/zones` |
| เทียบหลายตัวในตารางเดียว | `/screener` |
| อยากรู้ WACC ของ sector | `/wacc` |
| ดู sensitivity (WACC×Margin / WACC×Price) | `/sensitivity` |
| อยากเข้าใจตรรกะเบื้องหลัง | `/methodology` |

---

## Critical Rules — AI ห้าม override

กฎเหล่านี้ยกมาจาก agent `reverse-dcf-screener` — ไม่มีข้อยกเว้น:

- **verify 2 รอบบังคับ** — อย่าเพิ่งเชื่อรอบแรก ไล่เช็คตัวเลขจากงบล่าสุดอีกรอบทุกตัว เจอเพี้ยน → แก้ → rerun
- **sector สะกดตรง WACC table เป๊ะ** — ผิดตัวเดียว VLOOKUP หลุด · ใส่ WACC จริงเป็น override (C9) เสมอ (ตารางเป็น placeholder)
- **เขียนได้เฉพาะ yellow input cells** — ห้ามแตะช่องสูตร เพื่อให้ Excel recalc เองตอนเปิด
- **ไม่กุข้อมูล** — ไม่พบให้เขียน "ไม่พบข้อมูล" + บอกแหล่งที่หาแล้ว · ทุก cell มี source note
- **ระบุ as-of date เสมอ** (`YYYY-MM-DD`) + สกุลเงินคงที่ · **TAM squishy ที่สุด** ใส่อย่างระวัง
- **ต้องมี Python 3 + `openpyxl`** (`pip install openpyxl`) เพื่อรัน `fill_engine.py`

---

## วิธีใช้ข้าม IDE

skill package นี้ **portable** — ใช้ได้ทั้ง Claude Code / Antigravity / Codex ผ่าน `SKILL.md` + `references/` + `scripts/fill_engine.py` ชุดเดียวกัน · วิธีติดตั้งต่อ IDE (รวม dependency `openpyxl` + เตือน Codex เปิด network) ดู **`INSTALL.md`**

---

## Disclaimer

เครื่องมือนี้เป็นกรอบวิเคราะห์ความคาดหวังเชิงการศึกษา **ไม่ใช่คำแนะนำการลงทุนรายบุคคล** · verdict (ถูก/Fair/แพง) + โซนราคา เป็น **framework signal** จาก Terminal-Anchored Reverse DCF ไม่ใช่คำสั่งซื้อขาย · ตัวเลขอิงสมมติฐานที่ระบุ (WACC, terminal margin/g/ROIC, TAM) และข้อมูล ณ as-of date · **WACC ในตารางเป็น placeholder · TAM squishy ที่สุด** — ผู้ใช้ต้อง verify เอกสารทางการล่าสุด (10-K/10-Q/IR) และพิจารณาบริบทของตนเองก่อนตัดสินใจ
