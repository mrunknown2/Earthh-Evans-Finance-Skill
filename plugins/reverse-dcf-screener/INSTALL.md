# INSTALL — Reverse DCF Screener

แกนกลางของ plugin นี้คือ **skill package แบบ portable** (`skills/reverse-dcf-screener/` — `SKILL.md` + `assets/` + `references/` + `scripts/`) ที่ทั้ง 3 IDE อ่านได้เหมือนกัน ติดตั้งได้ตามตารางด้านล่าง

## Dependency (จำเป็นทุก IDE)

```
pip install openpyxl
```

ต้องมี **Python 3** + `openpyxl` ทุกที่ — `scripts/fill_engine.py` ใช้ openpyxl กรอก input cells ลง Excel template (engine พังถ้าไม่มี) · และต้องมี **Excel / Google Sheets** เพื่อเปิดไฟล์ผลลัพธ์ให้สูตรในช่อง recalc

## 3 IDE

| IDE | วิธีติดตั้ง |
|---|---|
| **Claude Code** | `/plugin marketplace add mrunknown2/Earthh-Evans-Finance-Skill` → `/plugin install reverse-dcf-screener` · commands resolve path ของ template/scripts ผ่าน `${CLAUDE_PLUGIN_ROOT}` ให้อัตโนมัติ |
| **Antigravity** | ก๊อปโฟลเดอร์ `skills/reverse-dcf-screener/` ทั้งดุ้นเข้าไปใน `.agents/skills/` ของ project · agent จะอ่าน `SKILL.md` + `references/` และรัน `scripts/fill_engine.py` (resolve path ของ template/scripts แบบ relative กับโฟลเดอร์ skill) |
| **Codex** | ก๊อปโฟลเดอร์ skill เข้าไปใน skills dir ของ Codex (หรือใช้เป็น plugin) · ⚠️ **Codex sandbox ปิด network เป็น default** → ต้องเปิด network access ก่อน ไม่งั้น WebFetch/WebSearch ดึงงบ (10-K/10-Q/Damodaran) ไม่ได้ |

## หมายเหตุการรัน `fill_engine.py` นอก Claude Code

`fill_engine.py` resolve path ของ template (`../assets/reverse_dcf_screener.xlsx`) **แบบ relative กับตำแหน่งไฟล์ตัวเอง** — ดังนั้นเรียกด้วย full path ของสคริปต์ได้เลย ไม่ต้อง `cd` เข้าไปในโฟลเดอร์ก่อน เช่น:

```
python3 /path/to/skills/reverse-dcf-screener/scripts/fill_engine.py
```

ขอแค่รันจากตำแหน่งที่สคริปต์มองเห็น `../assets/reverse_dcf_screener.xlsx` ได้ (โครงสร้าง `scripts/` กับ `assets/` ต้องอยู่ข้างกันในโฟลเดอร์ skill เดิม) ไฟล์ผลลัพธ์จะถูกเขียนลง `analyses/<TICKER>_<วันที่>.xlsx` ใน working directory ปัจจุบัน

---

> เรียบเรียงจาก **Earthh Evans · Invest Hub** · เครื่องมือเชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล
