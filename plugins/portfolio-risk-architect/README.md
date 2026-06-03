# Portfolio Risk Architect

วินิจฉัย & ออกแบบความเสี่ยงพอร์ต **multi-asset** (Equity / ETF / Crypto) แบบที่ฝ่าย CIO / Risk Desk ของกองทุนใช้จริง — มอง **ความเสี่ยงที่แบกจริง** ไม่ใช่แค่จำนวนเงินที่ลง

> เรียบเรียงจาก **Earthh Evans · Invest Hub** — Institutional-quality content for retail investors

## plugin นี้มีอะไร

| ชนิด | ชื่อ | หน้าที่ |
|---|---|---|
| 🧩 Skill | `portfolio-risk-architect` | หลักคิด 5 + Diagnostic Workflow 8 ขั้น (auto-trigger เมื่อคุยเรื่องความเสี่ยงพอร์ต) |
| 🤖 Agent | `portfolio-risk-architect` | subagent บทบาท Senior Multi-Asset Strategist (เรียกผ่าน Agent tool) |
| ⚙️ Engine | `scripts/portfolio_engine.py` | คำนวณ risk contribution / DR / ENB / VaR-CVaR / Monte Carlo / frontier แบบ **deterministic** (stdlib ล้วน + seeded) — โมเดล**ไม่เดาเลขเรื่องเงิน** |
| ⚡ Commands | 9 คำสั่ง | `/full` `/xray` `/overlap` `/risk` `/corr` `/stress` `/montecarlo` `/frontier` `/rebalance` |

> 🔢 **ตัวเลขความเสี่ยงทุกตัวมาจาก engine ที่รันจริง ไม่ใช่ LLM ประเมิน** — input เดิม (รวม `seed`) ให้ผลเดิมเป๊ะ (reproducible). schema + สูตร: [`skills/portfolio-risk-architect/references/engine.md`](skills/portfolio-risk-architect/references/engine.md)

## ติดตั้ง

```
/plugin marketplace add mrunknown2/Earthh-Evans-Finance-Skill
/plugin install portfolio-risk-architect
```

ต้องมี **Python 3** เพื่อรัน engine — **ไม่ต้อง `pip install`** (stdlib ล้วน · เลี่ยง numpy เพื่อ portability ข้าม IDE/provider)

## ใช้งาน

**1. Skill (อัตโนมัติ)** — แค่คุยเรื่องพอร์ต Claude จะดึง methodology มาใช้เอง
```
ช่วยดูพอร์ต VOO 40% / QQQ 30% / BTC 30% หน่อย กระจายความเสี่ยงพอไหม
```

**2. Command (เรียกมือ)** — เริ่มที่ `/full` แล้วเจาะเฉพาะมุม
```
พอร์ต: VOO 30%, QQQ 30%, BTC 30%, cash 10%, ฐาน USD, horizon 10 ปี, ทน drawdown ~30%.
/full
```
จากนั้นเจาะ เช่น `/risk` (ดูใครแบกความเสี่ยงจริง) · `/stress` (drawdown วิกฤต) · `/montecarlo` (ช่วงผลลัพธ์)

**3. Agent** — เรียก subagent `portfolio-risk-architect` ผ่าน Agent tool สำหรับวิเคราะห์เชิงลึกแบบ isolated

## คำสั่งทั้งหมด

| Command | ทำอะไร |
|---|---|
| `/full` | วินิจฉัยครบ 8 ขั้น + ภาพหลัก (เริ่มต้นแนะนำ) |
| `/xray` | look-through holdings → หุ้นรายตัวจริง + treemap |
| `/overlap` | heatmap ความซ้ำซ้อนระหว่างกอง |
| `/risk` | Capital Weight vs Risk Contribution bar chart |
| `/corr` | correlation matrix (ปกติ vs วิกฤต) |
| `/stress` | drawdown วิกฤตจริง (2008/2020/2022/2024) |
| `/montecarlo` | 10,000 เส้นทาง → distribution ผลตอบแทน & max DD |
| `/frontier` | efficient frontier + จุดพอร์ต |
| `/rebalance` | before–after risk metrics หลังปรับ |

## Disclaimer

เครื่องมือนี้เป็น **กรอบวิเคราะห์ความเสี่ยงเชิงการศึกษา ไม่ใช่คำแนะนำการลงทุนรายบุคคล** ตัวเลขในตัวอย่างเป็นค่าประมาณเชิงสาธิต (illustrative) ผลจำลองเป็นช่วงความเป็นไปได้ภายใต้สมมติฐาน ไม่ใช่การพยากรณ์ ผู้ใช้ควร verify ข้อมูลล่าสุดและพิจารณาบริบทภาษี/สภาพคล่อง/เป้าหมายของตนเองก่อนตัดสินใจ
