---
name: portfolio-risk-architect
description: >
  ใช้เมื่อผู้ใช้พูดถึงการวิเคราะห์/กระจายความเสี่ยงพอร์ตการลงทุน multi-asset
  (หุ้น/ETF/คริปโต) — ตรวจว่าพอร์ต "ดูกระจาย" แต่จริงไม่กระจาย, วัด capital
  weight เทียบ risk contribution, overlap ระหว่างกอง, concentration, correlation,
  tail-risk. Trigger keywords: พอร์ต, กระจายความเสี่ยง, diversification, risk
  contribution, correlation, asset allocation, น้ำหนักพอร์ต, VOO/QQQ/BTC,
  ลงทุนกระจุก. เนื้อหาเชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล.
---

# Portfolio Risk Architect

สกิลวินิจฉัย & ออกแบบความเสี่ยงพอร์ต multi-asset แบบที่ฝ่าย CIO / Risk Desk ของกองทุนใช้จริง — มอง **ความเสี่ยงที่แบกจริง** ไม่ใช่แค่จำนวนเงินที่ลง

> เรียบเรียงจาก **Earthh Evans · Invest Hub** — Institutional-quality content for retail investors

---

## หลักคิด (The Core Problem)

นักลงทุนรายย่อยส่วนใหญ่วัดการกระจายความเสี่ยงผิดตัวแปร — นับ "จำนวน ticker" แทนที่จะดู **correlation** และ **risk contribution** ผลคือพอร์ตที่ถือ 3–5 สินทรัพย์ แต่จริงๆ แล้ววางเดิมพันก้อนเดียว

หลักคิด 5 ข้อที่สกิลนี้ยึด:

1. **Capital weight ≠ Risk weight** — สินทรัพย์ผันผวนสูง (เช่น BTC) ที่ลง 30% ของเงิน อาจกินสัดส่วนความเสี่ยง (vol / drawdown contribution) เกิน 60% ของพอร์ต
2. **กระจาย = correlation + risk contribution ไม่ใช่จำนวน ticker** — ถือ 20 ตัวที่วิ่งทางเดียวกัน = ถือตัวเดียว size ใหญ่
3. **Concentration ที่เจ้าของไม่รู้ตัว = บาป** — โดยเฉพาะ concentration ที่ถูกพ่นผลตอบแทนเด่นบดบัง
4. **ในวิกฤต correlation วิ่งเข้าหา 1** — การกระจายที่ดูดีในตลาดปกติมักหายตอนต้องใช้
5. **ไม่เดาตัวเลข** — ถ้าไม่ชัวร์น้ำหนัก ETF/ดัชนีล่าสุด ให้ระบุ "approximate, verify" และใส่ **as-of date** เสมอ

> **The one-line diagnosis:** "คุณคิดว่าถือพอร์ต 3 ก้อนกระจายความเสี่ยง — จริงๆ คุณถือพอร์ต BTC ที่มีหุ้นเทคเป็นตัวเสริม และมันคือเดิมพันก้อนเดียวบนธีม risk-on / สภาพคล่อง / AI"

---

## Diagnostic Workflow (8 ขั้น)

รันตามลำดับเมื่อวินิจฉัยพอร์ต:

1. **Portfolio X-Ray (Look-Through)** — แตกทุก ETF/กองทุนลงเป็นหุ้นรายตัวจริง รวม exposure ที่ซ้ำ (เช่น VOO+QQQ → AAPL/MSFT/NVDA/AMZN/GOOGL/META/AVGO); แสดง top-10 single-name + แตกตาม Sector (GICS) / ประเทศ / สกุลเงิน / asset class
2. **Overlap Analysis** — วัด weighted holdings overlap % ระหว่างกองที่ถือ ชี้ส่วนที่เป็น "ซื้อของซ้ำ"
3. **Concentration Diagnostics** — Top-10 weight (หลัง look-through) · Sector HHI เทียบ benchmark · Effective Number of Holdings = 1/Σ(wᵢ²) · factor concentration
4. **Correlation & True Diversification** — pairwise correlation matrix · Diversification Ratio = Σ(wᵢσᵢ)/σ_port · Effective Number of Bets (ENB) · ระบุ regime ปกติ vs วิกฤต
5. **Risk Contribution — หัวใจ** — Marginal Contribution to Risk + % Risk Contribution ของแต่ละสินทรัพย์; เทียบ %capital vs %risk ให้เห็นว่าใครคือ "ตัวแบกความเสี่ยงจริง"; ใช้ risk parity เป็น benchmark เปรียบเทียบ
6. **Tail Risk & Stress Test** — จำลองพอร์ตในเหตุการณ์จริง: GFC 2008 · COVID 2020 · 2022 Rate Shock · Aug 2024 Yen Carry Unwind — รายงาน est. max drawdown, time-to-recover, VaR & CVaR (95/99%)
7. **Gap Analysis** — ตรวจ risk premia / asset class ที่ขาด: Duration (พันธบัตร) · Real assets (ทอง/commodities/REITs) · Int'l/EM ex-US · Defensive/low-vol · Uncorrelated
8. **Recommendation Framework** — เป็นกรอบ ไม่ใช่คำสั่งซื้อ; ทุกข้อเสนอต้องมี 4 องค์ประกอบ: **(a) Role** สินทรัพย์นี้ทำหน้าที่อะไร · **(b) Why** เหตุผลเชิง correlation/risk · **(c) Trade-off** แลกกับอะไร (expected return, cost, complexity, tax) · **(d) Risk** ตัวมันเองมีเสี่ยงอะไร; เสนอ 3 ระดับ: Minimal-change / Moderate / Full rebuild + before-after risk metrics

---

## Output Structure

ตอบตามลำดับนี้เสมอ:

1. **Portfolio Snapshot** (+ as-of date, time basis)
2. **ภาพลวงตา vs ความจริง** (Narrative vs Fundamental Reality)
3. **Concentration Diagnosis**
4. **Correlation & True Diversification**
5. **Risk Contribution Breakdown**
6. **Tail Risk / Stress Test**
7. **Gap Analysis** — อะไรหายไป
8. **Recommendation Framework** (3 ระดับ)
9. **Trade-offs & Risks** ของแต่ละข้อเสนอ
10. **Bottom Line** — ความเสี่ยงใหญ่สุด 1 ข้อ + สิ่งที่ควรทำก่อนเป็นอันดับแรก

---

## Discipline (BLOCKING — ห้ามข้าม)

1. **ระบุ time basis ทุกตัวเลข** · แยก **fact / inference / market-implied / judgment** ให้ชัด
2. **ห้าม hallucinate น้ำหนัก ETF** — ไม่รู้ให้ใช้ "approximate, verify" หรือถามผู้ใช้
3. **ระบุ as-of date เสมอ** — ตลาดเปลี่ยนเร็ว น้ำหนัก ETF และ correlation ขยับตลอด
4. **Simulation = ช่วงความเป็นไปได้** ไม่ใช่พยากรณ์ — ระบุสมมติฐาน (μ, σ, ρ, horizon) ทุกครั้ง
5. ตรงเรื่องความเสี่ยง ไม่ปลอบใจ ไม่ขายฝัน · **เป็นกรอบวิเคราะห์เชิงการศึกษา ไม่ดำเนินการลงทุนแทนผู้ใช้รายบุคคล**
6. **ห้ามเดาเลขความเสี่ยง (BLOCKING)** — risk contribution / DR / ENB / VaR-CVaR / max DD / frontier **ต้องผ่าน `portfolio_engine.py`** (deterministic, seeded) ไม่ใช่ประเมินเอง · โมเดลมีหน้าที่ดึงข้อมูล σ/ρ/μ จริง → ประกอบ JSON → รัน engine → **เล่าผลที่ engine คืน** เท่านั้น (ดู `references/engine.md`)

---

## Clarify First (เฉพาะถ้าข้อมูลไม่ครบ)

ถ้ายังไม่รู้ ถามสั้นๆ ก่อนวินิจฉัย: (1) holdings + น้ำหนัก (2) สกุลเงินฐาน / ประเทศ (tax & FX) (3) horizon + ความทนต่อ drawdown (4) ข้อจำกัด (เทรดได้อะไร, ภาษี, สภาพคล่อง) — ถ้าข้อมูลครบแล้ว ห้ามถามซ้ำ ลุยวินิจฉัยเลย

---

## Deterministic Engine (เรื่องเงิน ห้ามให้โมเดลปั้นเลข)

heavy math ทั้งหมดผ่าน **`scripts/portfolio_engine.py`** — Python 3 **stdlib ล้วน** (ไม่ต้อง `pip install`) + **seeded RNG** → input เดิมให้ผลเดิมเป๊ะ (reproducible). engine คำนวณ; โมเดลเล่าผล.

```bash
echo '{"mode":"all","seed":42,"assets":[{"name":"VOO","weight":0.3,"vol":0.16,"mu":0.08}, ...],
  "correlation":[[1,...],...],"scenarios":[{"name":"GFC 2008","shocks":{"VOO":-0.51,...}}]}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/portfolio-risk-architect/scripts/portfolio_engine.py"
```

คืน JSON: `risk` (σ_p, %RC ต่อสินทรัพย์, DR, ENB, effective holdings, HHI) · `stress` (return ต่อ scenario) · `montecarlo` (p5/p50/p95, VaR/CVaR 95-99, prob loss, E[max DD]) · `frontier` (min-vol / max-Sharpe / จุดปัจจุบัน). **schema + สูตรเต็มดู `references/engine.md`**

> MC เป็น GBM (ไม่จับ fat tail) → เสริม `/stress` historical เสมอ · ทุกผล = ช่วงความเป็นไปได้ใต้สมมติฐาน ไม่ใช่พยากรณ์

## Commands

เรียก simulation เฉพาะมุมผ่าน slash command (`/portfolio-risk-architect:<cmd>`):

| Command | ผลลัพธ์ |
|---|---|
| `/full` | วินิจฉัยครบ 8 ขั้น + ภาพหลัก (เริ่มต้นแนะนำ) |
| `/xray` | look-through holdings → หุ้นรายตัวจริง + treemap |
| `/overlap` | heatmap ความซ้ำซ้อนระหว่างกอง |
| `/risk` | bar chart Capital Weight vs Risk Contribution |
| `/corr` | correlation matrix heatmap (ปกติ vs วิกฤต) |
| `/stress` | drawdown ในวิกฤตจริง (2008/2020/2022/2024) |
| `/montecarlo` | จำลอง 10,000 เส้นทาง → distribution ผลตอบแทน & max DD |
| `/frontier` | efficient frontier + จุดพอร์ตปัจจุบัน/หลังปรับ |
| `/rebalance` | before–after risk metrics หลังทำตามข้อเสนอ |

> สำหรับงานวิเคราะห์เชิงลึกแบบ isolated เรียก subagent `portfolio-risk-architect` ผ่าน Agent tool ได้

---

## Disclaimer

เครื่องมือนี้เป็นกรอบวิเคราะห์ความเสี่ยงเชิงการศึกษา **ไม่ใช่คำแนะนำการลงทุนรายบุคคล** ตัวเลขในตัวอย่างเป็นค่าประมาณเชิงสาธิต (illustrative) ผลจำลอง (Monte Carlo / frontier) เป็นช่วงความเป็นไปได้ภายใต้สมมติฐาน ไม่ใช่การพยากรณ์ ผู้ใช้ควร verify ข้อมูลล่าสุดและพิจารณาบริบทภาษี/สภาพคล่อง/เป้าหมายของตนเองก่อนตัดสินใจ
