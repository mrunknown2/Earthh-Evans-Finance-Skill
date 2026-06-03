---
description: "อธิบายตรรกะ Terminal-Anchored Reverse DCF เชิงการศึกษา (อ่าน references/methodology.md)"
allowed-tools:
  - Read
model: opus
---

# /reverse-dcf-screener:methodology

**Methodology** — อธิบายตรรกะเบื้องหลัง Terminal-Anchored Reverse DCF เชิงการศึกษา ว่าทำไมถึงคำนวณแบบนี้

## Input ที่ต้องการ

- **(ไม่บังคับ)** หัวข้อที่อยากเจาะ — เช่น `plausible`, `verdict`, `zones`, `convention` (ไม่ระบุ = อธิบายภาพรวม)

## สิ่งที่ทำ

- อ่าน `${CLAUDE_PLUGIN_ROOT}/skills/reverse-dcf-screener/references/methodology.md` แล้วอธิบายเชิงการศึกษา ครอบคลุม:
  - **แนวคิด** — "ราคาตอนนี้คาดหวังให้บริษัทโตปีละกี่ % แล้วทำได้จริงไหม" (expectation investing)
  - **ตรรกะ Terminal-Anchored 5 สเต็ป** — reinv → Terminal Value → FCFF → conversion → Implied Terminal Revenue → **Market-Implied CAGR**
  - **Plausible heuristic** — Cap A (Hist/Forward × Fade) · Cap B (TAM × Max-pen) · Cap C (absolute ceiling) → MIN
  - **Verdict + Buffer** — Gap = Implied − Plausible → แพง / Fair / ถูก
  - **โซนราคา 4 ระดับ** — Strong Buy / Fair / Caution / Red Flag จาก Plausible CAGR
  - **Convention** — N = ปี explicit, รายได้ปลายทาง = ปี N+1, วัด CAGR ตลอด N+1 ปี
  - **ข้อควรระวัง** — mature overstate, TAM squishy ที่สุด, WACC placeholder, tips สำหรับ cyclical/pre-profit
- ตอบเป็นภาษาเข้าใจง่าย ยกสูตรประกอบเมื่อช่วยให้เห็นภาพ

## ตัวอย่างสั่ง

```
/reverse-dcf-screener:methodology plausible
```

## Discipline

อธิบายเชิงการศึกษาเท่านั้น ไม่แนะนำซื้อขายตัวใด · ย้ำข้อจำกัด (TAM squishy, WACC placeholder) เสมอ · เรียบเรียงจาก Earthh Evans · Invest Hub · เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล
