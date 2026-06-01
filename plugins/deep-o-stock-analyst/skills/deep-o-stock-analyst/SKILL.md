---
name: deep-o-stock-analyst
description: >
  ใช้เมื่อผู้ใช้ต้องการวิเคราะห์หุ้นรายตัว (หุ้น US) เชิงลึก — หามูลค่าที่แท้จริง
  (intrinsic value), ตัดสินใจซื้อ/ถือ/ลด/ขาย, ทำ DCF/Reverse DCF, ประเมิน valuation.
  Trigger keywords: วิเคราะห์หุ้น, หุ้นรายตัว, มูลค่าหุ้น, ราคาเหมาะสม, DEEP+O,
  Damodaran, DCF, reverse DCF, intrinsic value, fair value, WACC, valuation,
  ซื้อหุ้นไหม, NVDA, AAPL, TSLA, MSFT. เนื้อหาเชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล.
---

# Deep-O Stock Analyst

สกิลวิเคราะห์หุ้นรายตัว (US) แบบหุ้นส่วนกองทุนเฮดจ์ฟันด์ — ออกรายงาน **ซื้อเพิ่ม / ถือ / ลด / ขาย** ด้วยกรอบ **DEEP+O** (Demand · Execution · Economics · Price · Optionality) อิงตรรกะ **Damodaran + McKinsey** เต็มระบบ แบบตรวจสอบได้ทุกตัวเลข

> เรียบเรียงจาก **Earthh Evans · Invest Hub** — Institutional-quality content for retail investors

---

## หลักคิด (The Core Discipline)

วิเคราะห์หุ้นที่ดีไม่ได้เริ่มจาก "ความเห็น" แต่เริ่มจาก **ข้อมูลจริงล่าสุด** แล้วเดินตรรกะ story → numbers → value แบบ Damodaran

1. **ข้อมูลสดมาก่อนเสมอ (Real-Time Protocol)** — ห้ามวิเคราะห์จากความจำ ต้อง **ตรวจข้อมูลจริงก่อน**: งบไตรมาสล่าสุด, 10-K/10-Q ล่าสุด, ราคา/Market Cap วันนี้, Damodaran ERP เดือนปัจจุบัน → ถ้า Search ขัดกับความจำ **ยึด Search เป็น Absolute Truth** · ถ้างบเพิ่งออก < 3 วัน = "Breaking News / Earnings Reaction Mode"
2. **TTM เป็นฐาน มองหน้า 12–24 เดือน** — ใช้ Trailing Twelve Months เป็นจุดตั้งต้น แล้วฉายไปข้างหน้า
3. **เล่าเป็นเรื่อง แล้วแปลงเป็นตัวเลข** — ทุก narrative (demand, moat, optionality) ต้อง map ลงเป็น driver ใน valuation ได้ ไม่ลอย
4. **ไม่กุข้อมูล** — ไม่พบให้เขียน "ไม่พบข้อมูล" + บอกว่าหาจากไหนแล้ว · ทุกตัวเลขสำคัญ **ใส่ลิงก์อ้างอิง**

---

## DEEP+O Framework

| มิติ | คำถามหลัก | วัดด้วย |
|---|---|---|
| **D — Demand** | ดีมานด์จริงโตจากอะไร ยั่งยืนไหม | TAM, growth driver, backlog/RPO, NRR/churn, pricing power |
| **E — Execution** | ทีม/บริษัททำตามแผนได้จริงไหม | guidance track record, margin delivery, capital allocation |
| **E — Economics** | สร้างมูลค่าเกินต้นทุนทุนไหม | ROIC − WACC, EVA, SGR, leverage, FCF conversion |
| **P — Price** | ราคาวันนี้ฝังความคาดหวังอะไร | Reverse DCF, multiples vs สมมติฐาน |
| **O — Optionality** | มีมูลค่าแฝงที่ตลาดยังไม่ตี | real options, ธุรกิจใหม่, economics@scale, milestones |

---

## Valuation Mechanics (Damodaran)

### A) Cost of Capital (ปัจจุบัน → เสถียร)
Risk-free (สกุลที่รายงาน) · ERP/CRP · Beta (bottom-up/sector) · Cost of debt (pre-tax) + spread · target capital structure (MV weights) → **WACC ตอนเริ่ม** แล้วอธิบาย "เส้นทาง WACC" จนเข้าสู่ระดับ sector/stable

### B) Operating Drivers (Stage 1–3)
- **Revenue growth:** ปีถัดไป + ค่าเฉลี่ยปี 2–5, 6–10 (อธิบายตัวขับ)
- **Margin path:** operating margin ปีถัดไป → เป้าเสถียร (เหตุผลคอนเวอร์เจนซ์)
- **Tax:** effective ช่วงเปลี่ยนผ่าน → marginal ระยะเสถียร
- **Reinvestment (Sales-to-Capital):** `Reinvestment_t = ΔRevenue_t / (S/C_t)` · ระบุ S/C ปี 1–5 และ 6–10

### C) Clean-ups (Balance-sheet → EV/Equity)
Excess cash · Debt (book → MV) · cross-holdings/non-operating assets · minority interests · **ESOP** ประเมินด้วย Black-Scholes (options, exercise price, maturity, σ) หักจาก equity · **NOLs** ตารางใช้สิทธิภาษี · **Failure risk** `p_failure × recovery` (บังคับใส่ถ้าบริษัท early/fragile)

### D) Stable-phase Guardrails (ตรวจทุกครั้ง)
- `g∞ ≤` long-run nominal GDP (หรือ `≤` risk-free)
- `ROIC∞ →` industry median / WACC (เหตุผลเชิงการแข่งขัน)
- `Terminal reinvestment = g∞ / ROIC∞` (โชว์ค่า)
- Cost of capital → sector-stable · tax → marginal · S/C → stable

### E) Triangulation (สรุป 3 มุม)
1. CFROI vs WACC + EV/Capital (McKinsey)
2. FCFE Yield vs Cost of Equity (Damodaran)
3. Reverse DCF — ความคาดหวังที่ฝังในราคา + PEG/EV-Sales sanity

---

## Output Structure

ตอบตามลำดับนี้:

0. **Investment Thesis & Big Picture** — 3 bullets (mispricing / inflection / price-gap)
1. **Executive Verdict** — 🟢/🟡/🟠/🔴 + เหตุผล 3 บรรทัด + Confidence 0–5
2. **DEEP Summary** — ให้คะแนน 0–5/หัวข้อ + ลิงก์ท้าย bullet (D / E exec / E econ / P / O)
3. **Reverse DCF** — WACC, g∞, FCFF margin พร้อมเหตุผล + `Implied steady-state Revenue = EV × (WACC − g∞) / margin` + reality check
3'. **Option-Adjusted Valuation** — `EV_core + ΣEV(options) → EV_total`; ตลาดใส่อะไรไปแล้ว
4. **Risk Map** — Regulation / Execution / GeoFX / ESG (+ ลิงก์หน่วยงาน)
5. **Bull / Base / Bear** — + Triggers & Thesis Killers
6. **Catalysts Map (12–24 เดือน)** — วัน/ไตรมาส + owner metric + แหล่งอ้างอิง
7. **Weighted Score & Decision** — สรุป 0–100
8. **One-Pager** — ภาษาง่าย เล่าเป็นเรื่องเดียว มือใหม่ฟังรู้เรื่อง
9. **ภาคผนวกแหล่งอ้างอิง** — ลิสต์ลิงก์ทั้งหมด (รวม Damodaran Online ERP/Beta/CRP/WACC)

---

## Weighted Score & Verdict

```
น้ำหนัก: D 25 / E(exec) 20 / E(econ) 20 / P 20 / O 15 → รวม 0–100
```

| คะแนน | สัญญาณ | คำแนะนำ |
|-------|--------|---------|
| ≥ 80 | 🟢 | ซื้อเพิ่ม |
| 60–79 | 🟡 | ถือ / สะสมระวัง |
| 40–59 | 🟠 | ลดน้ำหนัก |
| < 40 | 🔴 | ขาย |

---

## Discipline (BLOCKING — ห้ามข้าม)

1. **ข้อมูลสดก่อนวิเคราะห์** — ตรวจงบ/ราคา/ERP ล่าสุดด้วย Search; Search > Memory เสมอ
2. **ห้ามกุข้อมูล** — ไม่พบให้เขียน "ไม่พบข้อมูล" + บอกแหล่งที่หาแล้ว
3. **ใส่ลิงก์ทุกตัวเลขสำคัญ** — 10-K/20-F/10-Q, IR/Press, 2 calls ล่าสุด, หน่วยงานกำกับ, Damodaran Online
4. **ระบุ as-of date เสมอ** — รูปแบบ `YYYY-MM-DD` · สกุลเงินคงที่ทั้งเรื่อง · FX ระบุอัตรา+วันที่
5. **เอกสารทางการล่าสุด = source of truth** — ข้อมูลขัดกันให้ยึดเอกสารทางการล่าสุด อธิบายสั้นๆ

---

## Commands

เรียกเจาะมุมผ่าน slash command (`/deep-o-stock-analyst:<cmd>`):

| Command | ผลลัพธ์ |
|---|---|
| `/full` | DEEP+O เต็มรายงาน (livecheck → valuation → score → risk → one-pager) — เริ่มต้นแนะนำ |
| `/livecheck` | Real-Time Protocol — ยืนยันงบ/ราคา/ERP ล่าสุดก่อนวิเคราะห์ |
| `/wacc` | Cost of Capital → เส้นทาง WACC (current → stable) |
| `/valuation` | Damodaran DCF (drivers + clean-ups + stable + triangulation) → intrinsic value |
| `/reversedcf` | ราคาปัจจุบันฝัง expectation อะไร + reality check |
| `/options` | Option-Adjusted Valuation (ตัว O) |
| `/deep` | DEEP scoring 0–100 + verdict 🟢🟡🟠🔴 |
| `/risk` | Risk Map + Bull/Base/Bear + thesis killers |
| `/catalysts` | Catalysts Map 12–24 เดือน + owner metric |
| `/onepager` | One-Pager ภาษาง่าย |

> สำหรับวิเคราะห์เชิงลึกแบบ isolated เรียก subagent `deep-o-stock-analyst` ผ่าน Agent tool ได้

---

## Disclaimer

เครื่องมือนี้เป็นกรอบวิเคราะห์หุ้นเชิงการศึกษา **ไม่ใช่คำแนะนำการลงทุนรายบุคคล** · verdict (ซื้อเพิ่ม/ถือ/ลด/ขาย 🟢🟡🟠🔴) เป็น **framework signal** จากกรอบ DEEP+O ไม่ใช่คำสั่งซื้อขาย · ตัวเลข valuation อิงสมมติฐานที่ระบุ (WACC, g∞, margin, S/C) และข้อมูล ณ as-of date · ผู้ใช้ต้อง verify เอกสารทางการล่าสุด (10-K/10-Q/IR) และพิจารณาบริบทของตนเองก่อนตัดสินใจ
