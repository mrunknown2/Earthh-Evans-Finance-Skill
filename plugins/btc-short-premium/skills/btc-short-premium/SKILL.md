---
name: btc-short-premium
description: >
  Use when ... BTC daily option, short premium, ขาย call/put เก็บ premium, Bybit
  option, IV/HV ratio, combination read, funding rate, liquidation, pin risk, theta
  decay, strike selection, short call, short put, SD distance, No-Trade gate,
  option checklist, position management, mark price anomaly ... → route ไป command
  ที่เหมาะ. เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล.
---

# BTC Short Premium

ระบบ **BTC Daily Short Premium** คือกรอบขาย Call/Put รายวันบน Bybit เพื่อเก็บ theta premium โดยวิเคราะห์จาก **5 รูป** (CoinGlass · Bybit Option Chain · TradingView D-4H-1H) ผ่าน 6 ขั้นตอน → ผลลัพธ์ **TRADE / SKIP / WAIT** พร้อม strike/size/entry/SL (Index Price) agent ชื่อ `btc-short-premium` ถือ framework เต็ม ครอบคลุม 8-Check · No-Trade Rules · Combination Read · Strike Selection · Critical Rules

> เรียบเรียงจาก **Earthh Evans · Invest Hub** — AI Commands Pack + Master Playbook v2.0

---

## Routing — สถานการณ์ → Command

| สถานการณ์ | Command |
|-----------|---------|
| ยังไม่มี position + ต้องเทรด | `/full` |
| อยากเช็คตลาดเร็ว | `/quick` |
| มี position เปิดอยู่ | `/position` |
| ไม่แน่ใจ Call หรือ Put | `/compare` |
| ได้ signal จาก AI อื่น | `/verify` |
| เห็น Loss แปลกๆ ตอนเพิ่งเปิด | `/anomaly` |
| ใกล้ 13:30 TH | `/pin` |
| จะเลือก strike | `/strike` |
| เช็คก่อนเปิด trade | `/checklist` |

---

## Critical Rules — AI ห้าม override

กฎเหล่านี้ยกมาจาก §9.5 (System Prompt Critical Rules) — ไม่มีข้อยกเว้น:

- **Liquidation > $200M** = SKIP เสมอ ไม่ว่า setup ดูดีแค่ไหน
- **Liquidation $50–200M** = caution · ลด size 30–50%
- **IV/HV < 1.15** = SKIP (no edge)
- **SD distance < 1.5** = SKIP (ใกล้ spot เกิน)
- **FOMC/CPI/NFP day** = SKIP
- **3 consecutive losses** = pause 2–3 days
- **Funding < −0.03%** = SKIP Short Call (squeeze risk)
- **SL ใช้ Index Price เสมอ** (ห้าม Mark Price)
- **Pin exit 13:30 TH** — ปิด position ก่อน TWAP settle 15:00 TH

---

## Disclaimer

Short crypto options เสี่ยงสูง — **ขาดทุนได้มากกว่า premium ที่เก็บ** (short option มี risk สูง/ไม่จำกัดฝั่ง Call) · crypto volatility สูง + liquidation/gamma squeeze เกิดได้รวดเร็ว · **Paper trade ≥ 2 สัปดาห์ก่อนใช้เงินจริง** · เริ่ม size 0.5–1% ของ portfolio · ผู้ใช้ต้อง verify ข้อมูล real-time เองและพิจารณาบริบทของตนเองก่อนตัดสินใจ · เนื้อหาเชิงการศึกษา **ไม่ใช่คำแนะนำลงทุนรายบุคคล** · verdict = framework signal ไม่ใช่คำสั่งซื้อขาย
