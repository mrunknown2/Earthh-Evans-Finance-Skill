# Design Spec — `deep-o-stock-analyst` (plugin #2)

> วันที่: 2026-06-02 · marketplace: `earthh-evans-finance` · สถานะ: approved (brainstorm) → รอ writing-plans

## 1. Goal

แปลง prompt ดิบ `deep-o-stock-analysis-prompt.md` (กรอบวิเคราะห์หุ้นรายตัว **DEEP+O** สไตล์ Damodaran + McKinsey) ให้เป็น Claude Code plugin เต็มรูป — skill (auto-trigger) + agent (subagent) + 10 slash commands — โดย **mirror โครงสร้างพี่ `portfolio-risk-architect`** เพื่อความสม่ำเสมอของ marketplace

**ขอบเขตหน้าที่:** วิเคราะห์ **หุ้นรายตัว** (single-name equity) ออก verdict ซื้อ/ถือ/ลด/ขาย — เป็นคู่เสริมพี่ `portfolio-risk-architect` ที่วิเคราะห์ **พอร์ตรวม** (สองตัวไม่ทับหน้าที่กัน)

## 2. Context / Reference

- Marketplace `earthh-evans-finance` มี plugin เดียวคือ `portfolio-risk-architect` (merged, PR #1)
- โครง template ที่ mirror:
  ```
  plugins/<name>/
  ├── .claude-plugin/plugin.json
  ├── README.md
  ├── skills/<name>/SKILL.md   ← auto-trigger skill
  ├── agents/<name>.md          ← subagent
  └── commands/*.md             ← N slash commands
  ```
- Source material: `deep-o-stock-analysis-prompt.md` (146 บรรทัด) ที่ root — จะถูก "หั่น" เป็น skill/agent/commands และเกลาไปพร้อมกัน (ดู §7)

## 3. Decisions (ล็อกจาก brainstorm)

| # | หัวข้อ | ตัดสิน |
|---|---|---|
| 1 | ขอบเขตตลาด | **US เป็นหลัก** (10-K/10-Q/20-F, SEC, Damodaran ERP) — ไม่รองรับ SET/ไทยในเวอร์ชันนี้ |
| 2 | จำนวน commands | **10 commands** (mirror เต็ม ≈ พี่ portfolio 9 cmd) |
| 3 | ชื่อ plugin | **`deep-o-stock-analyst`** (folder name + slash prefix) |
| 4 | โทน verdict | **คงคม ซื้อ/ถือ/ลด/ขาย 🟢🟡🟠🔴** + ห่อด้วย disclaimer ว่าเป็น framework signal เชิงการศึกษา |

## 4. File Structure (deliverables)

```
plugins/deep-o-stock-analyst/
├── .claude-plugin/plugin.json
├── README.md
├── skills/deep-o-stock-analyst/SKILL.md
├── agents/deep-o-stock-analyst.md
└── commands/
    ├── full.md
    ├── livecheck.md
    ├── wacc.md
    ├── valuation.md
    ├── reversedcf.md
    ├── options.md
    ├── deep.md
    ├── risk.md
    ├── catalysts.md
    └── onepager.md
```
+ แก้ไข `.claude-plugin/marketplace.json` (เพิ่ม entry ตัวที่ 2)

## 5. Component Design

### 5.1 SKILL.md (auto-trigger)

- **frontmatter `description`** มี trigger keywords: `วิเคราะห์หุ้น, หุ้นรายตัว, มูลค่าหุ้น, DEEP+O, Damodaran, DCF, intrinsic value, fair value, reverse DCF, WACC, valuation, ซื้อหุ้นไหม, NVDA/AAPL/TSLA/หุ้น US` + ปิดท้าย "เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล"
- **เนื้อหา (mirror โครง SKILL พี่):**
  1. หลักคิด — Real-Time Protocol + ปรัชญา Damodaran/McKinsey (story→numbers→value)
  2. DEEP+O framework (Demand / Execution / Economics / Price / Optionality)
  3. Valuation mechanics ย่อ (WACC path · S/C reinvestment · clean-ups · stable guardrails · triangulation)
  4. Output Structure — รายงาน DEEP+O §0–§9
  5. Weighted Score (D25/E20/E20/P20/O15 = 100) + Verdict scale (≥80🟢 / 60-79🟡 / 40-59🟠 / <40🔴)
  6. Discipline (BLOCKING): ห้ามกุข้อมูล · ใส่ลิงก์ทุกตัวเลขสำคัญ · as-of date · YYYY-MM-DD · เอกสารทางการล่าสุด = source of truth
  7. Commands table (10)
  8. Disclaimer block

### 5.2 agents/deep-o-stock-analyst.md (subagent)

- **frontmatter:** `name`, `description`, `tools: Read, Write, Glob, Grep, WebSearch, WebFetch`, `model: opus`
  - 🔑 **ต่างจากพี่ portfolio** — ต้องมี `WebSearch` + `WebFetch` เพราะ MANDATORY REAL-TIME PROTOCOL บังคับ live data check
- **เนื้อหา:** ROLE (หุ้นส่วนวิเคราะห์เฮดจ์ฟันด์) → MANDATORY REAL-TIME PROTOCOL (Step A/B) → กติกาเคร่งครัด → สิ่งที่ต้องดึง → Valuation mechanics (Damodaran A–E) → DEEP+O output structure → Weighted score + Verdict → Discipline → Disclaimer

### 5.3 Commands (10) — map กับ section ของ prompt เดิม

ทุก command: frontmatter (`description`, `allowed-tools`, `model: opus`) + body (Input / สิ่งที่ทำ / ตัวอย่างสั่ง / Discipline). command ที่ดึง live data ต้องมี `WebSearch` + `WebFetch` ใน allowed-tools

| Command | map prompt section | allowed-tools |
|---|---|---|
| `/full` | orchestrate ทั้ง prompt (livecheck → ... → onepager) | WebSearch, WebFetch, Read, Write |
| `/livecheck` | "MANDATORY REAL-TIME PROTOCOL" Step A + B | WebSearch, WebFetch |
| `/wacc` | Valuation **A) Cost of Capital** → WACC path | WebSearch, WebFetch, Read |
| `/valuation` | Valuation **B) Drivers + C) Clean-ups + D) Stable + E) Triangulation** → intrinsic value | WebSearch, WebFetch, Read |
| `/reversedcf` | Report **§3 Reverse DCF** (implied steady-state) | WebSearch, WebFetch, Read |
| `/options` | Report **§3' Option-Adjusted** + DEEP §2.5 O | WebSearch, WebFetch, Read |
| `/deep` | Report **§2 DEEP Summary + §7 Weighted Score + §1 Verdict** | WebSearch, WebFetch, Read |
| `/risk` | Report **§4 Risk Map + §5 Bull/Base/Bear** + thesis killers | WebSearch, WebFetch, Read |
| `/catalysts` | Report **§6 Catalysts Map** (12–24 เดือน) | WebSearch, WebFetch, Read |
| `/onepager` | Report **§8 One-Pager** (ภาษาง่าย) | Read |

> `/full` คือ entry point หลัก (แนะนำเริ่มที่นี่) แล้วเจาะมุมด้วย command อื่น — pattern เดียวกับ `/full` ของพี่ portfolio

### 5.4 README.md

mirror โครง README พี่: ตาราง"plugin นี้มีอะไร" · ติดตั้ง · ใช้งาน 3 แบบ (skill อัตโนมัติ / command / agent) · command list (10) · Disclaimer · ระบุขอบเขต "หุ้นรายตัว US · เสริมพี่ portfolio-risk-architect"

### 5.5 plugin.json + marketplace.json

- `plugin.json`: name `deep-o-stock-analyst`, version `0.1.0`, description, repository (เดียวกับ marketplace), license MIT, author mrunknown2, keywords (`stock, equity, valuation, dcf, damodaran, deep-o, intrinsic-value, reverse-dcf, hedge-fund, earth-evans`)
- `marketplace.json`: เพิ่ม object ที่ 2 ใน `plugins[]` (source `./plugins/deep-o-stock-analyst`)

## 6. Disclaimer Policy

ทุก surface (SKILL, agent, README, ทุก command body) ปิดท้ายด้วย disclaimer สอดคล้องกับพี่ portfolio:

> เครื่องมือนี้เป็นกรอบวิเคราะห์เชิงการศึกษา **ไม่ใช่คำแนะนำการลงทุนรายบุคคล** · verdict (ซื้อ/ถือ/ลด/ขาย) เป็น **framework signal** จากกรอบ DEEP+O ไม่ใช่คำสั่งซื้อขาย · ตัวเลข valuation อิงสมมติฐาน (WACC, g∞, margin) ที่ระบุไว้ · ผู้ใช้ต้อง verify เอกสารทางการล่าสุดและพิจารณาบริบทของตนเองก่อนตัดสินใจ

## 7. Prompt Refinements (เกลาไปพร้อมแปลง)

แก้ไขจาก `deep-o-stock-analysis-prompt.md` ตอนหั่นเป็นไฟล์:

| # | จุด | แก้เป็น |
|---|---|---|
| R1 | ไม่มี Disclaimer เลย | เติม disclaimer block (§6) ทุก surface |
| R2 | Valuation section กระโดด A→B→C→D→**K** (E–J หาย) | รีเลเบล Triangulation **K → E** ให้ต่อเนื่อง |
| R3 | placeholder `> วันที่:` / `> หุ้น:` | รับเป็น input ของ command (เช่น `/full NVDA` หรือถาม ticker ถ้าไม่ระบุ) |
| R4 | prompt บังคับ search แต่ pattern พี่ portfolio ไม่มี web tool | agent + commands ที่ดึง live data ใส่ `WebSearch` + `WebFetch` |
| R5 | as-of date / unit consistency | คงกติกาเดิม (YYYY-MM-DD, สกุลเงินคงที่, FX ระบุอัตรา+วันที่) ใน Discipline ทุก surface |

> source file `deep-o-stock-analysis-prompt.md` — เก็บไว้ที่ root เป็น reference (ตัดสินใจตอน writing-plans ว่าจะ track/ย้าย/ลบ)

## 8. Out of Scope (YAGNI)

- ❌ ตลาดไทย/SET, 56-1 One Report, CRP รายประเทศนอก US
- ❌ การเชื่อม API ราคาหุ้น real-time (ใช้ WebSearch/WebFetch ตาม protocol เท่านั้น)
- ❌ Portfolio-level analysis (เป็นหน้าที่พี่ `portfolio-risk-architect`)
- ❌ Backtesting / สร้างกราฟราคาในอดีต

## 9. Success Criteria

1. โครงไฟล์ครบตาม §4 + ผ่านการ validate marketplace (plugin โหลดได้)
2. SKILL auto-trigger ด้วย keyword หุ้น/valuation/DEEP+O
3. ทั้ง 10 commands มี frontmatter ถูก format + allowed-tools ตรงตาราง §5.3
4. agent มี WebSearch+WebFetch + Real-Time Protocol ครบ
5. Disclaimer ปรากฏทุก surface (§6)
6. Refinements R1–R5 ถูก apply
7. marketplace.json มี 2 plugins, JSON valid
