# Prompt — ดึงงบมา → สร้าง JSON ป้อน `fill_engine.py`

> ฐานจาก sheet "AI_Prompts" cell B4 (PROMPT A) ของไฟล์ต้นฉบับ Earthh Evans
> **ต่างจากต้นฉบับ:** output target เปลี่ยนจาก "กรอก cell ใน Excel ตรงๆ" → **เป็น JSON object** สำหรับส่งเข้า `scripts/fill_engine.py` (สคริปต์จะกรอก cell + คำนวณให้เอง) · การ append ลง screener ทำผ่านคำสั่ง `/screener` (ไม่ทำในขั้นนี้)

---

## Prompt (เปลี่ยน `[TICKER]` แล้วใช้)

> คุณคือ **buy-side equity analyst** — ดึงข้อมูลเพื่อป้อนโมเดล **Reverse DCF (Terminal-Anchored)**
> หุ้น: **[TICKER]**
>
> ### ⚠️ ข้อบังคับสำคัญ (อ่านก่อนลงมือ)
> 1. **ตรวจเช็คข้อมูลละเอียด — ลำดับแหล่ง (source hierarchy):**
>    `10-K / 10-Q / 20-F ล่าสุด` > `earnings presentation / transcript (earnings call)` > `company guidance` > `analyst consensus` > `market data`
>    ถ้าแหล่งขัดกัน → ยึดแหล่ง quality สูงสุด
> 2. **ระบุ time basis ทุกตัวเลข** — `FY` (ปีบัญชี) / `LTM` (12 เดือนล่าสุด) / `NTM` (12 เดือนข้างหน้า) ให้ชัดทุกครั้ง
> 3. **ห้ามเดา** — ถ้าไม่มั่นใจ 100% ให้เขียน **"ต้อง verify"** กำกับ อย่าใส่ตัวเลขมั่ว
> 4. **as-of date** — ระบุวันที่ดึงข้อมูล (ราคา/market cap เปลี่ยนทุกวัน) ทุกครั้ง
> 5. **Sector ต้องสะกดตรงตาราง `wacc-damodaran.md` เป๊ะ** (ก๊อปชื่อมาเลย) ไม่งั้น WACC lookup ในไฟล์จะดึงไม่ติด
>
> ### ข้อมูลที่ต้องส่ง (10 อย่าง + หน่วย + source note)
> 1. **Current Revenue R0** ($B) — FY ล่าสุด (ระบุไตรมาส/ปีบัญชี)
> 2. **Enterprise Value (EV)** ($B) = market cap + net debt (ถ้า private ใช้ valuation รอบล่าสุด)
> 3. **Sector** — แมปชื่อใน Damodaran (เช่น `Semiconductor`, `Aerospace/Defense`, `Software (System/Application)`)
> 4. **Terminal EBIT margin** (%) — ประเมินจาก margin ปัจจุบัน + เพดานอุตสาหกรรม (อย่าสูงเกินจริง)
> 5. **Terminal ROIC** (%) — จาก ROIC ปัจจุบัน / peer (ห้าม hardcode 20% ถ้าจริงต่ำ)
> 6. **Tax rate** (%) — effective tax จริง (ระวังบริษัท Cayman/Ireland → ต่ำกว่า 21%)
> 7. **Historical Revenue CAGR 3 ปี** (%) — ระบุ base period ชัด (peak→now / trough→now / cycle blend)
> 8. **TAM** ($B) + **Forward CAGR FY+1** (%) — จาก company guidance หรือ consensus
> 9. **Current price + Shares outstanding + Net debt** — สำหรับตาราง WACC × Price
> 10. **Analyst consensus** — avg target + range + FY+1 revenue consensus
>
> ### ⛔ Output = JSON object เดียว (สำหรับ `fill_engine.py`)
> **อย่ากรอก cell Excel ตรงๆ** — ส่งกลับเป็น JSON ตาม schema ด้านล่าง (key ต้องตรงเป๊ะ) แล้ว pipe เข้า `python3 scripts/fill_engine.py`
>
> ### ปิดท้ายด้วย flag (นอก JSON)
> - **มูลค่าบริษัทส่วนใหญ่อยู่ปลายทางหรือยัง?** (เหมาะกับ Terminal-Anchored ไหม) — ตอบ **Y/N + เหตุผล**
> - **สิ่งที่ต้อง verify เพิ่ม** — ลิสต์ตัวเลขที่ไม่มั่นใจ 100%

---

## JSON Schema (key ต้องตรงเป๊ะกับ `fill_engine.py`)

```json
{"ticker":"", "revenue_r0":0, "ev":0, "sector":"", "wacc":0,
 "terminal_margin":0, "terminal_g":0, "terminal_roic":0, "tax":0, "horizon_n":10,
 "hist_cagr":0, "fade":0.70, "tam":0, "max_pen":0.25, "abs_ceiling":0.45, "buffer":0.05,
 "price":0, "shares_m":0, "net_debt":0, "consensus_fy1":0,
 "analyst_target":0, "analyst_range":""}
```

### หน่วย (units) — สำคัญมาก
- **$B (พันล้านดอลลาร์):** `revenue_r0`, `ev`, `tam`, `net_debt`, `consensus_fy1`
- **millions (ล้านหุ้น):** `shares_m`
- **decimals (ทศนิยม ไม่ใช่ %):** `wacc`, `terminal_margin`, `terminal_g`, `terminal_roic`, `tax`, `hist_cagr`, `fade`, `max_pen`, `abs_ceiling`, `buffer` → เช่น **0.35 = 35%**
- **integer (ปี):** `horizon_n` (default 10)
- **$/share:** `price`, `analyst_target`
- **text:** `ticker`, `sector` (ตรงตาราง WACC), `analyst_range` (เช่น `"$29 - $100+"`)

### หมายเหตุ key สำคัญ
- `wacc` — ใส่ค่า WACC จริงที่ดึงมา (สคริปต์ใช้เป็น **override** ป้องกัน WACC table placeholder ดึงผิด sector)
- `consensus_fy1` — รายได้ consensus FY+1 ($B) · สคริปต์ใช้ derive `Forward CAGR = consensus_fy1/revenue_r0 − 1` ให้เอง (ไม่ต้องส่ง forward CAGR แยก)
- `tam = 0` → สคริปต์ปลดล็อก Cap B (ตั้ง 999) ให้ Cap A กับ Cap C ตัดสิน Plausible แทน
- ค่า default ที่ใส่ไว้ในไฟล์อยู่แล้ว — ปรับได้ถ้ามีเหตุผล: `fade 0.70`, `max_pen 0.25`, `abs_ceiling 0.45`, `buffer 0.05`, `horizon_n 10`

### วิธีรัน
```bash
echo '<JSON ด้านบน>' | python3 scripts/fill_engine.py
```
สคริปต์จะ: ก๊อป template → กรอก input cells (คงสูตร Excel ไว้ recalc ตอนเปิด) → สร้าง `analyses/<TICKER>_<date>.xlsx` → print ผลลัพธ์ (Implied/Plausible CAGR, Gap, Verdict, โซนราคา) เป็น JSON
การ append ลง master screener → ใช้คำสั่ง **`/screener`** แยกต่างหาก

---

> เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล / educational, not personal investment advice — เรียบเรียงจาก Earthh Evans · Invest Hub
