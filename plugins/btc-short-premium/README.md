# BTC Daily Short Premium

ระบบเทรด **BTC Daily Short Premium** — ขาย Call/Put รายวันบน **Bybit** เพื่อเก็บ premium จาก theta decay วิเคราะห์ 6 ขั้นจาก **รูป 5 ภาพ** (CoinGlass · Bybit Option Chain · TradingView D/4H/1H) → ออก verdict **TRADE / SKIP / WAIT** พร้อม strike/size/entry/SL ที่ Index Price เรียบเรียงจาก **Earthh Evans · Invest Hub**

> ระบบนี้เป็น **vision-based** — user แคปรูป 5 ภาพส่งให้ AI อ่าน ไม่ใช่ดึงข้อมูล real-time อัตโนมัติ

## เครื่องมือที่ต้องมี

| เครื่องมือ | หน้าที่ |
|-----------|---------|
| **Bybit** | เปิด position Short Call/Put · ดู Option Chain expiry วันนี้ (IV, delta, premium, open interest) |
| **CoinGlass** | ดู derivatives overview (OI, volume, liquidation, funding rate) ของ BTC |
| **TradingView** | chart ราคา BTC timeframe Daily / 4H / 1H (trend, support/resistance, ATR, MA) |
| **ForexFactory** | macro calendar — เช็ค FOMC / CPI / NFP วันนี้และวันใกล้ settle |

## 5 รูปที่ต้องแคป

| # | รูป | ข้อมูลที่ AI อ่าน |
|---|-----|------------------|
| 1 | **CoinGlass Derivatives** — แถว BTC | OI, Volume 24h, Liquidation 24h, Funding Rate |
| 2 | **Bybit Option Chain** — expiry วันนี้ | Strike, IV, delta, bid/ask, premium, OI รายตัว |
| 3 | **TradingView Daily** | trend, support/resistance หลัก, MA50/200, ATR(14) |
| 4 | **TradingView 4H** | swing structure, ATR 4H, volume profile |
| 5 | **TradingView 1H** | momentum เข้า/ออก, ระยะ pin risk ก่อน settle |

> แคปครบก่อนรัน `/full` — AI จะ extract ตัวเลขจากรูปโดยตรง (ไม่ approximate)

## Commands (9 ตัว)

| Command | ใช้เมื่อ |
|---------|---------|
| `/full` | Full Daily Analysis 6 ขั้น → TRADE/SKIP/WAIT + strike/size/entry/SL (เริ่มต้นแนะนำ) |
| `/quick` | เช็คตลาดเร็ว ~2 นาที → regime (quiet/recovery/cascade) → ควร `/full` ต่อ หรือ skip วันนี้ |
| `/position` | มี position เปิดอยู่ → วิเคราะห์ safe/danger zone → hold/close/adjust + TP zone |
| `/compare` | Short Call [X] vs Short Put [Y] — เทียบ alignment/RR/PoP → แนะนำพร้อมเหตุผล |
| `/verify` | ตรวจ signal จาก bot/AI อื่นกับ 8-Check + No-Trade + Combination framework ของระบบนี้ |
| `/anomaly` | Mark Price หรือ Unrealized Loss ดูแปลกๆ → วิเคราะห์ว่าจริงหรือ noise (ดู Ask + Index Price) |
| `/pin` | ใกล้ 13:30 TH — gamma squeeze risk → ปิดทันที / hold ถึง 13:30 / hold ถึง settle 15:00 |
| `/strike` | เลือก strike ตาม regime + คำนวณ SD distance + delta sweet spot + size ตาม Playbook 2.5 |
| `/checklist` | 8-Check ทีละข้อ + No-Trade Rules 7 ข้อ → pass/fail gate ก่อนเปิด position |

## Workflow ตอนเช้า (07:00 TH)

```
07:00  เปิด Bybit · CoinGlass · TradingView · ForexFactory
       ↓
07:05  แคป 5 รูป (CoinGlass → Option Chain → D → 4H → 1H)
       ↓
07:10  รัน /full  (แนบ 5 รูป + macro view + portfolio size)
       ↓
       TRADE?  → เปิด position + ตั้ง SL ที่ Index Price ทันที
       SKIP?   → ปิด session · บันทึกเหตุผล
       WAIT?   → กลับมาเช็ค /quick อีกครั้งใน 1–2 ชม.
       ↓
13:30  /pin  — ตัดสินใจ pin risk (ปิดก่อน หรือถือถึง settle)
       ↓
15:00  Settle — avg BTC Index Price 30 นาทีสุดท้าย (TWAP)
```

**Tips:**
- `/quick` ก่อนแคปรูปครบ — กรองวันที่ไม่ควรเทรดออกเร็ว (ประหยัดเวลา)
- `/checklist` คู่ขนานกับ `/full` เพื่อ double-check gate ก่อนกด confirm
- size เริ่มต้น 0.5–1% ของพอร์ต ระหว่าง paper trade; ขยับขึ้นหลังชนะ ≥ 10 trade ติดกัน

## ติดตั้ง

```
/plugin marketplace add mrunknown2/Earthh-Evans-Finance-Skill
/plugin install btc-short-premium
```

## ⚠️ Disclaimer

เครื่องมือนี้เป็นกรอบวิเคราะห์เชิงการศึกษา **ไม่ใช่คำแนะนำลงทุนรายบุคคล**

- **ขาดทุนได้มากกว่า premium ที่เก็บ** — short option มีความเสี่ยงสูง/ไม่จำกัด (โดยเฉพาะ naked short call)
- crypto มี volatility สูงผิดปกติ + liquidation cascade + gamma squeeze สามารถทำให้ position กลับทิศรวดเร็วมาก
- **paper trade ≥ 2 สัปดาห์ ก่อนใช้เงินจริง** (ตรงจาก Playbook) — ทำความเข้าใจระบบครบก่อน
- เริ่ม size **0.5–1% ของพอร์ต** เท่านั้น อย่าเพิ่ง full size จนมั่นใจในระบบของตัวเอง
- verdict (TRADE/SKIP/WAIT) คือ **framework signal** จากกรอบ 6 ขั้น **ไม่ใช่คำสั่งซื้อขาย**
- ผู้ใช้ต้อง verify ข้อมูล real-time เอง (ราคา, IV, liquidation, funding ณ เวลาจริง) ก่อนตัดสินใจ
- พิจารณาบริบทภาษี/เป้าหมาย/ความเสี่ยงของตนเองก่อนทุกครั้ง — ผู้ใช้รับผิดชอบผลการเทรดเองทั้งสิ้น
