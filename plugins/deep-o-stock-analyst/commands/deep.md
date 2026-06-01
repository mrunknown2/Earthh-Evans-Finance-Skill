---
description: "DEEP scoring 0–100 (D25/E20/E20/P20/O15) + verdict ซื้อ/ถือ/ลด/ขาย 🟢🟡🟠🔴"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
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
- ถ่วงน้ำหนักเป็น **0–100**:

```
น้ำหนัก: D 25 / E(exec) 20 / E(econ) 20 / P 20 / O 15
```

| คะแนน | สัญญาณ | คำแนะนำ |
|-------|--------|---------|
| ≥ 80 | 🟢 | ซื้อเพิ่ม |
| 60–79 | 🟡 | ถือ / สะสมระวัง |
| 40–59 | 🟠 | ลดน้ำหนัก |
| < 40 | 🔴 | ขาย |

→ **Verdict + Confidence 0–5** + เหตุผล 3 บรรทัด

## ตัวอย่างสั่ง

```
/deep NVDA
```

## Discipline

ทุกตัวเลข/ข้อเท็จจริงสำคัญ **ใส่ลิงก์อ้างอิง** · ระบุ **as-of date** (YYYY-MM-DD) · verdict = framework signal ไม่ใช่คำสั่งซื้อขาย · ห้ามกุข้อมูล · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
