# Portfolio Risk Architect — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** สร้าง Claude Code plugin marketplace + plugin แรก `portfolio-risk-architect` (1 skill + 1 agent + 9 commands) จาก source `source/Portfolio_Risk_Architect_Skill.pdf`

**Architecture:** marketplace.json (root) ลงทะเบียน 1 plugin. Plugin มี skill (core methodology, auto-trigger), agent (System Prompt subagent), 9 commands (simulation triggers). เนื้อหาทั้งหมดสกัดจาก source PDF — ไม่แต่งเพิ่ม, ค่าตัวเลข = illustrative + verify.

**Tech Stack:** Markdown + YAML frontmatter + JSON (Claude Code plugin format). Validation: `python3 -m json.tool` (JSON), `grep` (frontmatter), `ls` (structure).

---

## Conventions (อ่านก่อนเริ่มทุก task)

- **ภาษา:** เนื้อหาไทย, technical terms คงรูปอังกฤษ
- **Source = ground truth:** ทุก content คัด/เรียบเรียงจาก `source/Portfolio_Risk_Architect_Skill.pdf` (อ่านด้วย Read tool, `pages` param). ห้าม fabricate ตัวเลข/หลักการที่ไม่มีใน source
- **Discipline (ใส่ทุก artifact ที่เกี่ยวข้อง):** ❶ ไม่ hallucinate ตัวเลข → "approximate, verify" ❷ as-of date เสมอ ❸ educational only ไม่ใช่คำแนะนำรายบุคคล ❹ simulation = ช่วงความเป็นไปได้ + ระบุสมมติฐาน ❺ แยก fact/inference/market-implied/judgment
- **Commit = guardrails L2:** ทุก commit step ต้อง**ขอนายท่าน confirm ก่อน** (อย่า auto-commit). อยู่ branch `feature/inject-mugi`
- **Reference format จริง:** ดูได้ที่ `~/.claude/plugins/marketplaces/baewkun-plugins/.claude-plugin/marketplace.json` + `~/.claude/plugins/cache/baewkun-plugins/*/.claude-plugin/plugin.json`

---

## File Structure (ปลายทาง)

| ไฟล์ | ความรับผิดชอบ |
|---|---|
| `.claude-plugin/marketplace.json` | ลงทะเบียน plugin `portfolio-risk-architect` ใน marketplace |
| `plugins/portfolio-risk-architect/.claude-plugin/plugin.json` | metadata ของ plugin |
| `plugins/portfolio-risk-architect/skills/portfolio-risk-architect/SKILL.md` | core methodology (หลักคิด 5 + workflow 8 ขั้น + discipline) |
| `plugins/portfolio-risk-architect/agents/portfolio-risk-architect.md` | subagent System Prompt |
| `plugins/portfolio-risk-architect/commands/full.md` | `/full` entry point — workflow 8 ขั้น |
| `plugins/portfolio-risk-architect/commands/{xray,overlap,risk,corr,stress,montecarlo,frontier,rebalance}.md` | 8 simulation commands |
| `plugins/portfolio-risk-architect/README.md` | install + ใช้งาน + เพิ่ม skill ใหม่ |
| `README.md` (root) | อัปเดต: marketplace overview |

---

## Task 0: อ่าน source ให้ครบ (reference สำหรับทุก task)

**Files:** อ่านอย่างเดียว — `source/Portfolio_Risk_Architect_Skill.pdf`

- [ ] **Step 1: อ่าน source ครบ 8 หน้า**

ใช้ Read tool: `Read(source/Portfolio_Risk_Architect_Skill.pdf, pages="1-8")`
จด/คัดข้อความสำคัญลง scratch:
- หน้า 2: หลักคิด 5 ข้อ (Capital weight ≠ Risk weight / กระจาย = correlation + risk contribution / Concentration / วิกฤต correlation→1 / ไม่เดาตัวเลข + as-of date)
- หน้า 3: `# ROLE`, `# PRIME DIRECTIVE` (5 ข้อ), `# DIAGNOSTIC WORKFLOW` (8 ขั้น: X-Ray / Overlap / Concentration / Correlation / Risk Contribution / Tail Risk-Stress / Gap Analysis / Recommendation)
- หน้า 4: `# OUTPUT STRUCTURE`, `# DISCIPLINE`, `# CLARIFY FIRST`, `# SIMULATION COMMANDS`
- หน้า 5: ตาราง 9 commands — column [Command / ผลลัพธ์ที่ได้ / ตัวแปร-สมมติฐาน]
- หน้า 6–7: worked example VOO30/QQQ30/BTC30/Cash10 + Recommendation 3 tiers
- หน้า 8: Deploy + Disclaimer

- [ ] **Step 2: ยืนยันว่าจดครบ**

Checklist: มี ROLE block, 5 directives, 8 workflow steps, ตาราง 9 commands ครบ, disclaimer wording. ถ้าขาด → อ่านหน้านั้นซ้ำ

*(ไม่มี commit — task อ่านอย่างเดียว)*

---

## Task 1: marketplace.json (root)

**Files:**
- Create: `.claude-plugin/marketplace.json`

- [ ] **Step 1: เขียนไฟล์**

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "earthh-evans-finance",
  "owner": {
    "name": "mrunknown2",
    "email": "noreply@example.com"
  },
  "metadata": {
    "description": "Earthh Evans Finance — Claude Code plugin marketplace แปลงความรู้การลงทุนของ Earth Evans (Invest Hub) เป็น skill/agent/command ใช้งานจริง. Plugin แรก: portfolio-risk-architect (วินิจฉัย & ออกแบบความเสี่ยงพอร์ต multi-asset). เนื้อหาเชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล.",
    "version": "0.1.0",
    "pluginRoot": "./"
  },
  "plugins": [
    {
      "name": "portfolio-risk-architect",
      "source": "./plugins/portfolio-risk-architect",
      "description": "Portfolio Risk Architect — วินิจฉัยความเสี่ยงพอร์ต multi-asset (Equity/ETF/Crypto) แบบ look-through: capital weight ≠ risk weight, overlap, concentration, correlation, risk contribution, tail-risk stress test, gap analysis + recommendation. 9 simulation commands. เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล.",
      "version": "0.1.0",
      "keywords": ["finance", "investing", "portfolio", "risk", "diversification", "correlation", "risk-contribution", "multi-asset", "stress-test", "monte-carlo", "asset-allocation", "earth-evans"]
    }
  ]
}
```

- [ ] **Step 2: validate JSON**

Run: `python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && echo "VALID JSON"`
Expected: `VALID JSON`

- [ ] **Step 3: commit** *(ขอนายท่าน confirm ก่อน)*

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat: add marketplace.json with portfolio-risk-architect plugin"
```

---

## Task 2: plugin.json

**Files:**
- Create: `plugins/portfolio-risk-architect/.claude-plugin/plugin.json`

- [ ] **Step 1: เขียนไฟล์**

```json
{
  "name": "portfolio-risk-architect",
  "version": "0.1.0",
  "description": "วินิจฉัย & ออกแบบความเสี่ยงพอร์ต multi-asset แบบ look-through (capital weight ≠ risk weight). Skill + agent + 9 simulation commands. เนื้อหาเชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล. เรียบเรียงจาก Earthh Evans · Invest Hub.",
  "repository": "https://github.com/mrunknown2/Earthh-Evans-Finance-Skill",
  "license": "MIT",
  "author": {
    "name": "mrunknown2"
  },
  "keywords": ["portfolio", "risk", "diversification", "correlation", "risk-contribution", "stress-test", "monte-carlo", "multi-asset", "asset-allocation"]
}
```

- [ ] **Step 2: validate JSON**

Run: `python3 -m json.tool plugins/portfolio-risk-architect/.claude-plugin/plugin.json > /dev/null && echo "VALID JSON"`
Expected: `VALID JSON`

- [ ] **Step 3: commit** *(ขอนายท่าน confirm ก่อน)*

```bash
git add plugins/portfolio-risk-architect/.claude-plugin/plugin.json
git commit -m "feat: add plugin.json for portfolio-risk-architect"
```

---

## Task 3: SKILL.md (core methodology)

**Files:**
- Create: `plugins/portfolio-risk-architect/skills/portfolio-risk-architect/SKILL.md`

- [ ] **Step 1: เขียน frontmatter + body**

frontmatter (บังคับ):
```yaml
---
name: portfolio-risk-architect
description: >
  ใช้เมื่อผู้ใช้พูดถึงการวิเคราะห์/กระจายความเสี่ยงพอร์ตการลงทุน multi-asset
  (หุ้น/ETF/คริปโต) — ตรวจว่าพอร์ต "ดูกระจาย" แต่จริงไม่กระจาย, วัด capital
  weight เทียบ risk contribution, overlap ระหว่างกอง, correlation, concentration,
  tail-risk. Trigger: พอร์ต, กระจายความเสี่ยง, risk contribution, correlation,
  asset allocation, VOO/QQQ/BTC, น้ำหนักพอร์ต. เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล.
---
```

body — H2 sections (เนื้อหาคัดจาก source หน้า 2–4):
1. `## หลักคิด (The Core Problem)` — หลักคิด 5 ข้อ (source หน้า 2)
2. `## Diagnostic Workflow (8 ขั้น)` — X-Ray / Overlap / Concentration / Correlation & True Diversification / Risk Contribution / Tail Risk & Stress / Gap Analysis / Recommendation (source หน้า 3) — แต่ละขั้นเขียน 1–3 บรรทัดว่าทำอะไร + metric หลัก (เช่น Diversification Ratio, Effective Number of Bets, HHI, Marginal Contribution to Risk)
3. `## Output Structure` — ลำดับ output (source หน้า 4)
4. `## Discipline` — Conventions §Discipline ทั้ง 5 ข้อ (BLOCKING)
5. `## Commands` — ตารางย่อ 9 commands + ชี้ว่าเรียกผ่าน `/portfolio-risk-architect:<cmd>` + ชี้ agent
6. `## Disclaimer` — educational only (source หน้า 8)

- [ ] **Step 2: validate frontmatter**

Run: `head -12 plugins/portfolio-risk-architect/skills/portfolio-risk-architect/SKILL.md | grep -E "^(name|description):" && echo "FRONTMATTER OK"`
Expected: เจอ `name:` + `description:` → `FRONTMATTER OK`

- [ ] **Step 3: validate discipline ครบ**

Run: `grep -c -E "verify|as-of|การศึกษา|สมมติฐาน" plugins/portfolio-risk-architect/skills/portfolio-risk-architect/SKILL.md`
Expected: ≥ 4 (discipline 5 ข้อปรากฏ)

- [ ] **Step 4: commit** *(ขอนายท่าน confirm ก่อน)*

```bash
git add plugins/portfolio-risk-architect/skills/
git commit -m "feat: add portfolio-risk-architect SKILL.md (core methodology)"
```

---

## Task 4: agent (System Prompt subagent)

**Files:**
- Create: `plugins/portfolio-risk-architect/agents/portfolio-risk-architect.md`

- [ ] **Step 1: เขียน frontmatter + System Prompt**

frontmatter:
```yaml
---
name: portfolio-risk-architect
description: Senior Multi-Asset Portfolio Strategist & Risk Manager — วินิจฉัยความเสี่ยงพอร์ตแบบ Risk Desk / CIO Office. ใช้เมื่อต้องการวิเคราะห์พอร์ตเชิงลึกแบบ isolated subagent.
tools: Read, Write, Glob, Grep
model: opus
---
```

body — คัด System Prompt จาก source หน้า 3–4 (verbatim เท่าที่อ่านได้):
- `# ROLE` — Senior Multi-Asset Portfolio Strategist & Risk Manager (CIO Office, ตรงไปตรงมา ไม่เชียร์)
- `# PRIME DIRECTIVE` — 5 ข้อ
- `# DIAGNOSTIC WORKFLOW` — 8 ขั้น
- `# OUTPUT STRUCTURE` · `# DISCIPLINE` · `# CLARIFY FIRST`
- `# SIMULATION COMMANDS` — สรุป 9 คำสั่ง

> หมายเหตุ: agent = persona/system-prompt (มุมมอง "เป็น Risk Desk"). SKILL.md = methodology/knowledge (มุมมอง "วิธีวินิจฉัย"). เนื้อหาทับซ้อนได้แต่ framing ต่างกัน — agent เขียนเป็นคำสั่งบุรุษที่ 2 ("คุณคือ..."), skill เขียนเป็นความรู้

- [ ] **Step 2: validate frontmatter**

Run: `head -8 plugins/portfolio-risk-architect/agents/portfolio-risk-architect.md | grep -E "^(name|description):" && echo "OK"`
Expected: `OK`

- [ ] **Step 3: commit** *(ขอนายท่าน confirm ก่อน)*

```bash
git add plugins/portfolio-risk-architect/agents/
git commit -m "feat: add portfolio-risk-architect agent (system prompt)"
```

---

## Task 5: /full command (entry point + template)

**Files:**
- Create: `plugins/portfolio-risk-architect/commands/full.md`

- [ ] **Step 1: เขียน command (เป็น template ให้ command อื่น)**

frontmatter:
```yaml
---
description: "รัน workflow วินิจฉัยพอร์ตครบ 8 ขั้น + ภาพหลัก (X-Ray, Risk Contribution, Stress) — เหมาะเริ่มต้น"
allowed-tools:
  - Read
  - Write
model: opus
---
```

body:
- `# /portfolio-risk-architect:full`
- Input ที่ต้องการ: holdings + น้ำหนัก, สกุลเงินฐาน/ประเทศ, horizon, ความทนต่อ drawdown (ถ้าไม่ครบ → ถามตาม CLARIFY FIRST)
- ขั้นตอน: เดิน Diagnostic Workflow 8 ขั้น (อ้าง skill) → output ตาม Output Structure
- ตัวอย่างสั่ง (source หน้า 5): `พอร์ต: VOO 30%, QQQ 30%, BTC 30%, cash 10%, ฐาน USD, อยู่ไทย, horizon 10 ปี, ทน drawdown ~30%. /full`
- Discipline block (ย่อ): ค่า simulation = illustrative + verify + as-of date

- [ ] **Step 2: validate frontmatter**

Run: `head -8 plugins/portfolio-risk-architect/commands/full.md | grep -E "^description:" && echo "OK"`
Expected: `OK`

- [ ] **Step 3: commit** *(ขอนายท่าน confirm ก่อน)*

```bash
git add plugins/portfolio-risk-architect/commands/full.md
git commit -m "feat: add /full command (entry point)"
```

---

## Task 6: commands ที่เหลือ 8 อัน

**Files (Create ทั้งหมด):**
- `commands/xray.md` · `overlap.md` · `risk.md` · `corr.md` · `stress.md` · `montecarlo.md` · `frontier.md` · `rebalance.md`
(prefix path: `plugins/portfolio-risk-architect/commands/`)

แต่ละไฟล์ใช้ template เดียวกับ `/full` (frontmatter `description` + `allowed-tools` + `model`) — เนื้อหาเฉพาะตาม source หน้า 5:

| ไฟล์ | description (frontmatter) | ทำอะไร | ตัวแปร/สมมติฐาน |
|---|---|---|---|
| `xray.md` | "แตก look-through holdings เป็นหุ้นรายตัวจริง + treemap น้ำหนัก sector/single-name" | แตก ETF เป็น exposure จริง (VOO+QQQ → AAPL/MSFT/...) | holdings ของแต่ละ ETF |
| `overlap.md` | "heatmap ความซ้ำซ้อนระหว่างกอง — ชี้ที่ 'ซื้อซ้ำ'" | weighted holdings overlap % | top holdings ของแต่ละกอง |
| `risk.md` | "bar chart เทียบ Capital Weight vs Risk Contribution — ภาพที่ทรงพลังสุด" | %capital vs %risk แต่ละสินทรัพย์ | vol, correlation |
| `corr.md` | "correlation matrix heatmap (ปกติ vs regime วิกฤต)" | pairwise correlation + ENB | return series / ค่าอ้างอิง |
| `stress.md` | "drawdown ของพอร์ตในวิกฤตจริง (GFC2008/COVID2020/2022/Yen2024)" | est. max drawdown, time-to-recover, VaR/CVaR | beta ต่อแต่ละ shock |
| `montecarlo.md` | "จำลอง 10,000 เส้นทาง (GBM) → distribution ผลตอบแทน & max drawdown" | distribution + ระบุสมมติฐานทุกครั้ง | μ, σ, ρ, horizon |
| `frontier.md` | "efficient frontier + จุดพอร์ตปัจจุบัน + จุดหลังปรับ" | frontier plot | μ, σ, ρ ของสินทรัพย์ |
| `rebalance.md` | "เปรียบเทียบ before–after risk metrics หลังทำตามข้อเสนอ" | before/after vol, ENB, risk contribution | น้ำหนักใหม่ที่เสนอ |

- [ ] **Step 1: เขียนทั้ง 8 ไฟล์** (วน template + เติมเฉพาะตามตาราง + Discipline block สำหรับ montecarlo/frontier เน้น "ช่วงความเป็นไปได้ ไม่ใช่พยากรณ์")

- [ ] **Step 2: validate ครบ 9 commands**

Run: `ls plugins/portfolio-risk-architect/commands/*.md | wc -l`
Expected: `9`

Run: `for f in full xray overlap risk corr stress montecarlo frontier rebalance; do head -3 "plugins/portfolio-risk-architect/commands/$f.md" | grep -q "^description:" && echo "$f OK" || echo "$f MISSING"; done`
Expected: ทุกไฟล์ `OK`

- [ ] **Step 3: commit** *(ขอนายท่าน confirm ก่อน)*

```bash
git add plugins/portfolio-risk-architect/commands/
git commit -m "feat: add 8 simulation commands (xray/overlap/risk/corr/stress/montecarlo/frontier/rebalance)"
```

---

## Task 7: README (plugin + root)

**Files:**
- Create: `plugins/portfolio-risk-architect/README.md`
- Modify: `README.md` (root — ปัจจุบันมีแค่ `# Earthh-Evans-Finance-Skill`)

- [ ] **Step 1: plugin README**

sections: ภาพรวม plugin · install (`/plugin marketplace add mrunknown2/Earthh-Evans-Finance-Skill` → `/plugin install portfolio-risk-architect`) · ใช้งาน (skill auto-trigger / agent / 9 commands + ตัวอย่าง `/full`) · Disclaimer (educational only)

- [ ] **Step 2: root README**

เพิ่มใต้ `# Earthh-Evans-Finance-Skill`: ภาพรวม marketplace · รายการ plugin (portfolio-risk-architect) · วิธี install · วิธีเพิ่ม skill ใหม่จาก source ถัดไป (วาง PDF ลง `source/` → สกัด → plugin ใหม่) · Disclaimer

- [ ] **Step 3: validate**

Run: `test -f plugins/portfolio-risk-architect/README.md && grep -q "marketplace add" README.md && echo "OK"`
Expected: `OK`

- [ ] **Step 4: commit** *(ขอนายท่าน confirm ก่อน)*

```bash
git add plugins/portfolio-risk-architect/README.md README.md
git commit -m "docs: add plugin + marketplace README"
```

---

## Task 8: Final validation

**Files:** อ่าน/ตรวจอย่างเดียว

- [ ] **Step 1: ตรวจ structure ครบ**

Run:
```bash
test -f .claude-plugin/marketplace.json && \
test -f plugins/portfolio-risk-architect/.claude-plugin/plugin.json && \
test -f plugins/portfolio-risk-architect/skills/portfolio-risk-architect/SKILL.md && \
test -f plugins/portfolio-risk-architect/agents/portfolio-risk-architect.md && \
test $(ls plugins/portfolio-risk-architect/commands/*.md | wc -l) -eq 9 && \
test -f plugins/portfolio-risk-architect/README.md && \
echo "STRUCTURE COMPLETE"
```
Expected: `STRUCTURE COMPLETE`

- [ ] **Step 2: validate JSON ทั้งหมด**

Run: `for j in .claude-plugin/marketplace.json plugins/portfolio-risk-architect/.claude-plugin/plugin.json; do python3 -m json.tool "$j" > /dev/null && echo "$j OK"; done`
Expected: ทั้ง 2 ไฟล์ `OK`

- [ ] **Step 3: ตรวจ name ตรงกันระหว่าง marketplace.json ↔ plugin.json**

Run: `grep '"name"' plugins/portfolio-risk-architect/.claude-plugin/plugin.json | head -1`
Expected: `"name": "portfolio-risk-architect"` (ตรงกับ `source` ใน marketplace.json)

- [ ] **Step 4: (ผู้ใช้ทดสอบจริง)** นายท่านรัน `/plugin marketplace add` ชี้ path local เพื่อ smoke test ว่า install ได้ — agent ไม่รันเอง (interactive)

- [ ] **Step 5: final commit** *(ขอนายท่าน confirm ก่อน)* — ถ้ายังมีไฟล์ค้าง (`.gitignore`, spec, plan)

```bash
git add .gitignore docs/
git commit -m "chore: add gitignore + design spec + implementation plan"
```

---

## Self-Review (เขียนเสร็จแล้ว — ตรวจกับ spec)

**Spec coverage:**
- §3 repo structure → Task 1–7 ✅
- §4.1 skill → Task 3 ✅ · §4.2 agent → Task 4 ✅ · §4.3 9 commands → Task 5–6 ✅
- §5 discipline/disclaimer → ใส่ใน Task 3 (skill), 4 (agent), 5–6 (commands), 7 (README) ✅
- §7 DoD ข้อ 1 (marketplace+plugin.json install) → Task 1,2,8 ✅ · ข้อ 2–4 → Task 3,4,5,6 ✅ · ข้อ 5 disclaimer → ทุก task ✅ · ข้อ 6 README → Task 7 ✅ · ข้อ 7 illustrative numbers → Conventions + Task 3,6 ✅

**Placeholder scan:** JSON content เต็ม. Markdown ระบุ section + source mapping + validation ชัด (source PDF = ground truth, ไม่ใช่ placeholder). ✅

**Type/name consistency:** plugin name = `portfolio-risk-architect` ตรงกันทุกที่ (marketplace source path, plugin.json name, skill name, agent name, commands path). ✅

**Gap:** Multi-provider (spec §6) = out of scope รอบนี้ (spec §8 ระบุชัด) — ไม่มี task = ตั้งใจ ✅
