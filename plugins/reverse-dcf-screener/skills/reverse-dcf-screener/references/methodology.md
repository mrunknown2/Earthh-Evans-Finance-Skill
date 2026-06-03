# Methodology — Reverse DCF Screener (Terminal-Anchored)

> เรียบเรียงจาก **Earthh Evans · Invest Hub** — sheet "วิธีใช้" + "Engine" ของไฟล์ต้นฉบับ
> เอกสารนี้คือ **แกนตรรกะ** ที่ `fill_engine.py` port มาเป็น Python (ตรงสูตร Excel 100%)

---

## แนวคิด — ทำไม Reverse DCF ต่างจาก screener P/E ทั่วไป

Screener ทั่วไปใช้ **P/E, PEG, EV/EBITDA ย้อนหลัง** = มองอดีต บอกได้แค่ว่า "ตอนนี้เทรดแพง/ถูกกว่าเมื่อก่อนหรือ peer แค่ไหน" แต่ไม่ได้บอกว่า **ตลาดคาดหวังอะไรไว้**

เครื่องมือนี้ **พลิกคำถาม** เป็น:

> "ราคาวันนี้กำลังเรียกร้องให้บริษัทโตปีละกี่ %?" → **Market-Implied CAGR**
> แล้วเทียบกับ "เพดานการเติบโตที่เป็นไปได้จริง" → **Plausible CAGR**

ส่วนต่าง **Gap = Implied − Plausible** คือคำตอบว่าแพงหรือถูก

จุดต่างสำคัญ: output **ไม่ใช่ราคาเป้าหมาย** (target price เปราะ — เปลี่ยน assumption นิดเดียวพังทั้งโมเดล) แต่เป็น **เกจวัดความคาดหวัง** (ทนทานกว่า) — เรามองที่ "ความคาดหวังที่ราคาฝังไว้" ไม่ใช่ตัวเลขในอดีต

---

## ตรรกะ Terminal-Anchored (5 สเต็ป)

สมมติว่า **มูลค่าเกือบทั้งก้อนอยู่ปลายทาง** (เหมาะกับหุ้น growth / pre-profit ที่กำไรช่วงต้นยังน้อย) แล้วถอดกลับ:

1. **TV (Terminal Value ปีที่ N)** — มูลค่าก้อนปลายทาง = ราคา ณ วันนี้ ทบ WACC ไป N ปี
   `TV = EV × (1+WACC)^N`
2. **FCFF (ปีถัดไป N+1)** — กระแสเงินสดอิสระจากสูตร Gordon Growth
   `FCFF = TV × (WACC − g)`
3. **R\*** (Implied Terminal Revenue) — ถอด FCFF กลับเป็น "รายได้ปลายทาง" ผ่าน conversion
   `conversion = margin × (1−tax) × (1−reinvestment)` โดย `reinvestment = g ÷ ROIC`
   `R* = FCFF ÷ conversion`
4. **Implied CAGR** — รายได้ปลายทางต้องโตจากรายได้วันนี้เฉลี่ยปีละกี่ %
   `Implied CAGR = (R*/R0)^(1/(N+1)) − 1`
5. **เทียบ Plausible** — เอา Implied CAGR ไปชน "เพดานที่เป็นไปได้จริง" (ดูหัวข้อถัดไป) → Gap → Verdict

---

## Plausible CAGR — Heuristic อัตโนมัติ (MIN ของ 3 เพดาน)

Plausible CAGR = **ค่าที่ต่ำที่สุด** ของ 3 เพดาน — "ข้อจำกัดที่ผูกมัดที่สุดชนะ" (the binding constraint wins):

| เพดาน | นิยาม | เหตุผล |
|---|---|---|
| **Cap A — Historical** | `MAX(Hist CAGR 3yr, Forward CAGR) × Fade factor` | การโตจริง decay ตามสเกล ใช้ fade (default 0.70) หักลง · Forward = `C50/R0 − 1` ถ้ามี consensus FY+1 |
| **Cap B — TAM** | CAGR ที่ทำให้รายได้ปลายทาง = `MaxPenetration% × TAM` | บริษัทโตเกินส่วนแบ่งสูงสุดของตลาดไม่ได้ · **ถ้า TAM = 0 → Cap B = 999** (ปลดล็อกเพดานนี้ออก ให้ A กับ C ตัดสินแทน) |
| **Cap C — Absolute** | เพดานแข็ง (default 0.45 = 45%) | การคงโต > 50% ต่อเนื่อง 10 ปี แทบไม่มีในประวัติศาสตร์ |

`Plausible CAGR = MIN(Cap A, Cap B, Cap C)`

---

## Verdict + Buffer

`Gap = Implied CAGR − Plausible CAGR`

| เงื่อนไข | Verdict |
|---|---|
| `Gap > Buffer` | 🔴 **แพง — Priced for Perfection** (ราคาต้องการ perfection — พลาดนิดเดียวร่วงหนัก) |
| `−Buffer ≤ Gap ≤ Buffer` | ⚪ **Fair — สมเหตุสมผล** |
| `Gap < −Buffer` | 🟢 **ถูก — Low Expectations** (ตลาดคาดหวังต่ำกว่าที่บริษัททำได้จริง) |

Buffer default = 0.05 (±5 percentage points) — โซนกันชนกัน false signal จากความ noise ของ assumption

---

## โซนราคา 4 ระดับ (Market-Implied Price Zones)

แปลง CAGR แต่ละระดับกลับเป็น "ราคาต่อหุ้น" ผ่านสูตร `ราคาโซน(CAGR)` ด้านล่าง — เพื่อบอกว่า **ราคาเท่าไหร่ถึงน่าสะสม**:

| โซน | CAGR ที่ใช้ | ความหมาย |
|---|---|---|
| 🟢 **Strong Buy** | `MAX(Plausible − 0.05, 0)` | ราคา **≤** ระดับนี้ = ตลาดคาดหวังต่ำกว่าเพดานจริงพอควร — margin of safety สูง |
| 🟢 **Fair Value** | `Plausible` | ราคาที่ความคาดหวัง = เพดานจริงพอดี |
| ⚠️ **Caution** | `Plausible + 0.05` ถึง `+0.10` | ราคาเริ่มเรียกร้องเกินเพดานจริง — ระวัง |
| 🔴 **Red Flag** | `Plausible + 0.10` | ราคา **>** ระดับนี้ = priced for perfection อย่างหนัก |

> โซนราคายิ่งต่ำ = ความคาดหวังที่ฝังในราคายิ่งต่ำ = ยิ่งมี margin of safety

---

## Convention (กฎเวลาของไฟล์นี้)

- **N** = จำนวนปี explicit (ช่วงพยากรณ์ชัดเจน)
- **รายได้ปลายทาง** = รายได้ของปีที่ **N+1** (ไม่ใช่ปี N)
- **วัด CAGR ตลอด N+1 ปี** — เช่น N = 10 → วัดการเติบโต 11 ปี (จึงใช้ exponent `1/(N+1)`)

ตรงนี้สำคัญ: ถ้าเข้าใจ convention ผิด (ใช้ N แทน N+1) ตัวเลข Implied CAGR จะเพี้ยน

---

## ข้อควรระวัง (ขีดจำกัดของเครื่องมือ)

1. **Mature stock → overstate** — Terminal-Anchored แม่นกับหุ้นที่มูลค่าเกือบทั้งก้อนอยู่ปลายทาง (growth/pre-profit) เท่านั้น · กับหุ้น mature ที่ cash flow ช่วงต้นเยอะ โมเดลจะ **overstate** CAGR ที่ต้องการ → ใช้เป็น stress test ได้ แต่อย่าตีความตรงตัว
2. **TAM squishy ที่สุด** — TAM เป็นตัวเลขที่ "นิ่ม" ที่สุดในโมเดล ระวังบริษัทเคลม TAM เว่อร์เกินจริง (Cap B จะหลวมทันที)
3. **WACC เป็น placeholder** — ค่า WACC ในชีต/ตาราง Damodaran เป็นค่า **ตัวอย่าง** ต้องโหลดของจริงจาก Damodaran (อัปเดต ม.ค. ทุกปี — ชุดล่าสุด ม.ค. 2026) มาวางทับ → ดู `wacc-damodaran.md`
4. **ตัวเลขทุกตัวต้อง verify** ก่อนใช้จริง

### Tips สำหรับผลลัพธ์ที่แม่นยำ
- **หุ้น cyclical** (semicon, oil, shipping) → อย่าใช้ hist CAGR จาก trough → now (จะบิดเบี้ยวด้วย momentum) — ใช้ blend full cycle หรือ 5 ปีแทน
- **หุ้น pre-profit ที่ inflection** (เช่น PL, RKLB) → ใช้ forward guidance FY+1 แทน hist CAGR เพราะอดีตไม่ represent อนาคต
- **verdict → ถูกมาก** อย่าเพิ่ง buy — เช็คก่อนว่า "ถูกเพราะกิจการย่ำแย่จริง" หรือ "ถูกเพราะ market ยังไม่รู้ thesis"
- **verdict → แพง** ไม่ได้แปลว่าขาย — แปลว่า "ราคาตอนนี้ต้องการ perfection — พลาดนิดเดียวร่วงหนัก"

---

## Formula Block (verbatim จาก spec §6 — port เป็น Python ตรง Excel 100%)

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

> เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล / educational, not personal investment advice — เรียบเรียงจาก Earthh Evans · Invest Hub
