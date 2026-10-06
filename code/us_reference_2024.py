"""
Fundamentals reference model for the US House, fitted and evaluated on 2024 (standard library only).
Data (local, not in this repository; see data/README.md): Split Ticket 2024 House file, Downballot presidential results by district, JHK Forecasts outcomes.
P(D wins) = Phi(a + b*(pres24_margin_D/10) + c*incD + d*incR + e*seatD + f*seatR [+ g*WAR for M1]); ridge probit (lambda = 1 on non-constant coefficients), 5-fold cross-validation grouped by STATE.
The intercept absorbs the 2024 national environment (information from the same year, "oracle"): the reference is a lower bound on error for a forecaster that must estimate the environment in advance.
Campaign spending is NOT used (capture date unknown; leakage risk). Run from the repository root.
"""
import csv
from us_common import Phi, parse_margin, fit_probit, metrics
ST = 'data/forecasters/splitticket_house_2024_datawrapper.csv'; DB = 'data/downballot/downballot_pres2020_2024_lines2024.csv'; JHK = 'data/jhk/jhk_output.csv'
A = list(csv.DictReader(open(ST, encoding='utf-8-sig')))
J = {r['s_id']: r for r in csv.DictReader(open(JHK)) if r['forecast'] == 'split' and r['election_id'] == '2024_house'}
def key(cd): s, n = cd.split('-'); return s + (str(int(n)) if n != 'AL' else '1')
def load_downballot(f):
    import re
    return {r[0]: dict(inc=r[1], party=r[2].strip('()'), m24=float(r[5])) for r in csv.reader(open(f)) if r and re.match(r'^[A-Z]{2}-(\d+|AL)$', r[0])}
DB24 = load_downballot(DB); rows = []
for r in A:
    cd = r['cd']; war = parse_margin(r['war_composite']); inc = r['incumbent'] == '1'; party = r['incumbent_party']
    rows.append(dict(cd=cd, st=cd[:2], y=1 - int(J[key(cd)]['probwin_outcome']), pres=DB24[cd]['m24'] / 10, incD=float(inc and party == 'D'), incR=float(inc and party == 'R'), seatD=float(party == 'D'), seatR=float(party == 'R'), war=0.0 if war is None else war, split_p=float(r['dem_prob_winning']) / 100))
def feats(r, war): return [1.0, r['pres'], r['incD'], r['incR'], r['seatD'], r['seatR']] + ([r['war']] if war else [])
sts = sorted({r['st'] for r in rows}); fold = {s: i % 5 for i, s in enumerate(sts)}; ys = [r['y'] for r in rows]; out = {}
for name, war in (('M0 fundamentals (pres 2024 + incumbency)', False), ('M1 = M0 + composite WAR', True)):
    oof = [None] * len(rows)
    for f in range(5):
        tr = [i for i, r in enumerate(rows) if fold[r['st']] != f]; b = fit_probit([feats(rows[i], war) for i in tr], [rows[i]['y'] for i in tr])
        for i, r in enumerate(rows):
            if fold[r['st']] == f: oof[i] = min(max(Phi(sum(bj * xj for bj, xj in zip(b, feats(r, war)))), 0.005), 0.995)
    out[name] = (oof, fit_probit([feats(r, war) for r in rows], ys))
print(f"{'model':48s}{'BS':>7s}{'BS_cal':>8s}{'alpha':>7s}{'beta':>7s}{'a-b':>7s}{'(a-b)cal':>9s}{'sum p':>7s}{'D wins':>7s}")
def line(n, m): print(f"{n:48s}{m['BS']:7.3f}{m['BS_cal']:8.3f}{m['alpha']:7.3f}{m['beta']:7.3f}{m['dif']:7.3f}{m['dif_cal']:9.3f}{m['sum_p']:7.1f}{m['D_wins']:7d}")
for n, (oof, b) in out.items(): line(n + ' (out of sample)', metrics(oof, ys))
line('Split Ticket 2024 (file)', metrics([min(max(r['split_p'], 0.005), 0.995) for r in rows], ys))
print('\ncoefficients (full fit; margin in units of 10 pp):')
for n, (oof, b) in out.items(): print(' ', n, [round(x, 3) for x in b])
