# Design Spec — Earth Evans Finance Marketplace (MVP: Portfolio Risk Architect)

| | |
|---|---|
| **วันที่** | 2026-06-02 |
| **สถานะ** | Draft — รอ นายท่าน review |
| **Branch** | `feature/inject-mugi` |
| **Source** | `source/Portfolio_Risk_Architect_Skill.pdf` (8 หน้า, gitignored) |
| **ผู้เรียบเรียง content ต้นทาง** | Earthh Evans · Invest Hub |

---

## 1. เป้าหมาย (Goal)

สร้าง **Claude Code plugin marketplace** ที่รวบรวมความรู้ของ Earth Evans (นักลงทุน/ผู้สอน) มาทำเป็น skill / agent / command ใช้งานได้จริง โดยวางโครงให้ **port ไป provider อื่น (Gemini / ChatGPT)** ได้ในอนาคต

MVP รอบนี้ = **plugin แรก** จาก source แรก: **Portfolio Risk Architect** — เครื่องมือวินิจฉัย & ออกแบบความเสี่ยงพอร์ต multi-asset

---

## 2. Decisions (สรุปจากการ brainstorm)

| หัวข้อ | มติ |
|---|---|
| Source material | ไฟล์ใน `source/` (gitignored) — PDF ดิบของ Earth Evans |
| Provider strategy | **Claude-first** แล้วค่อย port (แยก content จาก provider config) |
| Artifact type | ครบ **skill + agent + command** |
| Domain (source แรก) | Portfolio Risk Diagnostic (Equity/ETF/Crypto/Multi-Asset) |
| Distribution | **Claude Code plugin marketplace** (`.claude-plugin/marketplace.json` + `plugins/`) |
| Plugin granularity | **1 plugin รวม artifact** — source ถัดไป = plugin ใหม่ในเครือเดียวกัน |
| Commands scope | **ครบ 9 คำสั่ง** (source ระบุชัดแล้ว) |
| ภาษา content | **ไทย** (technical terms คงรูปอังกฤษ) |

---

## 3. โครงสร้าง repo

```
Earthh-Evans-Finance-Skill/
├── .claude-plugin/
│   └── marketplace.json                       # ลงทะเบียน plugin ทั้งหมดใน marketplace
├── plugins/
│   └── portfolio-risk-architect/
│       ├── .claude-plugin/
│       │   └── plugin.json                     # metadata: name, version, description, author
│       ├── skills/
│       │   └── portfolio-risk-architect/
│       │       └── SKILL.md                     # 🧩 core methodology (auto-trigger)
│       ├── agents/
│       │   └── portfolio-risk-architect.md      # 🤖 subagent (System Prompt)
│       ├── commands/
│       │   ├── full.md            # /full       รัน workflow 8 ขั้น + ภาพหลัก
│       │   ├── xray.md            # /xray       look-through holdings + treemap
│       │   ├── overlap.md         # /overlap    heatmap ความซ้ำซ้อนระหว่างกอง
│       │   ├── risk.md            # /risk       Capital Weight vs Risk Contribution
│       │   ├── corr.md            # /corr       correlation matrix heatmap
│       │   ├── stress.md          # /stress     drawdown ในวิกฤตจริง (2008/2020/2022/2024)
│       │   ├── montecarlo.md      # /montecarlo จำลอง 10,000 เส้นทาง → distribution
│       │   ├── frontier.md        # /frontier   efficient frontier + จุดพอร์ต
│       │   └── rebalance.md       # /rebalance  before-after risk metrics
│       └── README.md                            # วิธี install + ใช้งาน + เพิ่ม skill ใหม่
├── source/                                       # 📥 PDF ดิบ (gitignored, local only)
├── docs/superpowers/specs/                       # spec นี้
├── CLAUDE.md  ·  .gitignore  ·  LICENSE  ·  README.md
```

**หลักคิดโครงสร้าง:** PDF ดิบเก็บใน `source/` (ไม่ publish) → สกัด+เรียบเรียงเป็น markdown artifacts ใน `plugins/` (publish) → ผู้ใช้ `/plugin marketplace add mrunknown2/Earthh-Evans-Finance-Skill` แล้ว install ได้

---

## 4. Artifact mapping (source → artifact)

ทุก artifact สกัดตรงจาก PDF — **ไม่แต่งเนื้อหาเพิ่มเอง** ค่าตัวเลขใน worked example ถือเป็น *illustrative* (ระบุชัดว่าต้อง verify)

### 4.1 Skill — `portfolio-risk-architect` (SKILL.md)
- **มาจาก:** หน้า 2 (Core Problem + หลักคิด 5) + หน้า 3–4 (Diagnostic Workflow 8 ขั้น + Output + Discipline + Clarify First)
- **หน้าที่:** auto-trigger เมื่อผู้ใช้คุยเรื่องวิเคราะห์/กระจายความเสี่ยงพอร์ต → ให้ Claude ใช้ framework วินิจฉัยแบบ look-through (capital weight ≠ risk weight)
- **frontmatter:** `name` + `description` เขียนให้ trigger แม่น (keyword: พอร์ต, กระจายความเสี่ยง, risk contribution, correlation, allocation)
- **อ้างอิงร่วม:** ชี้ไป agent + commands ในชุดเดียวกัน

### 4.2 Agent — `portfolio-risk-architect.md`
- **มาจาก:** หน้า 3–4 (`# ROLE` Senior Multi-Asset Portfolio Strategist & Risk Manager + PRIME DIRECTIVE + WORKFLOW + DISCIPLINE)
- **หน้าที่:** subagent สวมบทบาท "Risk Desk / CIO Office" เรียกผ่าน Agent tool เพื่อวินิจฉัยพอร์ตแบบ isolated
- **tools:** read-only analysis (ไม่ต้อง DB/git) — เน้น reasoning + simulation narrative

### 4.3 Commands — 9 ไฟล์
- **มาจาก:** หน้า 4–5 (SIMULATION COMMANDS + Command Layer table)
- **หน้าที่:** slash command เรียกแต่ละ simulation/มุมมองเฉพาะ; แต่ละไฟล์ระบุ: สิ่งที่ทำ, input ที่ต้องการ, ตัวแปร/สมมติฐาน, รูปแบบ output
- `/full` = entry point (รันครบ 8 ขั้น) · ที่เหลือ = เจาะเฉพาะมุม

---

## 5. Discipline / Disclaimer ที่ต้อง preserve (BLOCKING — ห้ามตัด)

content การเงิน + สอดคล้อง guardrails (data privacy / no fabrication) — ทุก artifact ต้องคง:

1. **ไม่ hallucinate ตัวเลข** — ถ้าไม่รู้ vol/น้ำหนัก/correlation จริง ให้ระบุ "approximate, verify" หรือถามผู้ใช้
2. **ระบุ as-of date เสมอ** — ตลาดเปลี่ยนเร็ว
3. **Educational only** — "เป็นกรอบวิเคราะห์เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล"
4. **Simulation = ช่วงความเป็นไปได้** — `/montecarlo`, `/frontier` ระบุสมมติฐาน (μ, σ, ρ, horizon) ทุกครั้ง ไม่ใช่พยากรณ์
5. **แยก fact / inference / market-implied / judgment** ในทุก output

---

## 6. Multi-provider (future — ยังไม่ทำรอบนี้)

- source PDF ระบุเองว่า deploy ได้ทั้ง Claude / GPT / Gemini
- Claude-first: ทำ `SKILL.md` + `agents/` + `commands/` (Claude format) ให้เสร็จก่อน
- Port ภายหลัง = plan แยกรอบ: gen `GEMINI.md` / `AGENTS.md` จาก content เดียวกัน (System Prompt เป็น provider-agnostic อยู่แล้ว)

---

## 7. MVP — Definition of Done

1. 🟢 `.claude-plugin/marketplace.json` + `plugins/portfolio-risk-architect/.claude-plugin/plugin.json` ถูก format — `/plugin marketplace add` + install ได้จริง
2. 🟢 `SKILL.md` — สกัด core methodology จาก source ครบ (5 หลักคิด + 8 ขั้น + discipline) + frontmatter trigger ดี
3. 🟢 `agents/portfolio-risk-architect.md` — System Prompt ครบ + frontmatter ถูก
4. 🟢 commands ครบ 9 ไฟล์ — แต่ละไฟล์ใช้งานเรียกได้
5. 🟢 Disclaimer/Discipline (§5) ปรากฏใน skill + agent + README
6. 🟢 `README.md` — วิธี install + ใช้งาน + วิธีเพิ่ม skill ใหม่จาก source ถัดไป
7. 🟢 อ้างอิงค่าตัวเลขทั้งหมดเป็น illustrative + ระบุ verify

---

## 8. Out of scope (YAGNI รอบนี้)

- ❌ Port ไป Gemini/ChatGPT (plan แยกรอบ)
- ❌ source ถัดไป (plugin อื่น) — ทำเมื่อนายท่านส่ง source เพิ่ม
- ❌ โค้ดรัน simulation จริง (Monte Carlo engine) — รอบนี้เป็น prompt/narrative ให้ AI วาด/จำลอง ไม่ใช่ executable
- ❌ CI / publish automation

---

## 9. หมายเหตุ / Open items

- source แรกได้แล้ว (`source/Portfolio_Risk_Architect_Skill.pdf`) — พร้อม implement
- ตอน implement: อ่าน text จริงจาก PDF ละเอียด (โดยเฉพาะ System Prompt หน้า 3–4 ที่ต้องคัดคำให้ตรง) ก่อนเขียน artifact
- ชื่อ author ใน `plugin.json`: ใช้ "Earthh Evans · Invest Hub" (content) — confirm กับนายท่านตอน implement
