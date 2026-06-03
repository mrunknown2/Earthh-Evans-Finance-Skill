---
description: "รัน DEEP+O เต็มรายงานจบในรอบเดียว (livecheck → valuation → DEEP score → risk → one-pager) — entry point หลัก"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Bash
model: opus
---

# /deep-o-stock-analyst:full

วิเคราะห์หุ้นรายตัวครบกรอบ **DEEP+O** จบในรอบเดียว — entry point หลักของสกิล

## Input ที่ต้องการ

- **ticker หุ้น** (เช่น `NVDA`, `AAPL`) — ถ้าผู้ใช้ไม่ระบุ ให้ถามก่อนเริ่ม

## สิ่งที่ทำ

เดินครบทุกขั้นตามลำดับ แล้วตอบตาม **Output Structure §0–§9**:

1. **Live Data Check** — ยืนยันงบล่าสุด/ราคา/Market Cap/ERP ด้วย Search (Search > Memory)
2. **Cost of Capital** → เส้นทาง WACC (current → stable)
3. **Damodaran DCF** (drivers + clean-ups + stable guardrails + triangulation) → **intrinsic value**
4. **Reverse DCF** — ราคาปัจจุบันฝัง expectation อะไร
5. **Option-Adjusted** — `EV_core + ΣEV(options)`
6. **DEEP score 0–100** + verdict 🟢🟡🟠🔴 + Confidence
7. **Risk Map** + Bull/Base/Bear + thesis killers
8. **Catalysts Map** 12–24 เดือน
9. **One-Pager** ภาษาง่าย
10. **ภาคผนวกแหล่งอ้างอิง** — ลิงก์ทั้งหมด

## ตัวอย่างสั่ง

```
/full NVDA
```

> ขั้น 2/3/4/6 (WACC, DCF, reverse DCF, DEEP score) **ตัวเลขต้องมาจาก `valuation_engine.py`** (deterministic) — ห้ามคำนวณในหัว · schema: `skills/deep-o-stock-analyst/references/engine.md`

## Discipline

**ตัวเลข valuation/score มาจาก engine** · ทุกตัวเลข/ข้อเท็จจริงสำคัญ **ใส่ลิงก์อ้างอิง** · ระบุ **as-of date** (YYYY-MM-DD) · ห้ามกุข้อมูล (ไม่พบให้เขียน "ไม่พบข้อมูล") · เชิงการศึกษา ไม่ใช่คำแนะนำรายบุคคล
