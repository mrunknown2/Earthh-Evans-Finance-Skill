---
description: "Strike Selection — เลือก strike ตาม regime + คำนวณ SD distance + delta"
allowed-tools:
  - Read
  - Bash
model: opus
---

# /btc-short-premium:strike

**Strike Selection** — คำนวณ SD distance จาก spot + IV → เลือก strike ที่ตรง delta sweet spot ตาม regime

## Input ที่ต้องการ

- **Regime** — Quiet / Borderline / Recovery / Macro (หรือระบุ Liquidation level เป็น USD)
- **Spot price (BTC)** — ราคาปัจจุบัน เช่น $74,000
- **IV (Implied Volatility)** — เป็น % เช่น 30%
- **Bybit Option Chain expiry วันนี้** — premium bid/ask, delta ทุก strike

## สิ่งที่ทำ

**คำนวณ SD (Standard Deviation Distance) — รันผ่าน engine ห้ามคิดเลขเอง:**

```bash
echo '{"mode":"sd","spot":74000,"strike":<strike>,"iv":0.30,"days":1}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/btc-short-premium/scripts/btc_calc.py"
```
คืน `daily_sd`, `sd` (กี่ SD ห่าง spot), `passes_1_5` (ต้อง true จึงผ่าน Check #3)

> Spot $74,000 · IV 30% → daily_sd ≈ **$1,162** · strike $76,000 → 1.72 SD ✅

**เลือก strike ตาม regime** (ดู `STRIKE SELECTION` ใน agent):

| Regime | Liquidation Level | Strike Distance | Delta | Size |
|--------|-------------------|----------------|-------|------|
| Quiet | < $50M | 1.5–2 SD | 0.13–0.15 | Full |
| Borderline | $50–150M | 2–2.5 SD | 0.08–0.12 | 70% |
| Recovery (post-cascade) | — | 2.5+ SD | 0.05–0.08 | 50% |
| Macro event nearby | — | 3+ SD or skip | < 0.05 | 30% or skip |

**Output ต่อ 1 regime:**
1. คำนวณ strike range (spot ± N×SD) → แปลงเป็น strike level จริง
2. เปิด option chain → หา strike ที่ delta อยู่ใน sweet spot ของ regime นั้น
3. แนะนำ **delta sweet spot 0.13–0.15** (Quiet) หรือตาม regime
4. ระบุ strike ที่แนะนำ + bid/ask premium + delta จากรูป chain

อ้างกฎและ threshold จาก `agents/btc-short-premium.md` — ไม่ redefine ตัวเลขเอง

## ตัวอย่างสั่ง

```
/strike
regime: quiet | spot: 74000 | IV: 30%
[แนบรูป Bybit Option Chain]
```

## Discipline

แสดงการคำนวณ SD ทีละขั้น · อ้าง delta จาก chain จริง (ไม่ approximate) · ระบุ regime ก่อน แล้วค่อย map threshold · ถ้า Liq > $200M = SKIP เสมอไม่ว่า strike ดูดีแค่ไหน · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
