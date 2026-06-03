---
description: "วิเคราะห์หมวด [11–13] Risk Assessment + Macro Alignment + Technical Context — Regulatory, Competitive Disruption, Balance Sheet Risk, Rate Cycle, MA50/MA200 Trend"
allowed-tools:
  - Read
  - Bash
  - WebSearch
  - WebFetch
model: opus
---

# /fundamental-checklist:risk

**Risk Assessment + Macro Alignment + Technical Context** — ตรวจความเสี่ยงรอบด้าน สภาพ Macro และ Price Action ตรงกับ Checklist หมวด [11–13]

## Input ที่ต้องการ

- **ticker หุ้น** + Sector
- ข้อมูล Balance Sheet: หนี้ที่ครบกำหนด 12–24 เดือน
- ข้อมูล Regulatory Environment ล่าสุด (WebSearch)
- Macro Conditions ปัจจุบัน: Fed Rate Stance, Dollar Index, Sector Tailwind/Headwind
- Technical Data: Price vs MA50/MA200, Volume Pattern, RSI

## สิ่งที่ทำ

### หมวด [11] Risk Assessment

| ประเภทความเสี่ยง | คำถามสำคัญ | Sector ที่กระทบ |
|----------------|-----------|--------------|
| Regulatory | กฎหมายที่กำลังจะออกคืออะไร? มีประวัติ Enforcement? | Big Tech, Healthcare, Finance |
| Competitive Disruption | ใครมี Incentive + Resource ทำลาย Business Model นี้? | Retail, Media, ทุก Sector |
| Customer Concentration | Top 3 ลูกค้า > 40% ของรายได้ไหม? | B2B Tech, กลาโหม, Specialty Mfg |
| Balance Sheet Risk | หนี้ครบกำหนดใน 12–24 เดือน ช่วงดอกเบี้ยสูง? | LBO, REITs, Airlines |
| Input Cost / Commodity | Margin รับได้ไหมถ้าต้นทุน Input พุ่ง? | อาหาร, พลังงาน, เคมี, Auto |
| Execution Risk | ประวัติ Miss Guidance? กำลัง Transformation ขนาดใหญ่? | บริษัทที่กำลัง Pivot |

- กำหนด verdict: `pass` / `caution` / `red`

### หมวด [12] Macro Alignment

| ปัจจัย Macro | ผลกระทบ | Asset ที่ได้ประโยชน์ |
|-------------|---------|-------------------|
| ดอกเบี้ยสูง/Policy เข้มงวด | Discount Rate สูง → Long-Duration ลำบาก | Value, Dividend, Banks |
| Rate Cut / Easing | Discount Rate ลด → Growth Re-rate | Tech, Growth, Real Estate |
| Dollar แข็ง | Headwind สำหรับ US Multinationals | บริษัทที่ขายในประเทศหลัก |
| AI Infrastructure Buildout | CapEx Cycle ขนาดใหญ่ | NVIDIA, Power Infra, Data Centers |
| Energy Transition | Secular Demand Shift | Renewables, Grid Storage, Copper |
| สังคมผู้สูงอายุ | Structural Growth Healthcare | Pharma, Medtech, Senior Housing |
| Supply Chain Reshoring | Manufacturing กลับมาอเมริกา | Industrials, Automation, Specialty Mfg |

- ประเมินว่า Sector นี้ Aligned กับ Macro ปัจจุบันหรือ Headwind?
- กำหนด verdict: `pass` / `caution` / `red`

### หมวด [13] Technical Context

> Technical ไม่กำหนด Intrinsic Value — ช่วยหาจังหวะ Entry เท่านั้น

- **MA50 / MA200** — หุ้นอยู่เหนือหรือต่ำกว่า? Fundamental ที่ดีหนักขึ้นถ้าอยู่เหนือ MA ทั้งสอง
- **Volume Pattern** — Breakout ด้วย Volume สูง = มีความเชื่อมั่น · Rally Volume ต่ำ = ต้องสงสัย
- **RSI Divergence** — ราคา New High แต่ RSI ไม่ = Momentum อ่อนแรง (Caution ไม่ใช่ Sell Signal)
- หลักสำคัญ: หุ้น Fundamental แข็งแต่อยู่ใน Downtrend = "เร็วเกินไป" ไม่ใช่ "ผิดพลาด"
- กำหนด verdict: `pass` / `caution` / `red`

## References ที่ใช้

- `references/checklist-15.md` หมวด [11], [12], [13] — Risk Matrix + Macro Table + Technical Principles

## ตัวอย่างสั่ง

```
/risk NVDA
/risk META
/risk T
```

## Discipline

ข้อมูลจริงก่อนเสมอ (WebSearch สำหรับ Regulatory + Macro ปัจจุบัน) · Technical เป็น Timing ไม่ใช่ Valuation อย่าให้ Technical override Fundamental · ระบุ as-of date + source ทุกตัวเลข · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
