"""Shared helpers (standard library only): normal cdf/pdf, margin parser, ridge probit fit, calibration metrics."""
import math, re
def Phi(x): return 0.5 * math.erfc(-x / math.sqrt(2))
def phi(x): return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)
def parse_margin(s):
    """'D+12.5' -> +12.5, 'R+3.0' -> -3.0 (positive = Democratic); None if not parseable."""
    m = re.match(r'\s*([RD])\+([\d.]+)', s or '')
    return None if not m else (float(m.group(2)) if m.group(1) == 'D' else -float(m.group(2)))
def solve(M, v):
    n = len(v); M = [row[:] + [v[i]] for i, row in enumerate(M)]
    for i in range(n):
        p = max(range(i, n), key=lambda k: abs(M[k][i])); M[i], M[p] = M[p], M[i]
        for k in range(i + 1, n):
            f = M[k][i] / M[i][i]
            for j in range(i, n + 1): M[k][j] -= f * M[i][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1): x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x
def fit_probit(X, y, lam=1.0, iters=60):
    """Probit by IRLS with a ridge penalty (lambda) on all coefficients except the intercept (first column)."""
    k = len(X[0]); b = [0.0] * k
    for _ in range(iters):
        H = [[0.0] * k for _ in range(k)]; g = [0.0] * k
        for xi, yi in zip(X, y):
            e = sum(bj * xj for bj, xj in zip(b, xi)); mu = min(max(Phi(e), 1e-6), 1 - 1e-6); f = max(phi(e), 1e-8); w = f * f / (mu * (1 - mu)); z = e + (yi - mu) / f
            for a in range(k):
                g[a] += w * xi[a] * z
                for c in range(k): H[a][c] += w * xi[a] * xi[c]
        for a in range(1, k): H[a][a] += lam
        nb = solve(H, g)
        if max(abs(u - v) for u, v in zip(nb, b)) < 1e-7: b = nb; break
        b = nb
    return b
def metrics(ps, ys):
    """alpha = mean (1-p)^2 over y=1; beta = mean p^2 over y=0; plus expected values under calibration (*_cal)."""
    pos = [(1 - p) ** 2 for p, y in zip(ps, ys) if y]; neg = [p ** 2 for p, y in zip(ps, ys) if not y]; a = sum(pos) / len(pos); b = sum(neg) / len(neg); n = len(ps)
    ac = sum(p * (1 - p) ** 2 for p in ps) / sum(ps); bc = sum((1 - p) * p * p for p in ps) / sum(1 - p for p in ps)
    return dict(BS=sum((p - y) ** 2 for p, y in zip(ps, ys)) / n, BS_cal=sum(p * (1 - p) for p in ps) / n, alpha=a, beta=b, dif=a - b, dif_cal=ac - bc, sum_p=sum(ps), D_wins=sum(ys))
