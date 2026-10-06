"""
Split Ticket and peers in the 2022 and 2024 House/Senate/President cycles from the JHK Forecasts database (data/jhk/jhk_output.csv): alpha, beta, alpha-beta, Brier and the values expected under calibration. Standard library only.
p = P(Democrat wins) = 1 - probwin; y = 1 - probwin_outcome. Run from the repository root.
"""
import csv, collections
def met(ps, ys):
    n = len(ps); pos = [(1 - p) ** 2 for p, y in zip(ps, ys) if y == 1]; neg = [p ** 2 for p, y in zip(ps, ys) if y == 0]
    a = sum(pos) / len(pos); b = sum(neg) / len(neg); sp = sum(ps); sq = sum(1 - p for p in ps); ac = sum(p * (1 - p) ** 2 for p in ps) / sp; bc = sum((1 - p) * p ** 2 for p in ps) / sq
    return dict(n=n, pi=sum(ys) / n, pbar=sp / n, BS=sum((p - y) ** 2 for p, y in zip(ps, ys)) / n, BS_cal=sum(p * (1 - p) for p in ps) / n, alpha=a, beta=b, dif=a - b, dif_cal=ac - bc)
G = collections.defaultdict(lambda: ([], []))
for r in csv.DictReader(open('data/jhk/jhk_output.csv')):
    if r['forecast'] in ('split', 'race_to_wh', 'ddhq', 'fte', 'econ') and r['year'] in ('2022', '2024') and r['probwin'] not in ('', 'NA') and r['probwin_outcome'] not in ('', 'NA'):
        k = (r['election_id'], r['forecast']); G[k][0].append(1 - float(r['probwin'])); G[k][1].append(1 - float(r['probwin_outcome']))
print(f"{'election':14s}{'forecaster':11s}{'n':>4s}{'pi':>6s}{'pbar':>6s}{'BS':>7s}{'BS_cal':>7s}{'alpha':>7s}{'beta':>7s}{'a-b':>7s}{'(a-b)cal':>9s}")
for (e, f), v in sorted(G.items()):
    if len(v[0]) < 30: continue
    m = met(*v); print(f"{e:14s}{f:11s}{m['n']:4d}{m['pi']:6.2f}{m['pbar']:6.2f}{m['BS']:7.3f}{m['BS_cal']:7.3f}{m['alpha']:7.3f}{m['beta']:7.3f}{m['dif']:7.3f}{m['dif_cal']:9.3f}")
