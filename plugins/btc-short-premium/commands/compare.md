---
description: "Strategy Comparison — Short Call vs Short Put อันไหนดีกว่า"
allowed-tools:
  - Read
  - Bash
model: opus
---

# /btc-short-premium:compare

**Strategy Comparison** — เทียบ Short Call vs Short Put 3 มุม → แนะนำ leg ที่ edge ดีกว่าพร้อมเหตุผล

## Input ที่ต้องการ

- **Option 1** — Short Call [strike] พร้อม premium bid/ask + IV + delta
- **Option 2** — Short Put [strike] พร้อม premium bid/ask + IV + delta
- **Macro view** — bearish / bullish / neutral (ความเห็นนายท่าน)
- **5 รูป** — CoinGlass, Bybit Option Chain, Daily, 4H, 1H

## สิ่งที่ทำ

เทียบ 3 มุมพร้อมกัน (อ้าง Combination Read + delta จาก `agents/btc-short-premium.md`):

1. **Aligned กับ macro** — leg ไหน direction ตรงกับ macro view มากกว่า; ถ้า macro bearish → Short Call aligned
2. **Risk-Reward** — premium เทียบ distance จาก spot; **SD distance ของแต่ละ leg รันผ่าน** `${CLAUDE_PLUGIN_ROOT}/skills/btc-short-premium/scripts/btc_calc.py` (mode `sd`) ไม่คิดเอง
3. **Probability of profit** — delta เป็น proxy PoP; delta ต่ำกว่า = PoP สูงกว่า; เทียบ sweet spot 0.13–0.15

สรุป **แนะนำ leg ที่ดีกว่า** พร้อมเหตุผล 3 บรรทัด (ห้าม "it depends" — commit ทิศทาง)

อ้างกฎและ threshold จาก `agents/btc-short-premium.md` — ไม่ redefine ตัวเลขเอง

## ตัวอย่างสั่ง

```
/compare
Option 1: Short Call 78000
Option 2: Short Put 70000
macro view: bearish
[แนบรูป 5 ภาพ: CoinGlass, OptionChain, Daily, 4H, 1H]
```

## Discipline

อ้างตัวเลขจริงจากรูปเท่านั้น · เคารพ Critical Rules ตาม framework · SL = Index Price · verdict ต้อง commit leg ที่เลือก · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
