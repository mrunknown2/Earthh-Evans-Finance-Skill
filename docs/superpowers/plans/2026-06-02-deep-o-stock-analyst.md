# deep-o-stock-analyst Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** แปลง prompt `deep-o-stock-analysis-prompt.md` เป็น Claude Code plugin `deep-o-stock-analyst` (skill + agent + 10 commands) mirror โครงพี่ `portfolio-risk-architect` พร้อมเกลา (R1–R5)

**Architecture:** Plugin แบบ markdown + JSON ล้วน ไม่มี runtime code — verification = JSON parse + frontmatter check + grep disclaimer/structure. โครงไฟล์ mirror `plugins/portfolio-risk-architect/` เป๊ะ. เนื้อหา derive จาก source prompt (`deep-o-stock-analysis-prompt.md`) + apply refinements R1–R5 จาก spec §7.

**Tech Stack:** Claude Code plugin spec (SKILL.md frontmatter, agent frontmatter `tools`/`model`, command frontmatter `description`/`allowed-tools`/`model`), JSON (plugin.json, marketplace.json)

---

## Reference Material (อ่านก่อนเริ่ม)

- **Spec:** `docs/superpowers/specs/2026-06-02-deep-o-stock-analyst-design.md`
- **Source prompt:** `deep-o-stock-analysis-prompt.md` (root) — เนื้อหาต้นฉบับทุก command
- **Mirror reference (พี่ portfolio):**
  - `plugins/portfolio-risk-architect/skills/portfolio-risk-architect/SKILL.md`
  - `plugins/portfolio-risk-architect/agents/portfolio-risk-architect.md`
  - `plugins/portfolio-risk-architect/commands/{full,risk,xray}.md`
  - `plugins/portfolio-risk-architect/.claude-plugin/plugin.json`
  - `.claude-plugin/marketplace.json`

## ⚠️ Guardrails note (อ่านก่อน execute)

- ทำงานบน branch `feature/deep-o-stock-analyst` (ห้ามแตะ `main`)
- **ทุก `git commit` = L2** — ต้องขอนายท่าน (พิมพ์ `commit`) ก่อนรันทุกครั้ง ห้าม commit เอง
- commit message ลงท้ายด้วย: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`

## 🔁 Reusable: DISCLAIMER block (ใช้ปิดท้ายทุก surface)

```markdown
## Disclaimer

เครื่องมือนี้เป็นกรอบวิเคราะห์หุ้นเชิงการศึกษา **ไม่ใช่คำแนะนำการลงทุนรายบุคคล** · verdict (ซื้อเพิ่ม/ถือ/ลด/ขาย 🟢🟡🟠🔴) เป็น **framework signal** จากกรอบ DEEP+O ไม่ใช่คำสั่งซื้อขาย · ตัวเลข valuation อิงสมมติฐานที่ระบุ (WACC, g∞, margin, S/C) และข้อมูล ณ as-of date · ผู้ใช้ต้อง verify เอกสารทางการล่าสุด (10-K/10-Q/IR) และพิจารณาบริบทของตนเองก่อนตัดสินใจ
```

สำหรับ command body (สั้น) ใช้บรรทัดเดียว:
```markdown
## Discipline

ทุกตัวเลข/ข้อเท็จจริงสำคัญ **ใส่ลิงก์อ้างอิง** · ระบุ **as-of date** (YYYY-MM-DD) · ห้ามกุข้อมูล (ไม่พบให้เขียน "ไม่พบข้อมูล") · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
```

---

## Task 1: Scaffold directory + plugin.json

**Files:**
- Create: `plugins/deep-o-stock-analyst/.claude-plugin/plugin.json`

- [ ] **Step 1: สร้างโครง directory**

Run:
```bash
mkdir -p plugins/deep-o-stock-analyst/.claude-plugin \
         plugins/deep-o-stock-analyst/skills/deep-o-stock-analyst \
         plugins/deep-o-stock-analyst/agents \
         plugins/deep-o-stock-analyst/commands
```

- [ ] **Step 2: เขียน plugin.json**

Create `plugins/deep-o-stock-analyst/.claude-plugin/plugin.json`:
```json
{
  "name": "deep-o-stock-analyst",
  "version": "0.1.0",
  "description": "วิเคราะห์หุ้นรายตัว (US) ด้วยกรอบ DEEP+O (Demand/Execution/Economics/Price/Optionality) สไตล์ Damodaran + McKinsey — ออก verdict ซื้อ/ถือ/ลด/ขาย แบบตรวจสอบได้ พร้อม intrinsic value, reverse DCF, option-adjusted valuation. Skill + agent + 10 commands. เนื้อหาเชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล. เรียบเรียงจาก Earthh Evans · Invest Hub.",
  "repository": "https://github.com/mrunknown2/Earthh-Evans-Finance-Skill",
  "license": "MIT",
  "author": {
    "name": "mrunknown2"
  },
  "keywords": ["stock", "equity", "valuation", "dcf", "damodaran", "deep-o", "intrinsic-value", "reverse-dcf", "hedge-fund", "earth-evans"]
}
```

- [ ] **Step 3: Verify JSON valid**

Run: `python3 -c "import json; json.load(open('plugins/deep-o-stock-analyst/.claude-plugin/plugin.json')); print('OK')"`
Expected: `OK`

- [ ] **Step 4: Commit** (ขอนายท่านก่อน — L2)

```bash
git add plugins/deep-o-stock-analyst/.claude-plugin/plugin.json
git commit -m "feat(deep-o): scaffold plugin dir + plugin.json" -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: SKILL.md (auto-trigger skill)

**Files:**
- Create: `plugins/deep-o-stock-analyst/skills/deep-o-stock-analyst/SKILL.md`

อ้างอิงโครงจากพี่ `portfolio-risk-architect/skills/.../SKILL.md` (frontmatter `name` + `description` แล้วเนื้อหา 8 sections)

- [ ] **Step 1: เขียน frontmatter**

```yaml
---
name: deep-o-stock-analyst
description: >
  ใช้เมื่อผู้ใช้ต้องการวิเคราะห์หุ้นรายตัว (หุ้น US) เชิงลึก — หามูลค่าที่แท้จริง
  (intrinsic value), ตัดสินใจซื้อ/ถือ/ลด/ขาย, ทำ DCF/Reverse DCF, ประเมิน
  valuation. Trigger keywords: วิเคราะห์หุ้น, หุ้นรายตัว, มูลค่าหุ้น, ราคาเหมาะสม,
  DEEP+O, Damodaran, DCF, reverse DCF, intrinsic value, fair value, WACC,
  valuation, ซื้อหุ้นไหม, NVDA, AAPL, TSLA, MSFT. เนื้อหาเชิงการศึกษา ไม่ใช่
  คำแนะนำลงทุนรายบุคคล.
---
```

- [ ] **Step 2: เขียน body (8 sections)** — derive จาก source prompt, apply R1/R2/R5

โครงเนื้อหา (เขียนเป็นภาษาไทย mirror โทนพี่ portfolio):
1. `# Deep-O Stock Analyst` + คำโปรย + บรรทัด `> เรียบเรียงจาก Earthh Evans · Invest Hub`
2. `## หลักคิด` — สรุป MANDATORY REAL-TIME PROTOCOL (source บรรทัด 8–25: live data check ก่อนวิเคราะห์, Search > Memory) + ปรัชญา Damodaran/McKinsey (story→numbers→value, TTM base + มองหน้า 12–24 เดือน)
3. `## DEEP+O Framework` — D Demand / E Execution / E Economics (ROIC-WACC, EVA, SGR) / P Price (Reverse DCF) / O Optionality (source บรรทัด 110–114)
4. `## Valuation Mechanics (Damodaran)` — ย่อจาก source บรรทัด 58–94: **A)** Cost of Capital → WACC path · **B)** Operating Drivers (revenue growth, margin path, tax, reinvestment ด้วย Sales-to-Capital) · **C)** Clean-ups (excess cash, debt MV, ESOP Black-Scholes, NOLs, failure risk p_failure×recovery) · **D)** Stable guardrails (g∞ ≤ nominal GDP, ROIC∞ → industry/WACC, terminal reinvestment = g∞/ROIC∞) · **E)** Triangulation (CFROI vs WACC · FCFE yield vs CoE · Reverse DCF) — **[R2: เดิม source ใช้หัวข้อ K → เปลี่ยนเป็น E]**
5. `## Output Structure` — รายงาน DEEP+O §0–§9 (source บรรทัด 98–146): 0 Thesis · 1 Verdict · 2 DEEP Summary · 3 Reverse DCF · 3' Option-Adjusted · 4 Risk Map · 5 Bull/Base/Bear · 6 Catalysts · 7 Weighted Score · 8 One-Pager · 9 Appendix
6. `## Weighted Score & Verdict` — ใส่ตารางเต็ม:
   ```markdown
   น้ำหนัก: D 25 / E(exec) 20 / E(econ) 20 / P 20 / O 15 → รวม 0–100

   | คะแนน | สัญญาณ | คำแนะนำ |
   |-------|--------|---------|
   | ≥ 80 | 🟢 | ซื้อเพิ่ม |
   | 60–79 | 🟡 | ถือ / สะสมระวัง |
   | 40–59 | 🟠 | ลดน้ำหนัก |
   | < 40 | 🔴 | ขาย |
   ```
7. `## Discipline (BLOCKING)` — source บรรทัด 35–42: ใช้ TTM · ห้ามกุข้อมูล (ไม่พบ→เขียน "ไม่พบข้อมูล") · ใส่ลิงก์ทุกตัวเลขสำคัญ (10-K/10-Q/IR/Damodaran Online) · YYYY-MM-DD · สกุลเงินคงที่ + FX ระบุอัตรา/วันที่ · เอกสารทางการล่าสุด = source of truth · **as-of date เสมอ [R5]**
8. `## Commands` — ตาราง 10 commands (ดู Task 7 mapping)
9. DISCLAIMER block (จาก Reusable ด้านบน) **[R1]**

- [ ] **Step 3: Verify frontmatter + disclaimer**

Run:
```bash
head -12 plugins/deep-o-stock-analyst/skills/deep-o-stock-analyst/SKILL.md | grep -q "name: deep-o-stock-analyst" && \
grep -q "ไม่ใช่คำแนะนำการลงทุนรายบุคคล" plugins/deep-o-stock-analyst/skills/deep-o-stock-analyst/SKILL.md && \
grep -q "ซื้อเพิ่ม" plugins/deep-o-stock-analyst/skills/deep-o-stock-analyst/SKILL.md && echo "OK"
```
Expected: `OK`

- [ ] **Step 4: Verify R2 applied (ไม่มีหัวข้อ K ค้าง)**

Run: `grep -c "K) Triangulation\|K)\s*Triangulation" plugins/deep-o-stock-analyst/skills/deep-o-stock-analyst/SKILL.md || echo "0 = good"`
Expected: `0` (ใช้ E) Triangulation แทน)

- [ ] **Step 5: Commit** (ขอนายท่านก่อน — L2)

```bash
git add plugins/deep-o-stock-analyst/skills/deep-o-stock-analyst/SKILL.md
git commit -m "feat(deep-o): add auto-trigger SKILL.md with DEEP+O framework" -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: agent (subagent)

**Files:**
- Create: `plugins/deep-o-stock-analyst/agents/deep-o-stock-analyst.md`

อ้างอิงพี่ `portfolio-risk-architect/agents/portfolio-risk-architect.md` (ROLE-based) — **แต่เพิ่ม WebSearch+WebFetch [R4]**

- [ ] **Step 1: เขียน frontmatter** — สังเกต `tools` มี web (R4)

```yaml
---
name: deep-o-stock-analyst
description: >
  Hedge Fund Equity Research Partner — วิเคราะห์หุ้นรายตัว (US) ด้วยกรอบ DEEP+O
  สไตล์ Damodaran + McKinsey ออก verdict ซื้อ/ถือ/ลด/ขาย แบบตรวจสอบได้ พร้อม live
  data check. ใช้เมื่อต้องวิเคราะห์หุ้นเชิงลึกแบบ isolated subagent. เชิงการศึกษา
  ไม่ใช่คำแนะนำลงทุนรายบุคคล.
tools: Read, Write, Glob, Grep, WebSearch, WebFetch
model: opus
---
```

- [ ] **Step 2: เขียน body** — โครง ROLE-based mirror agent พี่ portfolio:
  1. `# ROLE` — หุ้นส่วนวิเคราะห์เฮดจ์ฟันด์ (source บรรทัด 29–31): ออกรายงานซื้อ/ถือ/ลด/ขาย อิง Damodaran + McKinsey, underwrite ความจริงเรื่องมูลค่า ไม่เชียร์
  2. `# MANDATORY REAL-TIME PROTOCOL` — source บรรทัด 8–25 เต็ม: STEP A (search IR latest results, SEC 10-K/10-Q, stock price today, Damodaran ERP) · STEP B (Data Override: Search > Memory; งบ < 3 วัน = Breaking News Mode)
  3. `# กติกาเคร่งครัด` — source บรรทัด 35–42
  4. `# สิ่งที่ต้องดึง` — source บรรทัด 45–54 (เอกสารล่าสุด, TTM metrics, โครงสร้างราคา, คุณภาพรายได้, guidance, regulatory, supply chain)
  5. `# Valuation Mechanics` — source บรรทัด 58–94, apply R2 (K→E)
  6. `# DEEP+O Output Structure` — source บรรทัด 98–146
  7. `# Weighted Score & Verdict` — ตารางเดียวกับ SKILL §6
  8. `# Discipline` — source บรรทัด 35–42 + as-of date [R5]
  9. `# Commands` — รายการ 10 commands (เรียกผ่าน slash)
  10. DISCLAIMER block [R1]

- [ ] **Step 3: Verify tools มี web + disclaimer**

Run:
```bash
grep -q "WebSearch" plugins/deep-o-stock-analyst/agents/deep-o-stock-analyst.md && \
grep -q "WebFetch" plugins/deep-o-stock-analyst/agents/deep-o-stock-analyst.md && \
grep -q "MANDATORY REAL-TIME PROTOCOL" plugins/deep-o-stock-analyst/agents/deep-o-stock-analyst.md && \
grep -q "ไม่ใช่คำแนะนำการลงทุนรายบุคคล" plugins/deep-o-stock-analyst/agents/deep-o-stock-analyst.md && echo "OK"
```
Expected: `OK`

- [ ] **Step 4: Commit** (ขอนายท่านก่อน — L2)

```bash
git add plugins/deep-o-stock-analyst/agents/deep-o-stock-analyst.md
git commit -m "feat(deep-o): add Hedge Fund Partner subagent (with live-data tools)" -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: Core commands — `/full` + `/livecheck`

**Files:**
- Create: `plugins/deep-o-stock-analyst/commands/full.md`
- Create: `plugins/deep-o-stock-analyst/commands/livecheck.md`

ทุก command pattern: `frontmatter (description, allowed-tools, model: opus)` → `# /deep-o-stock-analyst:<cmd>` → คำโปรย → `## Input ที่ต้องการ` → `## สิ่งที่ทำ` → `[## ตัวอย่างสั่ง]` → `## Discipline`

- [ ] **Step 1: เขียน `full.md`**

frontmatter:
```yaml
---
description: "รัน DEEP+O เต็มรายงานจบในรอบเดียว (livecheck → valuation → DEEP score → risk → one-pager) — entry point หลัก"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Write
model: opus
---
```
body:
- `# /deep-o-stock-analyst:full`
- คำโปรย: วิเคราะห์หุ้นรายตัวครบกรอบ DEEP+O — entry point หลัก
- `## Input ที่ต้องการ`: ticker หุ้น (เช่น NVDA); ถ้าไม่ระบุให้ถาม **[R3]**
- `## สิ่งที่ทำ`: เดินครบ — (1) Live Data Check → (2) Cost of Capital/WACC → (3) Damodaran DCF → intrinsic value → (4) Reverse DCF → (5) Option-adjusted → (6) DEEP score 0–100 + verdict → (7) Risk Map + Bull/Base/Bear → (8) Catalysts → (9) One-Pager → (10) Appendix links. ตอบตาม Output Structure §0–§9
- `## ตัวอย่างสั่ง`: ```
  /full NVDA
  ```
- `## Discipline`: บรรทัดสั้น (จาก Reusable)

- [ ] **Step 2: เขียน `livecheck.md`** — map source "MANDATORY REAL-TIME PROTOCOL" บรรทัด 8–25

frontmatter:
```yaml
---
description: "Real-Time Protocol — ยืนยันงบ/ราคา/ERP ล่าสุดด้วย Search ก่อนวิเคราะห์ (Search > Memory)"
allowed-tools:
  - WebSearch
  - WebFetch
model: opus
---
```
body:
- `# /deep-o-stock-analyst:livecheck`
- คำโปรย: ขั้นบังคับก่อนสวมบทวิเคราะห์ — ห้ามใช้ Training Data จนผ่าน Live Data Check
- `## Input ที่ต้องการ`: ticker หุ้น
- `## สิ่งที่ทำ`: **STEP A** — search 4 อย่าง: `IR [ticker] latest financial results press release` (ไตรมาสล่าสุด + วันประกาศ + ลิงก์) · `SEC Filings [ticker] 10-Q/10-K latest` · `[ticker] stock price today` + Market Cap · `Damodaran Implied Equity Risk Premium [current month/year]`. **STEP B** — Data Override: Search > Memory; งบล่าสุด < 3 วัน = ระบุ "Breaking News/Earnings Reaction Mode"
- `## Output`: as-of date + ไตรมาสล่าสุด + ราคา/Market Cap + ERP + ลิงก์ทุกจุด
- `## Discipline`: บรรทัดสั้น

- [ ] **Step 3: Verify ทั้งสองไฟล์**

Run:
```bash
for f in full livecheck; do
  grep -q "allowed-tools" plugins/deep-o-stock-analyst/commands/$f.md && \
  grep -q "WebSearch" plugins/deep-o-stock-analyst/commands/$f.md && echo "$f OK"
done
```
Expected: `full OK` แล้ว `livecheck OK`

- [ ] **Step 4: Commit** (ขอนายท่านก่อน — L2)

```bash
git add plugins/deep-o-stock-analyst/commands/full.md plugins/deep-o-stock-analyst/commands/livecheck.md
git commit -m "feat(deep-o): add /full + /livecheck commands" -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: Valuation commands — `/wacc` `/valuation` `/reversedcf` `/options`

**Files:**
- Create: `plugins/deep-o-stock-analyst/commands/wacc.md`
- Create: `plugins/deep-o-stock-analyst/commands/valuation.md`
- Create: `plugins/deep-o-stock-analyst/commands/reversedcf.md`
- Create: `plugins/deep-o-stock-analyst/commands/options.md`

แต่ละไฟล์ใช้ pattern command + `allowed-tools: [WebSearch, WebFetch, Read]`, `model: opus`

- [ ] **Step 1: `wacc.md`** — map source บรรทัด 61–64 (A Cost of Capital)
  - description: `"คำนวณ Cost of Capital → เส้นทาง WACC (current → sector-stable)"`
  - สิ่งที่ทำ: Risk-free + ERP/CRP + Beta (bottom-up) + Cost of debt (pre-tax) + spread + target capital structure (MV weights) → WACC ตอนเริ่ม; อธิบาย "เส้นทาง WACC" จนเข้า sector/stable

- [ ] **Step 2: `valuation.md`** — map source บรรทัด 65–94 (B Drivers + C Clean-ups + D Stable + E Triangulation), apply R2
  - description: `"Damodaran DCF เต็ม (drivers + clean-ups + stable guardrails + triangulation) → intrinsic value"`
  - สิ่งที่ทำ: Operating drivers (revenue growth stage 1–3, margin path, tax, reinvestment ด้วย Sales-to-Capital `Reinvestment_t = ΔRevenue_t / (S/C_t)`) → Clean-ups (excess cash, debt MV, ESOP Black-Scholes, NOLs, failure risk `p_failure × recovery`) → Stable guardrails (`g∞ ≤ nominal GDP`, `ROIC∞ → industry/WACC`, `terminal reinvestment = g∞/ROIC∞`) → **E) Triangulation** (CFROI vs WACC · FCFE yield vs CoE · Reverse DCF) → intrinsic value/share

- [ ] **Step 3: `reversedcf.md`** — map source บรรทัด 116–119 (§3)
  - description: `"Reverse DCF — ราคาปัจจุบันฝัง expectation อะไร + reality check"`
  - สิ่งที่ทำ: จาก WACC, g∞, FCFF margin → `Implied steady-state Revenue = EV × (WACC − g∞) / margin` + reality check ว่าตลาดคาดหวังโตเท่าไหร่ สมจริงไหม

- [ ] **Step 4: `options.md`** — map source บรรทัด 120–121 (§3') + บรรทัด 114 (O)
  - description: `"Option-Adjusted Valuation — ตัว O ใน DEEP+O (inventory, stage, window, milestones)"`
  - สิ่งที่ทำ: `EV_core (Reverse DCF) + ΣEV(options) → EV_total`; ชี้ว่าตลาดใส่มูลค่า optionality อะไรไปแล้ว (real options, ธุรกิจใหม่, economics@scale)

- [ ] **Step 5: Verify ทั้ง 4 ไฟล์**

Run:
```bash
for f in wacc valuation reversedcf options; do
  grep -q "model: opus" plugins/deep-o-stock-analyst/commands/$f.md && \
  grep -q "deep-o-stock-analyst:$f" plugins/deep-o-stock-analyst/commands/$f.md && echo "$f OK"
done
```
Expected: 4 บรรทัด `<name> OK`

- [ ] **Step 6: Commit** (ขอนายท่านก่อน — L2)

```bash
git add plugins/deep-o-stock-analyst/commands/wacc.md plugins/deep-o-stock-analyst/commands/valuation.md plugins/deep-o-stock-analyst/commands/reversedcf.md plugins/deep-o-stock-analyst/commands/options.md
git commit -m "feat(deep-o): add valuation commands (/wacc /valuation /reversedcf /options)" -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: Verdict & narrative commands — `/deep` `/risk` `/catalysts` `/onepager`

**Files:**
- Create: `plugins/deep-o-stock-analyst/commands/deep.md`
- Create: `plugins/deep-o-stock-analyst/commands/risk.md`
- Create: `plugins/deep-o-stock-analyst/commands/catalysts.md`
- Create: `plugins/deep-o-stock-analyst/commands/onepager.md`

- [ ] **Step 1: `deep.md`** — map source §2 DEEP Summary + §7 Weighted Score + §1 Verdict (บรรทัด 104–114, 132–141)
  - frontmatter `allowed-tools: [WebSearch, WebFetch, Read]`
  - description: `"DEEP scoring 0–100 (D25/E20/E20/P20/O15) + verdict ซื้อ/ถือ/ลด/ขาย 🟢🟡🟠🔴"`
  - สิ่งที่ทำ: ให้คะแนน 0–5 แต่ละหัวข้อ D/E/E/P/O พร้อมลิงก์ → ถ่วงน้ำหนักเป็น 0–100 → verdict ตามตาราง + Confidence 0–5
  - ใส่ตาราง verdict เต็ม (เหมือน SKILL §6)

- [ ] **Step 2: `risk.md`** — map source §4 Risk Map + §5 Bull/Base/Bear (บรรทัด 123–127)
  - frontmatter `allowed-tools: [WebSearch, WebFetch, Read]`
  - description: `"Risk Map (Regulation/Execution/GeoFX/ESG) + Bull/Base/Bear + thesis killers"`
  - สิ่งที่ทำ: Risk Map 4 ด้าน + ลิงก์หน่วยงานกำกับ → Bull/Base/Bear scenarios + Triggers & Thesis Killers

- [ ] **Step 3: `catalysts.md`** — map source §6 Catalysts Map (บรรทัด 129–130)
  - frontmatter `allowed-tools: [WebSearch, WebFetch, Read]`
  - description: `"Catalysts Map 12–24 เดือน — วัน/ไตรมาส + owner metric + แหล่งอ้างอิง"`
  - สิ่งที่ทำ: ตาราง catalyst (timeline 12–24 เดือน) แต่ละตัวมี owner metric + แหล่งอ้างอิง

- [ ] **Step 4: `onepager.md`** — map source §8 One-Pager (บรรทัด 142–143)
  - frontmatter `allowed-tools: [Read]` (ไม่ต้อง web — สรุปจากที่วิเคราะห์แล้ว)
  - description: `"One-Pager ภาษาง่าย — เล่าเป็นเรื่องเดียวแบบนั่งฟังรายงานในห้องประชุม"`
  - สิ่งที่ทำ: สรุปทุกแง่มุมเป็นเรื่องเล่าภาษาง่าย ไม่มี bullet มือใหม่ฟังรู้เรื่อง

- [ ] **Step 5: Verify ทั้ง 4 ไฟล์ + onepager ไม่มี web tool**

Run:
```bash
for f in deep risk catalysts onepager; do
  grep -q "deep-o-stock-analyst:$f" plugins/deep-o-stock-analyst/commands/$f.md && echo "$f OK"
done
grep -q "WebSearch" plugins/deep-o-stock-analyst/commands/onepager.md && echo "onepager has web (unexpected)" || echo "onepager no-web OK"
```
Expected: `deep OK` / `risk OK` / `catalysts OK` / `onepager OK` / `onepager no-web OK`

- [ ] **Step 6: Commit** (ขอนายท่านก่อน — L2)

```bash
git add plugins/deep-o-stock-analyst/commands/deep.md plugins/deep-o-stock-analyst/commands/risk.md plugins/deep-o-stock-analyst/commands/catalysts.md plugins/deep-o-stock-analyst/commands/onepager.md
git commit -m "feat(deep-o): add verdict + narrative commands (/deep /risk /catalysts /onepager)" -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: README.md

**Files:**
- Create: `plugins/deep-o-stock-analyst/README.md`

mirror โครง `plugins/portfolio-risk-architect/README.md`

- [ ] **Step 1: เขียน README** — sections:
  1. `# Deep-O Stock Analyst` + คำโปรย (วิเคราะห์หุ้นรายตัว US ด้วยกรอบ DEEP+O สไตล์ Damodaran+McKinsey)
  2. `> เรียบเรียงจาก Earthh Evans · Invest Hub`
  3. `## plugin นี้มีอะไร` — ตาราง: Skill / Agent / 10 Commands
  4. `## ติดตั้ง`:
     ```
     /plugin marketplace add mrunknown2/Earthh-Evans-Finance-Skill
     /plugin install deep-o-stock-analyst
     ```
  5. `## ใช้งาน` 3 แบบ (skill อัตโนมัติ / command `/full NVDA` / agent)
  6. `## คำสั่งทั้งหมด` — ตาราง 10 commands (mapping จาก spec §5.3)
  7. `## ขอบเขต` — วิเคราะห์**หุ้นรายตัว US** · เสริมพี่ `portfolio-risk-architect` (พอร์ตรวม) ไม่ทับกัน
  8. DISCLAIMER block [R1]

- [ ] **Step 2: Verify**

Run:
```bash
grep -q "deep-o-stock-analyst" plugins/deep-o-stock-analyst/README.md && \
grep -q "/full" plugins/deep-o-stock-analyst/README.md && \
grep -q "ไม่ใช่คำแนะนำการลงทุนรายบุคคล" plugins/deep-o-stock-analyst/README.md && echo "OK"
```
Expected: `OK`

- [ ] **Step 3: Commit** (ขอนายท่านก่อน — L2)

```bash
git add plugins/deep-o-stock-analyst/README.md
git commit -m "docs(deep-o): add plugin README" -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 8: Register in marketplace.json

**Files:**
- Modify: `.claude-plugin/marketplace.json` (เพิ่ม object ที่ 2 ใน `plugins[]`)

- [ ] **Step 1: เพิ่ม entry** — แก้ array `plugins` ให้มี object ที่ 2 (ต่อจาก portfolio-risk-architect):

```json
    {
      "name": "deep-o-stock-analyst",
      "source": "./plugins/deep-o-stock-analyst",
      "description": "Deep-O Stock Analyst — วิเคราะห์หุ้นรายตัว (US) ด้วยกรอบ DEEP+O (Demand/Execution/Economics/Price/Optionality) สไตล์ Damodaran + McKinsey: live-data check, Damodaran DCF → intrinsic value, reverse DCF, option-adjusted valuation, DEEP score 0–100 → verdict ซื้อ/ถือ/ลด/ขาย. 10 commands. เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล.",
      "version": "0.1.0",
      "keywords": ["finance", "investing", "stock", "equity", "valuation", "dcf", "damodaran", "deep-o", "intrinsic-value", "reverse-dcf", "hedge-fund", "earth-evans"]
    }
```
(อย่าลืม comma หลัง object แรก)

- [ ] **Step 2: Verify JSON valid + มี 2 plugins**

Run:
```bash
python3 -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); n=[p['name'] for p in d['plugins']]; print('OK', n) if len(n)==2 and 'deep-o-stock-analyst' in n else print('FAIL', n)"
```
Expected: `OK ['portfolio-risk-architect', 'deep-o-stock-analyst']`

- [ ] **Step 3: Commit** (ขอนายท่านก่อน — L2)

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat(deep-o): register deep-o-stock-analyst in marketplace" -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 9: Final verification + source file decision

**Files:**
- (decision) `deep-o-stock-analysis-prompt.md` ที่ root

- [ ] **Step 1: Verify โครงไฟล์ครบ 14 ไฟล์**

Run:
```bash
find plugins/deep-o-stock-analyst -type f | sort
```
Expected (14 ไฟล์): plugin.json, README.md, SKILL.md, agent .md, + 10 commands

- [ ] **Step 2: Verify ทุก JSON valid**

Run:
```bash
python3 -c "import json; json.load(open('plugins/deep-o-stock-analyst/.claude-plugin/plugin.json')); json.load(open('.claude-plugin/marketplace.json')); print('JSON OK')"
```
Expected: `JSON OK`

- [ ] **Step 3: Verify disclaimer ปรากฏทุก surface (SKILL+agent+README+ทุก command)**

Run:
```bash
miss=0
for f in plugins/deep-o-stock-analyst/skills/deep-o-stock-analyst/SKILL.md \
         plugins/deep-o-stock-analyst/agents/deep-o-stock-analyst.md \
         plugins/deep-o-stock-analyst/README.md \
         plugins/deep-o-stock-analyst/commands/*.md; do
  grep -q "เชิงการศึกษา\|ไม่ใช่คำแนะนำ" "$f" || { echo "MISSING disclaimer: $f"; miss=1; }
done
[ $miss -eq 0 ] && echo "ALL surfaces have disclaimer"
```
Expected: `ALL surfaces have disclaimer`

- [ ] **Step 4: Verify ทุก command frontmatter ถูก (description + allowed-tools + model)**

Run:
```bash
for f in plugins/deep-o-stock-analyst/commands/*.md; do
  grep -q "^description:" "$f" && grep -q "allowed-tools:" "$f" && grep -q "model: opus" "$f" || echo "BAD frontmatter: $f"
done
echo "frontmatter check done"
```
Expected: ไม่มีบรรทัด `BAD frontmatter` + `frontmatter check done`

- [ ] **Step 5: ตัดสินใจชะตา source file** — ถามนายท่าน: เก็บ `deep-o-stock-analysis-prompt.md` ไว้เป็น reference / ย้ายเข้า `plugins/deep-o-stock-analyst/` / ลบ (เนื้อหาถูกหั่นเข้า plugin หมดแล้ว). **ไม่ลบเองโดยไม่ถาม** (guardrails L2.3)

- [ ] **Step 6: รายงานผล + เสนอ PR** — สรุป plugin #2 เสร็จ เสนอนายท่านเปิด PR เข้า main (guardrails: merge เข้า main = L1 ต้องนายท่านทำเอง; เปิด PR = L2 ขอก่อน)

---

## Self-Review (ผู้เขียน plan ตรวจเอง)

**1. Spec coverage** — เทียบ spec §4–§9:
- §4 file structure → Task 1–8 ✅
- §5.1 SKILL → Task 2 ✅ · §5.2 agent → Task 3 ✅ · §5.3 commands (10) → Task 4,5,6 ✅ · §5.4 README → Task 7 ✅ · §5.5 plugin.json+marketplace → Task 1,8 ✅
- §6 disclaimer → Task 9 Step 3 verify ✅
- §7 refinements R1(disclaimer)→ทุก task · R2(K→E)→Task 2/3/5 · R3(input ticker)→Task 4 · R4(web tools)→Task 3/4/5/6 · R5(as-of)→Task 2/3 ✅
- §9 success criteria → Task 9 verify ทั้งหมด ✅

**2. Placeholder scan** — ไม่มี TBD/TODO; ทุก frontmatter/JSON ใส่เต็ม; body content map ไป source บรรทัดชัด (ไม่ใช่ placeholder เพราะ source file มีจริง)

**3. Type consistency** — ชื่อ plugin `deep-o-stock-analyst` · slash prefix `/deep-o-stock-analyst:<cmd>` · 10 command names (full/livecheck/wacc/valuation/reversedcf/options/deep/risk/catalysts/onepager) ตรงกันทุก task · verdict table เหมือนกันใน SKILL/agent/deep
```
