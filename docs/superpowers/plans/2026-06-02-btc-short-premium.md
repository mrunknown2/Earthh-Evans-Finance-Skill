# BTC Short Premium Plugin — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** สร้าง Claude Code plugin `btc-short-premium` (ตัวที่ 3 ของ marketplace `earthh-evans-finance`) แปลงระบบเทรด BTC Daily Short Premium ของ Earthh Evans เป็น agent + 9 commands + skill เต็มชุด.

**Architecture:** Agent-centric — `agents/btc-short-premium.md` เก็บ framework เต็ม (6-step, 8-Check, No-Trade, Combination Read, Critical Rules, SL method), commands thin self-contained, skill ทำ routing. Hybrid input: user แคปรูป 5 ภาพ + AI ใช้ WebSearch เฉพาะ macro check. เข้า pattern เดียวกับ `deep-o-stock-analyst` เป๊ะ.

**Tech Stack:** Markdown + YAML frontmatter (Claude Code plugin format) · JSON manifest · ไม่มี runtime code/test — verification = JSON parse + frontmatter validity + structure parity.

**Companion spec (source of truth สำหรับ content/ตัวเลข):** `docs/superpowers/specs/2026-06-02-btc-short-premium-design.md` — โดยเฉพาะ **§5** (agent), **§6** (commands), **§9** (framework reference: ตัวเลข/เกณฑ์ทั้งหมด). ทุก task ที่เขียน framework content ต้องยึดตัวเลขจาก §9 เป๊ะ.

**Conventions (ยึดจาก plugin เดิม `deep-o-stock-analyst`):**
- ภาษาไทย-อังกฤษผสม · desk-note tone
- ทุก command frontmatter: `description` (string) + `allowed-tools` (list) + `model: opus`
- ทุก command มี sections: `# /btc-short-premium:<cmd>` → **Input ที่ต้องการ** → **สิ่งที่ทำ** → **ตัวอย่างสั่ง** → **Discipline**
- ทุก surface ปิดท้ายด้วย disclaimer (spec §8)

**Branch:** ทำบน `feature/btc-short-premium` (สร้างแล้ว). ทุก commit ขออนุญาตนายท่าน per-action (guardrails L2) — ใน plan นี้เขียน `git commit` ไว้เป็นขั้นตอน แต่ผู้ทำต้องขอ OK ก่อน run จริง.

---

## File Structure

```
plugins/btc-short-premium/
├── .claude-plugin/plugin.json          # Task 1
├── agents/btc-short-premium.md         # Task 2  (หัวใจ — framework เต็ม)
├── commands/
│   ├── full.md                         # Task 3
│   ├── quick.md                        # Task 3
│   ├── position.md                     # Task 4
│   ├── compare.md                      # Task 4
│   ├── verify.md                       # Task 4
│   ├── anomaly.md                      # Task 4
│   ├── pin.md                          # Task 4
│   ├── strike.md                       # Task 5
│   └── checklist.md                    # Task 5
├── skills/btc-short-premium/SKILL.md   # Task 6
└── README.md                           # Task 7
.claude-plugin/marketplace.json         # Task 8 (modify — add entry + bump version)
```

แต่ละไฟล์มี responsibility เดียวชัดเจน. Commands กลุ่มเดียวกัน (daily/special/helper) commit ด้วยกันเพราะ change together.

---

## Task 1: Scaffold plugin.json

**Files:**
- Create: `plugins/btc-short-premium/.claude-plugin/plugin.json`

- [ ] **Step 1: สร้าง plugin.json** (เนื้อหาเต็มจาก spec §7.2)

```json
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

- [ ] **Step 2: Verify JSON parse ได้**

Run: `python3 -c "import json; json.load(open('plugins/btc-short-premium/.claude-plugin/plugin.json')); print('OK')"`
Expected: `OK`

- [ ] **Step 3: Verify ตรง pattern deep-o** (เช็ค key ครบ)

Run: `python3 -c "import json; d=json.load(open('plugins/btc-short-premium/.claude-plugin/plugin.json')); assert all(k in d for k in ['name','version','description','license','author','keywords']); print('keys OK')"`
Expected: `keys OK`

- [ ] **Step 4: Commit** (ขอ OK นายท่านก่อน)

```bash
git add plugins/btc-short-premium/.claude-plugin/plugin.json
git commit -m "feat(btc-short-premium): scaffold plugin.json"
```

---

## Task 2: Agent — `btc-short-premium.md` (หัวใจ plugin)

**Files:**
- Create: `plugins/btc-short-premium/agents/btc-short-premium.md`
- Reference: spec §5 (โครง), §9 (ตัวเลข/เกณฑ์ทั้งหมด) — **ยึดตัวเลขจาก §9 เป๊ะ ห้ามแก้**
- Pattern reference: `plugins/deep-o-stock-analyst/agents/deep-o-stock-analyst.md`

- [ ] **Step 1: เขียน frontmatter** (เต็ม ตาม spec §5)

```yaml
---
name: btc-short-premium
description: >
  Senior Option Trader — Bybit BTC Daily Short Premium desk. วิเคราะห์ setup
  จากรูป 5 ภาพ (CoinGlass/OptionChain/D-4H-1H) ตามกรอบ 6 ขั้น → TRADE/SKIP/WAIT
  พร้อม strike/size/entry/SL. เช็ค macro (FOMC/CPI/NFP) อัตโนมัติ. เชิงการศึกษา
  ไม่ใช่คำแนะนำลงทุนรายบุคคล.
tools: Read, WebSearch, WebFetch
model: opus
---
```

- [ ] **Step 2: เขียน body** — ตามลำดับ section นี้ (เนื้อหา/ตัวเลขจาก spec §9):

  1. `# ROLE` — Senior Option Trader · Bybit BTC Daily Options · Thai-English desk-note tone · direct, no fluff, no emotional bias
  2. `# MANDATORY MACRO CHECK — ขั้นบังคับก่อนเริ่ม` — ก่อนวิเคราะห์ทุกครั้ง ต้อง WebSearch: (a) ปฏิทินเศรษฐกิจวันนี้ มี FOMC/CPI/NFP ก่อน settle 15:00 TH ไหม (b) sanity-check ราคา BTC ปัจจุบัน. ถ้าตรงวันประกาศ macro → บังคับ SKIP (No-Trade Rule #1). **ห้ามดึงข้อมูลที่ต้อง login (Bybit/CoinGlass real-time) — ตัวเลข trade มาจากรูป user เท่านั้น**
  3. `# 6-STEP METHODOLOGY` — Snapshot → 8-Check → No-Trade → Combination Read → Verdict (TRADE/SKIP/WAIT + confidence) → Action (ถ้า TRADE: strike/size/entry/SL)
  4. `# 8-CHECK FRAMEWORK` — ตาราง 8 ข้อจาก spec §9.1
  5. `# NO-TRADE RULES (7)` — รายการจาก spec §9.2
  6. `# COMBINATION READ (4 patterns)` — ตารางจาก spec §9.3
  7. `# STRIKE SELECTION` — ตาราง regime จาก spec §9.4 + SD formula จาก §9.7
  8. `# CRITICAL RULES — ห้าม override` — รายการจาก spec §9.5 (เน้น: Liq>$200M, IV/HV<1.15, SD<1.5, FOMC/CPI/NFP)
  9. `# SL METHOD` — จาก spec §9.6 (Index Price, Call: Strike−$500, Put: Strike+$500, RR 1:2, Market, Pin exit 13:30 TH)
  10. `# OUTPUT FORMAT` — 6-step structure · อ้างตัวเลขจริงจากรูป · ห้าม approximate · ทุก verdict cite data จากรูป · commit ทิศทาง (ห้าม "it depends")
  11. `# FIELD-NOTE GUARDRAILS` — บทเรียน 1 (Mark Price ปลอม → ใช้ Ask/Index Price) · 2 (Combination Read สำคัญกว่า indicator เดี่ยว) · 3 (รอ Liquidation < $50M) · 6 (Pin exit 13:30)
  12. `# Reference Thresholds` — IV/HV, Funding zones, Liquidation tiers, Strategy targets, Settlement จาก spec §9.7
  13. `# Commands` — list slash ทั้ง 9: `/full /quick /position /compare /verify /anomaly /pin /strike /checklist`
  14. `## Disclaimer` — เต็มจาก spec §8 (เน้น: ขาดทุน > premium, paper trade ≥ 2 สัปดาห์, ไม่ใช่คำแนะนำ)

- [ ] **Step 3: Verify frontmatter valid** (มี `---` คู่ + required keys)

Run:
```bash
python3 -c "
import re
t=open('plugins/btc-short-premium/agents/btc-short-premium.md').read()
m=re.match(r'^---\n(.*?)\n---\n', t, re.S); assert m, 'no frontmatter'
fm=m.group(1)
assert 'name: btc-short-premium' in fm
assert 'model: opus' in fm
assert 'tools:' in fm
print('frontmatter OK')
"
```
Expected: `frontmatter OK`

- [ ] **Step 4: Verify ตัวเลข critical อยู่ครบ** (กัน framework หล่น)

Run:
```bash
grep -c -E '200M|1\.15|13:30|Index Price' plugins/btc-short-premium/agents/btc-short-premium.md
```
Expected: ≥ 4 (มี Liq $200M, IV/HV 1.15, Pin 13:30, Index Price ครบ)

- [ ] **Step 5: Commit** (ขอ OK นายท่านก่อน)

```bash
git add plugins/btc-short-premium/agents/btc-short-premium.md
git commit -m "feat(btc-short-premium): add Senior Option Trader agent with full framework"
```

---

## Task 3: Commands — Daily Triggers (`/full`, `/quick`)

**Files:**
- Create: `plugins/btc-short-premium/commands/full.md`
- Create: `plugins/btc-short-premium/commands/quick.md`
- Reference: spec §6 (ตาราง command), §9 · Pattern: `plugins/deep-o-stock-analyst/commands/deep.md`

- [ ] **Step 1: เขียน `full.md`**

Frontmatter:
```yaml
---
description: "Full Daily Analysis 6 ขั้นจากรูป 5 ภาพ → TRADE/SKIP/WAIT + strike/size/entry/SL 🟢🟡🔴"
allowed-tools:
  - Read
  - WebSearch
  - WebFetch
model: opus
---
```
Body sections:
- `# /btc-short-premium:full` + 1 บรรทัดสรุป
- **Input ที่ต้องการ:** 5 รูป (1.CoinGlass Derivatives BTC row · 2.Bybit Option Chain expiry วันนี้ · 3.TradingView Daily · 4.4H · 5.1H) + macro view (bearish/bullish/neutral) + portfolio size
- **สิ่งที่ทำ:** MANDATORY MACRO CHECK (WebSearch FOMC/CPI/NFP วันนี้) → 6-step (Snapshot → 8-Check → No-Trade → Combination Read → Verdict → Action) → ถ้า TRADE ระบุ strike/size/entry premium/SL (Index Price). อ้างกฎจาก agent framework
- **ตัวอย่างสั่ง:** ` /full ` + แนบ 5 รูป + "macro view: bearish, portfolio $8K"
- **Discipline:** อ้างตัวเลขจริงจากรูป · ห้าม approximate · เคารพ Critical Rules · SL = Index Price · verdict = framework signal · เชิงการศึกษา

- [ ] **Step 2: เขียน `quick.md`**

Frontmatter:
```yaml
---
description: "Quick Morning Check ~2 นาที — regime (quiet/recovery/cascade) → ควร full ต่อ หรือ skip"
allowed-tools:
  - Read
  - WebSearch
model: opus
---
```
Body sections:
- `# /btc-short-premium:quick` + 1 บรรทัดสรุป
- **Input ที่ต้องการ:** CoinGlass + 1H chart
- **สิ่งที่ทำ:** WebSearch macro วันนี้ (sanity) → อ่าน regime จาก Liquidation + Funding (ดู §9.7 tiers) → บอกว่าตลาดอยู่ regime ไหน (quiet/recovery/cascade) → ควรเปิด `/full` ต่อ หรือ skip. ถ้า Liq > $200M → บอก SKIP เลย ไม่ต้องแคปครบ 5 รูป
- **ตัวอย่างสั่ง:** ` /quick ` + แนบ CoinGlass + 1H
- **Discipline:** (เหมือน full — อ้างตัวเลขจริง · เชิงการศึกษา)

- [ ] **Step 3: Verify frontmatter ทั้ง 2 ไฟล์**

Run:
```bash
for f in full quick; do
python3 -c "
import re
t=open('plugins/btc-short-premium/commands/$f.md').read()
m=re.match(r'^---\n(.*?)\n---\n', t, re.S); assert m, '$f no frontmatter'
assert 'model: opus' in m.group(1), '$f no model'
assert 'allowed-tools' in m.group(1), '$f no tools'
print('$f OK')
"; done
```
Expected: `full OK` / `quick OK`

- [ ] **Step 4: Commit** (ขอ OK นายท่านก่อน)

```bash
git add plugins/btc-short-premium/commands/full.md plugins/btc-short-premium/commands/quick.md
git commit -m "feat(btc-short-premium): add daily trigger commands (/full, /quick)"
```

---

## Task 4: Commands — Special Triggers (`/position`, `/compare`, `/verify`, `/anomaly`, `/pin`)

**Files:**
- Create: `commands/position.md`, `compare.md`, `verify.md`, `anomaly.md`, `pin.md` (ใน `plugins/btc-short-premium/`)
- Reference: spec §6 (Input/Output แต่ละตัว), §9 · source Trigger A–E

ทุกไฟล์ใช้ structure เดียวกัน (`# /btc-short-premium:<cmd>` → Input → สิ่งที่ทำ → ตัวอย่างสั่ง → Discipline) + `model: opus`. Discipline block เหมือนกันทุกตัว (อ้างตัวเลขจริง · เคารพ Critical Rules · SL Index Price · เชิงการศึกษา).

- [ ] **Step 1: เขียน `position.md`** (Trigger A)

Frontmatter: `description: "Position Check — position เปิดอยู่ → hold/close/adjust + TP zone"` · `allowed-tools: [Read]` · `model: opus`
Body: Input = position ปัจจุบัน (strategy/strike/entry premium/spot/time to expiry) + option chain + 1H chart · สิ่งที่ทำ = ประเมิน safe zone vs danger zone → hold ต่อ/ปิดกำไร/ปิดขาดทุน/adjust + บอก trigger ที่ต้องระวัง + TP zone

- [ ] **Step 2: เขียน `compare.md`** (Trigger B)

Frontmatter: `description: "Strategy Comparison — Short Call vs Short Put อันไหนดีกว่า"` · `allowed-tools: [Read]` · `model: opus`
Body: Input = Option 1 Short Call [strike] + Option 2 Short Put [strike] + macro view + 5 รูป · สิ่งที่ทำ = เทียบ aligned กับ macro / Risk-Reward / Probability of profit → แนะนำพร้อมเหตุผล

- [ ] **Step 3: เขียน `verify.md`** (Trigger C)

Frontmatter: `description: "AI Signal Verification — ตรวจ signal จาก bot/AI อื่นกับ framework เรา"` · `allowed-tools: [Read, WebSearch]` · `model: opus`
Body: Input = signal จาก [bot/AI ชื่อ] + 5 รูป · สิ่งที่ทำ = WebSearch macro → เทียบ signal กับ 8-Check + No-Trade + Combination Read → ตัดสิน ตาม signal หรือ override (เน้นบทเรียน: Combination Read แพ้ AI signal เดี่ยวๆ ไม่ได้ — pattern ชนะ)

- [ ] **Step 4: เขียน `anomaly.md`** (Trigger D)

Frontmatter: `description: "Mark Price Anomaly — Unrealized Loss แปลกๆ จริงหรือ noise"` · `allowed-tools: [Read]` · `model: opus`
Body: Input = position + Mark Price + Unrealized Loss % + spot + option chain · สิ่งที่ทำ = อธิบายว่า Mark Price คำนวณจาก IV model (อาจ inflate) → ดู **Ask Price** แทน Mark เพื่อรู้ราคาปิดจริง + ดู **Index Price** ว่า option ในเงินจริงไหม → hold/close (บทเรียน 1: Mark Price = ของปลอม)

- [ ] **Step 5: เขียน `pin.md`** (Trigger E)

Frontmatter: `description: "Pin Risk Decision — ใกล้ 13:30 TH ปิดหรือถือ"` · `allowed-tools: [Read]` · `model: opus`
Body: Input = position + spot + distance from strike + premium ตอนนี้ + entry premium + 1H chart + เวลาปัจจุบัน · สิ่งที่ทำ = ประเมิน gamma squeeze risk ใน TWAP window (14:30–15:00) → ปิดทันที / hold ถึง 13:30 / hold ถึง settle. เน้น Pin Rule: ปิด 13:30 TH (90 นาทีก่อน settle) ถ้า BTC ห่าง strike < $200

- [ ] **Step 6: Verify frontmatter ทั้ง 5 ไฟล์**

Run:
```bash
for f in position compare verify anomaly pin; do
python3 -c "
import re
t=open('plugins/btc-short-premium/commands/$f.md').read()
m=re.match(r'^---\n(.*?)\n---\n', t, re.S); assert m, '$f no frontmatter'
assert 'model: opus' in m.group(1); assert 'allowed-tools' in m.group(1)
print('$f OK')
"; done
```
Expected: `position OK` ... `pin OK` (5 บรรทัด)

- [ ] **Step 7: Commit** (ขอ OK นายท่านก่อน)

```bash
git add plugins/btc-short-premium/commands/position.md plugins/btc-short-premium/commands/compare.md plugins/btc-short-premium/commands/verify.md plugins/btc-short-premium/commands/anomaly.md plugins/btc-short-premium/commands/pin.md
git commit -m "feat(btc-short-premium): add special trigger commands (/position /compare /verify /anomaly /pin)"
```

---

## Task 5: Commands — Helpers (`/strike`, `/checklist`)

**Files:**
- Create: `commands/strike.md`, `commands/checklist.md` (ใน `plugins/btc-short-premium/`)
- Reference: spec §9.1 (8-Check), §9.2 (No-Trade), §9.4 (strike selection), §9.7 (SD formula)

- [ ] **Step 1: เขียน `strike.md`**

Frontmatter: `description: "Strike Selection — เลือก strike ตาม regime + คำนวณ SD distance + delta"` · `allowed-tools: [Read]` · `model: opus`
Body: Input = regime (หรือ Liquidation level) + spot + IV + option chain · สิ่งที่ทำ = คำนวณ SD = Spot × IV × √(1/365) (spec §9.7) → เลือก strike distance + delta + size ตามตาราง regime (spec §9.4) → แนะนำ strike + delta ที่ sweet spot 0.13–0.15 (quiet) · แสดงการคำนวณ SD ให้เห็น

- [ ] **Step 2: เขียน `checklist.md`**

Frontmatter: `description: "Pre-Trade Gate — 8-Check Framework + No-Trade Rules ทีละข้อ → pass/fail"` · `allowed-tools: [Read, WebSearch]` · `model: opus`
Body: Input = 5 รูป (หรือตัวเลข) · สิ่งที่ทำ = WebSearch macro (Check #1) → เดิน 8-Check ทีละข้อ (spec §9.1) แสดง ✅/❌ + ค่าจริง → เดิน No-Trade Rules 7 ข้อ (spec §9.2) → สรุป pass/fail gate (ขาด 1 = ลด size หรือ skip)

- [ ] **Step 3: Verify frontmatter ทั้ง 2 ไฟล์**

Run:
```bash
for f in strike checklist; do
python3 -c "
import re
t=open('plugins/btc-short-premium/commands/$f.md').read()
m=re.match(r'^---\n(.*?)\n---\n', t, re.S); assert m; assert 'model: opus' in m.group(1)
print('$f OK')
"; done
```
Expected: `strike OK` / `checklist OK`

- [ ] **Step 4: Verify ครบ 9 commands**

Run: `ls plugins/btc-short-premium/commands/*.md | wc -l`
Expected: `9`

- [ ] **Step 5: Commit** (ขอ OK นายท่านก่อน)

```bash
git add plugins/btc-short-premium/commands/strike.md plugins/btc-short-premium/commands/checklist.md
git commit -m "feat(btc-short-premium): add helper commands (/strike, /checklist)"
```

---

## Task 6: Skill — `SKILL.md`

**Files:**
- Create: `plugins/btc-short-premium/skills/btc-short-premium/SKILL.md`
- Reference: spec §7.1 · source Quick Reference Card (หน้า 21) · Pattern: `plugins/deep-o-stock-analyst/skills/deep-o-stock-analyst/SKILL.md`

- [ ] **Step 1: เขียน frontmatter**

```yaml
---
name: btc-short-premium
description: >
  Use when ... BTC daily option, short premium, ขาย call/put เก็บ premium, Bybit
  option, IV/HV ratio, combination read, funding rate, liquidation, pin risk, theta
  decay ... → route ไป command ที่เหมาะ. เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล.
---
```

- [ ] **Step 2: เขียน body** — สรุประบบ 2-3 ประโยค + ตาราง routing สถานการณ์ → command (ยกจาก Quick Reference Card):

| สถานการณ์ | Command |
|-----------|---------|
| ยังไม่มี position + ต้องเทรด | `/full` |
| อยากเช็คตลาดเร็ว | `/quick` |
| มี position เปิดอยู่ | `/position` |
| ไม่แน่ใจ Call หรือ Put | `/compare` |
| ได้ signal จาก AI อื่น | `/verify` |
| เห็น Loss แปลกๆ ตอนเพิ่งเปิด | `/anomaly` |
| ใกล้ 13:30 TH | `/pin` |
| จะเลือก strike | `/strike` |
| เช็คก่อนเปิด trade | `/checklist` |

+ Critical Rules ที่ AI ห้าม override (spec §9.5) + disclaimer สั้น

- [ ] **Step 3: Verify frontmatter**

Run:
```bash
python3 -c "
import re
t=open('plugins/btc-short-premium/skills/btc-short-premium/SKILL.md').read()
m=re.match(r'^---\n(.*?)\n---\n', t, re.S); assert m
assert 'name: btc-short-premium' in m.group(1); assert 'description:' in m.group(1)
print('SKILL OK')
"
```
Expected: `SKILL OK`

- [ ] **Step 4: Commit** (ขอ OK นายท่านก่อน)

```bash
git add plugins/btc-short-premium/skills/btc-short-premium/SKILL.md
git commit -m "feat(btc-short-premium): add skill with command routing"
```

---

## Task 7: README

**Files:**
- Create: `plugins/btc-short-premium/README.md`
- Reference: spec §7.4, §8 · source Playbook 0.5 (workflow timeline) · Pattern: `plugins/deep-o-stock-analyst/README.md`

- [ ] **Step 1: เขียน README** — sections:
  - หัวเรื่อง + 1 ย่อหน้าอธิบายระบบ (BTC Daily Short Premium คืออะไร)
  - **เครื่องมือที่ต้องมี:** Bybit, CoinGlass, TradingView, ForexFactory (source 0.3)
  - **5 รูปที่ต้องแคป** (source 0.4)
  - **ตาราง 9 commands** (จาก spec §6)
  - **Workflow ตอนเช้า** — timeline 07:00 TH (source 0.5): เปิด tools → แคป 5 รูป → `/full` → ถ้า TRADE เปิด position + ตั้ง SL Index Price → 13:30 pin exit → 15:00 settle
  - **⚠️ Disclaimer** เต็มจาก spec §8 (เน้น: ขาดทุน > premium, paper trade ≥ 2 สัปดาห์, crypto เสี่ยงสูง, ไม่ใช่คำแนะนำ)

- [ ] **Step 2: Verify disclaimer + commands อยู่ครบ**

Run:
```bash
grep -c -E 'paper trade|premium|/full|/pin' plugins/btc-short-premium/README.md
```
Expected: ≥ 4

- [ ] **Step 3: Commit** (ขอ OK นายท่านก่อน)

```bash
git add plugins/btc-short-premium/README.md
git commit -m "docs(btc-short-premium): add README with workflow + disclaimer"
```

---

## Task 8: Register in marketplace.json

**Files:**
- Modify: `.claude-plugin/marketplace.json` (spec §7.3)

- [ ] **Step 1: อ่านไฟล์ปัจจุบัน**

Run: `cat .claude-plugin/marketplace.json`
Expected: เห็น array `plugins` มี 2 entries (portfolio-risk-architect, deep-o-stock-analyst) + `metadata.version` = `0.1.0`

- [ ] **Step 2: เพิ่ม entry ตัวที่ 3** ลงท้าย array `plugins` (หลัง deep-o-stock-analyst):

```json
    {
      "name": "btc-short-premium",
      "source": "./plugins/btc-short-premium",
      "description": "BTC Short Premium — Senior Option Trader desk สำหรับ Bybit BTC Daily Options (ขาย Call/Put รายวันเก็บ premium). วิเคราะห์ 6 ขั้นจากรูป 5 ภาพ (CoinGlass/OptionChain/D-4H-1H) → TRADE/SKIP/WAIT พร้อม strike/size/entry/SL(Index Price). 8-Check + No-Trade Rules + Combination Read + Critical Rules. agent + 9 commands + skill. เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล.",
      "version": "0.1.0",
      "keywords": ["finance","btc","bitcoin","option","short-premium","theta","bybit","daily-option","iv-hv","combination-read","pin-risk","earth-evans"]
    }
```

- [ ] **Step 3: อัปเดต `metadata.description`** ให้สะท้อน 3 plugins (เดิมเขียน "Plugin แรก: portfolio-risk-architect" → เปลี่ยนเป็นกลางๆ ครอบคลุม 3 ตัว เช่น "...3 plugins: portfolio-risk-architect, deep-o-stock-analyst, btc-short-premium.")

- [ ] **Step 4: Bump `metadata.version`** `0.1.0` → `0.2.0`

- [ ] **Step 5: Verify JSON parse + มี 3 entries + version ถูก**

Run:
```bash
python3 -c "
import json
d=json.load(open('.claude-plugin/marketplace.json'))
names=[p['name'] for p in d['plugins']]
assert 'btc-short-premium' in names, 'missing entry'
assert len(d['plugins'])==3, f'expected 3 got {len(d[\"plugins\"])}'
assert d['metadata']['version']=='0.2.0', d['metadata']['version']
print('marketplace OK:', names)
"
```
Expected: `marketplace OK: ['portfolio-risk-architect', 'deep-o-stock-analyst', 'btc-short-premium']`

- [ ] **Step 6: Commit** (ขอ OK นายท่านก่อน)

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat(btc-short-premium): register in marketplace (bump 0.2.0)"
```

---

## Task 9: Final Verification

**Files:** ไม่สร้างใหม่ — verify ทั้ง plugin

- [ ] **Step 1: Verify โครงไฟล์ครบ 12 ไฟล์**

Run: `find plugins/btc-short-premium -type f | sort`
Expected (12): plugin.json · agent · 9 commands · SKILL.md · README.md

- [ ] **Step 2: Verify ทุก JSON parse ได้**

Run:
```bash
python3 -c "import json; json.load(open('plugins/btc-short-premium/.claude-plugin/plugin.json')); json.load(open('.claude-plugin/marketplace.json')); print('all JSON OK')"
```
Expected: `all JSON OK`

- [ ] **Step 3: Verify ทุก .md มี frontmatter**

Run:
```bash
for f in $(find plugins/btc-short-premium -name '*.md'); do
  head -1 "$f" | grep -q '^---' && echo "OK $f" || echo "FAIL $f"
done
```
Expected: ทุกบรรทัดขึ้นต้น `OK`

- [ ] **Step 4: Structure parity กับ deep-o** (เทียบจำนวน + โครง)

Run:
```bash
echo "deep-o files:"; find plugins/deep-o-stock-analyst -type f | sed "s#deep-o-stock-analyst#NAME#g" | sort
echo "btc files:"; find plugins/btc-short-premium -type f | sed "s#btc-short-premium#NAME#g" | sort
```
Expected: โครงตรงกัน (ยกเว้น deep-o มี `docs/` เพิ่ม — btc ไม่ต้องมีก็ได้ ตาม portfolio-risk)

- [ ] **Step 5: รัน deps-check** scan broken cross-plugin references

Run: `/misc:deps-check`
Expected: ไม่มี broken reference ที่เกี่ยวกับ btc-short-premium

- [ ] **Step 6: (optional) ตรวจ plugin โหลดใน Claude Code** — restart/reload แล้วเช็คว่า `/btc-short-premium:full` ปรากฏใน command list

---

## Self-Review Checklist (ผู้เขียน plan ตรวจแล้ว)

- ✅ **Spec coverage:** ทุก section ใน spec มี task รองรับ — §5 agent→T2 · §6 commands→T3-5 · §7.1 skill→T6 · §7.2 plugin.json→T1 · §7.3 marketplace→T8 · §7.4 README→T7 · §8 disclaimer→T2/T6/T7 · §9 framework→T2 (อ้างใน T3-5) · §10 verify→T9
- ✅ **No placeholder:** ทุก task มี frontmatter เต็ม + section outline ชัด + ตัวเลขอ้าง spec §9 (committed source of truth) + verify command รันได้จริง + commit
- ✅ **Type/name consistency:** plugin name `btc-short-premium` ตรงทุกที่ · 9 commands ตรงกับ spec §6 · marketplace version 0.2.0 ตรงกับ spec §7.3
- ✅ **YAGNI:** ไม่มี /sl แยก, ไม่มี auto-trade, ไม่แตะ 2 plugins เดิม (นอกจาก marketplace entry) — ตรง spec §11
```
