# Reverse DCF Screener — Playbook การใช้งาน

> Terminal-Anchored Reverse DCF — ถอด "ความคาดหวัง" ที่ราคาฝังไว้ออกมาเป็นตัวเลข: ราคาวันนี้บังคับให้บริษัทโตปีละกี่ % (**Market-Implied CAGR**) แล้วเทียบกับเพดานที่ทำได้จริง (**Plausible CAGR**) → สรุป **ถูก / Fair / แพง** + **โซนราคาน่าสะสม 4 ระดับ**

## ติดตั้ง

```
/plugin marketplace add mrunknown2/Earthh-Evans-Finance-Skill
/plugin install reverse-dcf-screener
```

**Dependency จำเป็น** (ไม่งั้น engine เขียนไฟล์ไม่ได้):

```
pip install openpyxl
```

- ต้องมี **Python 3** + `openpyxl` — `fill_engine.py` ใช้ openpyxl เฉพาะตอน **เขียนไฟล์** (`/analyze`, `/full`, `/screener`) · ส่วนคำนวณ verdict / screener-view เป็น Python stdlib ล้วน รันได้แม้ไม่มี package
- ต้องมี **Excel / Google Sheets** เปิดไฟล์ผลลัพธ์ `analyses/<TICKER>_<date>.xlsx` เพื่อให้สูตรในช่อง recalc เห็นเลขครบ (openpyxl เขียนสูตรได้แต่ไม่ recalc)
- ถ้าเจอ `error: externally-managed-environment` (PEP 668 — macOS homebrew / Linux ใหม่): ใช้ `python3 -m venv .venv && . .venv/bin/activate && pip install openpyxl` หรือ `pipx` หรือ `pip install --break-system-packages openpyxl`
- ใช้นอก Claude Code (Antigravity / Codex) ได้ — ดู `../plugins/reverse-dcf-screener/INSTALL.md` (Codex ต้องเปิด network access ก่อน ไม่งั้น WebFetch ดึงงบไม่ได้)

## Quickstart — เริ่มเร็วสุด

คำสั่งเริ่มต้นแนะนำคือ `/full <ticker>` — เดินครบ analyze → verify → zones → append screener จบในคำสั่งเดียว:

```
/reverse-dcf-screener:full IREN
```

→ agent ดึงงบ IREN จริง → กรอก `analyses/IREN_<วันที่>.xlsx` → verify รอบ 2 → สรุป Implied / Plausible / Gap / Verdict + โซนราคา 4 ระดับ → append ลง master screener · เปิดไฟล์ใน Excel สูตร recalc ครบ

**ต้องเตรียมก่อนกด:**
- `pip install openpyxl` แล้ว + มี Python 3
- มี ticker ที่จะวิเคราะห์
- (ถ้ามี) สมมติฐานที่อยากกำหนดเอง — terminal margin / horizon N / TAM / WACC override

> ยังไม่แน่ใจว่าหุ้นเหมาะกับวิธีนี้ไหม → กด `/quick <ticker>` ก่อนเช็ค fit (มูลค่าอยู่ปลายทางหรือยัง + EV/Sales sanity)

## เตรียมข้อมูลก่อนใช้ (Inputs)

`/analyze` และ `/full` ต้องประกอบ JSON ครบ key (units สำคัญมาก — engine อ่านตรง key):

| input | คือ | หน่วย |
|---|---|---|
| `revenue_r0` | Current Revenue R0 (FY/LTM ล่าสุด) | $B |
| `ev` | Enterprise Value = market cap + net debt | $B |
| `sector` | ชื่อ sector ตามตาราง Damodaran (สะกดตรงเป๊ะ) | text |
| `wacc` | WACC จริง (ส่งเป็น override C9 กัน table placeholder ดึงผิด sector) | decimal |
| `terminal_margin` | Terminal EBIT margin | decimal |
| `terminal_g` | terminal growth g | decimal |
| `terminal_roic` | Terminal ROIC | decimal |
| `tax` | effective tax rate | decimal |
| `horizon_n` | horizon N (ปี explicit) — default 10 | integer |
| `hist_cagr` | Historical Revenue CAGR 3 ปี | decimal |
| `fade` | fade factor — default 0.70 | decimal |
| `tam` | Total Addressable Market (TAM = 0 → ปลดล็อก Cap B) | $B |
| `max_pen` | max penetration — default 0.25 | decimal |
| `abs_ceiling` | absolute ceiling — default 0.45 | decimal |
| `buffer` | buffer ตัดสิน verdict — default 0.05 | decimal |
| `price`, `shares_m`, `net_debt` | ราคา / หุ้น (ล้านหุ้น) / net debt (cash net → ติดลบ) | $/share, millions, $B |
| `consensus_fy1` | รายได้ consensus FY+1 (engine derive Forward CAGR ให้เอง) | $B |
| `analyst_target`, `analyst_range` | avg target + range | $/share, text |

> decimals = ทศนิยม ไม่ใช่ % (เช่น 0.35 = 35%) · ดึงงบตามลำดับแหล่ง: `10-K / 10-Q / 20-F` > `earnings presentation / transcript` > `guidance` > `consensus` > `market data` · ระบุ **as-of date** (YYYY-MM-DD) ทุกตัวเลข · ห้ามเดา (ไม่พบ → "ไม่พบข้อมูล")

## คำสั่งทั้งหมด

| คำสั่ง | ทำอะไร | input |
|---|---|---|
| `/full <ticker>` | Pipeline เต็ม — analyze → verify → zones → append screener จบในคำสั่งเดียว (เริ่มต้นแนะนำ) | ticker (บังคับ) + (ถ้ามี) สมมติฐาน override |
| `/analyze <ticker>` | Step 1 — ดึงงบ → กรอก Engine → สร้าง Excel + Implied/Plausible/Gap/Verdict เบื้องต้น | ticker (บังคับ) + (ถ้ามี) สมมติฐาน override |
| `/verify [ticker]` | Step 2 — ไล่เช็คทุกตัวเลขจากงบล่าสุด *อีกรอบ* (discipline บังคับ) → rerun engine | ไม่บังคับ ticker (ไม่ระบุ = ไฟล์ล่าสุดใน `analyses/`); ต้องผ่าน `/analyze` มาก่อน |
| `/zones [ticker]` | Step 3 — โซนราคา 4 ระดับ (Strong Buy/Fair/Caution/Red Flag) + ปักหมุดราคาปัจจุบัน อิง Market-Implied CAGR | ไม่บังคับ ticker (ไม่ระบุ = ไฟล์ล่าสุด); ต้องผ่าน analyze (+verify) |
| `/quick <ticker>` | เช็คเร็วก่อนวิเคราะห์เต็ม — เหมาะ Terminal-Anchored ไหม (มูลค่าอยู่ปลายทาง?) + EV/Sales sanity | ticker (บังคับ) |
| `/screener [ticker]` | append หุ้นลง master screener (`analyses/screener.xlsx`) + แสดงตารางเทียบแพง/ถูกหลายตัว | ไม่บังคับ ticker (ไม่ระบุ = ไฟล์ล่าสุด); ต้องผ่าน analyze (+verify) |
| `/wacc <sector>` | lookup WACC ราย sector จากตารางในชุด + พยายามดึงค่าจริงจาก Damodaran (WebFetch) + เตือน placeholder | sector (ตามชื่อ WACC table) หรือ ticker ที่ map เป็น sector ได้ |
| `/sensitivity [ticker]` | ตาราง Implied CAGR ตาม WACC × Terminal Margin และ WACC × Price | ไม่บังคับ ticker (ไม่ระบุ = ไฟล์ล่าสุด); ต้องผ่าน analyze (+verify) |
| `/methodology [หัวข้อ]` | อธิบายตรรกะ Terminal-Anchored Reverse DCF เชิงการศึกษา | ไม่บังคับ — หัวข้อ เช่น `plausible`, `verdict`, `zones`, `convention` |

> ทุกคำสั่งใช้ prefix เต็มได้: `/reverse-dcf-screener:full IREN`

## Workflow ที่ใช้บ่อย

**1. วิเคราะห์หุ้นเดี่ยว ทีละสเต็ป (ควบคุมเอง)**

```
/reverse-dcf-screener:analyze IREN      # ดึงงบ → กรอก Engine → Excel + verdict เบื้องต้น
/reverse-dcf-screener:verify  IREN      # เช็คทุกตัวเลขจากงบอีกรอบ → rerun engine ทับไฟล์เดิม
/reverse-dcf-screener:zones   IREN      # โซนราคา 4 ระดับ + ราคาปัจจุบันตกโซนไหน
```

**2. รวบจบในคำสั่งเดียว + เทียบหลายตัว**

```
/reverse-dcf-screener:quick    IREN     # (option) เช็คก่อนว่าเหมาะ Terminal-Anchored ไหม
/reverse-dcf-screener:full     IREN     # analyze → verify → zones → append screener
/reverse-dcf-screener:screener NVDA     # เพิ่มตัวที่ 2 ลง master → ตารางเทียบ Gap เรียงถูก/แพง
```

**3. ดู sensitivity / WACC ก่อนเชื่อ verdict**

```
/reverse-dcf-screener:wacc        Software (System/Application)   # หา WACC override (C9)
/reverse-dcf-screener:sensitivity IREN                            # grid WACC×Margin, WACC×Price
```

## อ่านผลลัพธ์ยังไง

หัวใจคือ **Market-Implied CAGR** (ราคาบังคับให้โตปีละกี่ %) เทียบ **Plausible CAGR** (เพดานที่ทำได้จริง):

`Gap = Implied CAGR − Plausible CAGR`

| เงื่อนไข | Verdict |
|---|---|
| `Gap > Buffer` | 🔴 **แพง — Priced for Perfection** (ราคาฝังความคาดหวังที่บริษัททำไม่ไหว) |
| `−Buffer ≤ Gap ≤ Buffer` | **Fair — สมเหตุสมผล** (ราคาเรียกร้องพอดีกับที่ทำได้จริง) |
| `Gap < −Buffer` | 🟢 **ถูก — Low Expectations** (ตลาดคาดหวังต่ำกว่าที่ทำได้จริง — น่าสะสม) |

**โซนราคา 4 ระดับ** (อิง Plausible CAGR เป็นจุดอ้าง):

| โซน | เกณฑ์ (CAGR ที่ราคาฝัง) | ความหมาย |
|---|---|---|
| 🟢 **Strong Buy** | Implied = `MAX(Plausible − 5%, 0)` | ตลาดคาดหวังต่ำกว่าที่ทำได้จริงมาก — น่าสะสมสุด |
| 🟢 **Fair Value** | Implied ≈ Plausible | ราคาเรียกร้องพอดีกับที่ทำได้จริง |
| ⚠️ **Caution** | Implied = Plausible +5% ถึง +10% | ราคาเริ่มเรียกร้องเกินจริง — ระวัง |
| 🔴 **Red Flag** | Implied ≥ Plausible +10% | priced for perfection — ราคาฝังความคาดหวังที่ทำไม่ไหว |

> **เลขแบบไหน = น่าสะสม** — Gap ติดลบมาก (Implied ต่ำกว่า Plausible) + ราคาปัจจุบันตกใต้โซน Strong Buy/Fair

**ตัวอย่างจริง (golden case จาก test ของ plugin — IREN):**
Implied CAGR ≈ **32%** · Plausible CAGR ≈ **42%** · Gap ≈ **−10%** → verdict **"ถูก — Low Expectations"** · โซนราคา: Strong Buy ≈ **$97** · Fair Value ≈ **$144** · Red Flag ≈ **$301** (ราคาฐาน $65.33)

## Engine — เลขไม่เดา

การคำนวณทั้งหมดวิ่งผ่าน `../plugins/reverse-dcf-screener/skills/reverse-dcf-screener/scripts/fill_engine.py` (Python stdlib-only ใน `compute()`, deterministic — โมเดลแค่ดึงข้อมูล + ตีความ ไม่ปัดเลขเอง). engine อ่าน JSON จาก stdin → print JSON ผล:

- **Terminal-Anchored implied CAGR (5 สเต็ป):** `TV = EV×(1+WACC)^N` → `FCFF = TV×(WACC−g)` → `conversion = margin×(1−tax)×(1−reinvestment)` โดย `reinvestment = g/ROIC` → `R* = FCFF/conversion` → `Implied CAGR = (R*/R0)^(1/(N+1)) − 1`
- **Plausible CAGR = MIN(Cap A, Cap B, Cap C):** Cap A = `MAX(Hist, Forward)×Fade` · Cap B = TAM-bound (`max_pen×TAM`; **TAM=0 → Cap B=999** ปลดล็อก ให้ A/C ตัดสิน) · Cap C = absolute ceiling (default 0.45)
- **Price zones:** คำนวณราคา ณ CAGR ต่างๆ (Plausible−5% / Plausible / +5% / +10%) → strong_buy / fair_value / caution / red_flag
- **โหมดเขียนไฟล์ (`/analyze`, `/full`):** ก๊อป template → กรอกเฉพาะ **yellow input cells** (Engine C4–C50) คงสูตรไว้ทั้งหมด → `analyses/<TICKER>_<date>.xlsx` (Excel recalc เองตอนเปิด) · ใส่ `"no_write":true` = คำนวณอย่างเดียว ไม่เขียนไฟล์ (`/zones`, `/sensitivity` ใช้โหมดนี้)
- **screener append mode (`"screener_file"` หรือ `"mode":"screener"`):** **append เท่านั้น** — หาแถวว่างถัดไป (เริ่ม row 10) เขียนเฉพาะ **input cols** (A Ticker · B Sector · D Rev R0 · E EV · F margin · G g · H ROIC · I N · J Hist CAGR · K TAM · Q WACC override) · **ไม่แตะ formula cols** C/L/M/N/O/P (Excel recalc เอง; แถวใหม่เกินบล็อกสูตร engine จะ translate สูตรให้อัตโนมัติ) · เซ็ต **globals S3–S7** (tax/fade/max_pen/abs_ceiling/buffer) ครั้งแรกถ้ายังว่าง แล้ว reuse ทุกแถว — มีค่าอยู่แล้วจะ **ไม่ทับ** (Gap จึงเทียบกันได้บนสมมติฐานเดียว) · master ใช้ **Cap A = Hist×Fade** (drop forward/consensus CAGR ที่มีเฉพาะ Engine รายตัว) → chat ตรงกับที่ Excel recalc

## ข้อควรระวัง / วินัย

- **verify 2 รอบบังคับ** — อย่าเพิ่งเชื่อรอบแรก ไล่เช็คทุกตัวเลขจากงบล่าสุดอีกรอบทุกตัว เจอเพี้ยน → แก้ → rerun (ห้ามข้าม)
- **screener = append เท่านั้น** — ไม่ทับแถวเดิม เขียนเฉพาะ input cols ห้ามแตะช่องสูตร · ค่าที่ลงตารางต้องผ่าน verify แล้ว
- **Gap เทียบกันได้เฉพาะ assumptions ฐานเดียว** — globals (tax/fade/max_pen/abs_ceiling/buffer) ต้องเหมือนกันทุกแถวถึงจะเทียบ Gap ข้ามหุ้นได้
- **sector สะกดตรง WACC table เป๊ะ** — ผิดตัวเดียว VLOOKUP หลุด · ใส่ WACC จริงเป็น override (C9) เสมอ (ตารางเป็น placeholder)
- **WACC ในตารางเป็น placeholder** · **TAM squishy ที่สุด** — กระทบ Plausible CAGR โดยตรง ใส่อย่างระวัง
- **ไม่กุข้อมูล** — ไม่พบให้เขียน "ไม่พบข้อมูล" + บอกแหล่งที่หาแล้ว · ระบุ as-of date เสมอ
- verdict + โซนราคา เป็น **framework signal** ไม่ใช่คำสั่งซื้อขาย · Terminal-Anchored เหมาะหุ้นที่มูลค่าอยู่ปลายทาง — หุ้น mature อาจ overstate (เช็ค `/quick` ก่อน)

## Disclaimer

เครื่องมือนี้เป็นกรอบวิเคราะห์ความคาดหวัง **เชิงการศึกษา ไม่ใช่คำแนะนำการลงทุนรายบุคคล** · ตัวเลขทุกตัวต้อง verify เองกับ 10-K/10-Q/IR ล่าสุด · WACC placeholder · TAM squishy ที่สุด · ผู้ใช้รับผิดชอบผลการลงทุนเองทั้งสิ้น · เรียบเรียงจาก Earthh Evans · Invest Hub

---

> กลับไปที่ README ของ plugin: [`../plugins/reverse-dcf-screener/README.md`](../plugins/reverse-dcf-screener/README.md)
