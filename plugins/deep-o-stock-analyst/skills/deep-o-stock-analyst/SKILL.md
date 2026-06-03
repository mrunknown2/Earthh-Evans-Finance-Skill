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
Excess cash · Debt (book → MV) · cross-holdings/non-operating assets · minority interests · **ESOP** ประเมินด้วย Black-Scholes (options, exercise price, maturity, σ) หักจาก equity · **NOLs** ตารางใช้สิทธิภาษี · **Failure risk** — expected-value blend เต็ม: `EV_adj = (1−p_failure)·EV_going_concern + p_failure·(recovery·EV)` (อย่าใส่แค่ `p×recovery` — ต้องมี `(1−p)` ถ่วง going-concern; บังคับถ้า early/fragile)

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
3. **Reverse DCF** — WACC, g∞, FCFF margin พร้อมเหตุผล → **terminal-anchored** (รัน `valuation_engine.py` mode `reverse_dcf`: `TV=EV·(1+WACC)^N → FCFF=TV·(WACC−g) → R*=FCFF/[margin·(1−tax)·(1−g/ROIC)] → ImpliedCAGR`) + reality check · **ห้ามใช้สูตรลัด `EV×(WACC−g)/margin`** (มันสับสน EV กับ terminal value → understate)
3'. **Option-Adjusted Valuation** — `EV_core + ΣEV(options) → EV_total`; ตลาดใส่อะไรไปแล้ว
4. **Risk Map** — Regulation / Execution / GeoFX / ESG (+ ลิงก์หน่วยงาน)
5. **Bull / Base / Bear** — + Triggers & Thesis Killers
6. **Catalysts Map (12–24 เดือน)** — วัน/ไตรมาส + owner metric + แหล่งอ้างอิง
7. **Weighted Score & Decision** — สรุป 0–100
8. **One-Pager** — ภาษาง่าย เล่าเป็นเรื่องเดียว มือใหม่ฟังรู้เรื่อง
9. **ภาคผนวกแหล่งอ้างอิง** — ลิสต์ลิงก์ทั้งหมด (รวม Damodaran Online ERP/Beta/CRP/WACC)

---

## Weighted Score & Verdict

ให้คะแนน **0–5/มิติ** แล้ว**normalize**เป็น 0–100 (ห้ามคูณดิบ — score×weight จะเต็ม 500):

```
total = Σ (scoreᵢ / 5) × weightᵢ        # weight: D 25 / E_exec 20 / E_econ 20 / P 20 / O 15 (รวม 100)
       = (D/5·25)+(Eexec/5·20)+(Eecon/5·20)+(P/5·20)+(O/5·15)   → 0–100
```

> รัน `valuation_engine.py` mode `deep` เพื่อคำนวณ (deterministic) — โมเดลไม่บวกเอง · **กฎ tie-break:** ถ้า P (Price) ต่ำ (แพง) แต่ D/E/O สูง → verdict ห้ามเขียว ให้ระบุชัดว่า "ธุรกิจดีแต่ราคาแพง"

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
6. **ห้ามเดาเลข valuation (BLOCKING)** — WACC / DCF intrinsic value / reverse DCF / DEEP score **ต้องผ่าน `valuation_engine.py`** (deterministic) ไม่ใช่บวก/คูณในหัว · โมเดลหาข้อมูลจริง → ประกอบ JSON → รัน engine → ตีความ (ดู `references/engine.md`)
7. **รู้ว่าเมื่อไร DCF ใช้ไม่ได้** — pre-profit / FCF ติดลบ → ใช้ช่วง revenue-multiple + path to profitability แทน · cyclical (TTM ที่ peak/trough หลอก) → normalize ทั้งวัฏจักร · ธนาคาร/ประกัน (FCFF/EV ไม่มีความหมาย) → ใช้ FCFE / excess-return / DDM · ระบุชัดเมื่อสลับโมเดล

---

## Deterministic Engine (เรื่องเงิน ห้ามให้โมเดลปั้นเลข)

heavy math ผ่าน **`scripts/valuation_engine.py`** — Python 3 **stdlib ล้วน** (ไม่ต้อง `pip install`). โมเดลคำนวณไม่ได้แม่นพอเรื่องตัวเลข — ให้ engine ทำ แล้วโมเดลเล่าผล + ใส่ลิงก์ + as-of date.

```bash
echo '{"mode":"reverse_dcf","ev":22.6,"revenue0":0.757,"wacc":0.095,"g_terminal":0.04,"terminal_margin":0.35,"terminal_roic":0.15,"tax":0.25,"horizon_n":10}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/deep-o-stock-analyst/scripts/valuation_engine.py"
```

modes: `wacc` (CAPM + MV weights) · `dcf` (FCFF + S/C reinvestment → intrinsic value/share) · `reverse_dcf` (terminal-anchored implied CAGR) · `deep` (0–5 → 0–100 normalized + verdict). schema เต็ม: `references/engine.md`

> reverse DCF ใช้สูตรเดียวกับปลั๊กอินพี่น้อง **`reverse-dcf-screener`** (terminal-anchored) — ตัวนั้นเน้น Excel + screener หลายตัว, ตัวนี้เป็น inline Damodaran-style quick read

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
