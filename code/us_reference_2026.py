"""
Fundamentals reference for the 2026 US House (standard library only). Fitted on 2024 with the CONTEMPORARY presidential vote (2024 results on 2024 lines) + incumbency + seat party; applied to 2026 with the 2024 presidential vote on 2026 lines and a uniform national shift
dE = (generic-ballot average of 2026) - (national two-party House vote of 2024 = -2.68; R 49.8 vs D 47.2).
P(D wins) = Phi(a + b*(m_pres24 + dE)/10 + c*incD + d*incR + e*seatD + f*seatR). Margins in points; rounding error of +-1 pp (Downballot). Assumes uniform swing and that generic-ballot polls measure the House vote without bias.
Generic-ballot average: RV/LV polls ending on or after 2026-06-01 (VoteHub API, CC BY 4.0; snapshot in data/votehub/), weight exp(-age/tau)*sqrt(n) with a 21-day half-life; two-party margin 100*(D-R)/(D+R).
Writes outputs/reference_2026_house_probabilities.csv (columns: cd, p_ref; no third-party values). Run from the repository root.
"""
import csv, json, math, re, random, datetime as dt
from us_common import Phi, fit_probit, metrics
def norm(s): s = re.sub(r'\b(jr|sr|ii|iii|iv)\b\.?', '', s.lower().replace('.', '').replace("'", '').replace('"', '')); return ' '.join(re.sub(r'\(.*?\)', '', s).split())
def load_db(f):
    return {r[0]: dict(inc=r[1], party=r[2].strip('()'), m24=float(r[5])) for r in csv.reader(open(f)) if r and re.match(r'^[A-Z]{2}-(\d+|AL)$', r[0])}
DB24 = load_db('data/downballot/downballot_pres2020_2024_lines2024.csv'); DB26 = load_db('data/downballot/downballot_pres2024_lines2026.csv')
# ---------- fit on 2024
A = {r['cd']: r for r in csv.DictReader(open('data/forecasters/splitticket_house_2024_datawrapper.csv', encoding='utf-8-sig'))}
J = {r['s_id']: r for r in csv.DictReader(open('data/jhk/jhk_output.csv')) if r['forecast'] == 'split' and r['election_id'] == '2024_house'}
def key(cd): s, n = cd.split('-'); return s + (str(int(n)) if n != 'AL' else '1')
tr = []
for cd, a in A.items():
    inc = a['incumbent'] == '1'; party = a['incumbent_party']; tr.append(dict(cd=cd, st=cd[:2], y=1 - int(J[key(cd)]['probwin_outcome']), m=DB24[cd]['m24'], incD=float(inc and party == 'D'), incR=float(inc and party == 'R'), seatD=float(party == 'D'), seatR=float(party == 'R')))
F = lambda r, sh=0.0: [1.0, (r['m'] + sh) / 10, r['incD'], r['incR'], r['seatD'], r['seatR']]
b24 = fit_probit([F(r) for r in tr], [r['y'] for r in tr])
sts = sorted({r['st'] for r in tr}); fold = {s: i % 5 for i, s in enumerate(sts)}; oof = [None] * len(tr)
for f in range(5):
    bb = fit_probit([F(r) for r in tr if fold[r['st']] != f], [r['y'] for r in tr if fold[r['st']] != f])
    for i, r in enumerate(tr):
        if fold[r['st']] == f: oof[i] = min(max(Phi(sum(u * v for u, v in zip(bb, F(r)))), 0.005), 0.995)
ys = [r['y'] for r in tr]; mt = metrics(oof, ys)
print('2024 fit (contemporary pres 2024; out of sample by state): BS %.4f alpha %.4f beta %.4f a-b %+.4f sum p %.1f (D wins %d)' % (mt['BS'], mt['alpha'], mt['beta'], mt['dif'], mt['sum_p'], mt['D_wins']))
print('coefficients [a, b(10pp), incD, incR, seatD, seatR] =', [round(x, 3) for x in b24])
# ---------- 2026 generic ballot
today = dt.date(2026, 10, 6); polls = json.load(open('data/votehub/generic_ballot_2026-10-06.json'))
def gb(start, pops, tau=21.0):
    num = den = 0.0; n = 0
    for p in polls:
        if p['end_date'] < start or p['population'] not in pops or p.get('internal') or p.get('partisan'): continue
        ans = {a['choice']: a['pct'] for a in p['answers']}
        if 'Dem' not in ans or 'Rep' not in ans: continue
        age = (today - dt.date.fromisoformat(p['end_date'])).days; w = math.exp(-age * math.log(2) / tau) * math.sqrt(min(p['sample_size'] or 800, 3000))
        num += w * 100 * (ans['Dem'] - ans['Rep']) / (ans['Dem'] + ans['Rep']); den += w; n += 1
    return num / den, n
E24 = -2.68
print('\nGeneric-ballot average (two-party margin, D - R, pp):')
base, nb = gb('2026-06-01', ('rv', 'lv')); print('  base (RV+LV, since Jun 1, 21-day half-life): %+.2f (n=%d)' % (base, nb))
for name, args in (('since Aug 1', ('2026-08-01', ('rv', 'lv'))), ('LV only', ('2026-06-01', ('lv',))), ('RV only', ('2026-06-01', ('rv',))), ('with adults', ('2026-06-01', ('rv', 'lv', 'a'))), ('45-day half-life', ('2026-06-01', ('rv', 'lv'), 45.0))):
    v, n = gb(*args); print('  %-16s %+.2f (n=%d)' % (name, v, n))
# ---------- 2026
S26 = {r['cd']: r for r in csv.DictReader(open('data/forecasters/splitticket_house_2026-10-06.csv'))}
rows = []
for cd, d in DB26.items():
    s = S26[cd]; names = {norm(s['dem_name']), norm(s['rep_name'])}; run = norm(d['inc']) in names
    rows.append(dict(cd=cd, m=d['m24'], incD=float(run and d['party'] == 'D'), incR=float(run and d['party'] == 'R'), seatD=float(d['party'] == 'D'), seatR=float(d['party'] == 'R'), split=float(s['win_prob_d']) / 100, run=run))
print('\nincumbents running (name matches the Split Ticket capture): %d of 435 (D %d, R %d)' % (sum(r['run'] for r in rows), sum(r['incD'] for r in rows), sum(r['incR'] for r in rows)))
def probs(dE): return [min(max(Phi(sum(u * v for u, v in zip(b24, F(r, dE)))), 0.0), 1.0) for r in rows]
random.seed(56)
def mc(dE, sn, N=4000):
    base_eta = [sum(u * v for u, v in zip(b24, F(r, dE))) for r in rows]; cont = 0; tot = 0
    for _ in range(N):
        sh = random.gauss(0, sn) / 10 * b24[1]; seats = sum(1 for e in base_eta if e + sh + random.gauss(0, 1) > 0); tot += seats; cont += seats >= 218
    return tot / N, cont / N
print('\n2026 reference (House) by national environment (dE = generic ballot - (%.2f)):' % E24)
print(f"{'scenario':16s}{'GB':>7s}{'dE':>7s}{'sum p D':>9s}{'P>50%':>7s}{'(a-b)cal':>10s}  [MC P(>=218) with sigma_n=2.5 is NOT used: no regional correlation]")
res = {}
for name, g in (('base', base), ('base - 2 pp', base - 2), ('base + 2 pp', base + 2), ('base - 4 pp', base - 4)):
    p = probs(g - E24); sp = sum(p); ac = sum(x * (1 - x) ** 2 for x in p) / sp; bc = sum((1 - x) * x * x for x in p) / (len(p) - sp); res[name] = p
    print(f"{name:16s}{g:7.2f}{g - E24:7.2f}{sp:9.1f}{sum(1 for x in p if x > .5):7d}{ac - bc:+10.4f}")
p = res['base']; sp_ = [r['split'] for r in rows]
mp, ms = sum(p) / 435, sum(sp_) / 435; cor = sum((a - mp) * (b - ms) for a, b in zip(p, sp_)) / math.sqrt(sum((a - mp) ** 2 for a in p) * sum((b - ms) ** 2 for b in sp_))
print('\nReference (base) vs Split Ticket 2026-10-06: sum p %.1f vs %.1f, correlation %.3f, BS_cal reference %.4f' % (sum(p), sum(sp_), cor, sum(x * (1 - x) for x in p) / 435))
w = csv.writer(open('outputs/reference_2026_house_probabilities.csv', 'w', newline='')); w.writerow(['cd', 'p_ref'])
for r, a in zip(rows, p): w.writerow([r['cd'], round(a, 4)])
