# Playbooks — คู่มือการใช้งานรายปลั๊กอิน

คู่มือใช้งานจริงของแต่ละ plugin ในมาร์เก็ตเพลส (ติดตั้ง → เตรียมข้อมูล → คำสั่ง → อ่านผลลัพธ์ → ข้อควรระวัง)
สำหรับภาพรวมมาร์เก็ตเพลสดูที่ [README หลัก](../README.md)

| Playbook | ขอบเขต | เริ่มที่ |
|---|---|---|
| [portfolio-risk-architect](portfolio-risk-architect.md) | วินิจฉัย & ออกแบบความเสี่ยงพอร์ตรวม multi-asset — risk contribution, correlation, stress, Monte Carlo, frontier | `/full` |
| [deep-o-stock-analyst](deep-o-stock-analyst.md) | วิเคราะห์หุ้นรายตัว (US) ด้วยกรอบ DEEP+O — WACC, DCF, reverse DCF, DEEP score → verdict | `/full <ticker>` |
| [btc-short-premium](btc-short-premium.md) | เดสก์ขาย Call/Put รายวันบน Bybit เก็บ premium — อ่านรูป 5 ภาพ → TRADE/SKIP/WAIT + strike/size/pin | `/full` |
| [reverse-dcf-screener](reverse-dcf-screener.md) | Terminal-Anchored reverse DCF — Implied CAGR เทียบ Plausible CAGR → ถูก/แพง + โซนราคา | `/full <ticker>` |

> ทุก playbook ชี้ไปยัง **engine ที่คำนวณแบบ deterministic** (Python stdlib-only, seeded) — โมเดลแค่ดึงข้อมูล + ตีความ ส่วนเลขเงินวิ่งผ่าน script ที่ตายตัว

## โครงสร้างเอกสาร

- `docs/` (โฟลเดอร์นี้) — **playbook สาธารณะ** สำหรับผู้ใช้ปลั๊กอิน · track เข้า public repo
- `design/` — **เอกสารออกแบบภายใน** (specs + implementation plans) · **gitignored ไม่ push** ขึ้น public repo

## Disclaimer

เนื้อหาทุก playbook เป็น **กรอบวิเคราะห์เชิงการศึกษา ไม่ใช่คำแนะนำการลงทุนรายบุคคล** · ผู้ใช้ควร verify ข้อมูลล่าสุดและพิจารณาบริบทของตนเองก่อนตัดสินใจ
