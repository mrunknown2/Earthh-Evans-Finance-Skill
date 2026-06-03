# Deep-O Stock Analyst — Playbook การใช้งาน

> ปลั๊กอินวิเคราะห์หุ้นรายตัว (**US**) ด้วยกรอบ **DEEP+O** (Demand · Execution · Economics · Price · Optionality) สไตล์หุ้นส่วนกองทุนเฮดจ์ฟันด์ อิงตรรกะ Damodaran + McKinsey — ออก verdict **ซื้อเพิ่ม / ถือ / ลด / ขาย** แบบตรวจสอบได้ทุกตัวเลข เหมาะเมื่อต้องการหา intrinsic value, เช็กว่าราคาแพง/ถูก, หรือตัดสินใจซื้อ-ถือ-ขายหุ้นตัวเดียว

## ติดตั้ง

```
/plugin install deep-o-stock-analyst
```

ต้องมี **Python 3** เพื่อรัน engine — **ไม่ต้อง `pip install`** (stdlib ล้วน)

## Quickstart — เริ่มเร็วสุด

คำสั่งเริ่มต้นที่ README แนะนำคือ `/full <ticker>` — รันครบกรอบ DEEP+O จบในรอบเดียว (livecheck → valuation → DEEP score → risk → one-pager)

```
/full NVDA
```

ถ้าไม่อยากใช้ command เลย แค่คุยเรื่องวิเคราะห์หุ้น Skill จะ auto-trigger เอง เช่น:

```
ช่วยวิเคราะห์ NVDA หน่อย ราคาตอนนี้แพงไปไหม
```

**ต้องเตรียมอะไรก่อนกด:** แค่ **ticker หุ้น** (ถ้าไม่ระบุ `/full` จะถามก่อนเริ่ม) — ส่วนงบ/ราคา/ERP ขั้น livecheck จะไปดึงสดด้วย Search ให้เอง

## เตรียมข้อมูลก่อนใช้ (Inputs)

หัวใจคือ **Real-Time Protocol** — ห้ามวิเคราะห์จากความจำ ต้องตรวจข้อมูลจริงก่อน (Search > Memory เสมอ) ข้อมูลที่ระบบต้องการ:

- **งบไตรมาสล่าสุด** + วันประกาศงบ (จาก Investor Relations / press release) — ถ้างบเพิ่งออก < 3 วัน = "Breaking News / Earnings Reaction Mode"
- **10-K / 10-Q ล่าสุด** (SEC Filings) + วันยื่นเอกสาร
- **ราคาปัจจุบัน + Market Cap วันนี้**
- **Damodaran ERP** เดือนปัจจุบัน (+ CRP ถ้ามี country risk)
- สำหรับ `/wacc`: **Risk-free** (สกุลที่รายงาน), **Beta** (bottom-up/sector ไม่ใช่ regression ดิบ), **pre-tax cost of debt** (rating/synthetic), **market-value weights** ของ equity/debt, **tax**
- สำหรับ `/valuation`: path ต่อปีของ **revenue growth · operating margin · tax · Sales-to-Capital (S/C)** + **g∞ · ROIC∞ · terminal margin · net debt · shares · cleanups**
- สำหรับ `/reversedcf`: **EV ปัจจุบัน · revenue ฐาน (R0) · WACC · g∞ · terminal margin · terminal ROIC · tax · horizon N**

> ทุกตัวเลข/ข้อเท็จจริงสำคัญ **ต้องใส่ลิงก์อ้างอิง** และระบุ **as-of date** (`YYYY-MM-DD`) · ไม่พบให้เขียน "ไม่พบข้อมูล" ห้ามกุ

## คำสั่งทั้งหมด

เรียกผ่าน `/deep-o-stock-analyst:<cmd>` (หรือย่อ `/<cmd>` ถ้าไม่ชนกัน)

| คำสั่ง | ทำอะไร | Input |
|---|---|---|
| `/full` | DEEP+O เต็มรายงานจบในรอบเดียว (livecheck → valuation → DEEP score → risk → one-pager) — entry point หลัก | ticker (ถ้าไม่ระบุจะถาม) |
| `/livecheck` | Real-Time Protocol — ยืนยันงบ/ราคา/Market Cap/ERP ล่าสุดด้วย Search ก่อนวิเคราะห์ | ticker |
| `/wacc` | Cost of Capital → เส้นทาง WACC (current → sector-stable) ผ่าน engine | ticker + (ถ้ามี) ผล `/livecheck` |
| `/valuation` | Damodaran DCF เต็ม (drivers + clean-ups + stable guardrails + triangulation) → intrinsic value | ticker + (ถ้ามี) ผล `/livecheck`, `/wacc` |
| `/reversedcf` | ถอด expectation ที่ตลาดฝังในราคา (terminal-anchored implied CAGR) + reality check | ticker + EV + R0 + WACC + g∞ + terminal margin + terminal ROIC + tax + N |
| `/options` | Option-Adjusted Valuation (ตัว O) — `EV_core + ΣEV(options) → EV_total` | ticker + EV_core จาก `/valuation` หรือ `/reversedcf` |
| `/deep` | DEEP scoring 0–100 (D25/E20/E20/P20/O15) + verdict 🟢🟡🟠🔴 | ticker + (ถ้ามี) ผลวิเคราะห์ก่อนหน้า |
| `/risk` | Risk Map (Regulation/Execution/GeoFX/ESG) + Bull/Base/Bear + thesis killers | ticker + thesis หลัก |
| `/catalysts` | Catalysts Map 12–24 เดือน + owner metric + แหล่งอ้างอิง | ticker |
| `/onepager` | One-Pager ภาษาง่าย เล่าเป็นเรื่องเดียว ไม่มี bullet | ผลวิเคราะห์ DEEP+O ที่ทำไว้ (หรือ ticker → แนะนำรัน `/full` ก่อน) |

> นอกจาก command ยังเรียก subagent `deep-o-stock-analyst` ผ่าน Agent tool เพื่อวิเคราะห์เชิงลึกแบบ isolated ได้

## Workflow ที่ใช้บ่อย

**1. วิเคราะห์หุ้นใหม่เต็มชุด (เร็วสุด)**
```
/full NVDA
```
รันครบทุกขั้นตาม Output Structure §0–§9 จบในคำสั่งเดียว — เหมาะตอนเริ่มต้นกับหุ้นที่ยังไม่เคยดู

**2. เช็กมูลค่าเร็วแบบเจาะทีละมุม (wacc → valuation → reversedcf)**
```
/livecheck NVDA      # ดึงงบ/ราคา/ERP สดก่อน
/wacc NVDA           # ได้ WACD current → stable
/valuation NVDA      # ได้ intrinsic value (ใช้ WACC จากขั้นก่อน)
/reversedcf NVDA     # ราคาวันนี้ฝัง implied CAGR เท่าไร สมจริงไหม
/deep NVDA           # รวมเป็นคะแนน 0–100 + verdict
```
แต่ละขั้นป้อนผลลัพธ์ขั้นก่อนต่อให้ขั้นถัดไป (WACC → DCF → reverse DCF cross-check)

**3. ทำ one-pager ส่งให้คนอ่านง่าย**
```
/full NVDA           # ทำชุดวิเคราะห์ให้ครบก่อน
/onepager            # ย่อทุกอย่างเป็นเรื่องเล่าภาษาง่าย ไม่มี bullet
```
`/onepager` เล่าตามข้อเท็จจริงที่วิเคราะห์มาเท่านั้น — ไม่เพิ่มตัวเลขใหม่ที่ไม่มีแหล่ง

## อ่านผลลัพธ์ยังไง

**DEEP score (0–100) → verdict** (จาก engine, ไม่ใช่โมเดลบวกเอง):

| คะแนน | สัญญาณ | คำแนะนำ |
|-------|--------|---------|
| ≥ 80 | 🟢 | ซื้อเพิ่ม |
| 60–79 | 🟡 | ถือ / สะสมระวัง |
| 40–59 | 🟠 | ลดน้ำหนัก |
| < 40 | 🔴 | ขาย |

- **tie-break สำคัญ:** ถ้า **P (Price) ต่ำ** (= หุ้นแพง) แม้ D/E/O สูง → verdict **ห้ามเขียว** ต้องระบุชัดว่า "ธุรกิจดีแต่ราคาแพง"

**DCF intrinsic value เทียบราคา** (`/valuation`):
- `value_per_share` **สูงกว่า** ราคาตลาด → ตลาดให้ราคาถูกกว่ามูลค่า (มี margin of safety)
- `value_per_share` **ต่ำกว่า** ราคาตลาด → ราคาแพงเทียบมูลค่า
- รายงานเป็น **ช่วง** (sensitivity WACC×g∞×margin) ไม่ใช่จุดเดียว — valuation ไวต่อ input มาก

**Reverse DCF implied CAGR** (`/reversedcf`):
- engine คืน `implied_cagr` = อัตราโตรายได้ที่ราคาปัจจุบัน "เรียกร้อง" ให้บริษัททำให้ได้
- เทียบกับ TAM + track record (historical CAGR + forward consensus): ถ้า implied_cagr **สูงเกินจริง** → ราคา price-in ความสมบูรณ์แบบไปแล้ว (แพง) · ถ้า **สมจริงหรือต่ำกว่า** ที่บริษัททำได้ → ยังมี upside

## Engine — เลขไม่เดา

การคำนวณเรื่องเงินทั้งหมดวิ่งผ่าน **`skills/deep-o-stock-analyst/scripts/valuation_engine.py`** — Python 3 **stdlib ล้วน**, **deterministic + reproducible** (ไม่มี numpy, portable ข้าม IDE/provider) โมเดลมีหน้าที่แค่ **ดึงข้อมูลจริง + ใส่ลิงก์ → ประกอบ JSON → รัน engine → เล่าผล** ไม่ปั้นเลขเอง

วิธีเรียก:
```bash
echo '<JSON>' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/deep-o-stock-analyst/scripts/valuation_engine.py"
```

4 modes:

- **`wacc`** — CAPM + market-value weights: `cost_of_equity = rf + β·(ERP+CRP)`, `cost_of_debt_after_tax = cod·(1−tax)`, WACC ถ่วงด้วยน้ำหนัก MV → คืน `wacc`, `cost_of_equity`, `cost_of_debt_after_tax`, `weight_equity/debt`
- **`dcf`** — FCFF + Sales-to-Capital reinvestment: `FCFFₜ = Revenueₜ·marginₜ·(1−tax) − ΔRevenueₜ/(S/C)ₜ`, `TV = FCFF_{N+1}/(WACC∞−g∞)`, terminal reinv = `g∞/ROIC∞` → คืน `firm_value`, `equity_value`, `value_per_share`, `terminal_value`, `terminal_reinvestment_rate`, `fcff_explicit[]`
- **`reverse_dcf`** — **terminal-anchored** (สูตรเดียวกับปลั๊กอินพี่น้อง `reverse-dcf-screener`): `TV=EV·(1+WACC)^N → FCFF=TV·(WACC−g) → R*=FCFF/[margin·(1−tax)·(1−g/ROIC)] → ImpliedCAGR=(R*/R0)^(1/(N+1))−1` → คืน `implied_cagr`, `implied_terminal_revenue`, `revenue_multiple_required`, `conversion`
- **`deep`** — normalize 0–5 ต่อมิติ → 0–100: `total = Σ(scoreᵢ/5)·weightᵢ` (น้ำหนัก D25/E20/E20/P20/O15 รวม 100) — **ไม่ใช่** `scoreᵢ·weightᵢ` (ซึ่งจะเต็ม 500) → คืน `total`, `contributions{}`, `verdict_band`, `signal`

ตัวอย่างจริงจาก reference (reverse_dcf):
```bash
echo '{"mode":"reverse_dcf","ev":22.6,"revenue0":0.757,"wacc":0.095,"g_terminal":0.04,"terminal_margin":0.35,"terminal_roic":0.15,"tax":0.25,"horizon_n":10}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/deep-o-stock-analyst/scripts/valuation_engine.py"
```

## ข้อควรระวัง / วินัย

**Discipline (BLOCKING — ห้ามข้าม) จาก SKILL:**
1. **ข้อมูลสดก่อนวิเคราะห์** — ตรวจงบ/ราคา/ERP ล่าสุดด้วย Search; Search > Memory เสมอ
2. **ห้ามกุข้อมูล** — ไม่พบให้เขียน "ไม่พบข้อมูล" + บอกแหล่งที่หาแล้ว
3. **ใส่ลิงก์ทุกตัวเลขสำคัญ** — 10-K/20-F/10-Q, IR/Press, หน่วยงานกำกับ, Damodaran Online
4. **ระบุ as-of date เสมอ** (`YYYY-MM-DD`) · สกุลเงินคงที่ทั้งเรื่อง · FX ระบุอัตรา+วันที่
5. **เอกสารทางการล่าสุด = source of truth** — ข้อมูลขัดกันให้ยึดเอกสารทางการล่าสุด
6. **ห้ามเดาเลข valuation (BLOCKING)** — WACC / DCF / reverse DCF / DEEP score **ต้องผ่าน engine** ไม่ใช่บวก/คูณในหัว
7. **รู้ว่าเมื่อไร DCF ใช้ไม่ได้:**
   - pre-profit / FCF ติดลบ → ใช้ revenue-multiple + path to profitability แทน
   - cyclical (TTM ที่ peak/trough หลอก) → normalize ทั้งวัฏจักร
   - ธนาคาร/ประกัน (FCFF/EV ไม่มีความหมาย) → ใช้ FCFE / excess-return / DDM

**Guardrails ก่อนส่งเข้า engine:**
- `g∞ ≤` long-run nominal GDP (หรือ `≤` risk-free)
- `ROIC∞ →` industry median / WACC (เหตุผลเชิงการแข่งขัน)
- **ห้ามใช้สูตรลัด** `EV×(WACC−g)/margin` ใน reverse DCF — มันสับสน EV ปัจจุบันกับ terminal value + ทิ้ง tax/reinvestment → understate ความคาดหวัง
- failure-risk ต้องใช้ blend เต็ม `EV_adj = (1−p)·EV + p·(recovery·EV)` (อย่าใส่แค่ `p×recovery`)
- รายงานเป็น **ช่วง** (sensitivity) เสมอ — valuation ไวต่อ input มาก

## Disclaimer

เครื่องมือนี้เป็นกรอบวิเคราะห์หุ้น **เชิงการศึกษา ไม่ใช่คำแนะนำการลงทุนรายบุคคล** · verdict (ซื้อเพิ่ม/ถือ/ลด/ขาย 🟢🟡🟠🔴) เป็น **framework signal** จากกรอบ DEEP+O ไม่ใช่คำสั่งซื้อขาย · ตัวเลข valuation อิงสมมติฐานที่ระบุ (WACC, g∞, margin, S/C) และข้อมูล ณ as-of date · ผู้ใช้ควร verify เอกสารทางการล่าสุด (10-K/10-Q/IR) และพิจารณาบริบทภาษี/เป้าหมาย/ความเสี่ยงของตนเองก่อนตัดสินใจ

---

🔗 กลับไปที่ [README ของปลั๊กอิน](../plugins/deep-o-stock-analyst/README.md)
