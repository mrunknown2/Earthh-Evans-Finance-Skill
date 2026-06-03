---
description: "ตรวจสุขภาพหุ้นครบทุกมิติจบในคำสั่งเดียว: Quick Screen → Companion Variables 6 Multiple → เดิน 15 หมวด → Scorecard → 3 คำถามสุดท้าย — entry point หลักของสกิล"
allowed-tools:
  - Read
  - Bash
  - WebSearch
  - WebFetch
model: opus
---

# /fundamental-checklist:full

วิเคราะห์หุ้นรายตัวครบกรอบ **15-Category Fundamental Due Diligence** จบในรอบเดียว — entry point หลักของสกิล

## Input ที่ต้องการ

- **ticker หุ้น** (เช่น `NVDA`, `AAPL`, `META`) — ถ้าผู้ใช้ไม่ระบุ ให้ถามก่อนเริ่ม

## สิ่งที่ทำ

เดินครบทุกขั้นตามลำดับ:

1. **Quick Screen Gate** — ดึงข้อมูลจริงล่าสุด (10-K / 10-Q / IR) → กรอก 10 เกณฑ์ → รัน engine `screen` mode → ถ้า gate = `avoid` (3+ fail) แจ้งผลและถามว่าต้องการดำเนินการต่อหรือไม่
2. **Companion Variables** — รัน engine `companion` mode ทีละ Multiple สำหรับทั้ง 6 ตัว (peg, pe, ev_sales, ev_ebitda, pb, fcf_yield) → สรุป verdict (cheap/fair/expensive/speculation) + gap ต่อ Multiple
3. **15 หมวด Due Diligence** — เดินหมวด [1–15] ตาม `references/checklist-15.md` → กำหนด verdict (`pass` / `caution` / `red`) ทีละหมวด พร้อมเหตุผล + as-of date + source · ระบุ red_flags ที่พบ · หยุดทันทีถ้า Critical Category (Moat / Financial Strength / Earnings Quality) ได้ `red`
4. **Scorecard** — รัน engine `scorecard` mode ด้วย verdicts ทั้ง 15 หมวด + red_flags + screen_result → อ่าน `overall_read` (STRONG / REVIEW / AVOID)
5. **3 คำถามสุดท้าย** (หมวด 15) — Qualitative gate ก่อนสรุปขั้นสุดท้าย

## Engine Calls

```bash
# Step 1: Quick Screen
echo '{"mode":"screen","criteria":{...}}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"

# Step 2: Companion (รันทีละ Multiple เช่น PEG)
echo '{"mode":"companion","multiple":"peg","pe":35,"eps_growth_5y":35}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"

# Step 4: Scorecard
echo '{"mode":"scorecard","categories":[...],"red_flags":[],"screen_result":{"passed":9,"total":10}}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```

## References ที่ใช้

- `references/companion-variables.md` — สูตร Justified Multiple ทุกตัว
- `references/checklist-15.md` — Benchmark ทุกหมวด + ข้อยกเว้น FCF/Banks
- `references/scorecard.md` — Logic STRONG/REVIEW/AVOID + Critical Categories
- `references/case-studies.md` — ตัวอย่าง NVDA/META/PTON สำหรับ calibration

## ตัวอย่างสั่ง

```
/full NVDA
/full AAPL
```

## Discipline

**ข้อมูลจริงก่อนเสมอ** (Search > Memory) · **Companion Variable ประกอบทุก Multiple** · **Engine คำนวณ ไม่ estimate ในหัว** · ทุกตัวเลขใส่ **as-of date + source** · STRONG/REVIEW/AVOID เป็น framework signal ไม่ใช่คำแนะนำซื้อขาย · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
