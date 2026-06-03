#!/usr/bin/env python3
"""Portfolio Risk engine — deterministic, stdlib-only.

Reads a JSON payload from stdin, prints a JSON result to stdout. Every number is
COMPUTED here (not LLM-estimated) so the agent reports facts, not guesses. Monte
Carlo and frontier use a SEEDED RNG, so identical inputs -> identical output.

No numpy/scipy (portable across IDEs/providers). Linear algebra is hand-rolled and
fine for the small asset counts a retail multi-asset portfolio has (<= ~30).

Modes (payload "mode"): "risk" | "corr" | "stress" | "montecarlo" | "frontier" | "all".
This computes; it does NOT decide. Verdicts/framing stay with the agent + disclaimer.
"""
import sys, json, math, random


# ---------- linear algebra (pure stdlib) ----------

def cov_matrix(vols, corr):
    """Sigma_ij = sigma_i * sigma_j * rho_ij."""
    n = len(vols)
    return [[vols[i] * vols[j] * corr[i][j] for j in range(n)] for i in range(n)]


def matvec(M, v):
    return [sum(M[i][k] * v[k] for k in range(len(v))) for i in range(len(M))]


def port_variance(w, cov):
    Sw = matvec(cov, w)
    return sum(w[i] * Sw[i] for i in range(len(w)))


def port_vol(w, cov):
    return math.sqrt(max(port_variance(w, cov), 0.0))


def cholesky(A):
    """Lower-triangular L with L Lᵀ = A. PSD-safe: a zero/negative pivot (e.g. a
    zero-vol cash row) clamps to 0 instead of raising, so sampling still works."""
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                d = A[i][i] - s
                L[i][j] = math.sqrt(d) if d > 0 else 0.0
            else:
                L[i][j] = (A[i][j] - s) / L[j][j] if L[j][j] != 0 else 0.0
    return L


# ---------- weights / concentration ----------

def normalize_weights(w):
    """Accept fractions OR raw dollar amounts — normalize to sum 1."""
    s = float(sum(w))
    if s == 0:
        raise ValueError("weights sum to zero")
    return [x / s for x in w]


def hhi(w):
    """Herfindahl index of weights (1 = single asset, 1/n = equal)."""
    return sum(x * x for x in w)


def effective_holdings(w):
    """1 / Σ wᵢ² — effective number of equally-weighted positions."""
    h = hhi(w)
    return 1.0 / h if h > 0 else 0.0


def enb(rc_pct):
    """Effective Number of Bets = 1 / Σ pᵢ² over RISK-contribution shares pᵢ
    (Herfindahl on risk, not capital). 1 = one bet; n = risk-parity."""
    s = sum(p * p for p in rc_pct)
    return 1.0 / s if s > 0 else 0.0


# ---------- risk contribution (the core) ----------

def risk_contributions(w, cov, names=None):
    """MCRᵢ = (Σw)ᵢ / σ_p ; RCᵢ = wᵢ·MCRᵢ ; %RCᵢ = RCᵢ / σ_p (Σ %RC = 1)."""
    sig = port_vol(w, cov)
    Sw = matvec(cov, w)
    out = []
    for i in range(len(w)):
        mcr = Sw[i] / sig if sig > 0 else 0.0
        rc = w[i] * mcr
        out.append({
            "name": names[i] if names else f"a{i}",
            "weight": w[i],
            "mcr": mcr,
            "rc": rc,
            "rc_pct": (rc / sig) if sig > 0 else 0.0,
        })
    return out


def diversification_ratio(w, vols, cov):
    """DR = Σ(wᵢσᵢ) / σ_p. 1 = no diversification; higher = more."""
    sig = port_vol(w, cov)
    wsum = sum(w[i] * vols[i] for i in range(len(w)))
    return wsum / sig if sig > 0 else 0.0


# ---------- stress ----------

def stress_return(w, shocks):
    """Portfolio return under a per-asset shock vector (rebalanced weights)."""
    return sum(w[i] * shocks[i] for i in range(len(w)))


# ---------- Monte Carlo (seeded -> deterministic) ----------

def _stdnorm(rng):
    """Box–Muller standard normal from a seeded RNG (deterministic)."""
    u1 = rng.random() or 1e-12
    u2 = rng.random()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def _percentile(sorted_vals, q):
    """Linear-interpolated percentile, q in [0,100]."""
    if not sorted_vals:
        return 0.0
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    pos = (q / 100.0) * (len(sorted_vals) - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return sorted_vals[lo]
    frac = pos - lo
    return sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac


def monte_carlo(w, vols, mus, cov, horizon_days=252, n_paths=10000, seed=42,
                steps_per_year=252):
    """Correlated GBM over the horizon, rebalanced each step. Returns distribution
    summary of total return + max drawdown. SEEDED => reproducible to the digit."""
    rng = random.Random(seed)
    n = len(w)
    L = cholesky(cov)
    n_steps = max(1, int(round(horizon_days / 252.0 * steps_per_year)))
    dt = 1.0 / steps_per_year
    sqdt = math.sqrt(dt)
    drift = [(mus[i] - 0.5 * cov[i][i]) * dt for i in range(n)]

    finals, maxdds = [], []
    for _ in range(n_paths):
        value, peak, mdd = 1.0, 1.0, 0.0
        for _s in range(n_steps):
            z = [_stdnorm(rng) for _ in range(n)]
            x = [sum(L[i][k] * z[k] for k in range(n)) for i in range(n)]  # corr, annual scale
            step_ret = 0.0
            for i in range(n):
                logret = drift[i] + x[i] * sqdt
                step_ret += w[i] * (math.exp(logret) - 1.0)
            value *= (1.0 + step_ret)
            if value > peak:
                peak = value
            dd = value / peak - 1.0
            if dd < mdd:
                mdd = dd
        finals.append(value - 1.0)
        maxdds.append(mdd)

    finals.sort()
    maxdds.sort()
    p5 = _percentile(finals, 5)
    p1 = _percentile(finals, 1)
    tail95 = [x for x in finals if x <= p5]
    tail99 = [x for x in finals if x <= p1]
    return {
        "n_paths": n_paths, "horizon_days": horizon_days, "seed": seed,
        "steps_per_year": steps_per_year,
        "p5": p5, "p25": _percentile(finals, 25), "p50": _percentile(finals, 50),
        "p75": _percentile(finals, 75), "p95": _percentile(finals, 95),
        "mean": sum(finals) / len(finals),
        "prob_loss": sum(1 for x in finals if x < 0) / len(finals),
        "var95": p5, "var99": p1,  # return at the tail (negative = loss)
        "cvar95": (sum(tail95) / len(tail95)) if tail95 else p5,
        "cvar99": (sum(tail99) / len(tail99)) if tail99 else p1,
        "expected_max_dd": sum(maxdds) / len(maxdds),
        "worst_max_dd": maxdds[0] if maxdds else 0.0,
    }


# ---------- efficient frontier (seeded random-weight envelope) ----------

def frontier(vols, mus, cov, n_samples=20000, seed=42, current_w=None, rf=0.0,
             long_only=True):
    """Deterministic random-weight (Monte Carlo) frontier. Long-only Dirichlet-ish
    sampling; reports the min-variance and max-Sharpe sampled portfolios plus a
    thinned cloud and the current portfolio's (vol, ret). NOT a QP-exact frontier —
    a reproducible, assumption-transparent approximation (good enough to show where
    the current portfolio sits relative to the achievable set)."""
    rng = random.Random(seed)
    n = len(vols)

    def point(w):
        sig = port_vol(w, cov)
        ret = sum(w[i] * mus[i] for i in range(n))
        return {"w": [round(x, 4) for x in w], "vol": sig, "ret": ret,
                "sharpe": ((ret - rf) / sig) if sig > 0 else 0.0}

    min_vol = max_sharpe = None
    cloud = []
    for k in range(n_samples):
        raw = [rng.random() for _ in range(n)]
        if not long_only:
            raw = [r - 0.5 for r in raw]
        s = sum(raw)
        if s == 0:
            continue
        w = [r / s for r in raw]
        pt = point(w)
        if min_vol is None or pt["vol"] < min_vol["vol"]:
            min_vol = pt
        if max_sharpe is None or pt["sharpe"] > max_sharpe["sharpe"]:
            max_sharpe = pt
        if k % max(1, n_samples // 60) == 0:  # thinned cloud for plotting
            cloud.append({"vol": pt["vol"], "ret": pt["ret"]})

    return {
        "n_samples": n_samples, "seed": seed,
        "min_vol": min_vol, "max_sharpe": max_sharpe,
        "current": point(current_w) if current_w else None,
        "cloud": cloud,
    }


# ---------- top-level dispatch ----------

def _unpack(d):
    assets = d["assets"]
    names = [a["name"] for a in assets]
    w = normalize_weights([a["weight"] for a in assets])
    vols = [a.get("vol", 0.0) for a in assets]
    mus = [a.get("mu", 0.0) for a in assets]
    n = len(assets)
    corr = d.get("correlation")
    if corr is None:  # default to identity if not supplied (agent must flag this)
        corr = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    cov = cov_matrix(vols, corr)
    return names, w, vols, mus, cov, corr


def analyze(d):
    names, w, vols, mus, cov, corr = _unpack(d)
    mode = d.get("mode", "all")
    seed = d.get("seed", 42)
    out = {"assets_in": names, "weights_normalized": [round(x, 6) for x in w]}

    if mode in ("risk", "corr", "all"):
        rc = risk_contributions(w, cov, names)
        sig = port_vol(w, cov)
        out["risk"] = {
            "portfolio_vol": sig,
            "diversification_ratio": diversification_ratio(w, vols, cov),
            "effective_holdings": effective_holdings(w),
            "enb": enb([x["rc_pct"] for x in rc]),
            "hhi": hhi(w),
            "assets": rc,
        }
    if mode in ("corr", "all"):
        out["correlation"] = corr  # echo back the matrix actually used
    if mode in ("stress", "all"):
        scen = d.get("scenarios", [])
        res = []
        for sc in scen:
            sh = sc.get("shocks", {})
            # an asset with no shock (missing OR null, e.g. BTC didn't exist in 2008)
            # is treated as flat (0); the agent must mark those N/A in the narration.
            na = [nm for nm in names if sh.get(nm) is None]
            shocks = [(0.0 if sh.get(nm) is None else sh[nm]) for nm in names]
            res.append({"name": sc.get("name"),
                        "portfolio_return": stress_return(w, shocks),
                        "na_assets": na})
        out["stress"] = res
    if mode in ("montecarlo", "all"):
        out["montecarlo"] = monte_carlo(
            w, vols, mus, cov,
            horizon_days=d.get("horizon_days", 252),
            n_paths=d.get("n_paths", 10000),
            seed=seed,
            steps_per_year=d.get("steps_per_year", 252),
        )
    if mode in ("frontier", "all"):
        out["frontier"] = frontier(
            vols, mus, cov,
            n_samples=d.get("n_samples", 20000),
            seed=seed, current_w=w, rf=d.get("rf", 0.0),
        )
    return out


def main():
    d = json.load(sys.stdin)
    print(json.dumps(analyze(d), ensure_ascii=False))


if __name__ == "__main__":
    main()
