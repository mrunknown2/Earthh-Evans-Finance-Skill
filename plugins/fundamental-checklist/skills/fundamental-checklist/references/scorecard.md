# Scorecard — วิธีอ่านและใช้ผล 15 หมวด

> Scorecard ไม่ใช่ Score 0–100 — เป็น **Framework Signal** ที่ aggregate ผล pass/caution/red
> ของ 15 หมวด + red flags + quick screen เข้าด้วยกัน → **STRONG / REVIEW / AVOID**
>
> Logic ทุกบรรทัดในเอกสารนี้ match `checklist_engine.py` → `scorecard()` **แบบ verbatim**

---

## วิธีอ่านผลแต่ละหมวด

### Verdict 3 ระดับต่อหมวด

| Verdict | ความหมาย | ผลต่อ Scorecard |
|---------|---------|----------------|
| `pass` | ผ่านเกณฑ์ Benchmark ของ Sector นั้น | นับเข้า `pass_count` |
| `caution` | อยู่ในเขตที่ต้องติดตาม ยังไม่ถึงขั้น Red Flag | นับเข้า `caution_count` |
| `red` | ผิดเกณฑ์ขั้นร้ายแรง หรือเป็น Active Red Flag | นับเข้า `red_count` |

### Output Keys ของ `scorecard()` (engine)

```python
{
  "pass_count":    int,   # จำนวนหมวดที่ verdict == "pass"
  "caution_count": int,   # จำนวนหมวดที่ verdict == "caution"
  "red_count":     int,   # จำนวนหมวดที่ verdict == "red"
  "red_flag_total": int,  # จำนวน red flags รวม (จาก list แยก)
  "screen_passed": int,   # หมวด 14 Quick Screen ผ่านกี่ข้อ
  "screen_total":  int,   # Quick Screen ทั้งหมดกี่ข้อ (10 ปกติ, 9 fcf_exempt, 8 is_financial)
  "critical_red":  bool,  # True ถ้า Moat / Financial Strength / Earnings Quality ใดข้อ = red
  "overall_read":  str    # "STRONG" | "REVIEW" | "AVOID"
}
```

---

## Critical Categories — Red = AVOID ทันที

```python
CRITICAL_CATEGORIES = {"Moat", "Financial Strength", "Earnings Quality"}
```

3 หมวดนี้คือรากฐานของการลงทุนระยะยาว — ถ้าหมวดใดหมวดหนึ่งเป็น `red`:

- `critical_red = True`
- `overall_read = "AVOID"` ไม่ว่าหมวดอื่นจะ pass ดีแค่ไหน
- ไม่มีการ override — ไม่มีตัวเลขอื่นที่ชดเชยได้

**ทำไมถึงเป็นอย่างนี้?**
- **Moat ไม่มี** → ข้อได้เปรียบในการแข่งขันหาย → ROIC จะลดลงหา WACC ในระยะยาว → Premium Valuation พัง
- **Financial Strength ต่ำมาก** → ความเสี่ยง Distress ช่วง Stress → บริษัทดีอาจเจ็บตายก่อนที่ Thesis จะพิสูจน์ตัวเอง
- **Earnings Quality แย่** → ตัวเลขที่เห็นไม่ใช่ความจริง → ทุกการวิเคราะห์ที่ทำมาบน Earnings ที่บิดเบือนไม่มีประโยชน์

---

## Overall Read Logic — Match Engine แบบ Verbatim

```python
# จาก checklist_engine.py → scorecard()

if critical_red or red_count >= 3:
    read = "AVOID"
elif (red_count == 0
      and screen_passed >= 0.8 * screen_total
      and len(red_flags) == 0
      and caution_count <= 1):
    read = "STRONG"
else:
    read = "REVIEW"
```

### ตารางสรุป Overall Read

| เงื่อนไข | Overall Read |
|---------|-------------|
| `critical_red == True` (Moat / Financial Strength / Earnings Quality เป็น red) | **AVOID** |
| `red_count >= 3` (ไม่ว่าหมวดไหน) | **AVOID** |
| `red_count == 0` AND `screen_passed >= 80%` AND `red_flag_total == 0` AND `caution_count <= 1` | **STRONG** |
| ทุกกรณีที่เหลือ | **REVIEW** |

### ความหมายของแต่ละ Overall Read

| Overall Read | ความหมาย | Action |
|-------------|---------|--------|
| **STRONG** | Fundamental แข็งแกร่งครบ, ไม่มี Red Flag, Quick Screen ผ่าน >80% | ดำเนินการ Deep Dive ต่อ, ตรวจ Valuation |
| **REVIEW** | มีจุดที่ต้องติดตาม แต่ไม่ถึงขั้น Deal-Breaker | Deep Dive เพิ่ม, Scenario Analysis, ปรับ Position Size |
| **AVOID** | มี Critical Failure หรือ Red Count สูง | ไม่ลงทุน หรือ Exit ถ้ามีอยู่แล้ว |

> **STRONG/REVIEW/AVOID เป็น Framework Signal ไม่ใช่ Score** — นักลงทุนยังต้องตัดสินใจขั้นสุดท้ายเอง

---

## Quick Screen (หมวด 14) กับ Scorecard

Quick Screen 10 เกณฑ์ (mode `screen`) เป็น Input ตัวหนึ่งของ Scorecard:

```
screen_result = {"passed": <n>, "total": <10 หรือ 9 หรือ 8>}
```

- **ปกติ:** total = 10
- **`fcf_exempt=True`** (Infrastructure Buildout): total = 9 (ข้ามเกณฑ์ FCF Conversion)
- **`is_financial=True`** (Banks/Insurers): total = 8 (ข้ามเกณฑ์ FCF + Net Debt/EBITDA)

เกณฑ์ STRONG ต้องการ `screen_passed >= 80% × screen_total`:
- ปกติ: ต้องผ่านอย่างน้อย 8/10
- fcf_exempt: ต้องผ่านอย่างน้อย 8/9
- is_financial: ต้องผ่านอย่างน้อย 7/8

---

## Red Flags — รายการแยก (ไม่ใช่ Verdict ของหมวด)

นอกจาก verdict ของ 15 หมวด ยังมี `red_flags` เป็น list แยก สำหรับ active warning signals:

ตัวอย่าง:
- Insider selling ต่อเนื่อง 3+ ครั้ง Open Market
- Goodwill > 40% of Total Assets
- DSO เพิ่มขึ้นพร้อม Revenue spike ปลาย Quarter
- FCF ติดลบ 2 ปีติด ขณะ Net Income เป็นบวก
- Operating Margin หดทุก Quarter ติดต่อ 4 ไตรมาส

`red_flag_total > 0` จะทำให้ไม่สามารถได้ `STRONG` ได้ (แม้ red_count == 0 และ screen ผ่านหมด)

---

## 3 คำถามสุดท้ายก่อนกดซื้อ — Qualitative Gate สุดท้าย

**หมวด 15 ของ Checklist** — ทำหลังจาก Scorecard ได้ `STRONG` หรือ `REVIEW` แล้ว เป็นขั้นตอนสุดท้ายก่อนตัดสินใจลงทุน

| คำถาม | ถ้าใช่ | ถ้าไม่ |
|-------|--------|--------|
| "ธุรกิจนี้จะใหญ่กว่าและทำกำไรได้มากกว่าใน 5–10 ปี?" | วิเคราะห์ต่อ | หยุด — ไม่มี Thesis |
| "ถ้าหุ้นตก 30% เราจะซื้อเพิ่มไหม?" | ความเชื่อมั่นผ่าน | Position ใหญ่เกินไป ลด Size |
| "บอกได้ชัดเจนไหมว่าทำไมตลาดถึง Misprice ตรงนี้?" | มี Edge แล้ว | รอก่อน — ยังไม่มี Variant View ที่ชัด |

Scorecard บอกว่า Fundamental ดีหรือไม่ — แต่ 3 คำถามนี้บอกว่า **ราคาตอนนี้สมเหตุสมผลหรือไม่** และ **คุณมี Conviction พอที่จะลงทุนหรือเปล่า**

---

## 10 หลักการปิดท้าย (Philosophy)

1. **ทุก Multiple คือ DCF ที่ถูกย่อรูปมา** — ให้ Decompress ด้วย Companion Variable ก่อนตัดสินใจ
2. **ROIC > WACC ต่อเนื่อง 5 ปีขึ้นไป = พิสูจน์ Moat แล้ว** — ทุกอย่างอื่นยังเป็นแค่ Hypothesis
3. **FCF คือความจริง** — Net Income ถูกจัดการได้ Cash ไม่ได้
4. **Trajectory ของ Margin สำคัญกว่าระดับปัจจุบัน** — Direction > Level
5. **Operating Leverage คือพลังที่ทรงพลังที่สุด** — หาธุรกิจที่ Revenue Growth โต Structural กว่า Cost
6. **Reverse DCF บังคับความซื่อสัตย์ทางปัญญา** — ถามก่อนว่า "ราคานี้ Assume อะไร?" ก่อนถามว่า "มูลค่าเท่าไร?"
7. **Insider ขายที่ Stock Highs + Fundamental แย่ลงพร้อมกัน = Exit Signal** — อย่างใดอย่างหนึ่งยังไม่พอ
8. **Capital Allocation คือจุดที่ Alpha ถูกสร้างและทำลาย** — ธุรกิจดีที่บริหารเงินทุนแย่ Underperform เสมอ
9. **ก่อนบอกว่า Misprice ต้องหา Variant View ที่ชัดเจนก่อน** — ตลาดไม่ได้ผิดเสมอไป
10. **Narrative โดยไม่มี Number ไม่ใช่การวิเคราะห์** — Number โดยไม่มี Narrative พลาด Context — นักลงทุนที่ดีถือทั้งสองไว้พร้อมกัน

---

## เรียก Engine — `scorecard` Mode

เรียก `checklist_engine.py` ผ่าน stdin JSON:

```json
{
  "mode": "scorecard",
  "categories": [
    {"name": "Business Overview",    "verdict": "pass"},
    {"name": "Moat",                 "verdict": "pass"},
    {"name": "Financial Strength",   "verdict": "pass"},
    {"name": "Profitability",        "verdict": "pass"},
    {"name": "Growth Quality",       "verdict": "pass"},
    {"name": "Capital Allocation",   "verdict": "pass"},
    {"name": "Valuation",            "verdict": "caution"},
    {"name": "Earnings Quality",     "verdict": "pass"},
    {"name": "Management Quality",   "verdict": "pass"},
    {"name": "Ownership Structure",  "verdict": "pass"},
    {"name": "Risk Assessment",      "verdict": "pass"},
    {"name": "Macro Alignment",      "verdict": "pass"},
    {"name": "Technical Context",    "verdict": "pass"},
    {"name": "Quick Screen",         "verdict": "pass"},
    {"name": "3 Final Questions",    "verdict": "pass"}
  ],
  "red_flags": [],
  "screen_result": {"passed": 9, "total": 10}
}
```

**ตัวอย่าง Output สำหรับ NVIDIA-like case (STRONG — caution ≤ 1, red_flags = 0, screen ≥ 80%):**

```json
{
  "pass_count": 14,
  "caution_count": 1,
  "red_count": 0,
  "red_flag_total": 0,
  "screen_passed": 9,
  "screen_total": 10,
  "critical_red": false,
  "overall_read": "STRONG",
  "note": "STRONG/REVIEW/AVOID เป็น framework signal ไม่ใช่ score. ปิดท้ายด้วย 3 คำถามสุดท้ายก่อนกดซื้อ (qualitative)."
}
```

**ตัวอย่าง Output สำหรับ Peloton-like case (AVOID):**

```json
{
  "pass_count": 6,
  "caution_count": 4,
  "red_count": 5,
  "red_flag_total": 7,
  "screen_passed": 3,
  "screen_total": 10,
  "critical_red": true,
  "overall_read": "AVOID",
  "note": "STRONG/REVIEW/AVOID เป็น framework signal ไม่ใช่ score. ปิดท้ายด้วย 3 คำถามสุดท้ายก่อนกดซื้อ (qualitative)."
}
```

### ข้อสังเกตสำคัญ

- `categories` ต้องมี name ตรงกับ `CRITICAL_CATEGORIES` ใน engine: `"Moat"`, `"Financial Strength"`, `"Earnings Quality"` (case-sensitive)
- `verdict` ใช้ lowercase: `"pass"` | `"caution"` | `"red"`
- `screen_result` มาจาก output ของ mode `screen` (วิ่ง mode screen ก่อน แล้วส่งผลเข้ามา)

---

> **เชิงการศึกษา — ไม่ใช่คำแนะนำลงทุนรายบุคคล / Educational, not personal investment advice**
> เรียบเรียงจาก **Earthh Evans · Invest Hub** — Ultimate Fundamental Stock Checklist 2025
> Logic ทุกบรรทัดในไฟล์นี้ตรงกับ `checklist_engine.py` → `scorecard()` แบบ verbatim
