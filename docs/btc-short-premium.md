# BTC Short Premium — Playbook การใช้งาน

> เดสก์ขาย Call/Put รายวันบน Bybit เก็บ premium จาก theta decay — วิเคราะห์ 6 ขั้นจากรูป 5 ภาพ (CoinGlass · Bybit Option Chain · TradingView D/4H/1H) → ออก verdict **TRADE / SKIP / WAIT** พร้อม strike/size/entry/SL ที่ Index Price

## ติดตั้ง

```
/plugin install btc-short-premium
```

(ถ้ายังไม่ได้เพิ่ม marketplace: `/plugin marketplace add mrunknown2/Earthh-Evans-Finance-Skill` ก่อน)

## Quickstart — เริ่มเร็วสุด

คำสั่งเริ่มต้นที่ README แนะนำคือ **`/full`** — Full Daily Analysis 6 ขั้น ออก TRADE/SKIP/WAIT + strike/size/entry/SL

สิ่งที่ต้องแนบตอนรัน `/full`:
- **รูป 5 ภาพ** — CoinGlass · Bybit Option Chain · TradingView Daily · 4H · 1H
- **Macro view** — bearish / bullish / neutral (ความเห็นนายท่าน)
- **Portfolio size** — ขนาดพอร์ตเป็น USD (ใช้คำนวณ size)

ตัวอย่างจริง (จาก `full.md`):

```
/full
[แนบรูป 5 ภาพ: CoinGlass, OptionChain, Daily, 4H, 1H]
macro view: bearish, portfolio $8K
```

> เคล็ด: รัน `/quick` ก่อนแคปรูปครบ เพื่อกรองวันที่ไม่ควรเทรดออกเร็ว (ประหยัดเวลา)

## เตรียมข้อมูลก่อนใช้ (Inputs)

ระบบนี้เป็น **vision-based** — นายท่านแคปรูปส่งให้ AI อ่านเอง ไม่ดึงข้อมูล real-time อัตโนมัติ

**รูป 5 ภาพที่ต้องแคป (ชื่อจริงจาก SKILL/README):**

| # | รูป | ข้อมูลที่ AI อ่าน |
|---|-----|------------------|
| 1 | **CoinGlass Derivatives** — แถว BTC | OI, Volume 24h, Liquidation 24h, Funding Rate |
| 2 | **Bybit Option Chain** — expiry วันนี้ | Strike, IV, delta, bid/ask, premium, OI รายตัว |
| 3 | **TradingView Daily** | trend, support/resistance หลัก, MA50/200, ATR(14) |
| 4 | **TradingView 4H** | swing structure, ATR 4H, volume profile |
| 5 | **TradingView 1H** | momentum เข้า/ออก, ระยะ pin risk ก่อน settle |

**ข้อมูลอื่นที่บางคำสั่งต้องมี:** macro view (bearish/bullish/neutral), portfolio size / equity (USD), risk%, IV, HV, spot, distance from strike, entry premium, premium ปัจจุบัน (Ask), เวลาปัจจุบัน (TH)

**IMAGE COMPLETENESS GATE (สำคัญ):** ถ้าขาดภาพใด หรืออ่านค่าสำคัญไม่ออก (spot, IV, HV, liq, funding, delta, premium) → **WAIT/SKIP ห้ามเดาแล้วออก TRADE** — ภาพไม่ครบ = ห้ามเดา verdict

## คำสั่งทั้งหมด

| คำสั่ง | ทำอะไร | Input |
|--------|--------|-------|
| `/full` | Full Daily Analysis 6 ขั้น → TRADE/SKIP/WAIT + strike/size/entry/SL (เริ่มต้นแนะนำ) | รูป 5 ภาพ + macro view + portfolio size (USD) |
| `/quick` | Quick Morning Check ~2 นาที → อ่าน regime (quiet/recovery/cascade) → ควรเปิด `/full` ต่อ หรือ skip วันนี้ | CoinGlass BTC row + TradingView 1H |
| `/position` | มี position เปิดอยู่ → safe/danger zone → hold/ปิดกำไร/ปิดขาดทุน/adjust + TP zone | Position ปัจจุบัน (strategy, strike, entry premium, spot ตอนเปิด, time to expiry) + Option Chain + 1H |
| `/compare` | เทียบ Short Call vs Short Put 3 มุม (aligned/RR/PoP) → แนะนำ leg ที่ edge ดีกว่า | Option 1 (Short Call) + Option 2 (Short Put) พร้อม premium/IV/delta + macro view + รูป 5 ภาพ |
| `/verify` | ตรวจ signal จาก bot/AI อื่นกับ 8-Check + No-Trade + Combination Read → ตาม signal หรือ override | Signal จาก bot/AI (strike, direction, เหตุผล) + รูป 5 ภาพ |
| `/anomaly` | Mark Price / Unrealized Loss แปลกๆ → noise หรือ loss จริง (ดู Ask + Index Price) → hold/close | Position + Mark Price + Unrealized Loss% + spot + Option Chain (bid/ask ของ strike ที่ถือ) |
| `/pin` | ใกล้ 13:30 TH → gamma squeeze risk → ปิดทันที / hold ถึง 13:30 / hold ถึง settle 15:00 | Position + spot + distance from strike + premium ปัจจุบัน + entry premium + 1H + เวลา (TH) |
| `/strike` | เลือก strike ตาม regime + คำนวณ SD distance + delta sweet spot + size | Regime (หรือ Liquidation level) + spot + IV% + Bybit Option Chain |
| `/checklist` | Pre-Trade Gate — เดิน 8-Check + No-Trade Rules 7 ข้อทีละข้อ → pass/fail | รูป 5 ภาพ หรือพิมพ์ตัวเลขดิบแทน (Liq, Funding, IV, HV, ATR ฯลฯ) |

## Workflow ที่ใช้บ่อย

**1) อ่านชุดเต็มตอนเช้า (07:00 TH) — `/full`**

```
07:00  เปิด Bybit · CoinGlass · TradingView · ForexFactory
07:05  แคป 5 รูป (CoinGlass → Option Chain → D → 4H → 1H)
07:10  /full  (แนบ 5 รูป + macro view + portfolio size)
       TRADE? → เปิด position + ตั้ง SL ที่ Index Price ทันที
       SKIP?  → ปิด session · บันทึกเหตุผล
       WAIT?  → กลับมาเช็ค /quick อีกครั้งใน 1–2 ชม.
13:30  /pin — ตัดสินใจ pin risk (ปิดก่อน หรือถือถึง settle)
15:00  Settle — avg BTC Index Price 30 นาทีสุดท้าย (TWAP)
```

> สามารถรัน `/checklist` คู่ขนานกับ `/full` เพื่อ double-check gate ก่อนกด confirm

**2) เลือก strike + size — `/strike`**

แนบ regime + spot + IV + Option Chain → engine คำนวณ SD distance → map ตามตาราง regime (Quiet 1.5–2 SD / delta 0.13–0.15 / Full size … ถึง Macro event 3+ SD or skip) → ระบุ strike + bid/ask + delta จากรูปจริง

```
/strike
regime: quiet | spot: 74000 | IV: 30%
[แนบรูป Bybit Option Chain]
```

**3) เช็ค pin risk ก่อนหมดอายุ — `/pin`**

ใกล้ 13:30 TH แนบ position + spot + distance + premium ปัจจุบัน + เวลา → engine คำนวณ `sd` ห่าง strike + `close_now` (true ถ้า < 0.3 SD) → ตัดสิน ปิดทันที / hold ถึง 13:30 แล้วประเมินใหม่ / hold ถึง settle

```
/pin
Short Call 78000 | entry premium 450 | premium ตอนนี้ 180
BTC spot: 77850 | distance: 150
เวลา: 13:00 TH
[แนบรูป 1H]
```

## อ่านผลลัพธ์ยังไง

- **Verdict (TRADE / SKIP / WAIT):** เป็น framework signal ต้อง commit ทิศทาง (ห้าม "it depends") — **ไม่ใช่คำสั่งซื้อขาย** · WAIT = ภาพไม่ครบ/รอ setup ชัดขึ้น · SKIP = ติด No-Trade Rule หรือไม่มี edge
- **IV/HV gate (zone):** อ้างจาก engine — `skip` (< 1.0, no edge) · `borderline` (1.0–1.15) · `ok` (1.15–1.5) · `sweet` (> 1.5) · `tradeable = true` เมื่อ ratio ≥ 1.15 · **IV/HV < 1.15 = SKIP** (< 1.0 = hard floor ห้ามขาย)
- **SD distance:** strike ต้อง **> 1.5 SD จาก spot** (`passes_1_5 = true`) จึงผ่าน Check #3 · **SD distance < 1.5 = SKIP** (ใกล้ spot เกิน)
- **Position size:** engine คืน `margin_at_risk`, `max_contracts`, `suggested_contracts` และ `above_default_band` (เตือนถ้า risk_pct > 1%) — default band คือ **0.5–1% ของ equity**
- **Pin distance:** engine คืน `sd` (กี่ SD ห่าง strike) + `close_now` — `close_now = true` เมื่อ < 0.3 SD → ถ้าถึง 13:30 TH **ปิด position ทันที** (90 นาทีก่อน settle 15:00)
- **No-Trade Rules / Critical Rules (= SKIP เสมอ):**
  - Liquidation **> $200M** = SKIP · **$50–200M** = caution ลด size 30–50% · Active liq ≥ $150M = SKIP (pre-cascade)
  - **IV/HV < 1.15** = SKIP · **SD distance < 1.5** = SKIP
  - **FOMC/CPI/NFP day** = SKIP · BTC rallied 5%+ วันก่อน = SKIP
  - **Funding < −0.03%** = SKIP Short Call · **> +0.03%** = SKIP Short Put
  - **3 ขาดทุนติด** = pause 2–3 วัน · Gut uncertainty / ภาพไม่ครบ = SKIP/WAIT
  - **SL ใช้ Index Price เสมอ** (ห้าม Mark Price)
- **Regime (`/quick`):** quiet (edge ดี → `/full`) · recovery (รอ settle ก่อน) · cascade (Liq > $200M หรือ Funding spike → SKIP ทันที ไม่ต้องแคปครบ 5 รูป)

## Engine — เลขไม่เดา

การคำนวณเชิงปริมาณวิ่งผ่าน `skills/btc-short-premium/scripts/btc_calc.py` (Python 3 stdlib ล้วน · ไม่ต้อง `pip install` · deterministic) — **โมเดลอ่านรูป + ตัดสิน, engine คำนวณเลขความเสี่ยง/ขนาด** ห้ามคิดเลขในหัว

4 modes:
- **`sd`** — daily SD (`Spot · IV · √(days/365)`) + SD distance + `passes_1_5` (> 1.5 SD)
- **`iv_hv`** — IV/HV gate → `ratio`, `zone`, `tradeable` (≥ 1.15)
- **`size`** — position sizing (margin-at-risk) → short option ไม่ cap ที่ premium จึง size บนสมมติฐาน max loss = `max_loss_mult × premium` (default 3×)
- **`pin`** — pin-risk proximity → `sd` + `close_now` (< 0.3 SD, scale กับ IV ไม่ใช่ $ ตายตัว)

เรียกใช้:

```bash
echo '<JSON>' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/btc-short-premium/scripts/btc_calc.py"
```

ตัวอย่างจาก reference: Spot $74,000 · IV 30% → daily_sd ≈ **$1,162** · strike $76,000 → 1.72 SD (ผ่าน) · schema เต็มดูที่ `skills/btc-short-premium/references/btc-calc.md`

> ขอบเขต engine: ไม่อ่านรูป · ไม่ดึงข้อมูล real-time · ไม่ตัดสิน TRADE/SKIP/WAIT — แค่คำนวณ gate ให้โมเดลตัดสิน

## ข้อควรระวัง / วินัย

**สำคัญ:**
- **ขาย option = ความเสี่ยงหางไม่จำกัด (uncapped tail)** — ขาดทุนได้มากกว่า premium ที่เก็บ โดยเฉพาะ naked short call · ขาดทุนจริงไม่ cap ที่ 2× premium
- **margin / liquidation** — บัญชีถูก force-liquidate ได้ก่อน SL ที่ Index Price จะถึง · crypto volatility สูง + liquidation cascade + gamma squeeze ทำให้ position กลับทิศเร็วมาก
- **No-Trade Rules / Critical Rules — AI ห้าม override** (Liq > $200M, IV/HV < 1.15, SD < 1.5, FOMC/CPI/NFP, funding extremes, 3 losses) — แม้ setup ดูดีแค่ไหน
- **Size cap จริง:** เริ่ม **0.5–1% ของพอร์ต** เท่านั้น จน **paper trade ≥ 2 สัปดาห์ผ่าน** · ขยับขึ้นหลังชนะ ≥ 10 trade ติดกัน · เพดาน 2–3% เฉพาะมี track record
- **SL = Index Price เสมอ** (ห้าม Mark Price) · Pin exit 13:30 TH ก่อน TWAP settle 15:00 TH
- verdict (TRADE/SKIP/WAIT) คือ framework signal **ไม่ใช่คำสั่งซื้อขาย** · ผู้ใช้ต้อง verify ข้อมูล real-time เองก่อนตัดสินใจ

## Disclaimer

เนื้อหานี้เป็นกรอบวิเคราะห์ **เชิงการศึกษา ไม่ใช่คำแนะนำการลงทุนรายบุคคล** · การขาย option มีความเสี่ยงขาดทุนสูง/หางไม่จำกัด (ขาดทุนเกิน premium ที่เก็บได้) · crypto มี volatility สูงผิดปกติ + liquidation/gamma squeeze เกิดได้รวดเร็ว · paper trade ≥ 2 สัปดาห์ก่อนใช้เงินจริง · ผู้ใช้รับผิดชอบผลการเทรดเองทั้งสิ้น · เรียบเรียงจาก **Earthh Evans · Invest Hub**

---

← กลับไป [plugin README](../plugins/btc-short-premium/README.md)
