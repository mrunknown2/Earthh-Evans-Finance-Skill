# portfolio_engine.py — deterministic compute reference

ตัวเลขความเสี่ยงทุกตัว (risk contribution, DR, ENB, VaR/CVaR, max drawdown, frontier)
**ต้องมาจาก engine นี้ ห้ามให้โมเดลเดาเอง** — เรื่องเงินต้อง deterministic. engine เป็น
**Python 3 stdlib ล้วน** (ไม่ต้อง `pip install` อะไร · portable ข้าม IDE/provider) และใช้
**seeded RNG** → input เดิม = output เดิมเป๊ะทุกครั้ง (reproducible).

โมเดลมีหน้าที่: (1) ดึง/รับ holdings + σ/ρ/μ จริง → ประกอบ JSON, (2) รัน engine, (3) **เล่าผล**
ที่ engine คืนมา + แยก fact/assumption + as-of date + disclaimer. โมเดล**ไม่คำนวณเอง**.

## วิธีเรียก

```bash
echo '<JSON>' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/portfolio-risk-architect/scripts/portfolio_engine.py"
```

## Input JSON

```jsonc
{
  "mode": "all",                 // risk | corr | stress | montecarlo | frontier | all
  "assets": [
    {"name": "VOO", "weight": 0.30, "vol": 0.16, "mu": 0.08},
    {"name": "QQQ", "weight": 0.30, "vol": 0.22, "mu": 0.10},
    {"name": "BTC", "weight": 0.30, "vol": 0.60, "mu": 0.20},
    {"name": "Cash","weight": 0.10, "vol": 0.00, "mu": 0.04}
  ],
  "correlation": [[1,0.9,0.4,0],[0.9,1,0.45,0],[0.4,0.45,1,0],[0,0,0,1]],  // NxN, ลำดับเดียวกับ assets
  "scenarios": [                  // เฉพาะ mode stress/all
    {"name": "GFC 2008", "shocks": {"VOO": -0.51, "QQQ": -0.53, "BTC": -0.60}}
  ],
  "horizon_days": 252,            // MC horizon
  "n_paths": 10000,               // MC paths
  "n_samples": 20000,             // frontier random-weight samples
  "seed": 42,                     // ⭐ fix ไว้ → reproducible
  "rf": 0.04,                     // risk-free สำหรับ Sharpe
  "steps_per_year": 252           // ความถี่ MC step
}
```

- `weight` รับ**เศษส่วนหรือจำนวนเงินดิบ**ก็ได้ — engine normalize ให้รวม = 1 เอง (`weights_normalized` ในผล)
- `vol`, `mu` = annualized · `correlation` ไม่ส่ง → ใช้ identity (engine ทำงานได้แต่ต้องเตือนผู้ใช้ว่าถือว่า uncorrelated)
- ถ้าค่า σ/ρ ไม่ชัวร์ → ใส่ค่า approximate แล้ว**เล่าผลโดยระบุว่า "approximate, verify" + as-of date**

## Output JSON (per mode)

| Key | ความหมาย |
|---|---|
| `risk.portfolio_vol` | σ_p = √(wᵀΣw) |
| `risk.assets[].rc_pct` | **% Risk Contribution** — `RCᵢ/σ_p`, รวม = 1 (เทียบกับ `weight` = %capital) |
| `risk.assets[].mcr` | Marginal Contribution to Risk = `(Σw)ᵢ/σ_p` |
| `risk.diversification_ratio` | `Σ(wᵢσᵢ)/σ_p` (1 = ไม่กระจาย, สูง = กระจายจริง) |
| `risk.effective_holdings` | `1/Σwᵢ²` |
| `risk.enb` | **Effective Number of Bets** = `1/Σ(rc_pctᵢ²)` (Herfindahl บน **risk** share ไม่ใช่ capital) |
| `risk.hhi` | `Σwᵢ²` |
| `stress[].portfolio_return` | `Σ(wᵢ·shockᵢ)` ต่อ scenario |
| `montecarlo.{p5,p50,p95}` | percentile ผลตอบแทนรวมตลอด horizon |
| `montecarlo.{var95,var99}` | return ที่ tail (ค่าติดลบ = ขาดทุน) |
| `montecarlo.{cvar95,cvar99}` | ค่าเฉลี่ยของ tail เกิน VaR |
| `montecarlo.{prob_loss,expected_max_dd,worst_max_dd}` | ความน่าจะขาดทุน · E[max DD] · max DD แย่สุด |
| `frontier.{min_vol,max_sharpe,current,cloud}` | จุด min-variance / max-Sharpe / พอร์ตปัจจุบัน / cloud สำหรับ plot |

## สูตร (port → Python, ตรวจสอบด้วย known-answer tests)

```
Σ            = D ρ D           # D = diag(σ)
σ_p          = sqrt(wᵀ Σ w)
MCRᵢ         = (Σw)ᵢ / σ_p
RCᵢ          = wᵢ · MCRᵢ        # Σ RCᵢ = σ_p
%RCᵢ         = RCᵢ / σ_p        # Σ %RCᵢ = 1   ← หัวใจ: เทียบกับ %capital
DR           = Σ(wᵢσᵢ) / σ_p
ENB          = 1 / Σ(%RCᵢ²)
Stress       = Σ(wᵢ · shockᵢ)
Monte Carlo  = correlated GBM (Cholesky(Σ) + Box–Muller), rebalanced, seeded
Frontier     = random long-only weights (seeded) → min-vol / max-Sharpe envelope
```

## ข้อจำกัดที่ต้องเล่าให้ผู้ใช้รู้ (อย่าปิด)

- **Monte Carlo เป็น GBM** (lognormal) → **ไม่จับ fat tail / regime shift / vol clustering** — p5/CVaR จึง*มองโลกในแง่ดีเกินจริงในวิกฤต* · เสริมด้วย `/stress` (historical) เสมอ
- **Frontier เป็น random-weight approximation** (ไม่ใช่ QP-exact) แต่ reproducible · ไวต่อ μ/σ/ρ มาก
- ในวิกฤต ρ → 1 → ลอง rerun ด้วย correlation regime วิกฤต (เช่น ดัน ρ ขึ้น) เทียบกับ regime ปกติ
- ทุกผล = **ช่วงความเป็นไปได้ภายใต้สมมติฐาน ไม่ใช่พยากรณ์** · `seed` คงที่เพื่อ reproducibility ไม่ใช่เพื่อความแม่น

> เชิงการศึกษา ไม่ใช่คำแนะนำลงทุนรายบุคคล · เรียบเรียงจาก **Earthh Evans · Invest Hub**
