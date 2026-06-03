# Deep-O Stock Analyst

วิเคราะห์หุ้นรายตัว (**US**) ด้วยกรอบ **DEEP+O** (Demand · Execution · Economics · Price · Optionality) สไตล์ที่หุ้นส่วนกองทุนเฮดจ์ฟันด์ใช้จริง — ออก verdict **ซื้อเพิ่ม / ถือ / ลด / ขาย** แบบตรวจสอบได้ทุกตัวเลข อิงตรรกะ **Damodaran + McKinsey**

> เรียบเรียงจาก **Earthh Evans · Invest Hub** — Institutional-quality content for retail investors

## plugin นี้มีอะไร

| ชนิด | ชื่อ | หน้าที่ |
|---|---|---|
| 🧩 Skill | `deep-o-stock-analyst` | กรอบ DEEP+O + valuation mechanics (auto-trigger เมื่อคุยเรื่องวิเคราะห์หุ้น/มูลค่าหุ้น) |
| 🤖 Agent | `deep-o-stock-analyst` | subagent บทบาท Hedge Fund Equity Research Partner (เรียกผ่าน Agent tool) |
| ⚙️ Engine | `scripts/valuation_engine.py` | คำนวณ WACC / DCF intrinsic value / reverse DCF (terminal-anchored) / DEEP score แบบ **deterministic** (stdlib ล้วน) — โมเดล**ไม่ปั้นเลขเรื่องเงิน** |
| ⚡ Commands | 10 คำสั่ง | `/full` `/livecheck` `/wacc` `/valuation` `/reversedcf` `/options` `/deep` `/risk` `/catalysts` `/onepager` |

> 🔢 **ตัวเลข valuation ทุกตัวมาจาก engine ที่รันจริง ไม่ใช่ LLM ประเมิน** — DEEP score normalize เป็น 0–100 จริง · reverse DCF เป็น terminal-anchored (สูตรเดียวกับ [`reverse-dcf-screener`](../reverse-dcf-screener/)). schema + สูตร: [`skills/deep-o-stock-analyst/references/engine.md`](skills/deep-o-stock-analyst/references/engine.md)

## ติดตั้ง

```
/plugin marketplace add mrunknown2/earthh-evans-finance-skill
/plugin install deep-o-stock-analyst
```

ต้องมี **Python 3** เพื่อรัน engine — **ไม่ต้อง `pip install`** (stdlib ล้วน)

## ใช้งาน

**1. Skill (อัตโนมัติ)** — แค่คุยเรื่องวิเคราะห์หุ้น Claude จะดึง methodology มาใช้เอง
```
ช่วยวิเคราะห์ NVDA หน่อย ราคาตอนนี้แพงไปไหม
```

**2. Command (เรียกมือ)** — เริ่มที่ `/full` แล้วเจาะเฉพาะมุม
```
/full NVDA
```
จากนั้นเจาะ เช่น `/valuation` (intrinsic value) · `/reversedcf` (ราคาฝัง expectation อะไร) · `/deep` (คะแนน + verdict) · `/risk` (Bull/Base/Bear)

**3. Agent** — เรียก subagent `deep-o-stock-analyst` ผ่าน Agent tool สำหรับวิเคราะห์เชิงลึกแบบ isolated

## คำสั่งทั้งหมด

| Command | ทำอะไร |
|---|---|
| `/full` | DEEP+O เต็มรายงาน — livecheck → valuation → score → risk → one-pager (เริ่มต้นแนะนำ) |
| `/livecheck` | Real-Time Protocol — ยืนยันงบ/ราคา/ERP ล่าสุดก่อนวิเคราะห์ |
| `/wacc` | Cost of Capital → เส้นทาง WACC (current → stable) |
| `/valuation` | Damodaran DCF (drivers + clean-ups + stable + triangulation) → intrinsic value |
| `/reversedcf` | ราคาปัจจุบันฝัง expectation อะไร + reality check |
| `/options` | Option-Adjusted Valuation (ตัว O) |
| `/deep` | DEEP scoring 0–100 + verdict 🟢🟡🟠🔴 |
| `/risk` | Risk Map + Bull/Base/Bear + thesis killers |
| `/catalysts` | Catalysts Map 12–24 เดือน + owner metric |
| `/onepager` | One-Pager ภาษาง่าย |

## ขอบเขต

วิเคราะห์ **หุ้นรายตัว (US)** — เป็นคู่เสริมพี่ [`portfolio-risk-architect`](../portfolio-risk-architect/) ที่วิเคราะห์ **พอร์ตรวม** (สองตัวไม่ทับหน้าที่กัน: ตัวนี้เจาะหุ้นเดี่ยว, อีกตัวมองความเสี่ยงทั้งพอร์ต)

## Disclaimer

เครื่องมือนี้เป็นกรอบวิเคราะห์หุ้นเชิงการศึกษา **ไม่ใช่คำแนะนำการลงทุนรายบุคคล** verdict (ซื้อเพิ่ม/ถือ/ลด/ขาย 🟢🟡🟠🔴) เป็น **framework signal** จากกรอบ DEEP+O ไม่ใช่คำสั่งซื้อขาย ตัวเลข valuation อิงสมมติฐานที่ระบุ (WACC, g∞, margin, S/C) และข้อมูล ณ as-of date ผู้ใช้ควร verify เอกสารทางการล่าสุด (10-K/10-Q/IR) และพิจารณาบริบทภาษี/เป้าหมาย/ความเสี่ยงของตนเองก่อนตัดสินใจ
