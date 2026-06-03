# Fundamental Checklist

เครื่องมือ **Fundamental Checklist — 15-Category Due Diligence** — ตรวจสุขภาพหุ้นอย่างครบถ้วนใน 15 มิติ: คำนวณ **Justified Multiple ครบ 6 ตัว** จาก Damodaran Companion Variables → Quick Screen 60 วิ → เดิน 15 หมวดพร้อม Red Flag system → สรุป **Scorecard: STRONG / REVIEW / AVOID**

> เรียบเรียงจาก **Earthh Evans · Invest Hub** — Ultimate Fundamental Stock Checklist 2025

## แนวคิด

> "ทุก Multiple คือ DCF ที่ถูกย่อรูปมา — P/E, EV/EBITDA, P/B ล้วนมี Companion Variables ซ่อนอยู่ ถ้ารู้ Variable นั้น ก็รู้ว่า Multiple ที่ 'ถูก' ควรเป็นเท่าไหร่"

**Damodaran Companion Variables** — ฐานรากของ Justified Multiple ทั้ง 6 ตัว:

| Multiple | Companion Variable หลัก |
|---|---|
| **Justified P/E** | Net Margin × (Payout Ratio / (WACC − g)) — ROE + g + WACC |
| **Justified EV/Sales** | Net Margin + Target Margin · WACC · g |
| **Justified EV/EBITDA** | (1−t) × (1 − Reinvestment Rate) / (WACC − g) |
| **Justified P/B** | (ROE − g) / (WACC − g) |
| **PEG Ratio** | P/E ÷ EPS Growth Rate (%) — fair ≈ 1.0 |
| **FCF Yield** | FCF / Market Cap — เปรียบเทียบ WACC / Bond Yield |

## Positioning เทียบ siblings

สี่ตัว **เสริมกัน ไม่ทับหน้าที่**:

| Plugin | โฟกัส | จุดเด่น |
|---|---|---|
| **fundamental-checklist** (ตัวนี้) | **Breadth** — Due diligence ครบ 15 มิติ | Quick Screen → Companion Variables 6 ตัว → 15 หมวด → Scorecard STRONG/REVIEW/AVOID |
| `deep-o-stock-analyst` | **Depth** — DEEP+O เจาะหุ้นเดี่ยว (US) | DEEP score 0–100, DCF intrinsic value, option-adjusted valuation, verdict ซื้อ/ถือ/ลด/ขาย |
| `reverse-dcf-screener` | **Expectation** — ถอดความคาดหวังที่ราคาฝัง | Market-Implied CAGR เทียบ Plausible CAGR → Gap → โซนราคา 4 ระดับ |
| `portfolio-risk-architect` | **Portfolio** — ความเสี่ยงพอร์ตรวม multi-asset | look-through, risk contribution, correlation, Monte Carlo, frontier |

> แนะนำใช้ **fundamental-checklist** เป็น gate filter ก่อน: ถ้า STRONG/REVIEW → ต่อด้วย `deep-o` (ขุดลึก) หรือ `reverse-dcf` (วัดความคาดหวัง) · ถ้า AVOID → ไม่ต้องเสียเวลา

## Setup

ไม่ต้อง `pip install` — **Python 3 stdlib only**

| ต้องมี | ใช้ทำอะไร |
|---|---|
| **Python 3** | รัน `checklist_engine.py` คำนวณ Justified Multiple + Scorecard logic (stdlib only — ไม่พึ่ง numpy/scipy/openpyxl) |
| **Web access** | agent ดึง 10-K / 10-Q / earnings + WACC จาก Damodaran (WebSearch / WebFetch) |

> ข้อแตกต่างสำคัญจาก `reverse-dcf-screener`: plugin นี้ **ไม่ต้อง** `pip install openpyxl` — engine วิ่งได้บน Python 3 ล้วนๆ ทุก IDE / Codex / Antigravity โดยไม่ต้องติดตั้งอะไรเพิ่ม

## Workflow 4 สเต็ป

```
1. /screen <TICKER>     Quick Screen 10 เกณฑ์ 60 วินาที → gate (STRONG/REVIEW/AVOID) + รายการ fail
                        รองรับข้อยกเว้น Banks + Infrastructure
       ↓
2. /companion <TICKER>  คำนวณ Justified Multiple ครบ 6 ตัว (P/E, EV/Sales, EV/EBITDA, P/B, PEG, FCF Yield)
                        → verdict ต่อ multiple: cheap/fair/expensive
       ↓
3. /business + /financials + /capital + /quality + /risk
                        เดิน 15 หมวดครบ (แยกตามกลุ่ม) → ติด Red Flag ไหน → นับ pass/fail
       ↓
4. (อยู่ใน /full)       Scorecard รวม: ผ่านกี่มิติ → STRONG / REVIEW / AVOID + 3 คำถามสุดท้าย
```

> หรือใช้ `/full <TICKER>` รวบทุกสเต็ปจบในคำสั่งเดียว

### อ่าน Scorecard

| Verdict | เกณฑ์ |
|---|---|
| **STRONG** | ผ่าน Critical Categories ทั้งหมด + ไม่มี hard Red Flag + pass ≥ 11/15 |
| **REVIEW** | ผ่าน Critical ทั้งหมด แต่ pass 8–10/15 หรือมี soft Red Flag บางตัว |
| **AVOID** | Fail Critical Category ใดก็ตาม หรือมี hard Red Flag |

**Critical Categories** (fail ตัวเดียว = AVOID ทันที): Business/Moat · Financial Strength · Earnings Quality

## Commands (10 ตัว)

| Command | กลุ่ม | ใช้เมื่อ |
|---|---|---|
| `/full <TICKER>` | Pipeline | เดิน pipeline ครบ: Quick Screen → Companion → 15 หมวด → Scorecard → 3 คำถามสุดท้าย (entry point หลัก) |
| `/screen <TICKER>` | Gate | Quick Screen 10 เกณฑ์ 60 วินาที → gate verdict + รายการ fail ก่อน Deep Dive |
| `/companion <TICKER>` | Valuation | คำนวณ Justified Multiple ครบ 6 ตัว จาก Damodaran Companion Variables |
| `/business <TICKER>` | หมวด 1–2 | Business Overview + Moat — Revenue Model, TAM, Recurring vs Cyclical, ROIC>WACC Moat Verification (Critical) |
| `/financials <TICKER>` | หมวด 3–5 | Financial Strength + Profitability + Growth Quality — Net Debt/EBITDA, FCF Conversion, ROIC vs WACC, Operating Leverage (Critical) |
| `/capital <TICKER>` | หมวด 6–7 | Capital Allocation + Valuation — Buyback Quality, M&A Track Record, Justified Multiple ครบ 6 ตัว (cross-ref deep-o + reverse-dcf) |
| `/quality <TICKER>` | หมวด 8–10 | Earnings Quality + Management Quality + Ownership Structure — FCF Conversion, Accrual Ratio, DSO, Insider Ownership (Critical) |
| `/risk <TICKER>` | หมวด 11–13 | Risk Assessment + Macro Alignment + Technical Context — Regulatory, Competitive Disruption, Balance Sheet Risk, Rate Cycle, MA50/200 |
| `/casestudy` | Case Study | ตัวอย่างจริง NVDA / META / PTON — เปรียบเทียบ Framework กับผลลัพธ์จริง บทเรียน Red Flag ก่อน Collapse |
| `/methodology` | อ้างอิง | อธิบายสูตร Companion Variable ครบ 6 ตัว + Scorecard Logic + ข้อยกเว้น FCF/Banks + 10 Closing Principles |

> **หมวด 14–15** (Insider Activity + Analyst/Market Sentiment) รวมอยู่ใน `/full` — ดูหลังสรุป 13 หมวดแรกแล้ว

## ตัวอย่าง Case Study

| หุ้น | Verdict | บทเรียนหลัก |
|---|---|---|
| **NVDA** | STRONG | Moat จาก CUDA ecosystem + AI TAM หมวด 1-2 STRONG · FCF Yield ต่ำแต่ Justified P/E ได้ support จาก margin expansion |
| **META** | REVIEW → BUY | Reality Labs ติด Red Flag (burn rate) แต่ Core Business STRONG · PEG < 1.0 ช่วงปี 2022 = undervalued ชัด |
| **PTON** | AVOID | Revenue Model cyclical สูง (ไม่ใช่ recurring) + ROIC < WACC + FCF ติดลบ → Moat และ Financial Strength fail พร้อมกัน |

## Installation

```
/plugin marketplace add mrunknown2/earthh-evans-finance-skill
/plugin install fundamental-checklist
```

> ใช้นอก Claude Code (Antigravity / Codex) ได้ด้วย — ดู [`INSTALL.md`](INSTALL.md)

## ตัวอย่างการใช้งาน

```
/fundamental-checklist:full NVDA
```

→ agent ดึงงบ NVDA → Quick Screen 10 เกณฑ์ → คำนวณ Justified Multiple 6 ตัว → เดิน 15 หมวด → สรุป Scorecard STRONG/REVIEW/AVOID + Red Flag ที่ติด + 3 คำถามสุดท้าย

## ⚠️ Disclaimer

เครื่องมือนี้เป็นกรอบวิเคราะห์ **เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล**

- **ตัวเลขทุกตัวต้อง verify เอง** — agent ดึงจากงบจริงแต่ผู้ใช้ต้องตรวจซ้ำกับ 10-K/10-Q/IR ล่าสุดก่อนตัดสินใจ
- **WACC เป็น placeholder** — ควรอัปเดตจาก Damodaran (ม.ค. ทุกปี) หรือใส่ override เอง
- **Justified Multiple อิง assumptions** — Net Margin เป้า, g, Payout Ratio ล้วนเป็นสมมติฐาน กระทบผลโดยตรง
- Scorecard (STRONG/REVIEW/AVOID) คือ **framework signal** จาก checklist 15 มิติ **ไม่ใช่คำสั่งซื้อขาย**
- พิจารณาบริบทภาษี/เป้าหมาย/ความเสี่ยงของตนเองก่อนทุกครั้ง — ผู้ใช้รับผิดชอบผลการลงทุนเองทั้งสิ้น
