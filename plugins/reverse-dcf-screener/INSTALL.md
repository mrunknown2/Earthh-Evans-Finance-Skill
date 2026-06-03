# INSTALL — Reverse DCF Screener

แกนกลางของ plugin นี้คือ **skill package แบบ portable** (`skills/reverse-dcf-screener/` — `SKILL.md` + `assets/` + `references/` + `scripts/`) ที่ทั้ง 3 IDE อ่านได้เหมือนกัน ติดตั้งได้ตามตารางด้านล่าง

## Dependency (จำเป็นทุก IDE)

```
pip install openpyxl
```

หรือใช้ไฟล์ pin: `pip install -r skills/reverse-dcf-screener/scripts/requirements.txt`

ต้องมี **Python 3** + `openpyxl` — `scripts/fill_engine.py` ใช้ openpyxl **เฉพาะตอนเขียนไฟล์** (`/analyze`, `/full`, `/screener`) · ต้องมี **Excel / Google Sheets** เพื่อเปิดไฟล์ผลลัพธ์ให้สูตรในช่อง recalc

> 💡 **ส่วนคำนวณ verdict / screener-view ไม่ต้องใช้ openpyxl** — `compute()` เป็น stdlib ล้วน ดังนั้นถ้าแค่อยากได้คำตอบถูก/แพงใน chat โดยไม่เขียนไฟล์ ก็รันได้แม้ไม่มี package · ถ้าไม่ได้ลง openpyxl แล้วสั่งเขียนไฟล์ engine จะ **แจ้ง error ชัดเจน + คำสั่งติดตั้ง** แทน traceback ดิบ

### ⚠️ ถ้าเจอ `error: externally-managed-environment` (PEP 668)

macOS (homebrew Python) และ Linux distro ใหม่ๆ บล็อก `pip install` ลง system Python ตรงๆ — เลือกทางใดทางหนึ่ง:

```bash
# (แนะนำ) virtualenv แยกของ project
python3 -m venv .venv && . .venv/bin/activate && pip install openpyxl

# หรือ pipx (ติดตั้งแยก sandbox)
pipx install openpyxl

# หรือ override (รู้ตัวว่าทำอะไรอยู่)
pip install --break-system-packages openpyxl
```

## 4 surface (ติดตั้งต่อ platform)

แกนคือโฟลเดอร์ skill เดียว — `skills/reverse-dcf-screener/` (SKILL.md + references + assets + scripts) · **ไม่มี build/zip สำเร็จรูปให้** — surface ที่ต้อง zip ให้ทำเอง (คำสั่งด้านล่าง)

| Surface | ติดตั้ง | network | หมายเหตุ |
|---|---|---|---|
| **Claude Code** / Claude Desktop (Code tab) | `/plugin marketplace add mrunknown2/earthh-evans-finance-skill` → `/plugin install reverse-dcf-screener` | เต็ม | ใช้ command/agent ครบ 1:1 · resolve path ผ่าน `${CLAUDE_PLUGIN_ROOT}` |
| **Claude Desktop** (Chat / Cowork) | zip โฟลเดอร์ skill เอง → อัปที่ **Customize → Skills** | varies | ใช้ SKILL.md self-sufficient ตรงๆ · โครงสร้างใน zip **verify ตอนอัป** |
| **Codex CLI** | copy โฟลเดอร์ skill → `.agents/skills/reverse-dcf-screener/` | **OFF default → เปิดเอง** | path อาจเป็น `.codex/skills` ในบางเวอร์ชัน — **verify** |
| **Antigravity** | copy → `<workspace>/.agent/skills/…` หรือ global `~/.gemini/antigravity/skills/…` | verify | path / sandbox อาจต่างตาม build — **verify** |

**zip ให้ Claude Desktop (Chat):**
```bash
cd plugins/reverse-dcf-screener/skills
zip -r reverse-dcf-screener.zip reverse-dcf-screener   # แล้วอัป reverse-dcf-screener.zip
```

**เปิด network ของ Codex** (จำเป็นตอนดึงงบ — ไม่จำเป็นตอน compute offline):
```bash
codex -a never -s workspace-write -c 'sandbox_workspace_write.network_access=true'
```

## ส่วนไหนต้อง network ส่วนไหนไม่

- **compute / verdict / โซนราคา** = Python stdlib **offline ได้ทุก platform** ✅
- **เขียน Excel** = ต้อง `openpyxl` (offline · ดู Dependency ด้านบน)
- **ดึงงบ** (10-K / 10-Q / Damodaran ผ่าน WebFetch/WebSearch) = ต้อง **network** → Codex เปิด flag, Desktop-Chat แล้วแต่ setting

## Verification checklist (รันจริงต่อ platform)

ทำทีละข้อหลังติดตั้งบนแต่ละ platform:

- [ ] **เห็น skill** — platform list ขึ้น `reverse-dcf-screener`
- [ ] **engine offline** — รัน:
  ```bash
  echo '{"ticker":"IREN","revenue_r0":0.757,"ev":22.6,"sector":"Software","wacc":0.095,"terminal_margin":0.35,"terminal_g":0.04,"terminal_roic":0.15,"tax":0.25,"horizon_n":10,"hist_cagr":0.60,"fade":0.70,"tam":150.0,"max_pen":0.25,"abs_ceiling":0.45,"buffer":0.05,"net_debt":-0.7,"shares_m":357.38,"no_write":true}' | python3 scripts/fill_engine.py
  ```
  คาดผล: JSON มี `"verdict"` ภาษาไทย + `"implied_cagr"` ≈ 0.32
- [ ] **เขียน Excel** — มี openpyxl แล้วสั่งเขียนไฟล์ได้ (ไม่มี → error message ชัด ไม่ใช่ traceback)
- [ ] **network** — หลังเปิด flag ดึงงบจริงได้
- [ ] **path gap** — ยืนยัน dir จริง (Codex `.agents` vs `.codex` · Antigravity `.agent` vs `.agents`) → อัปเดตหัวตารางตามผลจริง
- [ ] **zip** — Desktop-Chat อัปแล้ว skill ทำงาน (SKILL.md ถูกอ่าน)

> เขียนค่าที่ likely ไว้ + ให้ verify — เจอ path/sandbox จริงต่างจากนี้ แก้ตารางด้านบนได้เลย

## หมายเหตุการรัน `fill_engine.py` นอก Claude Code

`fill_engine.py` resolve path ของ template (`../assets/reverse_dcf_screener.xlsx`) **แบบ relative กับตำแหน่งไฟล์ตัวเอง** — ดังนั้นเรียกด้วย full path ของสคริปต์ได้เลย ไม่ต้อง `cd` เข้าไปในโฟลเดอร์ก่อน เช่น:

```
python3 /path/to/skills/reverse-dcf-screener/scripts/fill_engine.py
```

ขอแค่รันจากตำแหน่งที่สคริปต์มองเห็น `../assets/reverse_dcf_screener.xlsx` ได้ (โครงสร้าง `scripts/` กับ `assets/` ต้องอยู่ข้างกันในโฟลเดอร์ skill เดิม) ไฟล์ผลลัพธ์จะถูกเขียนลง `analyses/<TICKER>_<วันที่>.xlsx` ใน working directory ปัจจุบัน

---

> เรียบเรียงจาก **Earthh Evans · Invest Hub** · เครื่องมือเชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล
