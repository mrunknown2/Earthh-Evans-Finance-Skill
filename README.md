# Earthh-Evans-Finance-Skill

Claude Code **plugin marketplace** ที่แปลงความรู้การลงทุนของ **Earth Evans** (Invest Hub) ให้เป็น skill / agent / command ใช้งานได้จริง — institutional-quality content สำหรับ retail investor ออกแบบให้ port ไป provider อื่น (Gemini / ChatGPT) ได้ในอนาคต

> เนื้อหาทุก plugin เป็น **กรอบวิเคราะห์เชิงการศึกษา ไม่ใช่คำแนะนำการลงทุนรายบุคคล**

## Plugins

| Plugin | ขอบเขต | ส่วนประกอบ |
|---|---|---|
| [`portfolio-risk-architect`](plugins/portfolio-risk-architect) | วินิจฉัย & ออกแบบความเสี่ยง **พอร์ตรวม** multi-asset (Equity/ETF/Crypto) — look-through, risk contribution, correlation, stress test, Monte Carlo, frontier, rebalance | 1 skill + 1 agent + **9 commands** |
| [`deep-o-stock-analyst`](plugins/deep-o-stock-analyst) | วิเคราะห์ **หุ้นรายตัว (US)** ด้วยกรอบ **DEEP+O** (Demand/Execution/Economics/Price/Optionality) สไตล์ Damodaran + McKinsey — DCF → intrinsic value, reverse DCF, option-adjusted valuation, DEEP score → verdict ซื้อ/ถือ/ลด/ขาย | 1 skill + 1 agent + **10 commands** |

> สองตัวเป็น **คู่เสริมกัน ไม่ทับหน้าที่**: `deep-o-stock-analyst` เจาะหุ้นเดี่ยว · `portfolio-risk-architect` มองความเสี่ยงทั้งพอร์ต

## ติดตั้ง

```
/plugin marketplace add mrunknown2/Earthh-Evans-Finance-Skill
/plugin install portfolio-risk-architect
/plugin install deep-o-stock-analyst
```

## คำสั่งโดยย่อ

**portfolio-risk-architect** — เริ่มที่ `/full`
```
/full · /xray · /overlap · /risk · /corr · /stress · /montecarlo · /frontier · /rebalance
```

**deep-o-stock-analyst** — เริ่มที่ `/full <ticker>`
```
/full · /livecheck · /wacc · /valuation · /reversedcf · /options · /deep · /risk · /catalysts · /onepager
```

รายละเอียดแต่ละคำสั่งดูใน README ของ plugin: [portfolio-risk-architect](plugins/portfolio-risk-architect/README.md) · [deep-o-stock-analyst](plugins/deep-o-stock-analyst/README.md)

## เพิ่ม skill ใหม่ (จาก source ถัดไป)

1. วาง source material (เช่น PDF) ลงโฟลเดอร์ `source/` (gitignored — เก็บ local เท่านั้น)
2. สกัด + เรียบเรียงเป็น plugin ใหม่ใต้ `plugins/<ชื่อ>/` (skills / agents / commands)
3. ลงทะเบียน plugin ใหม่ใน `.claude-plugin/marketplace.json`

## โครงสร้าง

```
.claude-plugin/marketplace.json      # ลงทะเบียน plugin ทั้งหมด
plugins/
  portfolio-risk-architect/          # skill + agent + 9 commands
  deep-o-stock-analyst/              # skill + agent + 10 commands
source/                              # source material ดิบ (gitignored)
docs/superpowers/                    # spec + implementation plan ของแต่ละ plugin
```

## Disclaimer

เนื้อหาทุก plugin ใน marketplace นี้เป็น **กรอบวิเคราะห์เชิงการศึกษา ไม่ใช่คำแนะนำการลงทุนรายบุคคล** ตัวเลขตัวอย่างเป็นค่าประมาณเชิงสาธิต ผลจำลองเป็นช่วงความเป็นไปได้ภายใต้สมมติฐาน ไม่ใช่การพยากรณ์ · verdict เป็น framework signal ไม่ใช่คำสั่งซื้อขาย ผู้ใช้ควร verify ข้อมูลล่าสุด (10-K/10-Q/IR) และพิจารณาบริบทภาษี/สภาพคล่อง/เป้าหมาย/ความเสี่ยงของตนเองก่อนตัดสินใจ
