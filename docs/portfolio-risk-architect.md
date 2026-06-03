# Portfolio Risk Architect — Playbook การใช้งาน

> ปลั๊กอินวินิจฉัย & ออกแบบความเสี่ยงพอร์ต **multi-asset** (Equity / ETF / Crypto) แบบที่ฝ่าย CIO / Risk Desk ของกองทุนใช้จริง — มอง **ความเสี่ยงที่แบกจริง** ไม่ใช่แค่จำนวนเงินที่ลง เหมาะเมื่ออยากรู้ว่าพอร์ตที่ "ดูกระจาย" จริงๆ แล้วกระจายไหม ใครคือตัวแบกความเสี่ยงตัวจริง และทนวิกฤตได้แค่ไหน

## ติดตั้ง

```
/plugin marketplace add mrunknown2/Earthh-Evans-Finance-Skill
/plugin install portfolio-risk-architect
```

ต้องมี **Python 3** เพื่อรัน engine — **ไม่ต้อง `pip install`** (stdlib ล้วน เลี่ยง numpy เพื่อ portability ข้าม IDE/provider)

## Quickstart — เริ่มเร็วสุด

เริ่มที่ `/full` (entry point หลัก — วินิจฉัยครบ 8 ขั้นในรอบเดียว) ตัวอย่างคำสั่งจริง:

```
พอร์ต: VOO 30%, QQQ 30%, BTC 30%, cash 10%, ฐาน USD, อยู่ไทย, horizon 10 ปี, ทน drawdown ~30%.
/full
```

ต้องเตรียมก่อนกด: รายการ holdings + น้ำหนัก, สกุลเงินฐาน/ประเทศ, horizon + ความทนต่อ drawdown, และข้อจำกัด (เทรดได้อะไร/ภาษี/สภาพคล่อง) — ถ้าให้ไม่ครบ Claude จะถามก่อน (Clarify First) ถ้าครบแล้วลุยเลย

> นอกจากเรียก command ตรงๆ ยังมี **Skill อัตโนมัติ** (แค่คุยเรื่องพอร์ต Claude จะดึง methodology มาใช้เอง) และ **Agent** `portfolio-risk-architect` (subagent บทบาท Senior Multi-Asset Strategist เรียกผ่าน Agent tool สำหรับวิเคราะห์เชิงลึกแบบ isolated)

## เตรียมข้อมูลก่อนใช้ (Inputs)

ขึ้นกับ command ที่จะใช้ แต่รวมๆ ต้องมี:

- **Holdings + น้ำหนัก** ของพอร์ต (เช่น VOO 30%, QQQ 30%, BTC 30%, cash 10%) — `weight` ใส่เป็นเศษส่วนหรือจำนวนเงินดิบก็ได้ engine normalize ให้รวม = 1 เอง
- **สกุลเงินฐาน / ประเทศที่อยู่** (tax & FX)
- **Horizon + ความทนต่อ drawdown**
- **ข้อจำกัด** — เทรดได้อะไร, ภาษี, สภาพคล่อง
- **vol (σ) ของแต่ละสินทรัพย์** — สำหรับ `/risk` `/corr` (annualized)
- **correlation (ρ) matrix** — NxN ลำดับเดียวกับ assets; ไม่ส่ง = engine ใช้ identity (ถือว่า uncorrelated → ต้องเตือนผู้ใช้)
- **μ (expected return, annualized)** — สำหรับ `/montecarlo` `/frontier`
- **horizon** — สำหรับ Monte Carlo
- **holdings ของแต่ละ ETF** — สำหรับ `/xray` `/overlap` (look-through)
- **per-asset shock ต่อ scenario** — สำหรับ `/stress` (ใช้ peak-to-trough จริงในช่วงเหตุการณ์; สินทรัพย์ที่ยังไม่เกิด ณ ตอนนั้น เช่น BTC ปี 2008 → mark N/A)
- **น้ำหนักใหม่ที่เสนอ** — สำหรับ `/rebalance` (เทียบ before–after)

> σ/ρ/น้ำหนัก ETF ที่ไม่ชัวร์ = ใส่ค่า approximate แล้วระบุ "approximate, verify" + **as-of date** เสมอ (ห้าม hallucinate น้ำหนัก ETF)

## คำสั่งทั้งหมด

| คำสั่ง | ทำอะไร | input ที่ต้องใช้ | allowed-tools |
|---|---|---|---|
| `/full` | วินิจฉัยครบ 8 ขั้น + ภาพหลัก (X-Ray, Risk Contribution, Stress) — เริ่มต้นแนะนำ | holdings+น้ำหนัก, สกุลเงิน/ประเทศ, horizon+ทน DD, ข้อจำกัด (+ σ/ρ/μ/scenarios สำหรับขั้น 3–6) | Read, Bash |
| `/xray` | look-through holdings → หุ้นรายตัวจริง + treemap (sector/ประเทศ/สกุลเงิน/asset class) | holdings+น้ำหนัก, holdings ของแต่ละ ETF | Read |
| `/overlap` | heatmap ความซ้ำซ้อนระหว่างกอง — ชี้ที่ "ซื้อซ้ำ" | top holdings ของแต่ละกอง/ETF | Read |
| `/risk` | bar chart Capital Weight vs Risk Contribution (ภาพที่ทรงพลังสุด) | holdings+น้ำหนัก, σ ของแต่ละสินทรัพย์ + correlation | Read, Bash |
| `/corr` | correlation matrix heatmap (regime ปกติ vs วิกฤต) + DR/ENB ทั้งสอง regime | return series หรือ correlation อ้างอิง + σ + น้ำหนัก | Read, Bash |
| `/stress` | drawdown ในวิกฤตจริง (GFC2008 / COVID2020 / 2022 Rate Shock / Aug2024 Yen Unwind) | holdings+น้ำหนัก, per-asset shock ต่อ scenario | Read, Bash |
| `/montecarlo` | จำลอง 10,000 เส้นทาง (GBM) → distribution ผลตอบแทน & max DD | holdings+น้ำหนัก, μ/σ/ρ + horizon | Read, Bash |
| `/frontier` | efficient frontier + จุดพอร์ตปัจจุบัน/หลังปรับ | สินทรัพย์ + μ/σ/ρ + น้ำหนักปัจจุบัน | Read, Bash |
| `/rebalance` | before–after risk metrics หลังทำตามข้อเสนอ | น้ำหนักเดิม + น้ำหนักใหม่ + σ/ρ/μ เดียวกันทั้งสองชุด | Read, Bash |

> ทุก command ใช้ `model: opus` · เรียกผ่าน prefix `/portfolio-risk-architect:<cmd>`

## Workflow ที่ใช้บ่อย

**1. วินิจฉัยพอร์ตครั้งแรก (end-to-end)**
```
พอร์ต: VOO 30%, QQQ 30%, BTC 30%, cash 10%, ฐาน USD, horizon 10 ปี, ทน drawdown ~30%.
/full
```
→ `/full` เดิน 8 ขั้นรวด (X-Ray → Overlap → Concentration → Correlation → Risk Contribution → Stress → Gap → Recommendation) แล้วเจาะต่อตามที่สนใจ เช่น `/risk` (ใครแบกความเสี่ยงจริง) หรือ `/stress`

**2. เช็ค correlation / overlap (พอร์ต "ดูกระจาย" จริงไหม)**
```
/xray      → แตก ETF เป็นหุ้นรายตัว ดูว่า mega-cap tech ทับซ้อนแค่ไหน
/overlap   → วัด weighted overlap % ระหว่างกอง (เช่น VOO vs QQQ)
/corr      → correlation matrix 2 regime (ปกติ vs วิกฤต) + ดู DR/ENB ยุบลงเท่าไรตอน ρ→1
```

**3. Stress + Monte Carlo ก่อนปรับพอร์ต แล้ววัดผลการปรับ**
```
/stress      → drawdown ในวิกฤตจริง (historical, จับ tail)
/montecarlo  → ช่วงผลลัพธ์ p5/p50/p95 + VaR/CVaR + E[max DD] (GBM, เสริม /stress)
/frontier    → ดูว่าพอร์ตปัจจุบันอยู่ใต้ envelope (ยังไม่ efficient) ไหม
/rebalance   → ใส่น้ำหนักใหม่ เทียบ before–after (σ_p, ENB, DR, rc_pct, E[max DD])
```

## อ่านผลลัพธ์ยังไง

- **Risk Contribution (`rc_pct` vs `weight`)** — หัวใจ: `weight` = %capital, `rc_pct` = %risk (รวม = 1) ถ้า BTC ลง 30% ของเงินแต่กิน 60–70% ของความเสี่ยง = พอร์ตนี้คือเดิมพัน BTC ที่มีหุ้นเทคเสริม ยิ่ง %risk เกิน %capital มาก = ตัวนั้นแบกความเสี่ยงเกินตัว
- **Diversification Ratio (`diversification_ratio`)** = Σ(wᵢσᵢ)/σ_p — **1 = ไม่กระจายเลย**, ยิ่งสูง = กระจายจริงมากขึ้น
- **ENB — Effective Number of Bets (`enb`)** = 1/Σ(rc_pct²) บน risk share — **1 = เดิมพันก้อนเดียว**, เข้าใกล้จำนวนสินทรัพย์ = ใกล้ risk-parity (กระจายดี) ต่างจาก `effective_holdings` (= 1/Σwᵢ² บน capital) ที่อาจดูดีกว่าความจริง
- **Stress (`portfolio_return` ต่อ scenario)** = Σ(wᵢ·shockᵢ) ตัวเลขติดลบมาก = drawdown หนักในวิกฤตนั้น สินทรัพย์ที่ไม่มี shock จะถูกนับเป็น 0 และ list ใน `na_assets` (ต้อง mark N/A ในการเล่า)
- **Monte Carlo** — `p5/p50/p95` = percentile ผลตอบแทนตลอด horizon (p5 = กรณีแย่, p50 = กลาง, p95 = ดี) · `var95/var99` = return ที่ tail (ติดลบ = ขาดทุน) · `cvar95/cvar99` = เฉลี่ยของ tail ที่เกิน VaR (แย่กว่า VaR) · `prob_loss` = ความน่าจะขาดทุน · `expected_max_dd`/`worst_max_dd` = max DD เฉลี่ย/แย่สุด ระวัง: GBM **มองโลกในแง่ดีเกินจริงในวิกฤต** → อ่านคู่ `/stress` เสมอ
- **Frontier** — `current` ที่อยู่ใต้/ในกลุ่ม cloud ใต้ envelope = ยังไม่ efficient (มีพอร์ตที่ risk เท่ากันแต่ return สูงกว่า หรือ return เท่ากันแต่ risk ต่ำกว่า) เทียบกับ `max_sharpe` / `min_vol`

## Engine — เลขไม่เดา

การคำนวณความเสี่ยงทุกตัว (risk contribution, DR, ENB, VaR/CVaR, max drawdown, frontier) วิ่งผ่าน `skills/portfolio-risk-architect/scripts/portfolio_engine.py` — **Python 3 stdlib ล้วน** (ไม่ต้อง `pip install`, linear algebra เขียนมือ ไม่พึ่ง numpy/scipy), **deterministic**, และ Monte Carlo / frontier ใช้ **seeded RNG** (Cholesky + Box–Muller, `seed` default 42) → input เดิม (รวม `seed`) ให้ output เดิมเป๊ะทุกครั้ง (reproducible)

เรียกแบบ pipe JSON เข้า stdin:
```bash
echo '<JSON>' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/portfolio-risk-architect/scripts/portfolio_engine.py"
```
mode รองรับ: `risk` · `corr` · `stress` · `montecarlo` · `frontier` · `all` (รันครบในรอบเดียว)

โมเดลมีหน้าที่แค่: ดึง/รับ holdings + σ/ρ/μ จริง → ประกอบ JSON → รัน engine → **เล่าผลที่ engine คืน** (แยก fact/assumption + as-of date + disclaimer) **ไม่ปั้นเลขเอง** · schema + สูตรเต็มดู `skills/portfolio-risk-architect/references/engine.md`

## ข้อควรระวัง / วินัย

- **ห้ามเดาเลขความเสี่ยง (BLOCKING)** — risk contribution / DR / ENB / VaR-CVaR / max DD / frontier ต้องผ่าน `portfolio_engine.py` เท่านั้น ห้ามประเมินในหัว
- **ห้าม hallucinate น้ำหนัก ETF** — ไม่รู้ให้ใช้ "approximate, verify" หรือถามผู้ใช้
- **ระบุ as-of date เสมอ** — น้ำหนัก ETF และ correlation ขยับตลอด · ระบุ time basis ทุกตัวเลข + แยก fact / inference / market-implied / judgment
- **correlation เป็นสมมติฐาน** — ในวิกฤต ρ วิ่งเข้าหา 1 การกระจายที่ดูดีตอนปกติมักหายตอนต้องใช้ → rerun ด้วย crisis regime เทียบเสมอ
- **Monte Carlo เป็น GBM** (lognormal) — ไม่จับ fat tail / regime shift / vol clustering → p5/CVaR มองโลกในแง่ดีเกินจริงในวิกฤต เสริม `/stress` historical เสมอ
- **Frontier เป็น random-weight approximation** (ไม่ใช่ QP-exact) แต่ reproducible · ไวต่อ μ/σ/ρ มาก
- **Simulation = ช่วงความเป็นไปได้ภายใต้สมมติฐาน ไม่ใช่พยากรณ์** — ระบุสมมติฐาน (μ, σ, ρ, horizon, seed) ทุกครั้ง
- ตรงเรื่องความเสี่ยง ไม่ปลอบใจ ไม่ขายฝัน · เป็นกรอบวิเคราะห์เชิงการศึกษา **ไม่ดำเนินการลงทุนแทนผู้ใช้รายบุคคล**

## Disclaimer

เครื่องมือนี้เป็น **กรอบวิเคราะห์ความเสี่ยงเชิงการศึกษา ไม่ใช่คำแนะนำการลงทุนรายบุคคล** ตัวเลขในตัวอย่างเป็นค่าประมาณเชิงสาธิต (illustrative) ผลจำลอง (Monte Carlo / frontier) เป็นช่วงความเป็นไปได้ภายใต้สมมติฐาน ไม่ใช่การพยากรณ์ ผู้ใช้ควร verify ข้อมูลล่าสุดและพิจารณาบริบทภาษี/สภาพคล่อง/เป้าหมายของตนเองก่อนตัดสินใจ

---

อ้างอิง: [README ของปลั๊กอิน](../plugins/portfolio-risk-architect/README.md)
