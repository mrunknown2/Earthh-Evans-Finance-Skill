# Companion Variables — Damodaran Framework
## ทุก Multiple คือ DCF ย่อรูป

> ทุก Multiple มีตัวแปร "ขับเคลื่อน" มันอยู่เบื้องหลัง — ก่อนจะใช้ Ratio ตัวไหน
> ต้องเข้าใจก่อนว่าอะไรคือตัวแปรที่ทำให้มันสูงหรือต่ำอย่างสมเหตุสมผล

เครื่องมือนี้แปลง Multiples ทั้ง 6 ตัวให้เป็น **Justified Multiple** ที่คำนวณจากปัจจัยพื้นฐาน — ไม่ใช่เทียบ Peer แบบ Gut-feel
สูตรทุกตัวมาจาก Damodaran (NYU Stern) และ port ตรงเข้าไปใน engine (`checklist_engine.py` → `companion()`)

---

## CV-1 | P/E Ratio — Companion Variable: EPS Growth Rate

P/E คนเดียวไม่มีความหมาย — P/E 30x ของบริษัทที่โต 5% ต่อปี กับ P/E 30x ของบริษัทที่โต 30% ต่อปี คือคนละเรื่องกันโดยสิ้นเชิง

### สูตร Justified P/E (Damodaran)

```
Justified P/E = (Payout Ratio × (1 + g)) / (Cost of Equity − g)
```

- `g` = อัตราการเติบโต EPS ที่ยั่งยืนระยะยาว
- สูตรนี้บอกว่า P/E "ควร" ซื้อขายที่เท่าไร ตาม Fundamental จริง

### PEG Ratio — ทางลัดที่ใช้งานได้จริง

```
PEG = P/E ÷ Expected EPS Growth Rate (5-Year CAGR)
```

| PEG | ความหมาย |
|-----|-----------|
| < 1.0 | อาจ Undervalued เทียบกับ Growth |
| 1.0–2.0 | Fair Value zone |
| > 2.0 | Growth ถูก Price In ไปแล้ว หรือ Overvalued |

### วิธีอ่าน P/E ให้ถูกต้อง

| P/E | EPS Growth (5Y) | PEG | สรุป | ตัวอย่าง |
|-----|-----------------|-----|------|----------|
| 35x | 35% | **1.0x** | Fair Value | NVIDIA FY2024 |
| 25x | 12% | 2.1x | แพง — ต้องดู Margin | Consumer Staple |
| 15x | 3% | 5.0x | Value Trap? | Retail ที่กำลังถดถอย |
| 50x | 50% | **1.0x** | Premium ที่สมเหตุสมผล | Early-stage Cloud SaaS |
| 12x | 15% | **0.8x** | Undervalued | Meta Q4 2022 |

### PEG Trap — จุดที่ทางลัดนี้พัง

1. **Growth Rate ต้องเป็น Sustainable Growth จริง** ไม่ใช่ปีเดียวที่ดีผิดปกติ
2. **PEG สมมติว่าความสัมพันธ์เป็น Linear** ซึ่งไม่จริงสำหรับ Growth สูงมากหรือต่ำมาก
3. **ต้องใช้คู่กับ Earnings Quality เสมอ**: EPS ได้มาจาก Operations หรือ Financial Engineering?
4. **แต่ละ Sector มี "PEG ปกติ" ไม่เท่ากัน** — SaaS Asset-light ยอมให้ PEG ต่ำกว่า Cyclical Industrial

> **PEG หลอกตาเพิ่มเติม:** ถ้า EPS Growth มาจาก Buyback หนัก + Margin One-off
> ให้ใช้ Revenue Growth + Margin Path ประกอบด้วยเสมอ เพราะ PEG ที่ดูต่ำอาจซ่อน Earnings ที่ไม่ได้มาจากการเติบโตของธุรกิจจริง

---

## CV-2 | EV/Sales — Companion Variable: After-Tax Operating Margin

EV/Sales เป็น Multiple ที่ถูกผิดผิดมากที่สุดใน Finance — EV/Sales โดยไม่ดู Margin แทบบอกอะไรไม่ได้เลย

### สูตร Justified EV/Sales (Damodaran)

```
Justified EV/Sales = After-Tax Operating Margin × (1 − Reinvestment Rate) / (WACC − g)

After-Tax Operating Margin = EBIT × (1 − Tax Rate) / Revenue
```

สูตรนี้บอกว่า EV/Sales "ที่ควรได้" ของแต่ละบริษัทขึ้นกับ Margin + Growth ที่แท้จริง

> **หมายเหตุสำคัญ:** ช่วงตัวเลข Justified EV/Sales ด้านล่างเป็น "ช่วงคร่าว ๆ" เท่านั้น
> ค่าจริงขึ้นอยู่กับ WACC และ g ของแต่ละบริษัท บริษัทเดียวกันแต่ WACC ต่างกัน 2% อาจให้ Justified EV/Sales ต่างกันถึง 30–50%

### ตาราง Benchmark EV/Sales — นำมาดูเดียว

| ประเภทธุรกิจ | After-Tax Op Margin | Justified EV/Sales | สิ่งที่ต้องระวัง |
|--------------|--------------------|--------------------|-----------------|
| SaaS ที่โตเต็มตัว (เช่น Salesforce) | 20–30% | 6–12x | Margin ต้องยั่งยืน ไม่ใช่แค่ปีเดียว |
| High-Growth SaaS (ยังขาดทุน) | 0–10% | 2–5x สูงสุด | ต้องมี Path to 20%+ Margin ที่ชัดเจน |
| E-Commerce / Retail | 2–5% | 0.3–1x | Margin ต่ำ = Multiple ต่ำคือปกติ |
| Semiconductor ชั้นนำ | 30–55% | 8–20x | Margin สูงรองรับ Multiple สูงได้ |
| E-Commerce Margin 2% แต่ EV/S 3x | 2% | **OVERVALUED** | นี่คือตัวอย่างที่ Formula พังทันที |

### ตัวอย่างจริง: ทำไม EV/Sales คนเดียวถึงอันตราย

| บริษัท | EV/Sales | After-Tax Op Margin | สรุป |
|--------|----------|--------------------|----- |
| NVIDIA (FY2025E) | ~20x | 55%+ | Multiple สูง แต่ Margin สูงกว่า = Justified |
| Wayfair (2021) | ~1.5x | -5% | Multiple ดูถูก แต่ Margin ติดลบ = ยังแพงอยู่ |
| Meta (2023) | ~5x | 35% | Margin Expansion ทำให้ Re-rate ได้มหาศาล |
| Peloton (ปลาย 2021) | ~6x | **-20%** | ดูสมเหตุสมผล แต่จริง ๆ แล้ว Overvalued สุด ๆ |

### วิธีใช้ EV/Sales ให้ถูกต้อง (4 ขั้นตอน)

1. **ขั้นที่ 1:** หา After-Tax Operating Margin ปัจจุบัน
2. **ขั้นที่ 2:** Estimate Margin ที่ยั่งยืนของธุรกิจโตเต็มตัว (ดู Industry Leader เป็น Benchmark)
3. **ขั้นที่ 3:** คำนวณ Justified EV/Sales ด้วยสูตร Damodaran
4. **ขั้นที่ 4:** เปรียบเทียบ EV/Sales ปัจจุบัน vs Justified — แล้วค่อยสรุป

> **Red Flag:** EV/Sales สูง + Margin กำลังหด = อันตรายสองชั้น

---

## CV-3 | EV/EBITDA — Companion Variables: CapEx Intensity & ROIC

EBITDA ตัด Interest กับ Tax ออก แต่ยัง**ตัด CapEx ออกด้วย** — นี่คือปัญหา บริษัทสองเจ้าที่มี EV/EBITDA เท่ากันอาจสร้าง Cash จริงต่างกันมากถ้า CapEx Intensity ต่างกัน

### การปรับ EV/EBITDA ให้แม่นขึ้น

```
EV / (EBITDA − Maintenance CapEx) = วัดได้แม่นกว่าสำหรับธุรกิจ Capital-Intensive
```

> ค่า CapEx ที่หักออกในสูตรนี้ = "Maintenance CapEx" เท่านั้น (CapEx ที่จำเป็นต่อการรักษา EBITDA ปัจจุบัน)
> ไม่ใช่ CapEx ทั้งก้อนในงบ — ถ้าหัก CapEx ทั้งหมดออกจะ Understate มูลค่าของบริษัทที่กำลังลงทุนเพื่อเติบโต

### ตาราง CapEx Adjustment

| Sector | EV/EBITDA | CapEx/Revenue | EV/EBIT จริง | สรุป |
|--------|-----------|---------------|-------------|------|
| Cloud Software | 20x | 2–3% | ~21x | เกือบเท่ากัน — Asset-Light |
| Telecom | 8x | 20–25% | ~20x | EV/EBITDA ดูถูก แต่ EV/EBIT แพงมาก |
| Semiconductor | 15x | 5–8% | ~17x | ต้องปรับนิดหน่อย |
| Airline | 6x | 15–20% | >20x | Value Trap Classic ของ Sector นี้ |
| Consumer Brand | 18x | 3–5% | ~20x | Premium พอรับได้ถ้า Moat แข็งแรง |

### ROIC คือ Companion Variable ที่ขาดไม่ได้

EV/EBITDA บอกว่าเราจ่ายเท่าไร — ROIC บอกว่าเราได้อะไรกลับมา — ต้องอ่านคู่กันเสมอ

| ROIC vs WACC | EV/EBITDA | ความหมาย |
|--------------|-----------|----------|
| ROIC >> WACC (เช่น 35% vs 10%) | สูง (15–25x) | สมเหตุสมผล — ทุกบาทที่ลงทุนสร้างมูลค่า |
| ROIC ≈ WACC | ปานกลาง (10–15x) | Fair Value — Growth ไม่ได้เพิ่มมูลค่าเกิน Cost |
| ROIC < WACC | ควรต่ำ (<10x) | ทำลายมูลค่า — Multiple ต่ำคือ Margin of Safety เดียวที่มี |

---

## CV-4 | P/B Ratio — Companion Variable: Return on Equity (ROE)

P/B < 1 ไม่ได้แปลว่าถูกเสมอ — บ่อยครั้งตลาด Price In ถูกต้องแล้วว่าบริษัทนั้นทำกำไรได้ต่ำกว่า Cost of Equity — บริษัทที่ ROE ต่ำกว่า Cost of Equity ควรซื้อขายต่ำกว่า Book Value โดยธรรมชาติ

### สูตร Justified P/B (Damodaran)

```
Justified P/B = (ROE − g) / (Cost of Equity − g)
```

- ถ้า ROE = CoE → P/B = 1.0x
- ถ้า ROE > CoE → P/B > 1 คือ Justified
- ถ้า ROE < CoE → P/B < 1 คือ Fair

### ตาราง Scenario P/B

| Scenario | ROE | Cost of Equity | g | Justified P/B | บทเรียน |
|----------|-----|----------------|---|---------------|---------|
| Quality Compounder | 30% | 10% | 8% | **11.0x** | ROE สูง = Premium ขนาดนี้ได้ |
| ธุรกิจทั่วไป | 12% | 10% | 4% | 1.33x | Premium นิดหน่อย สมเหตุสมผล |
| Value Trap | 8% | 10% | 3% | 0.71x | P/B ต่ำกว่า 1 คือ Fair ไม่ใช่ถูก |
| ธุรกิจกำลังถดถอย | 5% | 10% | 1% | 0.44x | P/B 0.5x ยังไม่ถูกจริง |
| ธนาคารในช่วง Stress | 4% | 12% | 2% | **0.20x** | P/B 0.3x ก็ยังแพงได้ |

### คำเตือน: ต้อง Decompose ROE ด้วย DuPont ก่อนเสมอ

```
DuPont Formula: ROE = Net Margin × Asset Turnover × Equity Multiplier
```

ROE ที่ดูสูง แต่มาจาก D/E สูง (Equity Multiplier) ≠ คุณภาพธุรกิจ

- ROE ที่ดีที่สุดมาจาก Net Margin ขยายตัว หรือ Asset Turnover ดีขึ้น
- ไม่ใช่จากการกู้หนี้มาเพิ่ม — ถ้า ROE ดีเพราะ Leverage อย่างเดียว = Financial Engineering ไม่ใช่ Moat

---

## CV-5 | FCF Yield / EV/FCF — Companion Variables: FCF Growth + Reinvestment Rate

FCF Yield คือการวัดโดยตรงว่า "ธุรกิจทำเงินได้กี่บาทต่อทุก 1 บาทของ Enterprise Value" — แต่ต้องอ่านบนพื้นฐานของ Growth Potential และ Capital Intensity ด้วย

### สูตร

```
FCF Yield = Free Cash Flow to Firm (FCFF) / Enterprise Value (EV)
```

FCF Yield > อัตราพันธบัตร 10 ปี = Equity มี Positive Risk Premium เทียบกับ Risk-Free Rate

### Asset-Light vs Capital-Intensive — ทำไม EV/FCF ที่ "สมเหตุสมผล" ถึงต่างกัน

| ประเภทธุรกิจ | Maintenance CapEx | คุณภาพ FCF | EV/FCF ที่ Justified | ตัวอย่าง |
|--------------|-------------------|------------|---------------------|---------|
| SaaS / Software | 1–3% ของ Revenue | สูงมาก | 30–50x ได้ | Adobe, Salesforce |
| Consumer Brand | 3–5% ของ Revenue | สูง | 20–35x | Apple, Coca-Cola |
| Semiconductor | 5–10% ของ Revenue | ปานกลาง | 15–25x | Texas Instruments |
| Industrial / Manufacturing | 10–15% ของ Revenue | ต่ำลง | 10–18x | Caterpillar |
| Telecom / Utility | 20–30% ของ Revenue | ต่ำ — CapEx หนักมาก | 5–12x สูงสุด | AT&T, Utilities |

### Maintenance CapEx vs Growth CapEx — ความแตกต่างที่ซ่อนอยู่

- **Maintenance CapEx** = เงินที่ต้องจ่ายเพื่อรักษา Asset ปัจจุบัน (ต้นทุนที่แท้จริงของการดำเนินธุรกิจ)
- **Growth CapEx** = เงินลงทุนเพื่อขยาย Capacity ในอนาคต (สร้างมูลค่าถ้า ROIC > WACC)
- CapEx ที่รายงานในงบรวมสองอย่าง — ต้อง Estimate เองเพื่อคำนวณ Owner Earnings ที่แท้จริง

### Owner Earnings แบบ Buffett (FCF ที่แม่นกว่า)

```
Owner Earnings = Net Income + D&A − Maintenance CapEx − Working Capital Changes
```

ถ้า Owner Earnings >> Reported FCF: บริษัทกำลังลงทุนเพื่อเติบโตหนัก (ดีถ้า ROIC > WACC)

---

## Master Summary Table — Companion Variables ทั้ง 6

| Multiple | ตัวขับเคลื่อนหลัก | คำถามสำคัญที่ต้องถาม | Red Flag |
|----------|-------------------|--------------------|---------|
| P/E | EPS Growth Rate | Growth ที่ยั่งยืนได้ 5 ปีข้างไปไหม? | EPS โตเพราะ Buyback อย่างเดียว Revenue ไม่โต |
| EV/Sales | After-Tax Op Margin | Margin ที่ยั่งยืนของธุรกิจนี้คือเท่าไร? | EV/Sales สูง + Margin กำลังหด |
| EV/EBITDA | CapEx Intensity + ROIC | ต้อง CapEx เท่าไรในการรักษา EBITDA นั้น? | EV/EBITDA ต่ำ แต่ ROIC < WACC |
| P/B | Return on Equity (ROE) | ROE ยั่งยืนเกิน Cost of Equity ได้ไหม? | P/B < 1 + ROE ต่ำกว่า CoE อยู่แล้ว = Value Trap |
| PEG | Growth Quality | Growth Rate นี้สมจริงและเกิดซ้ำได้ไหม? | ใช้ Growth Spike 1 ปีเป็นตัวหาร |
| EV/FCF | FCF Growth + Reinvestment | ธุรกิจนี้ Asset-Light หรือ Capital-Heavy? | FCF พองเพราะตัด Maintenance CapEx |

---

## เรียก Engine — `companion` Mode

เรียก `checklist_engine.py` ผ่าน stdin JSON:

**CV-1 PEG:**
```json
{"mode": "companion", "multiple": "peg", "pe": 35, "eps_growth_5y": 35}
```

**CV-1 Justified P/E:**
```json
{"mode": "companion", "multiple": "pe", "payout": 0.3, "g": 0.08, "coe": 0.10, "actual_pe": 35}
```

**CV-2 Justified EV/Sales:**
```json
{"mode": "companion", "multiple": "ev_sales", "ebit": 32.7e9, "tax": 0.21, "revenue": 60.9e9, "reinv_rate": 0.05, "wacc": 0.09, "g": 0.05, "actual_ev_sales": 22}
```

**CV-3 EV/(EBITDA−MaintCapEx):**
```json
{"mode": "companion", "multiple": "ev_ebitda", "ebitda": 40e9, "maint_capex": 3e9, "ev": 600e9, "roic": 1.0, "wacc": 0.09}
```

**CV-4 Justified P/B:**
```json
{"mode": "companion", "multiple": "pb", "roe": 0.30, "g": 0.08, "coe": 0.10, "actual_pb": 11}
```

**CV-5 FCF Yield + Owner Earnings:**
```json
{"mode": "companion", "multiple": "fcf_yield", "fcff": 27e9, "ev": 1200e9, "ni": 29.8e9, "da": 3.4e9, "maint_capex": 2e9, "wc_change": 1e9}
```

---

> **เชิงการศึกษา — ไม่ใช่คำแนะนำลงทุนรายบุคคล / Educational, not personal investment advice**
> เรียบเรียงจาก **Earthh Evans · Invest Hub** — Ultimate Fundamental Stock Checklist 2025
> สูตรทุกตัว port ตรงเข้า `checklist_engine.py` — ตัวเลขที่ engine คำนวณ = ตัวเลขที่ได้จากสูตรนี้
