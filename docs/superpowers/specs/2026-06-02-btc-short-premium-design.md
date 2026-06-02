# Design — `btc-short-premium` plugin

- **Date:** 2026-06-02
- **Status:** Approved (brainstorm) → ready for implementation plan
- **Author:** มูกิ C (สำหรับนายท่าน)
- **Marketplace:** `earthh-evans-finance`
- **Source docs:** `source/MasterPlaybook_v2_Complete.pdf` (52 หน้า) + `source/AI_Commands_Pack (1).pdf` (21 หน้า)

---

## 1. Overview

Plugin ตัวที่ 3 ของ marketplace `earthh-evans-finance` — แปลงระบบเทรด **BTC Daily Short Premium** (ขาย Call/Put รายวันบน Bybit เก็บ premium) ของ Earthh Evans เป็น Claude Code plugin เต็มชุด เข้าชุดกับ `portfolio-risk-architect` และ `deep-o-stock-analyst`.

**Source 2 ไฟล์เป็นคู่กัน:**
- **Master Playbook v2.0** = knowledge base (Concepts, Technical Framework, Field Notes 13 วัน, AI Skill Activation)
- **AI Commands Pack** = ready-to-use prompts 3 Tier (System Prompt / Daily Trigger / Special Triggers)

**ความต่างหลักจาก 2 plugins เดิม:** ระบบนี้เป็น **vision-based** (user แคปรูป 5 ภาพส่งให้ AI อ่าน) ไม่ใช่ search-based เต็มตัวแบบ DEEP+O.

---

## 2. Decisions (เคาะกับนายท่านแล้ว)

| # | ประเด็น | ตัดสินใจ |
|---|---------|----------|
| 1 | Scope | **เต็มชุด** — agent + 9 commands + skill + README + plugin.json (เข้าชุด 2 ตัวเดิม) |
| 2 | Input model | **Hybrid** — user แนบรูป/พิมพ์ตัวเลข + AI ใช้ WebSearch เฉพาะ macro calendar (FOMC/CPI/NFP) + sanity ราคา BTC. **ไม่** ดึงข้อมูลที่ต้อง login (Bybit option chain / CoinGlass real-time) |
| 3 | Commands | **9 ตัว** — Core 7 (Triggers) + `/strike` + `/checklist` |
| 4 | ชื่อ plugin | **`btc-short-premium`** |
| 5 | Architecture | **Agent-centric** — agent เก็บ framework เต็ม, commands thin self-contained, skill routing (ตาม pattern deep-o เป๊ะ) |
| 6 | model | **opus** (ตาม 2 ตัวเดิม) |
| 7 | Disclaimer | **เข้มกว่า** 2 ตัวเดิม (short crypto options เสี่ยงสูง: ขาดทุน > premium, paper trade ≥ 2 สัปดาห์) |

---

## 3. Architecture — File Tree

```
plugins/btc-short-premium/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── agents/
│   └── btc-short-premium.md          # Senior Option Trader — framework เต็ม
├── commands/
│   ├── full.md                       # /full      Full Daily Analysis 6 ขั้น
│   ├── quick.md                      # /quick     regime check เร็ว
│   ├── position.md                   # /position  เช็ค position เปิดอยู่
│   ├── compare.md                    # /compare   Short Call vs Put
│   ├── verify.md                     # /verify    ตรวจ signal AI อื่น
│   ├── anomaly.md                    # /anomaly   Mark Price anomaly
│   ├── pin.md                        # /pin       Pin risk decision
│   ├── strike.md                     # /strike    เลือก strike + SD calc
│   └── checklist.md                  # /checklist 8-Check + No-Trade gate
└── skills/
    └── btc-short-premium/
        └── SKILL.md
```

---

## 4. Data Flow (Hybrid)

```
นายท่าน ── แคป 5 รูป (CoinGlass / Bybit Option Chain / TradingView D-4H-1H) หรือพิมพ์ตัวเลข
            │
            ▼
        /command (เช่น /full)
            │
            ├─→ [Read]      AI อ่านรูป → extract: price, funding, OI, liq, IV, HV, delta, premium ...
            ├─→ [WebSearch] เช็ค macro calendar วันนี้ (FOMC/CPI/NFP) + sanity ราคา BTC ปัจจุบัน
            │               (เฉพาะ /full /quick /verify /checklist)
            ▼
        6-step framework
            │
            ▼
        Output: TRADE / SKIP / WAIT + (ถ้า TRADE) strike / size / entry / SL(Index Price)
```

**5 รูปที่ระบบต้องการ** (source หน้า 6–9): (1) CoinGlass Derivatives BTC row · (2) Bybit Option Chain expiry วันนี้ · (3) TradingView Daily · (4) TradingView 4H · (5) TradingView 1H.

---

## 5. Agent Design — `agents/btc-short-premium.md`

**Frontmatter:**
```yaml
name: btc-short-premium
description: >
  Senior Option Trader — Bybit BTC Daily Short Premium desk. วิเคราะห์ setup
  จากรูป 5 ภาพ (CoinGlass/OptionChain/D-4H-1H) ตามกรอบ 6 ขั้น → TRADE/SKIP/WAIT
  พร้อม strike/size/entry/SL. เช็ค macro (FOMC/CPI/NFP) อัตโนมัติ. เชิงการศึกษา
  ไม่ใช่คำแนะนำลงทุนรายบุคคล.
tools: Read, WebSearch, WebFetch
model: opus
```

**โครงเนื้อหา (ยกจาก source):**

| Section | เนื้อหา | ที่มา |
|---------|---------|------|
| ROLE | Senior Option Trader · Bybit BTC Daily Options · Thai-English desk-note tone · no emotional bias | System Prompt [ROLE] |
| MANDATORY MACRO CHECK | ก่อนวิเคราะห์ทุกครั้ง: WebSearch ปฏิทิน FOMC/CPI/NFP วันนี้ + sanity ราคา BTC · ถ้าตรงวันประกาศ → SKIP | Hybrid (เพิ่มเอง) |
| 6-STEP METHODOLOGY | Snapshot → 8-Check → No-Trade → Combination Read → Verdict → Action | System Prompt [METHODOLOGY] |
| 8-CHECK FRAMEWORK | (ดู §9.1) | Playbook 2.3 |
| NO-TRADE RULES (7) | (ดู §9.2) | Playbook 2.4 |
| COMBINATION READ (4) | (ดู §9.3) | Playbook 1.4 / 3 |
| STRIKE SELECTION | (ดู §9.4) | Playbook 2.5 |
| CRITICAL RULES (ห้าม override) | (ดู §9.5) | System Prompt [CRITICAL] |
| SL METHOD | Index Price เท่านั้น · Call: Strike−$500 · Put: Strike+$500 · RR 1:2 · Market order · Pin exit 13:30 TH | Playbook 2.6 / 3.2 / 3.7 |
| OUTPUT FORMAT | 6-step structure · อ้างตัวเลขจริงจากรูป · cite data · ห้าม approximate · commit ทิศทาง | System Prompt [OUTPUT] |
| FIELD-NOTE GUARDRAILS | บทเรียน 1 (Mark Price ปลอม→ใช้ Ask/Index) · 2 (Combination > indicator เดี่ยว) · 3 (รอ Liq<$50M) · 6 (Pin exit 13:30) | Playbook 3.2–3.7 |
| COMMANDS | list slash ทั้ง 9 | (เหมือน deep-o) |
| Disclaimer | (ดู §8) | Playbook คำเตือน |

---

## 6. Commands Design

ทุก command: frontmatter (`description` / `allowed-tools` / `model: opus`) + sections (`# /btc-short-premium:<cmd>` · Input ที่ต้องการ · สิ่งที่ทำ · ตัวอย่างสั่ง · Discipline). Thin + self-contained.

| Command | allowed-tools | Input | สิ่งที่ทำ (Output) | ที่มา |
|---------|--------------|-------|-------------------|------|
| `/full` | Read, WebSearch, WebFetch | 5 รูป + macro view + portfolio size | 6-step เต็ม → TRADE/SKIP/WAIT + strike/size/entry/SL | Daily Trigger v1 |
| `/quick` | Read, WebSearch | CoinGlass + 1H chart | regime (quiet/recovery/cascade) → ควร full ต่อ หรือ skip | Daily Trigger v2 |
| `/position` | Read | position ปัจจุบัน + option chain + 1H | safe/danger zone → hold/close/adjust + TP zone | Trigger A |
| `/compare` | Read | Short Call [X] vs Short Put [Y] + macro + 5 รูป | aligned / RR / PoP → แนะนำพร้อมเหตุผล | Trigger B |
| `/verify` | Read, WebSearch | signal จาก bot/AI อื่น + 5 รูป | เทียบ 8-Check + No-Trade + Combination → ตาม/override | Trigger C |
| `/anomaly` | Read | position + Mark/Unrealized Loss + spot + chain | จริงหรือ noise → ดู Ask + Index → hold/close | Trigger D |
| `/pin` | Read | position + spot + distance + premium + 1H + เวลา | gamma squeeze risk → ปิดทันที / hold 13:30 / hold settle | Trigger E |
| `/strike` | Read | regime + spot + IV + option chain | SD calc + delta sweet spot + size by regime → strike | Playbook 2.5 + 3.5 |
| `/checklist` | Read, WebSearch | 5 รูป (หรือตัวเลข) | 8-Check ทีละข้อ + No-Trade 7 ข้อ → pass/fail gate | Playbook 2.3 + 2.4 |

**allowed-tools rationale:** เฉพาะ `/full /quick /verify /checklist` ที่ต้องเช็ค macro จึงได้ `WebSearch` · ที่เหลือ vision/คำนวณล้วน → `Read` พอ (ไม่เปิดสิทธิ์เกินจำเป็น).

---

## 7. Skill, Manifest, README

### 7.1 `skills/btc-short-premium/SKILL.md`
```yaml
name: btc-short-premium
description: >
  Use when ... BTC daily option, short premium, ขาย call/put เก็บ premium, Bybit
  option, IV/HV ratio, combination read, funding rate, liquidation, pin risk, theta
  decay ... → route ไป command ที่เหมาะ. เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล.
```
เนื้อหา: สรุประบบ + ตาราง routing สถานการณ์→command (ยกจาก Quick Reference Card หน้า 21).

### 7.2 `.claude-plugin/plugin.json`
```jsonc
{
  "name": "btc-short-premium",
  "version": "0.1.0",
  "description": "Senior Option Trader desk — Bybit BTC Daily Short Premium (ขาย Call/Put รายวันเก็บ premium). วิเคราะห์ 6 ขั้นจากรูป 5 ภาพ → TRADE/SKIP/WAIT พร้อม strike/size/entry/SL(Index Price). agent + 9 commands + skill. เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล. เรียบเรียงจาก Earthh Evans · Invest Hub.",
  "repository": "https://github.com/mrunknown2/Earthh-Evans-Finance-Skill",
  "license": "MIT",
  "author": { "name": "mrunknown2" },
  "keywords": ["btc","bitcoin","option","short-premium","theta","bybit","daily-option","iv-hv","combination-read","pin-risk","earth-evans"]
}
```

### 7.3 `marketplace.json` changes (minimal)
- เพิ่ม entry ตัวที่ 3 ใน array `plugins` (name/source/description/version/keywords ตาม pattern เดิม)
- อัปเดต `metadata.description` ให้สะท้อน 3 plugins (เดิมเขียน "Plugin แรก: portfolio-risk-architect" → ปรับให้ครอบคลุม)
- bump `metadata.version` `0.1.0` → `0.2.0` (next minor — เพิ่ม plugin = feature release)

### 7.4 `README.md`
แนะนำระบบ · ตาราง 9 commands · workflow ตอนเช้า (07:00 TH timeline จาก Playbook 0.5) · ⚠️ disclaimer.

---

## 8. Disclaimer (เข้มกว่า 2 ตัวเดิม)

ใส่ในทุก surface (agent, README, commands):
- **ขาดทุนได้มากกว่า premium ที่เก็บ** — short option มี risk ไม่จำกัด/สูง
- crypto volatility สูง + liquidation/gamma squeeze risk
- **Paper trade ≥ 2 สัปดาห์ ก่อนใช้เงินจริง** · เริ่ม size 0.5–1% (ตรงจาก source)
- เชิงการศึกษา · **ไม่ใช่คำแนะนำลงทุนรายบุคคล** · verdict = framework signal ไม่ใช่คำสั่งซื้อขาย
- ผู้ใช้ต้อง verify ข้อมูล real-time เอง + พิจารณาบริบทตนเอง

---

## 9. Framework Reference (ตัวเลข/เกณฑ์จาก source — ใช้ตอน implement)

### 9.1 8-Check Framework (Playbook 2.3)
| # | Check | เกณฑ์ผ่าน |
|---|-------|-----------|
| 1 | Macro Event | ไม่มี FOMC/CPI/NFP ก่อน settle |
| 2 | IV/HV Ratio | ≥ 1.15 (ideal > 1.5) |
| 3 | SD Distance | Strike > 1.5 SD จาก spot |
| 4 | Funding Rate | Neutral zone (±0.01%) |
| 5 | Delta | 0.13–0.15 (sweet spot) |
| 6 | Resistance/Support | Strike confluence กับ MA/level |
| 7 | ATR Filter | Strike > 1.5× ATR 4H |
| 8 | Combination Read | ไม่ติด pattern อันตราย |

> กฎ: ขาด 1 ข้อ = ลด size หรือ skip.

### 9.2 No-Trade Rules — 7 ข้อห้ามแตะ (Playbook 2.4)
1. FOMC/CPI/NFP day = SKIP เสมอ
2. IV < HV (ratio < 1.0) = SKIP (ไม่มี edge)
3. BTC rallied 5%+ วันก่อน = SKIP (vol expansion)
4. ขาดทุน 3 ครั้งติด = หยุด 2–3 วัน
5. Active liquidation event > $200M = SKIP
6. Funding < −0.03% = SKIP Short Call (squeeze risk)
7. Gut uncertainty = SKIP

### 9.3 Combination Read — 4 patterns (Playbook 1.4 / 3)
| Pattern | สัญญาณ | Action |
|---------|--------|--------|
| 1 Bullish Accumulation | Price↑ + Volume↑ + OI↑ | Short Put อาจเหมาะ · Short Call เสี่ยง |
| 2 Long Capitulation | Price↓ + Vol↑↑ + OI↓ + Liq>$200M | **SKIP** — รอ Liq<$50M |
| 3 New Shorts Piling | Price↓ + Volume↑ + OI↑ | Short Call OK (aligned) |
| 4 Quiet Deleveraging | flat + Vol↓ + OI↓ + Liq↓ | เปิดได้ทั้ง Call/Put ตาม macro |

> หลักการ: อ่าน Price + Volume + OI + Liquidation **พร้อมกัน** — ตัวเลขเดี่ยวไม่บอกอะไร.

### 9.4 Strike Selection by Regime (Playbook 2.5)
| Regime | Strike Distance | Delta | Size |
|--------|----------------|-------|------|
| Quiet (Liq < $50M) | 1.5–2 SD | 0.13–0.15 | Full |
| Borderline ($50–150M) | 2–2.5 SD | 0.08–0.12 | 70% |
| Recovery (post-cascade) | 2.5+ SD | 0.05–0.08 | 50% |
| Macro event nearby | 3+ SD or skip | < 0.05 | 30% or skip |

### 9.5 Critical Rules — AI ห้าม override (System Prompt / Quick Ref)
- Liquidation > $200M = **SKIP เสมอ** (ไม่ว่าอะไรก็ดูแค่ไหน)
- Liquidation $50–200M = caution, reduce size 30–50%
- IV/HV < 1.15 = SKIP (no edge)
- SD distance < 1.5 = SKIP (ใกล้ spot เกิน)
- FOMC/CPI/NFP day = SKIP
- 3 consecutive losses = pause 2–3 days
- Funding < −0.03% = SKIP Short Call

### 9.6 SL Method (Playbook 2.6 / 3.2)
- **ใช้ Index Price เสมอ** (ห้าม Mark Price — มัน inflate จาก IV spike)
- Short Call SL trigger: Index Price = Strike − $500
- Short Put SL trigger: Index Price = Strike + $500
- RR 1:2 (max loss = 2× premium) · Order Type: Market
- Pin Risk Exit: ปิด position 13:30 TH (90 นาทีก่อน settle 15:00 — เลี่ยง TWAP gamma squeeze)

### 9.7 Reference thresholds
- **IV/HV (Playbook 1.3):** <1.0 SKIP · 1.0–1.15 borderline · 1.15–1.5 OK · >1.5 sweet spot
- **Funding zones (1.5):** <−0.03% short crowded (SKIP Short Call) · ±0.01% neutral SAFE · >+0.03% long crowded (SKIP Short Put)
- **Liquidation tiers (1.6):** <$50M safe · $50–150M borderline · $150–200M pre-cascade SKIP · >$200M cascade ห้ามเทรด
- **SD Distance calc (3.5):** Daily (24h) SD = Spot × IV × √(1/365) · ตัวอย่าง BTC $74,000 · IV 30% → SD ≈ $1,162 · Strike ต้องห่าง > 1.5 SD
- **Strategy targets (2.1):** Win Rate 85–93% (รวม SL) · Delta 0.13–0.15 · RR 1:2 · TTE 8–24h · size 2–3% portfolio · target $10–30/วัน
- **Settlement (2.2):** 08:00 UTC (15:00 TH) ทุกวัน · settle price = avg BTC Index Price 30 นาทีสุดท้าย (TWAP)

---

## 10. Verification Plan

Plugin = markdown (ไม่มี unit test). Verify เชิงโครงสร้าง:
1. `plugin.json` + `marketplace.json` parse เป็น JSON ได้ (ไม่พัง)
2. โครงไฟล์ครบตาม §3 · ทุก command/agent มี frontmatter ถูก format
3. `marketplace.json` มี entry `btc-short-premium` ครบ field (name/source/description/version/keywords)
4. รัน `/misc:deps-check` scan broken cross-plugin references
5. เทียบ structure กับ `deep-o-stock-analyst` ว่า parity (ไฟล์ครบ, frontmatter pattern ตรง)

---

## 11. Out of Scope (YAGNI)

- ❌ ไม่ดึงข้อมูลที่ต้อง login (Bybit option chain / CoinGlass real-time) — user แคปรูป
- ❌ ไม่ทำ command `/sl` แยก (รวมใน `/strike` + `/position`)
- ❌ ไม่ทำ auto-trade / order execution — plugin เป็น analysis/advisory เท่านั้น
- ❌ ไม่ทำ backtest engine / journal storage
- ❌ ไม่แตะ 2 plugins เดิม (นอกจากเพิ่ม entry ใน marketplace.json)
