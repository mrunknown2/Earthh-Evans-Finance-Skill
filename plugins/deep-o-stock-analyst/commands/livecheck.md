---
description: "Real-Time Protocol — ยืนยันงบ/ราคา/ERP ล่าสุดด้วย Search ก่อนวิเคราะห์ (Search > Memory)"
allowed-tools:
  - WebSearch
  - WebFetch
model: opus
---

# /deep-o-stock-analyst:livecheck

ขั้นบังคับก่อนสวมบทวิเคราะห์ — **ห้ามใช้ Training Data จนผ่าน Live Data Check**

## Input ที่ต้องการ

- **ticker หุ้น** (เช่น `NVDA`)

## สิ่งที่ทำ

**STEP A — ยืนยันข้อมูลล่าสุด (Search เท่านั้น):**
1. `Investor Relations [ticker] latest financial results press release` → ไตรมาสล่าสุด (Qx YYYY) + วันประกาศงบ + ลิงก์
2. `SEC Filings [ticker] 10-Q/10-K latest` → วันยื่นเอกสารล่าสุด
3. `[ticker] stock price today` + `Market Cap today`
4. `Damodaran Implied Equity Risk Premium [current month/year]`

**STEP B — Data Override:**
- Search ขัดกับความจำ → ยึด **Search** เป็น Absolute Truth
- งบล่าสุด < 3 วัน → ระบุ **"Breaking News / Earnings Reaction Mode"**

## Output

as-of date · ไตรมาสล่าสุด · ราคา/Market Cap · ERP · **ลิงก์อ้างอิงทุกจุด** → พร้อมส่งต่อให้ขั้นวิเคราะห์

## Discipline

ทุกตัวเลข/ข้อเท็จจริงสำคัญ **ใส่ลิงก์อ้างอิง** · ระบุ **as-of date** (YYYY-MM-DD) · ห้ามกุข้อมูล (ไม่พบให้เขียน "ไม่พบข้อมูล") · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
