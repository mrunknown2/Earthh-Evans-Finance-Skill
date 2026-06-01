---
description: "รัน workflow วินิจฉัยพอร์ตครบ 8 ขั้น + ภาพหลัก (X-Ray, Risk Contribution, Stress) — เหมาะเริ่มต้น"
allowed-tools:
  - Read
  - Write
model: opus
---

# /portfolio-risk-architect:full

รันการวินิจฉัยพอร์ตแบบครบทั้ง 8 ขั้นในรอบเดียว — entry point หลักของสกิล Portfolio Risk Architect

## Input ที่ต้องการ

ถ้าผู้ใช้ยังให้ไม่ครบ ให้ถามก่อน (Clarify First):
1. **holdings + น้ำหนัก** (เช่น VOO 30%, QQQ 30%, BTC 30%, cash 10%)
2. **สกุลเงินฐาน / ประเทศที่อยู่** (tax & FX)
3. **horizon + ความทนต่อ drawdown**
4. **ข้อจำกัด** (เทรดได้อะไร, ภาษี, สภาพคล่อง)

## สิ่งที่ทำ

เดิน **Diagnostic Workflow 8 ขั้น** ตามลำดับ:
1. Portfolio X-Ray (Look-Through) → 2. Overlap → 3. Concentration → 4. Correlation & True Diversification → 5. Risk Contribution → 6. Tail Risk & Stress → 7. Gap Analysis → 8. Recommendation Framework (3 ระดับ)

แล้วตอบตาม **Output Structure**: Snapshot → ภาพลวงตา vs ความจริง → Concentration → Correlation → Risk Contribution → Stress → Gap → Recommendation → Trade-offs → Bottom Line

พร้อมภาพหลัก: X-Ray treemap, Capital vs Risk Contribution bar chart, Stress drawdown

## ตัวอย่างสั่ง

```
พอร์ต: VOO 30%, QQQ 30%, BTC 30%, cash 10%, ฐาน USD, อยู่ไทย, horizon 10 ปี, ทน drawdown ~30%.
/full
```

## Discipline

ค่าตัวเลข vol/correlation/น้ำหนัก ETF ที่ไม่ชัวร์ = **illustrative, ต้อง verify** · ระบุ **as-of date** · แยก fact/inference/judgment · เป็นกรอบเชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล
