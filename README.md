# Earthh-Evans-Finance-Skill

Claude Code **plugin marketplace** ที่แปลงความรู้การลงทุนของ **Earth Evans** (Invest Hub) ให้เป็น skill / agent / command ใช้งานได้จริง — institutional-quality content สำหรับ retail investor ออกแบบให้ port ไป provider อื่น (Gemini / ChatGPT) ได้ในอนาคต

> เนื้อหาทุก plugin เป็น **กรอบวิเคราะห์เชิงการศึกษา ไม่ใช่คำแนะนำการลงทุนรายบุคคล**

## Plugins

| Plugin | ขอบเขต | ส่วนประกอบ |
|---|---|---|
| [`portfolio-risk-architect`](plugins/portfolio-risk-architect) | วินิจฉัย & ออกแบบความเสี่ยง **พอร์ตรวม** multi-asset (Equity/ETF/Crypto) — look-through, risk contribution, correlation, stress test, Monte Carlo, frontier, rebalance | 1 skill + 1 agent + **9 commands** |
| [`deep-o-stock-analyst`](plugins/deep-o-stock-analyst) | วิเคราะห์ **หุ้นรายตัว (US)** ด้วยกรอบ **DEEP+O** (Demand/Execution/Economics/Price/Optionality) สไตล์ Damodaran + McKinsey — DCF → intrinsic value, reverse DCF, option-adjusted valuation, DEEP score → verdict ซื้อ/ถือ/ลด/ขาย | 1 skill + 1 agent + **10 commands** |
| [`btc-short-premium`](plugins/btc-short-premium) | เดสก์ **BTC Daily Short Premium** บน Bybit (ขาย Call/Put รายวันเก็บ premium) — วิเคราะห์ 6 ขั้นจาก **รูป 5 ภาพ** (CoinGlass / Option Chain / TradingView D-4H-1H) → **TRADE/SKIP/WAIT** + strike/size/entry/SL (Index Price) · 8-Check · No-Trade Rules · Combination Read · Pin risk | 1 skill + 1 agent + **9 commands** |
| [`reverse-dcf-screener`](plugins/reverse-dcf-screener) | ถอดความคาดหวังที่ราคาฝัง — **Terminal-Anchored Reverse DCF** หุ้นถูก/แพง + โซนราคา — **Market-Implied CAGR** เทียบ **Plausible CAGR** → Gap → ถูก/Fair/แพง + โซนราคา 4 ระดับ · กรอกงบจริงลง Excel template + verify 2 รอบ · portable (Claude Code/Codex/Antigravity) | 1 skill + 1 agent + **9 commands** |

> สี่ตัว **เสริมกัน ไม่ทับหน้าที่**: `deep-o-stock-analyst` เจาะหุ้นเดี่ยว (US equity) · `portfolio-risk-architect` มองความเสี่ยงทั้งพอร์ต multi-asset · `btc-short-premium` เดสก์เทรด crypto options รายวัน (vision-based) · `reverse-dcf-screener` วัด "ความคาดหวัง" ที่ราคาฝัง (expectation investing) ผ่าน Excel engine

## Deterministic engines — เลขเงินไม่เดา

เรื่องเงินๆ ทองๆ ต้องผิดน้อยที่สุด ทุก plugin จึงมี **engine เป็น Python stdlib-only** (ไม่พึ่ง numpy/scipy → portable ทุก IDE / Codex / Antigravity) ที่รันเลขแบบ **deterministic** — โมเดลแค่ดึงข้อมูล + ตีความ ส่วนคณิตศาสตร์การเงินวิ่งผ่าน script ที่ตายตัว (Monte Carlo / frontier ใช้ seeded RNG → ทำซ้ำผลได้) คุมความถูกต้องด้วย known-answer test

| Plugin | Engine | คำนวณ | Tests |
|---|---|---|---|
| portfolio-risk-architect | `portfolio_engine.py` | risk contribution, diversification ratio, ENB, Monte Carlo (GBM, seeded), efficient frontier, stress | 18 |
| deep-o-stock-analyst | `valuation_engine.py` | WACC (CAPM), DCF, terminal-anchored reverse DCF, DEEP score (0–100) | 12 |
| btc-short-premium | `btc_calc.py` | daily SD, SD distance, IV/HV gate, position sizing, pin distance | 8 |
| reverse-dcf-screener | `fill_engine.py` | Terminal-Anchored implied CAGR, plausible-CAGR caps, price zones, Excel fill/append | 10 |

> รวม **48 known-answer tests** (เลขคำนวณด้วยมือ) ผ่านทั้งหมด · seeded → reproducible · Excel เก็บสูตรไว้ให้ recalc เองตอนเปิด

## ติดตั้ง

```
/plugin marketplace add mrunknown2/Earthh-Evans-Finance-Skill
/plugin install portfolio-risk-architect
/plugin install deep-o-stock-analyst
/plugin install btc-short-premium
/plugin install reverse-dcf-screener
```

## คำสั่งโดยย่อ

**portfolio-risk-architect** — เริ่มที่ `/full`
```
/full · /xray · /overlap · /risk · /corr · /stress · /montecarlo · /frontier · /rebalance
```

**deep-o-stock-analyst** — เริ่มที่ `/full <ticker>`
```
/full · /livecheck · /wacc · /valuation · /reversedcf · /options · /deep · /risk · /catalysts · /onepager
```

**btc-short-premium** — เริ่มที่ `/full` (แนบรูป 5 ภาพ + macro view + portfolio size)
```
/full · /quick · /position · /compare · /verify · /anomaly · /pin · /strike · /checklist
```

**reverse-dcf-screener** — เริ่มที่ `/full <ticker>`
```
/full · /analyze · /verify · /zones · /quick · /screener · /wacc · /sensitivity · /methodology
```

รายละเอียดแต่ละคำสั่งดูใน README ของ plugin: [portfolio-risk-architect](plugins/portfolio-risk-architect/README.md) · [deep-o-stock-analyst](plugins/deep-o-stock-analyst/README.md) · [btc-short-premium](plugins/btc-short-premium/README.md) · [reverse-dcf-screener](plugins/reverse-dcf-screener/README.md)

📖 **คู่มือใช้งานเต็ม (playbook) รายปลั๊กอิน** — ติดตั้ง → เตรียมข้อมูล → คำสั่ง → อ่านผลลัพธ์ → ข้อควรระวัง: [`docs/`](docs/README.md)

## เพิ่ม skill ใหม่ (จาก source ถัดไป)

1. วาง source material (เช่น PDF) ลงโฟลเดอร์ `source/` (gitignored — เก็บ local เท่านั้น)
2. สกัด + เรียบเรียงเป็น plugin ใหม่ใต้ `plugins/<ชื่อ>/` (skills / agents / commands) — เลขเงินทำเป็น **deterministic engine** (`scripts/<engine>.py` + test) ไม่ให้โมเดลปั้นเอง
3. ลงทะเบียน plugin ใหม่ใน `.claude-plugin/marketplace.json`
4. เขียน **playbook** การใช้งานใน `docs/<ชื่อ>.md` · เก็บ design spec/plan ไว้ใน `design/` (internal, gitignored)

## โครงสร้าง

```
.claude-plugin/marketplace.json      # ลงทะเบียน plugin ทั้งหมด
plugins/
  portfolio-risk-architect/          # skill + agent + 9 commands + engine
  deep-o-stock-analyst/              # skill + agent + 10 commands + engine
  btc-short-premium/                 # skill + agent + 9 commands + engine
  reverse-dcf-screener/              # skill + agent + 9 commands + Excel engine
docs/                                # playbook สาธารณะ รายปลั๊กอิน (track เข้า repo)
design/                              # เอกสารออกแบบภายใน specs+plans (gitignored — ไม่ push)
source/                              # source material ดิบ Earth Evans (gitignored)
```

## Changelog

รูปแบบอิง [Keep a Changelog](https://keepachangelog.com) · เวอร์ชันอ้างอิง **marketplace** (แต่ละ plugin มีเวอร์ชันของตัวเองใน `plugin.json`)

### [0.4.0] — 2026-06-03
**Deterministic engines + ความถูกต้องเชิงตัวเลข (review remediation)**
- เพิ่ม **deterministic engine (Python stdlib-only, seeded)** ครบทุก plugin — เลขเงินวิ่งผ่าน script ไม่ให้โมเดลปั้นเอง · รวม **48 known-answer tests**
  - ใหม่: `portfolio_engine.py` · `valuation_engine.py` · `btc_calc.py` (reverse-dcf มี `fill_engine.py` อยู่ก่อนแล้ว)
- แก้บั๊กความถูกต้อง HIGH-severity 6 จุด (H1–H6): DEEP score normalize เป็น 0–100, reverse DCF เปลี่ยนเป็น terminal-anchored, screener chat ตรงกับที่ Excel recalc, BTC size cap / max-loss / image-completeness gate ฯลฯ
- ลบ orphan doc ที่สูตรเก่าไม่ตรง · ทุก plugin → `v0.2.0` · owner → `baewkun`

### [0.3.0] — 2026-06-03
**reverse-dcf-screener — ปลั๊กอินที่ 4**
- เพิ่ม **reverse-dcf-screener** (Terminal-Anchored Reverse DCF): Market-Implied CAGR เทียบ Plausible CAGR → ถูก/Fair/แพง + โซนราคา 4 ระดับ · กรอกงบลง Excel template + verify 2 รอบ · portable
- **screener append mode** — เพิ่มหุ้นลง master Screener sheet (เขียนเฉพาะ input cols ไม่แตะ formula cols) เทียบหลายตัวบนสมมติฐานเดียว
- dependency robustness — เช็ค openpyxl แบบ graceful + คำแนะนำ PEP 668 + `requirements.txt`

### [0.2.0] — 2026-06-02
**btc-short-premium — ปลั๊กอินที่ 3**
- เพิ่ม **btc-short-premium**: เดสก์ขาย Call/Put รายวันบน Bybit เก็บ premium · วิเคราะห์ 6 ขั้นจากรูป 5 ภาพ (CoinGlass / Option Chain / TradingView D-4H-1H) → TRADE/SKIP/WAIT + strike/size/entry/SL · 8-Check + No-Trade Rules + Pin risk

### [0.1.0] — 2026-06-02
**Marketplace bootstrap + 2 ปลั๊กอินแรก**
- เพิ่ม **portfolio-risk-architect**: วินิจฉัยความเสี่ยงพอร์ต multi-asset แบบ look-through (capital weight ≠ risk weight) — risk contribution, correlation, stress test, Monte Carlo, frontier, rebalance
- เพิ่ม **deep-o-stock-analyst**: วิเคราะห์หุ้นรายตัว (US) ด้วยกรอบ DEEP+O สไตล์ Damodaran + McKinsey — DCF, reverse DCF, option-adjusted valuation, DEEP score → verdict
- bootstrap `.claude-plugin/marketplace.json` + guardrails (3-Level Permission Model) + persona มูกิ C

## Disclaimer

เนื้อหาทุก plugin ใน marketplace นี้เป็น **กรอบวิเคราะห์เชิงการศึกษา ไม่ใช่คำแนะนำการลงทุนรายบุคคล** ตัวเลขตัวอย่างเป็นค่าประมาณเชิงสาธิต ผลจำลองเป็นช่วงความเป็นไปได้ภายใต้สมมติฐาน ไม่ใช่การพยากรณ์ · verdict เป็น framework signal ไม่ใช่คำสั่งซื้อขาย ผู้ใช้ควร verify ข้อมูลล่าสุด (10-K/10-Q/IR) และพิจารณาบริบทภาษี/สภาพคล่อง/เป้าหมาย/ความเสี่ยงของตนเองก่อนตัดสินใจ
