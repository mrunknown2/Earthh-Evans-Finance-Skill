# Earthh-Evans-Finance-Skill

Claude Code **plugin marketplace** ที่แปลงความรู้การลงทุนของ **Earth Evans** (Invest Hub) ให้เป็น skill / agent / command ใช้งานได้จริง — ออกแบบให้ port ไป provider อื่น (Gemini / ChatGPT) ได้ในอนาคต

## Plugins

| Plugin | คำอธิบาย |
|---|---|
| [`portfolio-risk-architect`](plugins/portfolio-risk-architect) | วินิจฉัย & ออกแบบความเสี่ยงพอร์ต multi-asset (Equity/ETF/Crypto) — look-through, risk contribution, stress test, recommendation. 1 skill + 1 agent + 9 commands |

## ติดตั้ง

```
/plugin marketplace add mrunknown2/Earthh-Evans-Finance-Skill
/plugin install portfolio-risk-architect
```

## เพิ่ม skill ใหม่ (จาก source ถัดไป)

1. วาง source material (เช่น PDF) ลงโฟลเดอร์ `source/` (gitignored — เก็บ local เท่านั้น)
2. สกัด + เรียบเรียงเป็น plugin ใหม่ใต้ `plugins/<ชื่อ>/` (skills / agents / commands)
3. ลงทะเบียน plugin ใหม่ใน `.claude-plugin/marketplace.json`

## โครงสร้าง

```
.claude-plugin/marketplace.json      # ลงทะเบียน plugin ทั้งหมด
plugins/<plugin>/                    # แต่ละ plugin (skills/agents/commands)
source/                              # source material ดิบ (gitignored)
docs/superpowers/                    # spec + implementation plan
```

## Disclaimer

เนื้อหาทุก plugin ใน marketplace นี้เป็น **กรอบวิเคราะห์เชิงการศึกษา ไม่ใช่คำแนะนำการลงทุนรายบุคคล** ตัวเลขตัวอย่างเป็นค่าประมาณเชิงสาธิต ผลจำลองเป็นช่วงความเป็นไปได้ภายใต้สมมติฐาน ไม่ใช่การพยากรณ์ ผู้ใช้ควร verify ข้อมูลล่าสุดและพิจารณาบริบทของตนเองก่อนตัดสินใจ
