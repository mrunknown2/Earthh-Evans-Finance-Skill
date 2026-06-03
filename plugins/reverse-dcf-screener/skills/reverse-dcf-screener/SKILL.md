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

## รัน Engine (portable — ทุก IDE)

skill package นี้ **portable** — `SKILL.md` + `references/` + `scripts/fill_engine.py` ชุดเดียว ใช้ได้ทั้ง Claude Code / Claude Desktop / Codex / Antigravity · การติดตั้งต่อ platform (path + dependency `openpyxl` + เปิด network ของ Codex) ดู **`INSTALL.md`**

**เรียก engine โดยตรง** (ไม่พึ่ง slash command / subagent) — ส่ง JSON ทาง stdin:

```bash
echo '<JSON>' | python3 scripts/fill_engine.py      # รันจากโฟลเดอร์ skill
# เรียกด้วย full path ก็ได้ — engine resolve template (../assets) relative กับตัวเอง ไม่พึ่ง CWD
```

**JSON input** (คีย์หลัก): `ticker, revenue_r0, ev, terminal_margin, terminal_g, terminal_roic, tax, horizon_n, hist_cagr, fade, tam, max_pen, abs_ceiling, buffer, net_debt, shares_m` · ออปชัน: `wacc` (override), `consensus_fy1` (forward CAGR), `price`
**JSON output** (คีย์หลัก): `implied_cagr, plausible_cagr, gap, verdict, zones{strong_buy,fair_value,caution_low,caution_high,red_flag}, cap_a, cap_b, cap_c, ev_sales`

**โหมด:**
- `"no_write": true` → คำนวณ verdict/zones อย่างเดียว **ไม่เขียนไฟล์** (ไม่ต้องมี openpyxl)
- ปกติ → เขียน `analyses/<TICKER>_<วันที่>.xlsx` (ต้องมี openpyxl)
- `"screener_file": "analyses/screener.xlsx"` → append ลง master Screener (เขียนเฉพาะ input cols)

---

## Workflow (เมื่อไม่มี subagent / slash command)

บน platform ที่ไม่มี subagent ของ Claude Code ให้ทำ 3 สเต็ปนี้ในเซสชันเดียว (เนื้อหาเดียวกับ agent `reverse-dcf-screener`):

1. **Analyze** — ดึงงบจริงล่าสุด (10-K / 10-Q / IR · ราคา + shares + net debt + EV วันนี้ · consensus FY+1) ตาม `references/prompt.md` → ประกอบ JSON → รัน engine (stdin) → อ่าน Implied/Plausible/Gap/Verdict
2. **Verify (รอบ 2 บังคับ — BLOCKING)** — ไล่เช็คทุกตัวเลขจากงบอีกรอบ (revenue R0, EV, margin, ROIC, shares, net debt, consensus) เจอเพี้ยน → แก้ JSON → rerun engine
3. **Zones** — อ่านผลที่ verify แล้ว → สรุปโซนราคา 4 ระดับ ว่าราคาจริงตกโซนไหน

> ข้อบังคับ (เหมือน Critical Rules ด้านบน): ไม่กุข้อมูล · ใส่ WACC จริงเป็น override · source note + as-of date ทุกค่า · ตรวจ Terminal-Anchored fit ก่อนรัน

## Disclaimer

เครื่องมือนี้เป็นกรอบวิเคราะห์ความคาดหวังเชิงการศึกษา **ไม่ใช่คำแนะนำการลงทุนรายบุคคล** · verdict (ถูก/Fair/แพง) + โซนราคา เป็น **framework signal** จาก Terminal-Anchored Reverse DCF ไม่ใช่คำสั่งซื้อขาย · ตัวเลขอิงสมมติฐานที่ระบุ (WACC, terminal margin/g/ROIC, TAM) และข้อมูล ณ as-of date · **WACC ในตารางเป็น placeholder · TAM squishy ที่สุด** — ผู้ใช้ต้อง verify เอกสารทางการล่าสุด (10-K/10-Q/IR) และพิจารณาบริบทของตนเองก่อนตัดสินใจ
