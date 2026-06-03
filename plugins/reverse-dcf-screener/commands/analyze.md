---
description: "Step 1 — ดึงงบ → กรอก Engine → Excel + Implied/Plausible/Gap/Verdict เบื้องต้น"
allowed-tools:
  - Read
  - Write
  - Bash
  - WebSearch
  - WebFetch
model: opus
---

# /reverse-dcf-screener:analyze

**Step 1 — Pull → Fill → Compute** — รับ ticker → ดึงงบจริง → กรอก Engine → สร้าง `analyses/<TICKER>_<date>.xlsx` → สรุป verdict เบื้องต้น

## Input ที่ต้องการ

- **ticker หุ้น** (เช่น `IREN`, `NVDA`) — บังคับ
- **(ถ้ามี)** สมมติฐานที่นายท่านอยากกำหนดเอง — terminal margin / horizon N / TAM / WACC override (ไม่งั้นใช้ค่า default + ค่าที่ดึงมาได้)

## สิ่งที่ทำ

1. **ดึงงบ** — อ่าน prompt ดึงข้อมูลจาก `${CLAUDE_PLUGIN_ROOT}/skills/reverse-dcf-screener/references/prompt.md` แล้วทำตาม (WebSearch/WebFetch หาแหล่งตามลำดับ 10-K → 10-Q → earnings release; ระบุ as-of date; ห้ามเดา)
2. **กรอกค่า 10 อย่าง** ที่ prompt กำหนด → ประกอบเป็น JSON ตาม schema (`ticker, revenue_r0, ev, sector, wacc, terminal_margin, terminal_g, terminal_roic, tax, horizon_n, hist_cagr, fade, tam, max_pen, abs_ceiling, buffer, price, shares_m, net_debt, consensus_fy1, analyst_target, analyst_range`)
3. **รัน engine** — pipe JSON เข้า `fill_engine.py`:
   ```
   echo '<JSON>' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/reverse-dcf-screener/scripts/fill_engine.py"
   ```
   จะได้ไฟล์ `analyses/<TICKER>_<date>.xlsx` (กรอก input cells, คงสูตรไว้ recalc ตอนเปิด) + JSON ผล
4. **สรุปเบื้องต้นใน chat** — รายงาน `implied_cagr` (Market-Implied CAGR) · `plausible_cagr` · `gap` · `verdict` · `ev_sales` · path ไฟล์ที่สร้าง
5. **เตือนต่อ** — แนะนำให้รัน `/reverse-dcf-screener:verify` รอบสองก่อนเชื่อผล (discipline บังคับ verify 2 รอบ)

WACC ส่งเป็น override (C9) เสมอเพื่อกัน WACC table placeholder ดึงผิด sector · ห้ามแตะช่องสูตร

## ตัวอย่างสั่ง

```
/reverse-dcf-screener:analyze IREN
```

## Discipline

อ้างงบจริงตามลำดับแหล่ง · ระบุ **as-of date** (YYYY-MM-DD) ทุกตัวเลข · ห้ามกุข้อมูล (ไม่พบ → เขียน "ไม่พบข้อมูล") · sector สะกดให้ตรง WACC table · TAM squishy ที่สุด ใส่อย่างระวัง · ผลรอบแรกยังไม่เชื่อ ต้อง verify · เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล
