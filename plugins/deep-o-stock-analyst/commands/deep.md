---
description: "DEEP scoring 0–100 (D25/E20/E20/P20/O15) + verdict ซื้อ/ถือ/ลด/ขาย 🟢🟡🟠🔴"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Bash
model: opus
---

# /deep-o-stock-analyst:deep

**DEEP Scoring & Verdict** — ให้คะแนนแต่ละมิติแล้วถ่วงน้ำหนักเป็นคำตัดสิน

## Input ที่ต้องการ

- **ticker หุ้น** + (ถ้ามี) ผลวิเคราะห์ก่อนหน้า (`/valuation`, `/reversedcf`)

## สิ่งที่ทำ

- ให้คะแนน **0–5/หัวข้อ** พร้อมลิงก์ท้าย bullet:
  - **D — Demand** (ดีมานด์/TAM/backlog/NRR)
  - **E — Execution** (track record/margin delivery)
  - **E — Economics** (ROIC − WACC, EVA, SGR, leverage)
  - **P — Price** (Reverse DCF: ราคาฝัง expectation อะไร)
  - **O — Optionality** (มูลค่าแฝง)
- **normalize → 0–100** ด้วย engine (ห้ามคูณดิบ — score×weight จะเต็ม 500 ทำให้เกณฑ์ ≥80 เอื้อมไม่ถึง):
  ```bash
  echo '{"mode":"deep","scores":{"demand":<0-5>,"execution":<0-5>,"economics":<0-5>,"price":<0-5>,"optionality":<0-5>}}' \
    | python3 "${CLAUDE_PLUGIN_ROOT}/skills/deep-o-stock-analyst/scripts/valuation_engine.py"
  ```
  engine คำนวณ `total = Σ(scoreᵢ/5 × weightᵢ)` (น้ำหนัก D25/E20/E20/P20/O15 รวม 100) → คืน `total`, `contributions`, `verdict_band`, `signal`

| คะแนน | สัญญาณ | คำแนะนำ |
|-------|--------|---------|
| ≥ 80 | 🟢 | ซื้อเพิ่ม |
| 60–79 | 🟡 | ถือ / สะสมระวัง |
| 40–59 | 🟠 | ลดน้ำหนัก |
| < 40 | 🔴 | ขาย |

→ **Verdict + Confidence 0–5** + เหตุผล 3 บรรทัด · **tie-break:** ถ้า P (Price) ต่ำ (หุ้นแพง) แม้ D/E/O สูง → verdict ห้ามเขียว ระบุ "ธุรกิจดีแต่ราคาแพง"

## ตัวอย่างสั่ง

```
/deep NVDA
```

## Discipline

ทุกตัวเลข/ข้อเท็จจริงสำคัญ **ใส่ลิงก์อ้างอิง** · ระบุ **as-of date** (YYYY-MM-DD) · verdict = framework signal ไม่ใช่คำสั่งซื้อขาย · ห้ามกุข้อมูล · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
