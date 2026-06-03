# WACC / Cost of Capital รายอุตสาหกรรม (Damodaran)

> ใช้สำหรับ lookup `WACC` ตาม `sector` ในโมเดล Reverse DCF — sector ต้องสะกดตรงคอลัมน์ "Industry / Sector" เป๊ะ ไม่งั้น lookup ในไฟล์ Excel จะดึงไม่ติด

---

## ⚠️ คำเตือน — ค่าเหล่านี้เป็น PLACEHOLDER

> 🟥 **ตัวเลขทุกค่าในตารางนี้เป็นค่า "ตัวอย่าง" (ILLUSTRATIVE / PLACEHOLDER)** — **ไม่ใช่** ค่าจริงปัจจุบัน
> ต้องโหลดของจริงจาก Damodaran มา **วางทับ** ก่อนใช้วิเคราะห์จริงเสมอ
>
> เวลาใช้งานจริง: agent ควรดึง WACC จริงมาใส่ผ่าน key `wacc` ใน JSON (override) แทนการพึ่งค่าในตารางนี้

---

## ตาราง (28 sectors)

| # | Industry / Sector | Cost of Capital (placeholder) |
|---|---|---|
| 1 | Software (System/Application) | 0.095 |
| 2 | Semiconductor | 0.11 |
| 3 | Computers/Peripherals | 0.09 |
| 4 | Internet/E-commerce Retail | 0.095 |
| 5 | Telecom Services | 0.07 |
| 6 | Aerospace/Defense | 0.085 |
| 7 | Auto & Truck | 0.085 |
| 8 | Banks (Money Center) | 0.09 |
| 9 | Pharma (Drugs) | 0.075 |
| 10 | Biotechnology | 0.095 |
| 11 | Healthcare Products | 0.075 |
| 12 | Retail (General) | 0.075 |
| 13 | Food Processing | 0.06 |
| 14 | Beverage (Soft) | 0.06 |
| 15 | Utilities (General) | 0.055 |
| 16 | Oil/Gas (Integrated) | 0.08 |
| 17 | Chemicals (Specialty) | 0.08 |
| 18 | Electronics (General) | 0.09 |
| 19 | Entertainment | 0.09 |
| 20 | Advertising | 0.09 |
| 21 | REIT | 0.07 |
| 22 | Insurance (General) | 0.08 |
| 23 | Machinery | 0.085 |
| 24 | Air Transport | 0.085 |
| 25 | Total Market (Avg) | 0.083 |

> หมายเหตุ: ตารางต้นฉบับมี 25 แถวข้อมูล (sectors) — รวม `Total Market (Avg)` เป็นค่ากลางตลาดสำหรับ sector ที่ไม่อยู่ในลิสต์ · ค่าทั้งหมดเป็นทศนิยม (0.095 = 9.5%)

---

## วิธีอัปเดต (สำคัญ)

แหล่งจริง: **Aswath Damodaran (NYU Stern)** — ตาราง *"Cost of Capital by Industry Sector (US)"*

🔗 https://pages.stern.nyu.edu/~adamodar

ขั้นตอน:
1. เข้าหน้า Damodaran data → หา **"Cost of Capital by Industry Sector"** (ชุด **US**)
2. **อัปเดต ม.ค. ทุกปี** — Damodaran refresh ข้อมูลต้นปี (ชุดล่าสุดที่อ้างในไฟล์ต้นฉบับ: **ม.ค. 2026**)
3. แมป sector ของหุ้นเข้ากับชื่ออุตสาหกรรมของ Damodaran แล้ว **วางทับค่าในตารางนี้**
4. ถ้าหุ้นข้ามอุตสาหกรรม (multi-segment) → ใช้ค่าถ่วงน้ำหนักตามสัดส่วนรายได้ หรือเลือก segment หลัก

> 💡 ในทางปฏิบัติ: ใส่ค่า WACC จริงผ่าน key `wacc` ใน JSON (override) ได้เลย — แม่นกว่าและเลี่ยงปัญหา sector สะกดไม่ตรง

---

> เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล / educational, not personal investment advice — เรียบเรียงจาก Earthh Evans · Invest Hub
