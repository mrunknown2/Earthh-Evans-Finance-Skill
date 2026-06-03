# Fundamental Checklist ครบ 15 หมวด

> 15 หมวดครอบคลุมทุกมิติของการวิเคราะห์พื้นฐาน — แต่ละหมวดมี Benchmark, Cross-check และความแตกต่างตาม Sector
> ใช้คู่กับ `checklist_engine.py` mode `screen` (หมวด 14) และ mode `scorecard` (aggregate ทั้ง 15 หมวด)

---

## [1] ภาพรวมธุรกิจ (Business Overview)

เข้าใจก่อนว่าบริษัททำเงินได้อย่างไร ก่อนที่จะแตะตัวเลขใด ๆ — ความผิดพลาดในการลงทุนส่วนใหญ่เริ่มจากการข้ามขั้นตอนนี้ไป

### 1a. Core Business Model

- ธุรกิจเป็น **Recurring** (Subscription, Usage-based) หรือ **Cyclical** (One-time, Commodity-tied)?
  - Cross-check: Recurring Revenue → Gross Margin ควรคงที่หรือขยายตัวตลอด 3 ปีขึ้นไป
  - Cyclical → ต้องรู้ก่อนว่าตอนนี้อยู่จุดไหนของ Cycle ก่อนทำ Valuation

### 1b. โมเดลรายได้ (Revenue Model)

| ประเภท | ความเสถียร | Metric สำคัญ | ตัวอย่าง Sector |
|--------|-----------|-------------|----------------|
| Subscription / SaaS | สูงมาก | NRR > 110% | Salesforce, Adobe, ServiceNow |
| Usage-Based | สูง | Usage Growth + Cohort Retention | Snowflake, AWS, Twilio |
| Transaction / Payments | Medium-High | TPV Growth + Take Rate | Visa, PayPal, Block |
| One-Time / Hardware | ต่ำ | Repeat Customer Rate, ASP Trend | Apple Hardware, PC |
| Contract (Backlog) | ปานกลาง | Backlog Size + Book-to-Bill | กลาโหม, ก่อสร้าง |
| Commodity / Cyclical | ต่ำ | Cycle Position, Balance Sheet | พลังงาน, เหล็ก, Airlines |

### 1c. TAM / SAM / SOM

- Growth Stock ต้องการ TAM ใหญ่พอที่จะ Support Thesis 10 ปี
- ถ้าบริษัทมี Market Share > 30% แล้ว การโตต้องต่อมาจาก Pricing Power หรือ Adjacent Market
- **Red Flag:** อ้าง TAM ใหญ่มากแต่ไม่อธิบายว่าจะ Capture ได้อย่างไร

---

## [2] ความสามารถในการแข่งขัน (Moat)

Moat มีอยู่จริงก็ต่อเมื่อ ROIC สูงกว่า WACC ได้อย่างต่อเนื่องตลอด Business Cycle — นี่คือวิธีที่ Damodaran ให้ Operationalize ความคิดของ Buffett ออกมาเป็นตัวเลข

| ประเภท Moat | กลไก | วิธีตรวจสอบ | Sector |
|-------------|------|------------|--------|
| Network Effect | มูลค่าเพิ่มขึ้นตามผู้ใช้ | DAU/MAU Growth, Engagement | Meta, Visa, Airbnb |
| Switching Cost | ออกจากระบบแพงหรือเจ็บปวด | Gross Retention >90%, NRR>100% | Enterprise Software |
| Cost Advantage | ต้นทุนต่ำกว่าคู่แข่งเชิงโครงสร้าง | Gross Margin สูงกว่า Peer ในราคาเดิม | Amazon AWS, Costco |
| Brand / Intangible | ตั้งราคาแพงกว่าได้ | Gross Margin Premium vs Category | Apple, LVMH, Nike |
| Efficient Scale | ตลาดเล็กไปสำหรับผู้เล่นคนที่ 2 | Local Monopoly Dynamics | Regulated Utilities |
| IP / Patent | การผูกขาดเชิงกฎหมาย | Patent Cliff Analysis, Pipeline | Pharma, Biotech, Semi |

### Moat Verification Test (วิธีของ Damodaran)

```
ROIC > WACC ต่อเนื่อง 5 ปีขึ้นไป = พิสูจน์ Moat แล้ว
ถ้า ROIC > WACC แค่ 1–2 ปี = อาจเป็น Cyclical Benefit ไม่ใช่ Structural Advantage
Incremental ROIC > Average ROIC = Moat กำลังขยาย ไม่ใช่แค่ตัวตาม
Gross Margin คงที่หรือขยายตัวช่วงเงินเฟ้อ = Pricing Power พิสูจน์ตัวเองแล้วภายใต้ Stress
```

> **CRITICAL:** Moat เป็นหนึ่งใน 3 หมวด Critical — ถ้า verdict = red → AVOID ทันที

---

## [3] ความแข็งแกร่งทางการเงิน (Financial Strength)

### 3a. การวิเคราะห์หนี้สิน — ใช้ Net Debt/EBITDA แทน D/E เป็นหลัก

| Net Debt / EBITDA | ประเมิน | สิ่งที่ต้องทำ |
|-------------------|---------|--------------|
| ติดลบ (Net Cash) | งบดุลแข็งแกร่งที่สุด | Premium Valuation มีสิทธิ์รับ |
| < 1.5x | ปลอดภัย | ดำเนินการปกติ |
| 1.5x – 2.5x | รับได้ | ติดตามถ้า Rate สูงขึ้น |
| 2.5x – 3.5x | เริ่มสูง | Stress Test กับ Scenario Rate สูง |
| > 3.5x | ความเสี่ยงสูง | ต้องการ FCF แข็งแกร่งมากในการ Service หนี้ |

### 3b. Interest Coverage Ratio = EBIT / Interest Expense

- > 5x: ปลอดภัยมาก
- 3–5x: รับได้
- 1.5–3x: ดึงดูด — อ่อนไหวต่อ Earnings ที่ลดลง
- < 1.5x ในช่วงดอกเบี้ยสูง: เสี่ยง Distress

### 3c. คุณภาพ Free Cash Flow

```
Cash Conversion = Operating Cash Flow / Net Income   (NI กลายเป็น operating cash จริงไหม)
> 100%: คุณภาพสูง (Cash จริงเกินกว่า Earnings รายงาน)
80–100%: ปกติ
< 70% ต่อเนื่อง: ต้องสอบสวน

FCF Conversion = Free Cash Flow / Net Income   (NI เหลือเป็น free cash หลังหัก CapEx)
= engine key `fcf_conversion` (screen หมวด [14]) — ใช้ FCF/NI ไม่ใช่ OCF/NI
ธุรกิจ CapEx หนัก (AI / Infrastructure buildout) → FCF Conversion ต่ำชั่วคราว ไม่ใช่ Red Flag → ใช้ `fcf_exempt=true`
```

> **อย่าสับสน 2 ตัวนี้:** `Cash Conversion` (OCF/NI · มักเกิน 100%) วัด earnings→operating cash · `FCF Conversion` (FCF/NI · ต่ำกว่าเพราะหัก CapEx) คือเกณฑ์ที่ engine ใช้จริง

| Sector | FCF Margin ที่คาดหวัง | หมายเหตุ |
|--------|----------------------|---------|
| Mature SaaS / Software | 20–35% | Asset-Light; FCF Margin สูงคือปกติ |
| Consumer Technology | 15–25% | Apple ทำได้ ~28% FCF Margin มาโดยตลอด |
| Semiconductor (Fabless) | 20–35% | NVIDIA >50% ใน FY2024 — Exceptional |
| Industrial / Manufacturing | 5–12% | รับได้สำหรับโมเดล CapEx-Heavy |
| Telecom / Utilities | 5–15% | Revenue สูง แต่ CapEx ดึงกลับ |
| E-Commerce / Retail | 2–8% | Margin ต่ำ; Scale คืออดตัวช่วยเดียว |

> **CRITICAL:** Financial Strength เป็นหนึ่งใน 3 หมวด Critical — ถ้า verdict = red → AVOID ทันที

---

## [4] ประสิทธิภาพการดำเนินงาน (Profitability)

### 4a. Gross Margin — บ่งบอก Pricing Power

- Trend ของ Gross Margin สำคัญกว่าระดับ ณ ปัจจุบัน
- GM ขยายตัวช่วงเงินเฟ้อ = พิสูจน์ Pricing Power แล้วภายใต้ Stress จริง
- GM หดตัวแล้วผู้บริหารบอกว่า "ชั่วคราว" = Red Flag จนกว่าจะพิสูจน์ได้

| Sector | GM Benchmark | สิ่งที่ขับเคลื่อน |
|--------|-------------|-----------------|
| SaaS / Software | > 70% | Variable Cost แทบไม่มี รายได้ส่วนเพิ่มเป็นกำไรทั้งหมด |
| Semiconductor Fabless | 55–70% | Product Mix + ASP Trend; NVIDIA 72%+ คือ Elite |
| Consumer Electronics | 35–45% | Apple 45%+ คือ Exceptional สำหรับ Hardware |
| Retail | 25–40% | ขึ้นกับ Private Label Mix และ Buying Power |
| Automotive | 15–25% | COGS สูงมาก; EV Transition กดดัน Margin ระยะสั้น |

### 4b. ROIC vs WACC — Metric เดียวที่สำคัญที่สุด

```
ROIC = NOPAT / Invested Capital
NOPAT = EBIT × (1 − Tax Rate)
Invested Capital = Total Equity + Total Debt − Excess Cash
เปรียบเทียบกับ WACC (ต้นทุนเงินทุนถ่วงน้ำหนัก)
```

> **ข้อควรระวัง:** Invested Capital ไม่ได้ Standard เสมอ
> - บริษัทที่มี Operating Lease หนัก (Airlines, Retail): ควรรวม Capitalized Lease Obligation เข้าใน Invested Capital
> - บริษัทที่มี SBC สูง: ควร Add Back SBC เป็นส่วนหนึ่งของต้นทุนจริง ทำให้ NOPAT และ ROIC จะดูดีเกินจริง
> - บริษัทที่มี M&A และ Goodwill หนัก: ROIC โดยไม่รวม Goodwill vs ROIC รวม Goodwill ต่างกันมาก

### Incremental ROIC vs Average ROIC — ความแตกต่างที่สำคัญ

- **Average ROIC** = ผลงานในอดีตบน Capital Base ทั้งหมด
- **Incremental ROIC** = ผลตอบแทนของเงินลงทุนใหม่ที่เพิ่งใส่ไป

บริษัทที่มี Average ROIC = 25% แต่ Incremental ROIC = 8% (ต่ำกว่า WACC) = กำลัง Compound ข้อได้เปรียบเก่า ขณะที่ทำลายมูลค่าบนการลงทุนใหม่ทุกบาท

> Incremental ROIC ลดลงเรื่อย ๆ = Moat กำลังหดตัว — นี่คือ Early Warning Signal ที่สำคัญที่สุด

---

## [5] คุณภาพการเติบโต (Growth Quality)

### 5a. Growth Test 3 มิติ

| มิติ | สิ่งที่ต้องตรวจ | Red Flag |
|------|----------------|---------|
| Revenue Growth | CAGR ต่อเนื่อง 3–5 ปี | ผลประโยชน์ชั่วคราวถูก Price In เป็น Secular Growth |
| EPS Growth | ขับเคลื่อนโดย Operations หรือ Buyback? | EPS โต Revenue แบน = Financial Engineering |
| FCF Growth | ต้องยืนยัน EPS Growth ว่าเป็น Cash จริง | FCF แบนขณะ EPS โต = Accruals กำลังสะสม |

### 5b. Operating Leverage Test

พิสูจน์ Scalability จริงของธุรกิจ: Revenue โตเร็วกว่า Cost

```
Degree of Operating Leverage (DOL) = % Change in Operating Income / % Change in Revenue
> 1.5 = Leverage ดี
> 2.0 = ยอดเยี่ยม
< 1.0 = Cost โตเร็วกว่า Revenue (คำเตือน)
```

- ตัวอย่างที่ดี: Meta 2023 — Revenue +16%, Operating Income +62% (DOL = 3.9)
- ตัวอย่างที่แย่: Peloton 2022 — Revenue ลด Operating Loss ลึกขึ้น (Negative Leverage)

---

## [6] การจัดสรรเงินทุน (Capital Allocation)

นี่คือหมวดที่นักลงทุนส่วนใหญ่ข้ามไป และเป็นจุดที่มีโอกาส Alpha ได้มากที่สุด — ธุรกิจดีที่ถูกบริหารเงินทุนแย่ก็ Underperform ได้เหมือนกัน

### Capital Allocation Hierarchy ของ Damodaran

| ลำดับ | การกระทำ | เมื่อไรถึงเหมาะ | มูลค่าถูกสร้างเมื่อ... |
|-------|---------|----------------|----------------------|
| 1 | Reinvest ใน Core Business | Incremental ROIC > WACC | ทุกบาทที่ลงทุนสร้าง Return เกิน Cost |
| 2 | Strategic M&A | Synergy ชัดเจน ราคาไม่แพงเกิน | ROIC หลัง Deal ดีขึ้นใน 2–3 ปี |
| 3 | Share Buyback | หุ้นต่ำกว่า Intrinsic Value จริง ๆ | ซื้อคืนถูก = เพิ่ม Value per Share |
| 4 | Dividend | ไม่มี High-ROIC Project เหลือ | คืนเงินให้ผู้ถือหุ้นอย่างมีประสิทธิภาพ |

### 6a. Buyback Quality Test

- **Buyback ดี:** ผู้บริหารซื้อคืนตอนหุ้นต่ำกว่า Intrinsic Value ที่คำนวณจาก FCF
- **Buyback แย่:** ซื้อคืนตอน Peak เพื่อ Offset Dilution จาก Stock Option Grant
- **Test:** ดูประวัติ 5 ปี — Share Count ลดลงมีนัยสำคัญไหม? Timing ใกล้ Low ไหม?
- **Cross-check:** Buyback หนักแต่ ROIC ลดลง = ควรใช้เงินนั้นลงทุนใน Growth ดีกว่า

### 6b. M&A Track Record

- Review ทุก Acquisition สำคัญใน 5–7 ปีที่ผ่านมา
- ROIC ดีขึ้นหรือลงหลัง Acquisition ใน 3 ปี?
- Goodwill คิดเป็น % เท่าไรของ Total Assets? ถ้า > 40% = ซื้อแพงต่อเนื่อง
- Classic Red Flag: Serial Acquirer ที่ Organic Revenue Growth หยุดโต = ซื้อ Growth มาซ่อน Stagnation

### 6c. CapEx Decomposition

```
True Owner Earnings = Net Income + D&A − Maintenance CapEx − Working Capital Changes
Maintenance CapEx ≈ Depreciation สำหรับ Asset-Light
               อาจ 2–3x D&A สำหรับ Heavy Infrastructure
```

---

## [7] Valuation — ใช้ Companion Variables ประกอบ

หมวดนี้นำ Companion Variable Framework จากส่วนที่ 1 มาใช้งานจริง — ทุก Multiple ต้องอ่านคู่กับตัวขับเคลื่อนของมัน

### 7a. Reverse DCF — เครื่องมือ Valuation ที่ซื่อสัตย์ที่สุด

แทนที่จะสร้าง DCF เพื่อหา Target Price ให้ถามก่อนว่า "ตลาดกำลัง Price In Growth Rate เท่าไร?"

- เอา Price ปัจจุบัน → Back-solve หา Growth Rate และ Margin Assumption ที่ Embedded อยู่
- ถ้าตลาด Imply Revenue Growth 30% ต่อปี 10 ปี → ถามว่า "ใครในอุตสาหกรรมนี้ทำได้จริงบ้าง?"
- ถ้า Implied Assumption ดูเกินจริง → หุ้นถูก Priced for Perfection → Downside Risk สูง
- ถ้า Implied Assumption ดูมองโลกแง่ร้ายเกินไปเมื่อเทียบ Fundamental → อาจมี Margin of Safety

> **Cross-ref:** สำหรับมูลค่าที่แท้จริง (Intrinsic Value) ใช้ plugin **`deep-o-stock-analyst`**
> สำหรับ Implied CAGR ที่ตลาดต้องการ ณ ราคาปัจจุบัน ใช้ plugin **`reverse-dcf-screener`**

### 7b. ตาราง Valuation Summary พร้อม Companion Variables

| Multiple | สูตร | Companion Variable | Rule of Thumb |
|----------|------|--------------------|---------------|
| P/E (Forward) | Price / FY+1 EPS | EPS Growth Rate (5Y CAGR) | PEG < 1 = Undervalued เทียบกับ Growth |
| EV/Sales | EV / Revenue | After-Tax Operating Margin | Justified = Margin × (1−RR) / (WACC−g) |
| EV/EBITDA | EV / EBITDA | CapEx/Revenue + ROIC | ปรับเป็น EV/EBIT สำหรับ CapEx-Heavy |
| P/B | Price / Book Value | ROE vs Cost of Equity | Justified P/B = (ROE−g) / (CoE−g) |
| PEG | P/E / Growth% | Growth Quality & Sustainability | PEG < 1 ถ้า Growth จริงและเกิดซ้ำได้ |
| FCF Yield | FCF / Enterprise Value | FCF Growth + Capital Intensity | > Yield พันธบัตร 10 ปี = Equity Premium มี |

---

## [8] คุณภาพกำไร (Earnings Quality)

### 8a. Three Quality Tests

| Test | Metric | ช่วง Healthy | สัญญาณเตือน |
|------|--------|-------------|------------|
| FCF Conversion | FCF / Net Income | 80–110% | < 70% ต่อเนื่อง 2 ปี → ส่อสวม Accruals |
| Accrual Ratio | (Net Income − FCF) / Avg Assets | ใกล้ 0 หรือติดลบ | เพิ่มขึ้นเรื่อย ๆ → Earnings ฝัง Accounting มากขึ้น |
| Revenue Quality | DSO Trend | คงที่หรือลดลง | DSO ขยาย + Revenue โต = อาจ Channel Stuffing |
| Recurring Mix | % Recurring / Total Revenue | > 60% สำหรับ Tech | Recurring % ลด = กำลังเปลี่ยนเป็น One-Time |
| Customer Concentration | Top 3 / Revenue | < 30% | > 40% = ลูกค้าออก 1 ราย = Risk Event |

### DSO ที่เพิ่มขึ้นไม่ได้แปลว่า "ไม่ดีเสมอ"

ต้องระวัง Sector ที่ DSO Noisy โดยธรรมชาติ (Usage-Based Marketplace, บริษัทที่ Shift Revenue Recognition Policy, Enterprise Software ที่ขายเป็นรายใหญ่)

### 8b. Red Flag ที่ควรระวัง

- Net Income โต YoY แต่ Operating Cash Flow แบนหรือลด
- Accounts Receivable โตเร็วกว่า Revenue มาก (อาจ Recognize รายได้เร็วเกิน)
- Revenue Spike ปลายไตรมาส + Inventory Build ที่ Distributor = Channel Stuffing
- Goodwill Impairment: ผู้บริหารประเมิน Acquisition ผิดพลาด — ขนาดใหญ่แค่ไหนและบ่อยแค่ไหน?

> **CRITICAL:** Earnings Quality เป็นหนึ่งใน 3 หมวด Critical — ถ้า verdict = red → AVOID ทันที

---

## [9] คุณภาพผู้บริหาร (Management Quality)

| หัวข้อ | สิ่งที่ประเมิน | แหล่งข้อมูล |
|--------|--------------|------------|
| Skin in the Game | % Insider Ownership + Trend | SEC Form 4, Proxy Statement |
| Capital Allocation Track Record | ผลลัพธ์ M&A, Buyback Timing, Dividend Sustainability | 10-K, Investor Presentations |
| Guidance Credibility | ประวัติ Beat/Miss vs Guidance ตัวเอง | Earnings Transcripts |
| Communication Quality | พูดถึงความเสี่ยงตรงไหม? ยอมรับข้อผิดพลาดไหม? | Earnings Calls, Shareholder Letter |
| Compensation Alignment | Incentive ผูกกับ ROIC/FCF หรือแค่ EPS/Revenue? | Proxy DEF 14A |

---

## [10] โครงสร้างผู้ถือหุ้น (Ownership Structure)

| สัญญาณ | อ่านเป็นบวก | อ่านเป็นลบ |
|--------|------------|-----------|
| Insider Ownership | > 10% และคงที่หรือเพิ่มขึ้น | สูงแต่ขายออกต่อเนื่องหลัง Lockup |
| Institutional Quality | Long-only Value Fund เป็น Top Holder | ส่วนใหญ่เป็น Short-term Momentum Fund |
| Insider Transaction | Open-market Buy ช่วงตลาดปรับฐาน | ขายเร็งขึ้นเมื่อราคาพุง |
| Float Size | Float เพียงพอสำหรับ Liquidity | Float น้อยมาก + Short Interest สูง = Squeeze Dynamics |

แหล่งข้อมูลฟรี: Yahoo Finance แท็บ "Holders" | Finviz | Dataroma (Superinvestors) | Whalewisdom / Fintel (13F Filings)

---

## [11] การประเมินความเสี่ยง (Risk Assessment)

| ประเภทความเสี่ยง | คำถามสำคัญ | Sector ที่กระทบมากที่สุด |
|----------------|-----------|----------------------|
| Regulatory | กฎหมายที่ออกจะ ประวัติธุรกิจ Enforce? | Big Tech, Healthcare, Finance |
| Competitive Disruption | ใครมี Incentive และ Resource ในการทำลาย Business Model นี้? | ทุก Sector โดยเฉพาะ Retail, Media |
| Customer Concentration | Top 3 ลูกค้าคิดเป็น > 40% ของรายได้ไหม? | B2B Tech, กลาโหม, Specialty Mfg |
| Balance Sheet | หนี้ครบกำหนดใน 12–24 เดือน ในช่วงดอกเบี้ยสูง? | LBO, REITs, Airlines |
| Input Cost / Commodity | Margin รับได้ไหมถ้าต้นทุน Input พุ่ง? | อาหาร, พลังงาน, เคมี, Auto |
| Execution Risk | ประวัติ Miss Guidance? กำลัง Transformation ขนาดใหญ่? | บริษัทที่กำลัง Pivot สำคัญ |

---

## [12] Macro Alignment

| ปัจจัย Macro | ผลกระทบ | Asset Class ที่ได้ประโยชน์ |
|-------------|---------|--------------------------|
| ดอกเบี้ยสูง / Policy เข้มงวด | Discount Rate สูง → Long-Duration Asset เสียเปรียบ | Value, Dividend, Banks |
| Rate Cut / Easing | Discount Rate ลด → Growth Re-rate | Tech, Growth, Real Estate |
| Dollar แข็ง | Headwind สำหรับ US Multinationals | บริษัทที่ขายในประเทศเป็นหลัก |
| AI Infrastructure Buildout | CapEx Cycle ขนาดใหญ่กำลังดำเนินอยู่ | NVIDIA, Power Infra, Data Centers |
| Energy Transition | Secular Demand Shift | Renewables, Grid Storage, Copper |
| สังคมผู้สูงอายุ | Structural Growth ด้าน Healthcare | Pharma, Medtech, Senior Housing |
| Supply Chain Reshoring | Manufacturing กลับมาอเมริกา | Industrials, Automation, Specialty Mfg |

---

## [13] มุมเทคนิค (Technical Context)

Technical Analysis ไม่ได้กำหนด Intrinsic Value — แต่ช่วยหาจังหวะ Entry ว่า Price Action ของตลาดยืนยันหรือขัดแย้งกับ Fundamental Thesis

- **MA50 / MA200:** ยืนยัน Trend — สัญญาณ Buy จาก Fundamental มีน้ำหนักมากกว่าถ้าอยู่เหนือ MA ทั้งสอง
- **Volume:** Breakout ด้วย Volume สูง = มีความเชื่อมั่น · Rally ด้วย Volume ต่ำ = ต้องสงสัย
- **RSI Divergence:** ราคา New High แต่ RSI ไม่ = Momentum เริ่มอ่อนแรง (ไม่ใช่ Sell Signal แต่เป็น Caution)
- **หลักสำคัญ:** หุ้น Fundamental แข็งแกร่งแต่อยู่ใน Downtrend คือ "เร็วเกินไป" ไม่ใช่ "ผิดพลาด"

---

## [14] Quick Checklist — Screen 60 วินาที

> รัน Screen นี้ก่อน Deep Dive เฉพาะหุ้นที่ผ่านส่วนใหญ่
> **maps ตรงกับ engine mode `screen`** — `checklist_engine.py` → `screen(criteria, is_financial, fcf_exempt)`

| เกณฑ์ | Threshold | ทดสอบอะไร | engine key |
|-------|----------|----------|-----------|
| ROIC vs WACC | ROIC > WACC ต่อเนื่อง 3 ปีขึ้นไป | Core Value Creation Test | `roic_gt_wacc_3y` |
| FCF Conversion (*) | FCF / Net Income > 80% | Earnings Quality Gate | `fcf_conversion` |
| Net Debt / EBITDA (**) | < 2.5x (หรือ Net Cash) | Balance Sheet Stability | `net_debt_ebitda` |
| Gross Margin Trend | คงตัวหรือขยายตัว 3 ปี | Pricing Power Confirmation | `gross_margin_stable_3y` |
| Revenue Growth Quality | Recurring % เพิ่ม, DSO คงที่ | Revenue Durability | `revenue_quality` |
| EV/Sales vs Margin | EV/Sales ถูก Justify โดย After-Tax Op Margin | Valuation Sanity Check | `ev_sales_justified` |
| PEG Ratio | < 1.5 บน Sustainable Growth ไม่ใช่ EPS จาก Buyback | Growth-Adjusted Valuation | `peg` |
| Insider Signal | ไม่มีการขายอย่างต่อเนื่องใน Open Market | Management Confidence | `insider_no_selling` |
| Macro Alignment | ธุรกิจได้ประโยชน์จาก Macro ปัจจุบัน | Timing / Tailwind Check | `macro_aligned` |
| Capital Allocation | Buyback ใน Low, M&A เพิ่ม ROIC | Management Quality Gate | `capital_allocation_ok` |

**(*) ข้อยกเว้น FCF Conversion:** ธุรกิจที่กำลังลงทุนหนักช่วง Infrastructure Buildout — FCF Conversion ต่ำชั่วคราว "ไม่ใช่ Red Flag" ถ้า Growth CapEx คือสาเหตุและ Incremental ROIC ในอนาคตสูง → ใช้ `fcf_exempt=true` ใน engine

**(**) ข้อยกเว้น Net Debt/EBITDA:** ธุรกิจการเงิน (Banks, Insurers, Financial Holding) — Metric ชุด Net Debt/EBITDA ไม่เหมาะ ใช้ ROE, P/B, NIM, CET1 Ratio แทน → ใช้ `is_financial=true` ใน engine

**Gate Verdict:** 0 fail = strong | 1–2 fail = review | 3+ fail = avoid

---

## [15] 3 คำถามสุดท้ายก่อนกดซื้อ

| คำถาม | ถ้าใช่ | ถ้าไม่ |
|-------|--------|--------|
| "ธุรกิจนี้จะใหญ่กว่าและทำกำไรได้มากกว่าใน 5–10 ปี?" | วิเคราะห์ต่อ | หยุด — ไม่มี Thesis |
| "ถ้าหุ้นตก 30% เราจะซื้อเพิ่มไหม?" | ความเชื่อมั่นผ่าน | Position ใหญ่เกินไป ลด Size |
| "บอกได้ชัดเจนไหมว่าทำไมตลาดถึง Misprice ตรงนี้?" | มี Edge แล้ว | รอก่อน — ยังไม่มี Variant View ที่ชัด |

---

## หมวด Critical — Red = AVOID ทันที

3 หมวดต่อไปนี้คือ `CRITICAL_CATEGORIES` ใน engine:

```python
CRITICAL_CATEGORIES = {"Moat", "Financial Strength", "Earnings Quality"}
```

ถ้าหมวดใดหมวดหนึ่งใน 3 หมวดนี้ได้ verdict = "red" → `overall_read = "AVOID"` โดยทันที ไม่ว่าหมวดอื่นจะ pass ดีแค่ไหน

---

> **เชิงการศึกษา — ไม่ใช่คำแนะนำลงทุนรายบุคคล / Educational, not personal investment advice**
> เรียบเรียงจาก **Earthh Evans · Invest Hub** — Ultimate Fundamental Stock Checklist 2025
