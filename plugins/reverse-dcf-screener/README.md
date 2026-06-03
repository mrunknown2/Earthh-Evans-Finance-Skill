# Reverse DCF Screener

เครื่องมือ **Reverse DCF Screener (Terminal-Anchored)** — ถอด "ความคาดหวัง" ที่ราคาหุ้นฝังไว้ออกมาเป็นตัวเลข: ราคาตอนนี้บังคับให้บริษัทโตปีละกี่ % (**Market-Implied CAGR**) แล้วเทียบกับสิ่งที่ทำได้จริง (**Plausible CAGR**) → สรุป **ถูก / Fair / แพง** + **โซนราคาน่าสะสม 4 ระดับ** AI ดึงงบจริง → กรอกลง Excel template → verify 2 รอบ → สรุปใน chat

> เรียบเรียงจาก **Earthh Evans · Invest Hub**

## แนวคิด

> "ไฟล์นี้ไม่ได้บอกว่าหุ้นจะขึ้นมั้ย แต่บอกว่า **ราคาตอนนี้คาดหวังให้โตเท่าไหร่ แล้วบริษัททำได้จริงรึเปล่า**"

DCF ปกติ = เดาการเติบโต → คำนวณราคา · **Reverse DCF = เริ่มจากราคาตลาด → ถอดกลับว่าราคานั้นฝัง "การเติบโต" ไว้เท่าไหร่** แล้วถามว่าสมเหตุสมผลไหม

- **Terminal-Anchored** — ยึดมูลค่าที่ปลายทาง (terminal year) เพราะมูลค่าหุ้นเติบโตส่วนใหญ่อยู่ที่นั่น → เหมาะหุ้นที่ "เรื่องราว" อยู่ข้างหน้า
- **Market-Implied CAGR** = อัตราโตที่ราคาปัจจุบัน "เรียกร้อง" · **Plausible CAGR** = เพดานที่เป็นไปได้จริง (อิง historical / forward / TAM / absolute ceiling)
- **Gap = Implied − Plausible** → ตัวตัดสินว่าราคาแพงไป (priced for perfection) หรือถูก (low expectations)

## Setup

⚠️ ต้องมีของพวกนี้ก่อนรัน plugin

| ต้องมี | ใช้ทำอะไร |
|---|---|
| **Python 3** | รัน `fill_engine.py` กรอก input + คำนวณ engine คู่ขนาน |
| **`pip install openpyxl`** | ไลบรารีเขียน/อ่านไฟล์ `.xlsx` (จำเป็น — engine พังถ้าไม่มี) |
| **Excel / Google Sheets** | เปิดไฟล์ผลลัพธ์ `analyses/<TICKER>_<วันที่>.xlsx` เพื่อให้สูตรในช่อง recalc เห็นเลขครบ |
| **Web access** | agent ใช้ WebSearch / WebFetch ดึง 10-K / 10-Q / earnings + WACC จาก Damodaran |

> `openpyxl` เขียนสูตรลง cell ได้แต่ **ไม่ recalc** → plugin จึงกรอกเฉพาะ input cells (สีเหลือง) คงสูตรไว้ทั้งหมด แล้วคำนวณซ้ำใน Python เพื่อสรุป chat · เปิดไฟล์ใน Excel เมื่อไหร่ สูตร recalc เองทันที

## Workflow 3 สเต็ป

```
1. /analyze <TICKER>   ดึงงบจริง → กรอก Engine ลง analyses/<TICKER>_<date>.xlsx
                       → คำนวณ Implied / Plausible / Gap / Verdict เบื้องต้น
       ↓
2. /verify             อย่าเพิ่งเชื่อรอบแรก — ไล่เช็คทุกตัวเลขจากงบล่าสุด *อีกรอบ*
                       (discipline บังคับ) → แก้ค่าที่เพี้ยน → rerun engine
       ↓
3. /zones              สรุปโซนราคา 4 ระดับ + เหตุผล อิง Market-Implied CAGR
```

> หรือใช้ `/full <TICKER>` รวบ analyze → verify → zones → append screener จบในคำสั่งเดียว

### อ่านผลโซนราคา 4 ระดับ

**หัวใจคือ Market-Implied CAGR** — ราคาปัจจุบันเรียกร้องให้โตปีละกี่ % เทียบกับ Plausible CAGR (เพดานที่ทำได้จริง):

| โซน | เกณฑ์ (อิง Plausible CAGR) | ความหมาย |
|---|---|---|
| 🟢 **Strong Buy** | ราคา ≤ จุดที่ Implied = `MAX(Plausible − 5%, 0)` | ตลาดคาดหวังต่ำกว่าที่ทำได้จริงมาก — low expectations |
| 🟢 **Fair Value** | Implied ≈ Plausible | ราคาเรียกร้องพอดีกับที่ทำได้จริง — สมเหตุสมผล |
| ⚠️ **Caution** | Implied = Plausible **+5% ถึง +10%** | ราคาเริ่มเรียกร้องเกินจริง — ระวัง |
| 🔴 **Red Flag** | Implied ≥ Plausible **+10%** | priced for perfection — ราคาฝังความคาดหวังที่บริษัททำไม่ไหว |

> **Gap > Buffer → "แพง"** · **Gap < −Buffer → "ถูก"** · ระหว่างนั้น → **"Fair"** (Gap = Implied − Plausible)

## Commands (9 ตัว)

| Command | ใช้เมื่อ |
|---|---|
| `/full <TICKER>` | Pipeline เต็ม — analyze → verify → zones → append screener จบในคำสั่งเดียว (เริ่มต้นแนะนำ) |
| `/analyze <TICKER>` | Step 1 — ดึงงบ → กรอก Engine → ได้ Excel + Implied/Plausible/Gap/Verdict เบื้องต้น |
| `/verify` | Step 2 — ไล่เช็คทุกตัวเลขจากงบล่าสุด *อีกรอบ* (discipline บังคับ) → rerun engine |
| `/zones` | Step 3 — โซนราคา 4 ระดับ (Strong Buy/Fair/Caution/Red Flag) + เหตุผล อิง Implied CAGR |
| `/quick <TICKER>` | เช็คเร็วก่อนวิเคราะห์เต็ม — เหมาะ Terminal-Anchored ไหม (มูลค่าอยู่ปลายทาง?) + EV/Sales sanity |
| `/screener` | append หุ้นลง master screener + แสดงตารางเทียบแพง/ถูกหลายตัว |
| `/wacc <sector>` | lookup WACC ราย sector + พยายามดึงค่าจริงจาก Damodaran (WebFetch) + เตือน placeholder |
| `/sensitivity` | ตาราง Implied CAGR ตาม WACC × Terminal Margin และ WACC × Price |
| `/methodology` | อธิบายตรรกะ Terminal-Anchored Reverse DCF เชิงการศึกษา |

## Installation

```
/plugin marketplace add mrunknown2/Earthh-Evans-Finance-Skill
/plugin install reverse-dcf-screener
```

> ใช้นอก Claude Code (Antigravity / Codex) ได้ด้วย — ดู [`INSTALL.md`](INSTALL.md)

## ตัวอย่างการใช้งาน

```
/reverse-dcf-screener:full IREN
```

→ agent ดึงงบ IREN → กรอก `analyses/IREN_<วันที่>.xlsx` → verify รอบ 2 → สรุป Implied/Plausible/Gap/Verdict + โซนราคา 4 ระดับ → append ลง master screener · เปิดไฟล์ใน Excel เห็นสูตร recalc ครบ

## ⚠️ Disclaimer

เครื่องมือนี้เป็นกรอบวิเคราะห์ **เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล**

- **ตัวเลขทุกตัวต้อง verify เอง** — agent ดึงจากงบจริงแต่ผู้ใช้ต้องตรวจซ้ำกับ 10-K/10-Q/IR ล่าสุดก่อนตัดสินใจ
- **WACC ในตารางเป็น placeholder** — ค่าใน `wacc-damodaran.md` เป็นค่าตั้งต้น ควรอัปเดตจาก Damodaran (ม.ค. ทุกปี) หรือใส่ override เอง
- **TAM squishy ที่สุด** — ตัวเลข Total Addressable Market + max penetration เป็นสมมติฐานที่อ่อนไหวสูง กระทบ Plausible CAGR โดยตรง
- verdict (ถูก/Fair/แพง) + โซนราคา คือ **framework signal** จากกรอบ Terminal-Anchored **ไม่ใช่คำสั่งซื้อขาย**
- Terminal-Anchored เหมาะหุ้นที่มูลค่าอยู่ปลายทาง — หุ้น mature อาจ overstate; เช็ค `/quick` ก่อนว่าเหมาะกับวิธีนี้ไหม
- พิจารณาบริบทภาษี/เป้าหมาย/ความเสี่ยงของตนเองก่อนทุกครั้ง — ผู้ใช้รับผิดชอบผลการลงทุนเองทั้งสิ้น
