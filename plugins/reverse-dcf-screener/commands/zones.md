---
description: "Step 3 — โซนราคา 4 ระดับ (Strong Buy/Fair/Caution/Red Flag) + เหตุผล อิง Market-Implied CAGR"
allowed-tools:
  - Read
  - Bash
model: opus
---

# /reverse-dcf-screener:zones

**Step 3 — Price Zones** — อ่านผลแล้วแปลเป็นโซนราคา 4 ระดับ พร้อมเหตุผล อิง Market-Implied CAGR เทียบ Plausible CAGR

## Input ที่ต้องการ

- **(ไม่บังคับ)** ticker — ถ้าไม่ระบุ ใช้ไฟล์ล่าสุดใน `analyses/`
- ต้องผ่าน `/reverse-dcf-screener:analyze` (+ `verify`) มาก่อน

## สิ่งที่ทำ

1. **อ่านผล** — re-run engine ในโหมดอ่านอย่างเดียว (`no_write:true`) จาก input cells ของไฟล์ล่าสุด เพื่อดึง `zones{}` + `plausible_cagr` + `current_price`:
   ```
   echo '<JSON+"no_write":true>' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/reverse-dcf-screener/scripts/fill_engine.py"
   ```
2. **แสดงโซนราคา 4 ระดับ** (อิง Plausible CAGR เป็นจุดอ้าง):
   - 🟢 **Strong Buy** — `zones.strong_buy` (CAGR = MAX(Plausible−5%, 0)) — ราคา ≤ ระดับนี้ = ตลาดคาดหวังต่ำกว่าที่บริษัททำได้
   - 🟢 **Fair Value** — `zones.fair_value` (CAGR = Plausible) — ราคาสะท้อนสิ่งที่ทำได้พอดี
   - ⚠️ **Caution** — `zones.caution_low` → `zones.caution_high` (CAGR = Plausible +5% ถึง +10%) — เริ่มแพง ความคาดหวังล้ำหน้า
   - 🔴 **Red Flag** — `zones.red_flag` (CAGR = Plausible +10%) — ราคา > ระดับนี้ = Priced for Perfection
3. **ปักหมุดราคาปัจจุบัน** — บอกว่า `current_price` ตกอยู่โซนไหน + ระยะห่างจากแต่ละ band
4. **เหตุผล 1-2 บรรทัด** — เทียบ Implied vs Plausible: ตลาดบังคับให้โตปีละกี่ % แล้วบริษัททำได้จริงแค่ไหน

## ตัวอย่างสั่ง

```
/reverse-dcf-screener:zones IREN
```

## Discipline

โซนคือกรอบความคาดหวัง ไม่ใช่เป้าราคา · ทุกตัวเลขมาจาก engine ไม่ปัดเอง · TAM squishy → Plausible อาจคลาด ระวังการตีความ band · เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล
