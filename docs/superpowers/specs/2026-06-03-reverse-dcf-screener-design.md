# Design Spec — `reverse-dcf-screener` Plugin

> **Date:** 2026-06-03
> **Author:** มูกิ C (Claude) ร่วมกับนายท่าน
> **Source material:** `source/reverse_DCF_Template.xlsx` (REVERSE DCF SCREENER — Terminal-Anchored, โดย Earthh Evans)
> **Status:** Approved design — pending implementation plan

---

## 1. ภาพรวม & เป้าหมาย (Overview)

ปลั๊กอินที่ **4** ของ marketplace `earthh-evans-finance` — แปลงเครื่องมือ Excel "Reverse DCF Screener (Terminal-Anchored)" ของ Earthh Evans เป็น skill/agent/commands ที่ใช้งานจริงได้

**Positioning (คงจิตวิญญาณ Earth):**
> "ไฟล์นี้ไม่ได้บอกว่าหุ้นจะขึ้นมั้ย แต่บอกว่า ราคาตอนนี้คาดหวังการเติบโตไว้เท่าไหร่ แล้วบริษัททำได้จริงรึเปล่า"

**สิ่งที่ผู้ใช้ได้:**
1. ไฟล์ Excel ที่กรอกข้อมูลครบ + คำนวณเสร็จ (สำเนาต่อหุ้น) — เปิดใน Excel เห็นผลทันที
2. คำสรุป verdict (ถูก/Fair/แพง) + โซนราคาน่าสะสมใน chat

**บทบาท (แบ่งหน้าที่ตามต้นฉบับ):**
| ใคร | หน้าที่ |
|---|---|
| **AI (agent)** | ดึงงบจริง (10-K/10-Q/earnings) → verify → กรอก input + คำนวณ → สรุป chat |
| **Excel (สูตรฝังในไฟล์)** | recalc เมื่อเปิด → โชว์ Implied/Plausible CAGR, Gap, Verdict, โซนราคา |
| **fill_engine.py** | กรอก input cells + คำนวณคู่ขนาน (Python) เพื่อให้ AI สรุปได้โดยไม่ต้องเปิด Excel |

---

## 2. สถาปัตยกรรม (Approach A: Portable-core + Claude Code wrapper)

แยก **แกนกลาง portable** (skill package มาตรฐาน — Claude Code / Antigravity / Codex อ่านได้เหมือนกัน) ออกจาก **เปลือก Claude Code** (เข้าชุด marketplace)

**ทำไม portable ได้:** ทั้ง 3 IDE บรรจบที่มาตรฐาน "skill = โฟลเดอร์ + `SKILL.md` + assets (template/scripts/references)"
- Claude Code → plugin + `skills/<name>/SKILL.md`
- Antigravity → Skills (`.agents/skills`, directory + SKILL.md + assets)
- Codex → Agent Skills (`/skills`, `$`) + AGENTS.md + plugins

### File tree

```
plugins/reverse-dcf-screener/
├── .claude-plugin/
│   └── plugin.json                    # เปลือก: manifest (Claude Code)
├── agents/
│   └── reverse-dcf-screener.md        # เปลือก: 1 agent (Reverse DCF Desk)
├── commands/                          # เปลือก: 9 slash commands
│   ├── analyze.md
│   ├── verify.md
│   ├── zones.md
│   ├── full.md
│   ├── quick.md
│   ├── screener.md
│   ├── wacc.md
│   ├── sensitivity.md
│   └── methodology.md
├── skills/
│   └── reverse-dcf-screener/          # ⭐ แกน portable — ทั้ง 3 IDE อ่านได้
│       ├── SKILL.md                   #   routing + critical rules + disclaimer
│       ├── assets/
│       │   └── reverse_dcf_screener.xlsx   # template สะอาด (ล้างเคสตัวอย่าง)
│       ├── references/
│       │   ├── methodology.md         #   สูตร Terminal-Anchored + ตรรกะเต็ม
│       │   ├── prompt.md              #   prompt ดึงงบ → JSON
│       │   └── wacc-damodaran.md      #   ตาราง WACC + วิธีอัปเดต
│       └── scripts/
│           └── fill_engine.py         #   กรอก cell + คำนวณ (รันที่ไหนก็ได้)
├── INSTALL.md                         # ติดตั้งต่อ IDE (Claude Code/Antigravity/Codex)
└── README.md                          # คู่มือ + disclaimer + เครดิต Earth
```

### แก้ที่ root (2 ไฟล์)
- `.claude-plugin/marketplace.json` → เพิ่ม entry ที่ 4 + metadata `"3 plugins"` → `"4 plugins"` + version `0.2.0` → `0.3.0`
- `README.md` (root) → เพิ่มแถวตาราง plugins + command summary block

---

## 3. Commands (9 ตัว, 3 กลุ่ม)

### กลุ่ม A — 3 สเต็ปหลัก (ตามคู่มือ Earth)
| Command | ทำอะไร | map | ไฟล์ |
|---|---|---|---|
| `/analyze <TICKER>` | ดึงงบ → กรอก Engine ลง `analyses/<หุ้น>_<วันที่>.xlsx` → คำนวณ → สรุปเบื้องต้น | Step 1 | สร้าง |
| `/verify` | ไล่เช็คตัวเลขจากงบล่าสุด**อีกรอบ** (discipline บังคับ) แก้ค่าที่เพี้ยน | Step 2 | แก้ |
| `/zones` | สรุปโซนราคา 4 ระดับ + เหตุผล อิง Market-Implied CAGR | Step 3 | อ่าน |

### กลุ่ม B — Pipeline
| Command | ทำอะไร |
|---|---|
| `/full <TICKER>` | analyze → verify → zones → append screener จบในคำสั่งเดียว |
| `/quick <TICKER>` | เช็คเร็ว: เหมาะ Terminal-Anchored ไหม + EV/Sales sanity (ก่อนวิเคราะห์เต็ม) |

### กลุ่ม C — ตาราง / Lookup
| Command | ทำอะไร | map |
|---|---|---|
| `/screener` | append หุ้นลง master screener + แสดงตารางเทียบแพง/ถูก | sheet Screener |
| `/wacc <sector>` | lookup WACC + พยายามดึงค่าจริงจาก Damodaran (WebFetch) + เตือน placeholder | sheet WACC_Damodaran |
| `/sensitivity` | ตาราง Implied CAGR ตาม WACC×Margin และ WACC×Price | sheet Engine |
| `/methodology` | อธิบายตรรกะ Terminal-Anchored เชิงการศึกษา | sheet วิธีใช้ |

---

## 4. Agent + SKILL.md

### Agent — `agents/reverse-dcf-screener.md`
**Persona:** *"Reverse DCF Desk"* — นักวิเคราะห์สาย expectation investing (Damodaran-style) โทน**มืออาชีพ + สอนได้**

**Frontmatter:**
```yaml
---
name: reverse-dcf-screener
description: >
  Reverse DCF Desk — ถอดความคาดหวังที่ราคาหุ้นฝังไว้ด้วย Terminal-Anchored
  Reverse DCF → Market-Implied CAGR เทียบ Plausible CAGR → หุ้นถูก/แพง +
  โซนราคาน่าสะสม. กรอก Engine ลง Excel + verify 2 รอบ. เชิงการศึกษา ไม่ใช่คำแนะนำ.
tools: Read, Write, Bash, WebSearch, WebFetch
model: opus
---
```
> จุดต่างจาก 3 ปลั๊กอินเดิม: ตัวนี้ **เขียนไฟล์ได้** (Write + Bash) เพราะกรอก Excel จริง

**Body sections:**
1. ROLE — persona + positioning
2. Discipline — ข้อมูลจริงก่อน · **verify 2 รอบบังคับ** · Terminal-Anchored fit-check · ไม่กุข้อมูล + as-of date
3. Methodology — สูตรครบ (ดู §6)
4. โซนราคา 4 ระดับ + เกณฑ์ CAGR
5. Workflow 3 สเต็ป
6. Critical Rules — yellow cells · sector สะกดตรง WACC table · source note ทุก cell · TAM squishy
7. Commands — ลิสต์ 9 ตัว
8. Disclaimer + เครดิต Earthh Evans

### SKILL.md — `skills/reverse-dcf-screener/SKILL.md` (แกน portable)
**Frontmatter:**
```yaml
---
name: reverse-dcf-screener
description: >
  ใช้เมื่ออยากรู้ว่าหุ้น "ถูกหรือแพง" ด้วยมุมความคาดหวัง — ราคาตอนนี้บังคับให้บริษัท
  โตปีละกี่ % แล้วทำได้จริงไหม. Terminal-Anchored Reverse DCF, Market-Implied CAGR,
  Plausible CAGR, expectation investing, โซนราคาน่าสะสม. เชิงการศึกษา ไม่ใช่คำแนะนำ.
---
```
**Body:** Intro + เครดิต Earth → Routing table (สถานการณ์ → command) → Critical Rules ย่อ → วิธีใช้ข้าม IDE (ชี้ `INSTALL.md`) → Disclaimer

---

## 5. Excel Handling (เครื่องยนต์)

### ปัญหา & ทางออก
`openpyxl` เขียนสูตรได้แต่ไม่ recalculate → **กลยุทธ์: กรอก input + คงสูตร + คำนวณคู่ขนาน**
1. ก๊อป template → `./analyses/<TICKER>_<วันที่>.xlsx` (ใน working dir ของ user)
2. เขียนเฉพาะ input cells (yellow) — **คงสูตรทั้งหมด ห้ามแตะช่องสูตร**
3. คำนวณซ้ำใน Python (port สูตรเป๊ะ) → print JSON ผลให้ AI สรุป chat
4. user เปิดใน Excel → สูตร recalc เองทันที

**ไม่ใช้ LibreOffice** (กันซับซ้อน — ยอมรับว่าไฟล์ต้องเปิดใน Excel ถึงเห็นเลขในช่องสูตร แต่ AI สรุป chat ได้ครบจากการคำนวณคู่ขนาน)

### `fill_engine.py` — interface
- **รับ:** JSON ของ input (ผ่าน stdin หรือ arg)
- **ทำ:** ก๊อป template → เขียน input cells → คำนวณ → print ผลเป็น JSON
- **คุณสมบัติ:** ไม่ต่อ DB · ไม่มี side effect อื่น · idempotent · รันได้ทุก agent

### Input cells (Engine sheet) — เขียนได้
| Cell | Field | Cell | Field |
|---|---|---|---|
| C4 | Ticker | C19 | Fade factor |
| C5 | Current Revenue R0 ($B) | C20 | TAM ($B) |
| C6 | Enterprise Value EV ($B) | C21 | Max penetration % |
| C7 | Sector (ตรง WACC table) | C22 | Absolute ceiling CAGR |
| C9 | WACC override (optional) | C40 | Buffer (±) |
| C11 | Terminal EBIT margin | C43 | Current Share Price ($) |
| C12 | Terminal growth g | C44 | Shares Outstanding (M) |
| C13 | Terminal ROIC | C45 | Net Debt ($B) |
| C14 | Tax rate | C48 | Analyst Price Target (Avg) |
| C15 | Horizon N | C49 | Analyst Range (text) |
| C18 | Historical Revenue CAGR 3yr | C50 | Consensus FY+1 Revenue ($B) |

**ห้ามแตะ (formula cells):** C8 (WACC auto VLOOKUP), C10 (WACC ใช้), C23 (Forward CAGR — derive จาก C50), C25–C36 (engine calc), C39 (Gap), C41 (Verdict), C46 (mktcap), D49/D50, sensitivity tables (G6:K10, G16:K21), verdict box, price zones (I34:I37)

### Screener sheet — append แถวใหม่
**เขียน:** A Ticker · B Sector · D Revenue R0 · E EV · F Term margin · G g · H ROIC · I N · J Hist CAGR · K TAM · Q WACC override (optional)
**ห้ามแตะ (formula):** C WACC · L Reinv · M Implied · N Plausible · O Gap · P Verdict
**Global assumptions (R/S):** S3 tax · S4 fade · S5 maxpen · S6 absceiling · S7 buffer

### Template cleanup
ล้างไฟล์ `assets/reverse_dcf_screener.xlsx` ให้สะอาด: ลบ input ตัวอย่าง IREN + **commentary SIMO ค้าง** (F31/F32/F38) + แถว Screener ตัวอย่าง (SpaceX/SIMO/PL/IREN) → เหลือ template เปล่าที่มีแต่สูตร

---

## 6. Methodology (สูตร port → Python, ตรง Excel 100%)

```
reinv       = g / ROIC
TV          = EV × (1+WACC)^N
FCFF        = TV × (WACC − g)
conversion  = margin × (1−tax) × (1−reinv)
R*          = FCFF / conversion
ImpliedCAGR = (R* / R0)^(1/(N+1)) − 1

Cap A = MAX(Hist, Forward) × Fade        # Forward = C50/R0−1 ถ้ามี
Cap B = (MaxPen × TAM / R0)^(1/(N+1)) − 1 # ถ้า TAM=0 → 999
Cap C = Absolute ceiling
Plausible = MIN(A, B, C)

Gap = ImpliedCAGR − Plausible
Verdict = Gap > Buffer  → "แพง — Priced for Perfection"
          Gap < −Buffer → "ถูก — Low Expectations"
          else          → "Fair — สมเหตุสมผล"

ราคาโซน(CAGR) = ((R0×(1+CAGR)^(N+1) × conversion / (WACC−g) / (1+WACC)^N) − NetDebt) × 1000 / Shares
   🟢 Strong Buy : CAGR = MAX(Plausible−0.05, 0)   (ราคา ≤)
   🟢 Fair Value : CAGR = Plausible
   ⚠️ Caution    : CAGR = Plausible+0.05 ถึง +0.10
   🔴 Red Flag   : CAGR = Plausible+0.10            (ราคา >)
```

**Convention:** N = ปี explicit · รายได้ปลายทาง = ปี N+1 · วัด CAGR ตลอด N+1 ปี

---

## 7. References (ไทยผสม EN ตามชุด repo)

| ไฟล์ | เนื้อหา |
|---|---|
| `methodology.md` | แนวคิด · ตรรกะ Terminal-Anchored · Plausible heuristic · Verdict · โซนราคา · Convention · ข้อควรระวัง (mature overstate, TAM squishy, WACC placeholder, tips cyclical/pre-profit) |
| `prompt.md` | ฐานจาก AI_Prompts B4 (persona + ข้อบังคับ + รายการข้อมูล 10 อย่าง + flag) แต่ **output = JSON schema สำหรับ `fill_engine.py`** (แทน "กรอก cell ตรง"); screener ผ่าน `/screener` |
| `wacc-damodaran.md` | ตาราง 25 sectors + ป้าย placeholder + ลิงก์ Damodaran + วิธีอัปเดต ม.ค. ทุกปี |

---

## 8. Integration & Docs

### plugin.json
```json
{
  "name": "reverse-dcf-screener",
  "version": "0.1.0",
  "description": "Reverse DCF Screener — Terminal-Anchored: ถอดความคาดหวังที่ราคาฝัง → Market-Implied CAGR เทียบ Plausible CAGR → หุ้นถูก/แพง + โซนราคาน่าสะสม. กรอก Excel template + verify 2 รอบ. portable (Claude Code/Codex/Antigravity). เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล.",
  "repository": "https://github.com/mrunknown2/Earthh-Evans-Finance-Skill",
  "license": "MIT",
  "author": { "name": "mrunknown2" },
  "keywords": ["finance","investing","stock","valuation","reverse-dcf","terminal-anchored","implied-cagr","expectation-investing","damodaran","excel","screener","earth-evans"]
}
```

### README.md (per-plugin)
Title + เครดิต Earth → concept table → **Setup (⚠️ Python3 + `pip install openpyxl`)** → workflow 3 สเต็ป + อ่านผลโซนราคา → commands table (9) → installation → usage example → disclaimer

### INSTALL.md (3 IDE)
| IDE | วิธี |
|---|---|
| Claude Code | `/plugin marketplace add ...` → `/plugin install reverse-dcf-screener` |
| Antigravity | ก๊อป `skills/reverse-dcf-screener/` → `.agents/skills/` |
| Codex | ก๊อปไป skills dir + **เปิด network** (sandbox ปิดเน็ต default) |
+ dependency: `pip install openpyxl`

### Disclaimer (ทุกไฟล์หลัก)
- "เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล / educational, not personal investment advice"
- "เรียบเรียงจาก **Earthh Evans · Invest Hub**"
- ⚠️ "ตัวเลขทุกตัวต้อง verify · WACC ในตารางเป็น placeholder · TAM squishy ที่สุด"

---

## 9. Dependencies & Non-Goals

**Dependencies:** Python 3 + `openpyxl` · web access (WebSearch/WebFetch) สำหรับดึงงบ

**Non-Goals (out of scope):**
- ❌ ไม่ recalc สูตรเอง (ไม่ใช้ LibreOffice) — ให้ Excel ทำตอนเปิด
- ❌ ไม่ทำ full stock analysis (DEEP+O) — นั่นคือ `deep-o-stock-analyst`
- ❌ ไม่ทำนายทิศทางราคา — เครื่องมือวัดความคาดหวัง
- ❌ ไม่แก้ logic/wrapper ของ 3 ปลั๊กอินเดิม

**Success Criteria:**
1. `/full <TICKER>` → ได้ไฟล์ `analyses/<TICKER>_<date>.xlsx` กรอกครบ + เปิดใน Excel เห็นผล recalc
2. ตัวเลข Python คำนวณ = สูตร Excel (cross-check กับเคสตัวอย่าง)
3. skill package ก๊อปไป Antigravity/Codex แล้วใช้ได้ (ผ่าน SKILL.md + references)
4. เข้าชุด pattern 3 ปลั๊กอินเดิม (disclaimer, เครดิต Earth, frontmatter)

---

## 10. Decisions Log (สิ่งที่นายท่านเคาะ)

| # | ประเด็น | ตัดสิน |
|---|---|---|
| 1 | รูปแบบ | Plugin ใหม่ standalone (ตัวที่ 4) |
| 2 | บทบาท | AI กรอก Excel + สรุป / Excel คำนวณ (ไม่ใช่ pure-prompt) |
| 3 | สถาปัตยกรรม | Approach A: portable-core + Claude Code wrapper |
| 4 | Portability | ใช้ได้ Claude Code + Codex + Antigravity (มาตรฐาน SKILL.md) |
| 5 | ไฟล์ output | (1) สำเนาต่อหุ้น + master screener |
| 6 | Commands | 9 ตัว (รวม `/methodology`) |
| 7 | Persona | Reverse DCF Desk — มืออาชีพ + สอนได้ |
| 8 | Agent tools | เขียนไฟล์ได้ (Write + Bash) |
| 9 | recalc | กรอก input + คงสูตร + Python คู่ขนาน (ไม่ LibreOffice) |
| 10 | References | 3 ไฟล์ · prompt ส่ง JSON · ไทยผสม EN |
| 11 | Versioning | plugin 0.1.0 · root bump 0.2.0→0.3.0 · "4 plugins" |
