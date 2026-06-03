# btc_calc.py — deterministic numeric gates

ระบบนี้ vision-based: การ**อ่านรูป + ตัดสิน TRADE/SKIP/WAIT เป็นของโมเดล** แต่ **ตัวเลขเชิงปริมาณ
ต้อง deterministic** — SD distance, IV/HV gate, position sizing, pin distance รันผ่าน `btc_calc.py`
(Python 3 stdlib ล้วน · ไม่ต้อง `pip install`) ห้ามคิดเลขในหัว.

```bash
echo '<JSON>' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/btc-short-premium/scripts/btc_calc.py"
```

## Modes

### `sd` — SD distance (Check #3: ต้อง > 1.5 SD)
```jsonc
{"mode":"sd","spot":74000,"strike":76000,"iv":0.30,"days":1}
```
→ `daily_sd` (= Spot·IV·√(days/365)), `distance_usd`, `sd` (กี่ SD), `passes_1_5`

### `iv_hv` — edge gate (Check #2)
```jsonc
{"mode":"iv_hv","iv":0.30,"hv":0.20}
```
→ `ratio`, `zone` (`skip` <1.0 / `borderline` 1.0–1.15 / `ok` 1.15–1.5 / `sweet` >1.5), `tradeable` (≥1.15)

### `size` — position sizing (margin-at-risk)
```jsonc
{"mode":"size","equity":10000,"risk_pct":0.01,"premium_per_contract":50,"max_loss_mult":3}
```
- `risk_pct` = สัดส่วน margin-at-risk ของ equity · **default band 0.5–1%** (เพดาน 2–3% เฉพาะมี track record)
- short option ไม่ cap ที่ premium → size บนสมมติฐาน **max loss = `max_loss_mult` × premium** (≥ 2–3×)
- → `margin_at_risk`, `max_loss_per_contract`, `max_contracts`, `suggested_contracts`, `above_default_band` (เตือนถ้า > 1%)

### `pin` — pin-risk proximity (0.3 SD, scale กับ IV ไม่ใช่ $ ตายตัว)
```jsonc
{"mode":"pin","spot":74050,"strike":74000,"iv":0.30,"days":1,"threshold_sd":0.3}
```
→ `sd`, `close_now` (true ถ้า < threshold) — ใช้ตอน 13:30 TH ก่อน TWAP settle

## ขอบเขต (อย่าทำ)

- ❌ ไม่อ่านรูป/ไม่ดึงข้อมูล real-time — ตัวเลข input มาจากรูปที่นายท่านแคปมาเท่านั้น
- ❌ ไม่ตัดสิน TRADE/SKIP/WAIT — แค่คำนวณ gate ให้โมเดลตัดสิน
- ตัวเลขเชิงคุณภาพ (Combination Read, pattern, regime) ยังเป็นของโมเดล

> ⚠️ short crypto options เสี่ยงสูง ขาดทุนเกิน premium ได้ · เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล · เรียบเรียงจาก **Earthh Evans · Invest Hub**
