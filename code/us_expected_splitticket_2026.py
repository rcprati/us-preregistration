"""
Expected values and simulated distribution of alpha, beta, alpha-beta and Brier for Split Ticket in 2026 (House and Senate) under calibration with correlated errors.
Gaussian copula: y_i = 1{Phi^-1(p_i) + e_i > 0}, e_i = sqrt(rho_n)*z_nat + sqrt(rho_s)*z_state + sqrt(1 - rho_n - rho_s)*eps_i. Standard library only; seed 57; B = 5000.
Input: data/forecasters/splitticket_{house,senate}_<date>.csv (argument 1: date suffix, default 2026-10-06). rho fixed before the results: House (0.12, 0.02), Senate (0.005, 0).
p = win_prob_d/100; 0 and 1 are treated as certainties. Run from the repository root.
"""
import csv, math, random, statistics, sys
suf = sys.argv[1] if len(sys.argv) > 1 else '2026-10-06'; N = statistics.NormalDist(); random.seed(57); B = 5000
def met(ps, ys):
    pos = [(1 - p) ** 2 for p, y in zip(ps, ys) if y]; neg = [p ** 2 for p, y in zip(ps, ys) if not y]
    if not pos or not neg: return None
    a = sum(pos) / len(pos); b = sum(neg) / len(neg); return dict(alpha=a, beta=b, dif=a - b, BS=sum((p - y) ** 2 for p, y in zip(ps, ys)) / len(ps), seats=sum(ys))
def pct(v, q): v = sorted(v); return v[min(len(v) - 1, int(q * len(v)))]
for name, f, col, rho in (('House', f'data/forecasters/splitticket_house_{suf}.csv', 'cd', (0.12, 0.02)), ('Senate', f'data/forecasters/splitticket_senate_{suf}.csv', 'State', (0.005, 0.0))):
    R = list(csv.DictReader(open(f))); ps = [float(r['win_prob_d']) / 100 for r in R]; st = [r[col][:2] if col == 'cd' else r[col] for r in R]; n = len(ps)
    sp = sum(ps); ac = sum(p * (1 - p) ** 2 for p in ps) / sp; bc = sum((1 - p) * p * p for p in ps) / (n - sp); bsc = sum(p * (1 - p) for p in ps) / n
    print(f'\n== {name}: n = {n}, sum p = {sp:.1f}, BS_cal {bsc:.4f}, alpha_cal {ac:.4f}, beta_cal {bc:.4f}, (a-b)_cal {ac - bc:+.4f}; p in {{0,1}}: {sum(1 for p in ps if p in (0, 1))}; 0.05<p<0.95: {sum(1 for p in ps if 0.05 < p < 0.95)} ==')
    z = [N.inv_cdf(p) if 0 < p < 1 else (-9.0 if p == 0 else 9.0) for p in ps]; sts = sorted(set(st))
    for lab, (rn, rs) in (('independent', (0.0, 0.0)), ('correlated', rho)):
        out = {k: [] for k in ('alpha', 'beta', 'dif', 'BS', 'ratio', 'seats')}
        for _ in range(B):
            zn = random.gauss(0, 1); zs = {s: random.gauss(0, 1) for s in sts}; ys = [1 if zi + math.sqrt(rn) * zn + math.sqrt(rs) * zs[s] + math.sqrt(1 - rn - rs) * random.gauss(0, 1) > 0 else 0 for zi, s in zip(z, st)]
            m = met(ps, ys)
            if m: [out[k].append(m[k]) for k in ('alpha', 'beta', 'dif', 'BS', 'seats')]; out['ratio'].append(m['BS'] / bsc)
        print(f'  null {lab:12s} (rho_n={rn}, rho_s={rs}) [5%; 50%; 95%]: ' + ' | '.join(f"{k} [{pct(v, .05):.4f}; {pct(v, .5):.4f}; {pct(v, .95):.4f}]" if k not in ('seats', 'ratio') else (f"D seats [{pct(v, .05):.0f}; {pct(v, .5):.0f}; {pct(v, .95):.0f}]" if k == 'seats' else f"BS/BS_cal [{pct(v, .05):.2f}; {pct(v, .5):.2f}; {pct(v, .95):.2f}]") for k, v in out.items()))
