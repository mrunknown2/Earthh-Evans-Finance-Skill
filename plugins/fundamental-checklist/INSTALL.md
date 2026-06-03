# INSTALL — Fundamental Checklist

แกนกลางของ plugin นี้คือ **skill package แบบ portable** (`skills/fundamental-checklist/` — `SKILL.md` + `references/` + `scripts/`) ที่ทั้ง 3 IDE อ่านได้เหมือนกัน ติดตั้งได้ตามตารางด้านล่าง

## Dependency

**ไม่มี — Python 3 stdlib เท่านั้น**

```
ไม่ต้อง pip install ใด ๆ ทั้งสิ้น
```

`checklist_engine.py` ใช้ `sys` และ `json` ล้วน ไม่มี third-party dependency เลย · ทำงานได้ทันทีบนทุก platform ที่มี Python 3 ติดตั้งอยู่แล้ว

> นี่คือความแตกต่างหลักจาก `reverse-dcf-screener` ซึ่งต้องการ `openpyxl` — `fundamental-checklist` ไม่เขียนไฟล์ Excel จึงไม่ต้องการ package ใดเพิ่มเติม

## 3 Surface (ติดตั้งต่อ platform)

แกนคือโฟลเดอร์ skill เดียว — `skills/fundamental-checklist/` (SKILL.md + references + scripts) · **ไม่มี build/zip สำเร็จรูปให้** — surface ที่ต้อง zip ให้ทำเอง (คำสั่งด้านล่าง)

| Surface | ติดตั้ง | network | หมายเหตุ |
|---|---|---|---|
| **Claude Code** / Claude Desktop (Code tab) | `/plugin marketplace add mrunknown2/earthh-evans-finance-skill` → `/plugin install fundamental-checklist` | เต็ม | ใช้ command/agent ครบ 1:1 · resolve path ผ่าน `${CLAUDE_PLUGIN_ROOT}` |
| **Antigravity** | copy `skills/fundamental-checklist/` → `<workspace>/.agent/skills/fundamental-checklist/` หรือ global `~/.gemini/antigravity/skills/fundamental-checklist/` | verify | path / sandbox อาจต่างตาม build — **verify** |
| **Codex CLI** | copy `skills/fundamental-checklist/` → `.agents/skills/fundamental-checklist/` | **OFF default → เปิดเอง** | path อาจเป็น `.codex/skills` ในบางเวอร์ชัน — **verify** |

**zip สำหรับ Claude Desktop (Chat):**
```bash
cd plugins/fundamental-checklist/skills
zip -r fundamental-checklist.zip fundamental-checklist   # แล้วอัป fundamental-checklist.zip
```

**เปิด network ของ Codex** (จำเป็นตอนดึงงบ — ไม่จำเป็นตอน compute offline):
```bash
codex -a never -s workspace-write -c 'sandbox_workspace_write.network_access=true'
```

## ส่วนไหนต้อง network ส่วนไหนไม่

- **compute / screen / scorecard / companion** = Python stdlib **offline ได้ทุก platform** ✅ — ไม่ต้อง network เลย
- **ดึงงบ** (10-K / 10-Q / IR / ราคาหุ้น ผ่าน WebFetch/WebSearch) = ต้อง **network** → Codex เปิด flag, Desktop-Chat แล้วแต่ setting

## Verification checklist (รันจริงต่อ platform)

ทำทีละข้อหลังติดตั้งบนแต่ละ platform:

- [ ] **เห็น skill** — platform list ขึ้น `fundamental-checklist`
- [ ] **engine offline — mode companion:**
  ```bash
  echo '{"mode":"companion","multiple":"peg","pe":35,"eps_growth_5y":100}' \
    | python3 scripts/checklist_engine.py
  ```
  คาดผล: JSON มี `"verdict":"undervalued"` และ `"actual":0.35`
- [ ] **engine offline — mode screen:**
  ```bash
  echo '{"mode":"screen","criteria":{"roic_gt_wacc_3y":true,"fcf_conversion":0.92,"net_debt_ebitda":1.2,"gross_margin_stable_3y":true,"revenue_quality":true,"ev_sales_justified":true,"peg":0.9,"insider_no_selling":true,"macro_aligned":true,"capital_allocation_ok":true}}' \
    | python3 scripts/checklist_engine.py
  ```
  คาดผล: JSON มี `"gate_verdict":"strong"` และ `"passed":10`
- [ ] **engine offline — mode scorecard:**
  ```bash
  echo '{"mode":"scorecard","categories":[{"name":"Moat","verdict":"pass"},{"name":"Financial Strength","verdict":"pass"},{"name":"Earnings Quality","verdict":"pass"}],"red_flags":[],"screen_result":{"passed":9,"total":10}}' \
    | python3 scripts/checklist_engine.py
  ```
  คาดผล: JSON มี `"overall_read":"STRONG"` (ถ้า caution_count ≤ 1 และ red = 0)
- [ ] **network** — หลังเปิด flag ดึงงบจริงได้
- [ ] **path gap** — ยืนยัน dir จริง (Codex `.agents` vs `.codex` · Antigravity `.agent` vs `.agents`) → อัปเดตหัวตารางตามผลจริง
- [ ] **zip** — Desktop-Chat อัปแล้ว skill ทำงาน (SKILL.md ถูกอ่าน)

> เขียนค่าที่ likely ไว้ + ให้ verify — เจอ path/sandbox จริงต่างจากนี้ แก้ตารางด้านบนได้เลย

## หมายเหตุการรัน `checklist_engine.py` นอก Claude Code

`checklist_engine.py` รับ JSON จาก stdin และพิมพ์ JSON ออก stdout — ไม่ต้อง `cd` เข้าโฟลเดอร์ก่อน เรียกด้วย full path ได้เลย:

```bash
echo '<JSON>' | python3 /path/to/skills/fundamental-checklist/scripts/checklist_engine.py
```

ไม่มีการอ่าน/เขียนไฟล์ใด ๆ ทั้งสิ้น — engine รับ input จาก stdin และคืน output ที่ stdout เท่านั้น

---

> เรียบเรียงจาก **Earthh Evans · Invest Hub** · เครื่องมือเชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล
