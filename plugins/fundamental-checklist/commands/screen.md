---
description: "Quick Screen 10 เกณฑ์ 60 วินาที — gate verdict (strong/review/avoid) + รายการ fail ก่อน Deep Dive; รองรับข้อยกเว้น Banks และ Infrastructure Buildout"
allowed-tools:
  - Read
  - Bash
  - WebSearch
  - WebFetch
model: opus
---

# /fundamental-checklist:screen

**Quick Screen Gate** — ตรวจ 10 เกณฑ์ด่านแรก 60 วินาที ก่อน Deep Dive เต็มรูปแบบ ตรงกับ Checklist หมวด [14]

## Input ที่ต้องการ

- **ticker หุ้น** + (ถ้ามี) บริบทพิเศษ: ธนาคาร/insurer → ระบุ `is_financial` / Infrastructure Buildout → ระบุ `fcf_exempt`

## สิ่งที่ทำ

- ดึงข้อมูลจริงล่าสุด (10-K / 10-Q / IR ล่าสุด) สำหรับทุกเกณฑ์
- กรอก 10 เกณฑ์ลงใน JSON:

| เกณฑ์ | engine key | threshold |
|-------|-----------|-----------|
| ROIC > WACC ต่อเนื่อง 3 ปี | `roic_gt_wacc_3y` | `true/false` |
| FCF Conversion | `fcf_conversion` | ตัวเลข (>0.8 = pass) |
| Net Debt / EBITDA | `net_debt_ebitda` | ตัวเลข (<2.5 = pass) |
| Gross Margin Trend 3 ปี | `gross_margin_stable_3y` | `true/false` |
| Revenue Quality (Recurring%, DSO) | `revenue_quality` | `true/false` |
| EV/Sales ถูก Justify โดย Margin | `ev_sales_justified` | `true/false` |
| PEG บน Sustainable Growth | `peg` | ตัวเลข (<1.5 = pass) |
| Insider ไม่ขาย Open Market ต่อเนื่อง | `insider_no_selling` | `true/false` |
| Macro Alignment | `macro_aligned` | `true/false` |
| Capital Allocation ดี | `capital_allocation_ok` | `true/false` |

- รัน engine `screen` mode → อ่าน `gate_verdict` + `failed_list` + `note`

## Engine Call

```bash
# บริษัททั่วไป
echo '{
  "mode":"screen",
  "criteria":{
    "roic_gt_wacc_3y":true,
    "fcf_conversion":0.92,
    "net_debt_ebitda":1.2,
    "gross_margin_stable_3y":true,
    "revenue_quality":true,
    "ev_sales_justified":true,
    "peg":0.9,
    "insider_no_selling":true,
    "macro_aligned":true,
    "capital_allocation_ok":true
  }
}' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"

# ธนาคาร/Insurer (is_financial=true → ข้าม FCF + Net Debt/EBITDA)
echo '{"mode":"screen","criteria":{"roic_gt_wacc_3y":true,"gross_margin_stable_3y":true,"revenue_quality":true,"ev_sales_justified":false,"peg":1.3,"insider_no_selling":true,"macro_aligned":true,"capital_allocation_ok":true},"is_financial":true}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"

# Infrastructure Buildout (fcf_exempt=true → ข้าม FCF Conversion ชั่วคราว)
echo '{"mode":"screen","criteria":{"roic_gt_wacc_3y":true,"net_debt_ebitda":2.1,"gross_margin_stable_3y":true,"revenue_quality":true,"ev_sales_justified":true,"peg":1.2,"insider_no_selling":true,"macro_aligned":true,"capital_allocation_ok":true},"fcf_exempt":true}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/fundamental-checklist/scripts/checklist_engine.py"
```

Output keys: `passed`, `failed`, `total`, `gate_verdict`, `failed_list`, `note`

## Gate Verdict

| ผล | ความหมาย | ขั้นต่อไป |
|----|---------|---------|
| `strong` (0 fail) | ผ่านทุกเกณฑ์ | Deep Dive ต่อ |
| `review` (1–2 fail) | มีจุดที่ต้องระวัง | Deep Dive ต่อ แต่ focus ที่ failed criteria |
| `avoid` (3+ fail) | Red Flag หลายจุด | แจ้งผล — ถามว่าต้องการ Deep Dive ต่อหรือไม่ |

## References ที่ใช้

- `references/checklist-15.md` หมวด [14] — Benchmark + ข้อยกเว้น FCF/Banks

## ตัวอย่างสั่ง

```
/screen NVDA
/screen JPM
/screen AMZN
```

## Discipline

ข้อมูลจริงก่อนเสมอ · ระบุ as-of date + source ทุกเกณฑ์ · ถ้าใช้ `is_financial` หรือ `fcf_exempt` ให้บอกเหตุผลชัดเจน · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
