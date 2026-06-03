# Reverse DCF Screener Plugin — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** สร้างปลั๊กอินที่ 4 `reverse-dcf-screener` — แปลง Excel "Reverse DCF Screener (Terminal-Anchored)" ของ Earthh Evans เป็น portable skill + Claude Code plugin (1 skill + 1 agent + 9 commands) ที่ดึงงบ → กรอก Excel template → คำนวณ → สรุป verdict + โซนราคา

**Architecture:** Portable-core (skill package: `SKILL.md` + assets + references + `fill_engine.py`) ที่ Claude Code/Codex/Antigravity อ่านได้เหมือนกัน + เปลือก Claude Code (plugin.json + agent + commands). เครื่องยนต์คำนวณคือ `fill_engine.py` (กรอก input cells + คำนวณคู่ขนาน, คงสูตร Excel ไว้ recalc ตอนเปิด)

**Tech Stack:** Python 3 + `openpyxl` · Markdown (agent/commands/skill/references) · Excel `.xlsx` template

**Spec:** `docs/superpowers/specs/2026-06-03-reverse-dcf-screener-design.md`

> ⚠️ **Git policy (นายท่านสั่ง):** ไม่ commit ราย task — สร้างไฟล์ทั้งหมดก่อน, ทดสอบจริง, แล้ว commit ทีเดียวตอนจบเมื่อนายท่านอนุมัติ (Task 9)

---

## File Structure

```
plugins/reverse-dcf-screener/
├── .claude-plugin/plugin.json
├── agents/reverse-dcf-screener.md
├── commands/{analyze,verify,zones,full,quick,screener,wacc,sensitivity,methodology}.md
├── skills/reverse-dcf-screener/
│   ├── SKILL.md
│   ├── assets/reverse_dcf_screener.xlsx
│   ├── references/{methodology,prompt,wacc-damodaran}.md
│   └── scripts/fill_engine.py
├── INSTALL.md
└── README.md
+ root: .claude-plugin/marketplace.json (edit), README.md (edit)
```

---

## Task 1: Template สะอาด + ตรวจโครงสูตร

**Files:**
- Create: `plugins/reverse-dcf-screener/skills/reverse-dcf-screener/assets/reverse_dcf_screener.xlsx`
- Reference (read-only): `source/reverse_DCF_Template.xlsx`

- [ ] **Step 1: เขียน script เตรียม template** (`/tmp/make_template.py`)

ก๊อป source → ล้างเคสตัวอย่าง → เซฟลง assets/ คงสูตร+conditional formatting+data validation ทั้งหมด

```python
import openpyxl, warnings, shutil, os
warnings.filterwarnings("ignore")
SRC = "source/reverse_DCF_Template.xlsx"
DST = "plugins/reverse-dcf-screener/skills/reverse-dcf-screener/assets/reverse_dcf_screener.xlsx"
os.makedirs(os.path.dirname(DST), exist_ok=True)
shutil.copy(SRC, DST)
wb = openpyxl.load_workbook(DST)  # keep_vba=False, formulas preserved
eng = wb["Engine"]
# ล้าง input ตัวอย่าง IREN (เฉพาะ input cells — ห้ามแตะสูตร)
for cell in ["C4","C5","C6","C7","C9","C11","C12","C13","C14","C15",
             "C18","C19","C20","C21","C22","C40","C43","C44","C45","C48","C49","C50"]:
    eng[cell] = None
# ล้าง commentary SIMO ค้าง (static text cells)
for cell in ["F31","F32","F38"]:
    eng[cell] = None
# ล้างแถวตัวอย่างใน Screener (rows 10-13: SpaceX/SIMO/PL/IREN) — เฉพาะ input cols
scr = wb["Screener"]
for r in range(10, 14):
    for col in ["A","B","D","E","F","G","H","I","J","K","Q"]:
        scr[f"{col}{r}"] = None
wb.save(DST)
print("template cleaned ->", DST)
```

- [ ] **Step 2: รัน + verify**

Run: `python3 /tmp/make_template.py && python3 -c "import openpyxl,warnings; warnings.filterwarnings('ignore'); wb=openpyxl.load_workbook('plugins/reverse-dcf-screener/skills/reverse-dcf-screener/assets/reverse_dcf_screener.xlsx'); e=wb['Engine']; print('C4(ticker)=',e['C4'].value,'| C30 formula=',e['C30'].value,'| C41 formula=',e['C41'].value)"`

Expected: `C4(ticker)= None | C30 formula= =(C29/C5)^(1/(C15+1))-1 | C41 formula= =IF(C39>C40,...` — input ว่าง, สูตรยังอยู่

---

## Task 2: `fill_engine.py` — เครื่องยนต์ (TDD เต็ม)

**Files:**
- Create: `plugins/reverse-dcf-screener/skills/reverse-dcf-screener/scripts/fill_engine.py`
- Test: `plugins/reverse-dcf-screener/skills/reverse-dcf-screener/scripts/test_fill_engine.py`

หน้าที่: รับ JSON input (stdin) → คำนวณ (port สูตร Excel) → ก๊อป template → เขียน input cells → print JSON ผล

- [ ] **Step 1: เขียน failing test (golden case IREN จากรูปจริงของ Earth)**

```python
# test_fill_engine.py
import json, subprocess, sys, os, math
HERE = os.path.dirname(__file__)
SCRIPT = os.path.join(HERE, "fill_engine.py")

IREN = {
    "ticker": "IREN", "revenue_r0": 0.757, "ev": 22.6, "sector": "Software (System/Application)",
    "wacc": 0.095, "terminal_margin": 0.35, "terminal_g": 0.04, "terminal_roic": 0.15,
    "tax": 0.25, "horizon_n": 10, "hist_cagr": 0.60, "fade": 0.70, "tam": 150.0,
    "max_pen": 0.25, "abs_ceiling": 0.45, "buffer": 0.05, "price": 65.33,
    "shares_m": 357.38, "net_debt": -0.7, "consensus_fy1": 1.09,
    "analyst_target": 79.04, "analyst_range": "$29 - $100+", "no_write": True
}

def run(payload):
    p = subprocess.run([sys.executable, SCRIPT], input=json.dumps(payload),
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    return json.loads(p.stdout)

def approx(a, b, tol=0.005): return abs(a-b) <= tol

def test_iren_golden():
    r = run(IREN)
    assert approx(r["implied_cagr"], 0.320), r["implied_cagr"]
    assert approx(r["plausible_cagr"], 0.420), r["plausible_cagr"]
    assert approx(r["gap"], -0.100), r["gap"]
    assert "ถูก" in r["verdict"], r["verdict"]
    assert approx(r["zones"]["fair_value"], 143.56, tol=0.6), r["zones"]["fair_value"]
    assert approx(r["zones"]["strong_buy"], 97.42, tol=0.6), r["zones"]["strong_buy"]
    assert approx(r["zones"]["red_flag"], 301.30, tol=1.0), r["zones"]["red_flag"]

def test_tam_zero_uses_other_caps():
    payload = dict(IREN); payload["tam"] = 0
    r = run(payload)
    # Cap B หลุด → Plausible = MIN(CapA=0.42, CapC=0.45) = 0.42
    assert approx(r["plausible_cagr"], 0.420), r["plausible_cagr"]

def test_expensive_verdict():
    payload = dict(IREN); payload["price"] = 250.0; payload["ev"] = 90.0
    r = run(payload)
    assert "แพง" in r["verdict"], (r["verdict"], r["implied_cagr"])
```

- [ ] **Step 2: รัน test ให้ fail**

Run: `cd plugins/reverse-dcf-screener/skills/reverse-dcf-screener/scripts && python3 -m pytest test_fill_engine.py -v`
Expected: FAIL (fill_engine.py ยังไม่มี / no such file)

- [ ] **Step 3: เขียน `fill_engine.py`**

```python
#!/usr/bin/env python3
"""Reverse DCF (Terminal-Anchored) engine — กรอก input + คำนวณคู่ขนาน.
รับ JSON ทาง stdin, print JSON ผลทาง stdout. คงสูตร Excel ไว้ recalc ตอนเปิด."""
import sys, json, os, shutil, datetime, warnings
warnings.filterwarnings("ignore")

TEMPLATE = os.path.join(os.path.dirname(__file__), "..", "assets", "reverse_dcf_screener.xlsx")

# map field -> Engine input cell (yellow) — ห้ามแตะช่องสูตร
ENGINE_CELLS = {
    "ticker":"C4","revenue_r0":"C5","ev":"C6","sector":"C7","wacc_override":"C9",
    "terminal_margin":"C11","terminal_g":"C12","terminal_roic":"C13","tax":"C14",
    "horizon_n":"C15","hist_cagr":"C18","fade":"C19","tam":"C20","max_pen":"C21",
    "abs_ceiling":"C22","buffer":"C40","price":"C43","shares_m":"C44","net_debt":"C45",
    "analyst_target":"C48","analyst_range":"C49","consensus_fy1":"C50",
}

def compute(d):
    R0=d["revenue_r0"]; EV=d["ev"]; W=d["wacc"]; m=d["terminal_margin"]
    g=d["terminal_g"]; roic=d["terminal_roic"]; tax=d["tax"]; N=d["horizon_n"]
    hist=d["hist_cagr"]; fade=d["fade"]; tam=d.get("tam",0); maxpen=d["max_pen"]
    absc=d["abs_ceiling"]; buf=d["buffer"]; nd=d["net_debt"]; sh=d["shares_m"]
    fwd = (d["consensus_fy1"]/R0 - 1) if d.get("consensus_fy1") else 0
    reinv = g/roic
    tv = EV*(1+W)**N
    fcff = tv*(W-g)
    conv = m*(1-tax)*(1-reinv)
    rstar = fcff/conv
    implied = (rstar/R0)**(1/(N+1)) - 1
    capA = max(hist, fwd)*fade
    capB = 999 if tam in (0,None) else (maxpen*tam/R0)**(1/(N+1)) - 1
    capC = absc
    plausible = min(capA, capB, capC)
    gap = implied - plausible
    if gap > buf: verdict = "แพง — Priced for Perfection"
    elif gap < -buf: verdict = "ถูก — Low Expectations"
    else: verdict = "Fair — สมเหตุสมผล"
    def price_at(cagr):
        return ((R0*(1+cagr)**(N+1)*conv/(W-g)/(1+W)**N) - nd)*1000/sh
    zones = {
        "strong_buy": price_at(max(plausible-0.05,0)),
        "fair_value": price_at(plausible),
        "caution_low": price_at(plausible+0.05),
        "caution_high": price_at(plausible+0.10),
        "red_flag": price_at(plausible+0.10),
    }
    return {
        "ticker": d.get("ticker"), "reinvestment": reinv, "terminal_value": tv,
        "fcff_n1": fcff, "conversion": conv, "implied_terminal_revenue": rstar,
        "implied_cagr": implied, "cap_a": capA, "cap_b": capB, "cap_c": capC,
        "plausible_cagr": plausible, "gap": gap, "verdict": verdict,
        "ev_sales": EV/R0, "current_price": d.get("price"), "zones": zones,
    }

def write_xlsx(d, out_path):
    import openpyxl
    shutil.copy(TEMPLATE, out_path)
    wb = openpyxl.load_workbook(out_path)
    eng = wb["Engine"]
    eng["C7"] = d.get("sector")
    if "wacc" in d and not d.get("sector_wacc_ok"):
        eng["C9"] = d["wacc"]   # ใส่ WACC เป็น override (กัน sector ดึงไม่ติด)
    for f, cell in ENGINE_CELLS.items():
        if f in ("sector","wacc_override"): continue
        if f in d and d[f] is not None:
            eng[cell] = d[f]
    wb.save(out_path)
    return out_path

def main():
    d = json.load(sys.stdin)
    res = compute(d)
    if not d.get("no_write"):
        os.makedirs("analyses", exist_ok=True)
        stamp = d.get("date") or datetime.date.today().isoformat()
        out = os.path.join("analyses", f"{d.get('ticker','STOCK')}_{stamp}.xlsx")
        res["file"] = write_xlsx(d, out)
    print(json.dumps(res, ensure_ascii=False))

if __name__ == "__main__":
    main()
```

> หมายเหตุ: test ส่ง `wacc` ตรงๆ + `no_write:True` → ใช้ `compute()` ล้วน. ตอนรันจริง agent ใส่ `wacc` (override) เพื่อกัน WACC table placeholder ดึงผิด

- [ ] **Step 4: รัน test ให้ pass**

Run: `cd plugins/reverse-dcf-screener/skills/reverse-dcf-screener/scripts && python3 -m pytest test_fill_engine.py -v`
Expected: PASS ทั้ง 3 tests

- [ ] **Step 5: ทดสอบ write จริง (สร้างไฟล์)**

Run: `cd <repo-root> && echo '{"ticker":"IREN","revenue_r0":0.757,"ev":22.6,"sector":"Software (System/Application)","wacc":0.095,"terminal_margin":0.35,"terminal_g":0.04,"terminal_roic":0.15,"tax":0.25,"horizon_n":10,"hist_cagr":0.60,"fade":0.70,"tam":150,"max_pen":0.25,"abs_ceiling":0.45,"buffer":0.05,"price":65.33,"shares_m":357.38,"net_debt":-0.7,"consensus_fy1":1.09}' | python3 plugins/reverse-dcf-screener/skills/reverse-dcf-screener/scripts/fill_engine.py`
Expected: JSON มี `"file":"analyses/IREN_<date>.xlsx"` + `"verdict":"ถูก — Low Expectations"` ; ไฟล์ถูกสร้าง

---

## Task 3: References (3 ไฟล์, ไทยผสม EN)

**Files:**
- Create: `.../references/methodology.md`
- Create: `.../references/prompt.md`
- Create: `.../references/wacc-damodaran.md`

- [ ] **Step 1: `methodology.md`** — ถอดจาก sheet วิธีใช้ + Engine. ต้องมี sections: แนวคิด · ตรรกะ Terminal-Anchored (5 สเต็ป) · Plausible heuristic (Cap A/B/C) · Verdict+Buffer · โซนราคา 4 ระดับ · Convention (N, N+1) · ข้อควรระวัง (mature overstate, TAM squishy, WACC placeholder, tips cyclical/pre-profit). ใส่บล็อกสูตรจาก spec §6

- [ ] **Step 2: `prompt.md`** — ฐานจาก AI_Prompts B4. ต้องมี: persona buy-side analyst · ข้อบังคับ (ลำดับแหล่ง 10-K/10-Q/earnings, time basis FY/LTM/NTM, ห้ามเดา, as-of date) · รายการข้อมูล 10 อย่าง · **JSON schema สำหรับ fill_engine.py** (keys ตาม `ENGINE_CELLS` + wacc/consensus_fy1) · flag ปิดท้าย (เหมาะ Terminal-Anchored ไหม + ต้อง verify อะไร). ระบุ screener ผ่าน `/screener`

JSON schema ที่ต้องระบุใน prompt.md:
```json
{"ticker":"", "revenue_r0":0, "ev":0, "sector":"", "wacc":0,
 "terminal_margin":0, "terminal_g":0, "terminal_roic":0, "tax":0, "horizon_n":10,
 "hist_cagr":0, "fade":0.70, "tam":0, "max_pen":0.25, "abs_ceiling":0.45, "buffer":0.05,
 "price":0, "shares_m":0, "net_debt":0, "consensus_fy1":0,
 "analyst_target":0, "analyst_range":""}
```

- [ ] **Step 3: `wacc-damodaran.md`** — ตาราง 25 sectors (ยกจาก `source` WACC_Damodaran) + ป้าย ⚠️ placeholder + ลิงก์ https://pages.stern.nyu.edu/~adamodar + วิธีอัปเดต ม.ค. ทุกปี

- [ ] **Step 4: verify** — `ls -1 .../references/` เห็น 3 ไฟล์ + `grep -l "Terminal-Anchored" methodology.md` + `grep -c "0\\." wacc-damodaran.md` ≥ 25 (source WACC_Damodaran มี 25 sectors จริง)

---

## Task 4: `SKILL.md` (แกน portable)

**Files:** Create `.../skills/reverse-dcf-screener/SKILL.md`

- [ ] **Step 1: เขียน SKILL.md** — frontmatter (name, description ตาม spec §4) + body: intro+เครดิต Earth · routing table (สถานการณ์→command) · critical rules ย่อ (verify 2 รอบ, sector ตรง table, ไม่กุ, as-of date) · วิธีใช้ข้าม IDE (ชี้ INSTALL.md) · disclaimer

- [ ] **Step 2: verify frontmatter** — `head -8 SKILL.md` เห็น `name: reverse-dcf-screener` + `description:` ; routing table มีครบ 9 commands

---

## Task 5: Agent

**Files:** Create `.../agents/reverse-dcf-screener.md`

- [ ] **Step 1: เขียน agent** — frontmatter (`tools: Read, Write, Bash, WebSearch, WebFetch` + `model: opus`) + body 8 sections ตาม spec §4 (ROLE, Discipline, Methodology, โซนราคา, Workflow 3 สเต็ป, Critical Rules, Commands, Disclaimer). ฝังสูตรจาก spec §6 + cell map จาก spec §5

- [ ] **Step 2: verify** — `head -10 agent.md` เห็น `tools:` มี Write+Bash ; `grep -c "verify" agent.md` ≥ 1 (discipline 2 รอบ)

---

## Task 6: Commands (9 ไฟล์)

**Files:** Create `.../commands/{analyze,verify,zones,full,quick,screener,wacc,sensitivity,methodology}.md`

แต่ละไฟล์: frontmatter (`description`, `allowed-tools`, `model: opus`) + body (`# /reverse-dcf-screener:<cmd>` · Input ที่ต้องการ · สิ่งที่ทำ · ตัวอย่างสั่ง · Discipline). allowed-tools ต่อ command:

| command | allowed-tools |
|---|---|
| analyze | Read, Write, Bash, WebSearch, WebFetch |
| verify | Read, Write, Bash, WebSearch, WebFetch |
| zones | Read, Bash |
| full | Read, Write, Bash, WebSearch, WebFetch |
| quick | Read, WebSearch, WebFetch |
| screener | Read, Write, Bash |
| wacc | Read, WebSearch, WebFetch |
| sensitivity | Read, Bash |
| methodology | Read |

- [ ] **Step 1: เขียน 3 สเต็ปหลัก** (analyze, verify, zones) — analyze: รับ ticker → รัน prompt.md ดึงงบ → สร้าง JSON → รัน fill_engine.py → สรุป. verify: เช็คงบรอบ 2 → แก้ค่าเพี้ยน → rerun. zones: อ่านผล → โซนราคา 4 ระดับ
- [ ] **Step 2: เขียน pipeline** (full, quick)
- [ ] **Step 3: เขียน lookup** (screener, wacc, sensitivity, methodology)
- [ ] **Step 4: verify** — `ls -1 commands/ | wc -l` = 9 ; ทุกไฟล์มี `model: opus` (`grep -L "model: opus" commands/*.md` ว่าง)

---

## Task 7: plugin.json + README + INSTALL

**Files:** Create `.../.claude-plugin/plugin.json`, `.../README.md`, `.../INSTALL.md`

- [ ] **Step 1: `plugin.json`** — ตาม spec §8 (name, version 0.1.0, description, repository, license MIT, author mrunknown2, keywords)
- [ ] **Step 2: `README.md`** — Title+เครดิต Earth · concept table · Setup (⚠️ `pip install openpyxl`) · workflow 3 สเต็ป + อ่านผลโซนราคา · commands table (9) · installation · usage example · disclaimer
- [ ] **Step 3: `INSTALL.md`** — ตาราง 3 IDE (Claude Code/Antigravity/Codex) + `pip install openpyxl` + เตือน Codex network
- [ ] **Step 4: verify** — `python3 -c "import json; json.load(open('plugins/reverse-dcf-screener/.claude-plugin/plugin.json'))"` ไม่ error ; README มี 9 commands

---

## Task 8: Root integration

**Files:** Modify `.claude-plugin/marketplace.json`, `README.md` (root)

- [ ] **Step 1: marketplace.json** — เพิ่ม entry ที่ 4 (name, source `./plugins/reverse-dcf-screener`, description, version 0.1.0, keywords) + metadata description `"3 plugins"`→`"4 plugins"` + version `0.2.0`→`0.3.0`
- [ ] **Step 2: root README** — เพิ่มแถวตาราง plugins (`reverse-dcf-screener | ถอดความคาดหวังราคา reverse DCF | 1 skill + 1 agent + 9 commands`) + command summary block (`/full · /analyze · /verify · /zones · /quick · /screener · /wacc · /sensitivity · /methodology`)
- [ ] **Step 3: verify** — `python3 -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); assert len(d['plugins'])==4; assert '4 plugins' in d['metadata']['description']; print('OK', d['metadata']['version'])"` → `OK 0.3.0`

---

## Task 9: End-to-end test + commit (รอนายท่านอนุมัติ)

- [ ] **Step 1: รัน engine end-to-end** — รัน `/full` (หรือเรียก fill_engine.py ตรง) กับเคส IREN → ได้ไฟล์ `analyses/IREN_<date>.xlsx` + verdict ถูกต้อง
- [ ] **Step 2: เปิดไฟล์ verify** — `python3 -c "import openpyxl,warnings; warnings.filterwarnings('ignore'); e=openpyxl.load_workbook('analyses/IREN_<date>.xlsx')['Engine']; print('C5=',e['C5'].value,'C43=',e['C43'].value,'C30 formula kept=',e['C30'].value)"` → input กรอกแล้ว, สูตรยังอยู่
- [ ] **Step 3: ทดสอบจริงกับหุ้นใหม่ 1 ตัว** (นายท่านเลือก ticker) — ตรวจว่า workflow ดึงงบ → กรอก → สรุป ครบ
- [ ] **Step 4: รายงานนายท่าน + ขออนุญาต commit** — โหลด guardrails skill, ถาม branch (เช่น `feat/reverse-dcf-screener`) + commit message, แล้ว commit ทั้งชุด (รวม spec + plan + plugin)

---

## Self-Review (เทียบ plan ↔ spec)

- ✅ **Spec coverage:** §2 file tree→Task 1-8 · §3 commands→Task 6 · §4 agent/skill→Task 4-5 · §5 Excel handling→Task 1-2 · §6 สูตร→Task 2 · §7 references→Task 3 · §8 integration→Task 7-8 · §9 deps/non-goals→honored (no LibreOffice) · §10 decisions→reflected
- ✅ **Placeholder scan:** fill_engine.py + test มี code เต็ม · golden case มีตัวเลขจริง · ไม่มี TBD
- ✅ **Type consistency:** `ENGINE_CELLS` keys ↔ test payload ↔ prompt.md JSON schema ตรงกัน · `compute()` return keys ↔ test assertions ตรงกัน · cell refs ↔ spec §5 ตรงกัน
- ⚠️ **Note:** `wacc` ใส่เป็น override (C9) ตอน write — กัน WACC table placeholder ดึงผิด sector (สอดคล้อง spec: agent ดึง WACC จริงมาใส่)
