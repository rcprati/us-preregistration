# US Pre-registration v1: probabilistic forecasters in the 2026 House and Senate elections: expected versus observed α, β and Brier

_Version 1 (2026-10-06) of the **US** series, a **new file**. It does not replace or alter earlier pre-registrations in the author's private repository (a third-party forecast evaluation for the same elections, and a separate series on Brazil); those remain as they are. This document contains **only what the paper on US probabilistic forecasters needs**. It counts as a pre-registration only once deposited (a commit with a server-side timestamp) **before 2026-11-03** and before any 2026 election result has been seen._

## 0. Knowledge state (transparency statement)

- **Already seen:** US presidential, Senate and House results from 2016 to 2024 and all of the paper's analyses of those cycles (the JHK Forecasts database, 33 forecasters; internal technical note v47, §5.43–§5.52), including α, β, α−β, Brier and the expected values of Split Ticket in 2022 and 2024.
- **Also seen:** Split Ticket's **2026-10-06** forecasts for the House and Senate (probabilities and margins), the 2026 generic-ballot average (VoteHub API), the 2024 presidential vote by district (The Downballot), and a third-party pre-registered forecast (Oswald/TMG), which is **not** used here.
- **Not seen:** **no result of the 2026 US general elections** (no partial counts, and no press projections used as data).
- **Fixed before the results:** the hypotheses (§1), the outcome rule (§2), the expected values and simulated distributions (§3), the statistics and interpretation rules (§4–§6) and the reference model (§3.3, frozen by hash).

## 1. Hypotheses

All concern **Split Ticket** (the main forecaster, because its data are in hand and it has a 2022 and 2024 track record) and, where indicated, other forecasters whose final 2026 probabilities are obtained (§2). One cycle only: **there are no persistence p-values** and no hypothesis is confirmed by significance; the criterion is the position of the observed value in the simulated distribution (§3, §5).

| ID | Hypothesis | Prediction and basis | Type |
|---|---|---|---|
| H1 | **Under-confidence.** In the House, observed Brier / Brier expected under calibration (BS_obs / BS_cal) < 1 | Yes: Split Ticket 0.79 (2022) and 0.52 (2024); House models pooled 0.69 [0.48; 0.91] (internal note §5.44) | confirmatory |
| H2 | **Correlated null.** In the House, observed α−β lies inside the 90% interval of the **correlated** null in §3 | Yes: in 2022 and 2024 Split Ticket's α−β (+0.031 and −0.009) was inside the correlated interval; in 2022 it was outside the independent one (internal note §5.44) | confirmatory |
| H3 | **Reference.** In the House, BS(Split Ticket) < BS(frozen fundamentals reference, §3.3) | Yes: the reference ignores candidates and district polls; in 2024, even with the national environment known, it only matched the professionals (internal note §5.51) | confirmatory |
| H4 | **Senate.** Descriptive: observed α, β, α−β and Brier, and their position in the simulated distribution | No directional hypothesis (35 races, 16 with p = 0 or 1) | exploratory |
| H5 | **National shock.** δ̂ (§4) of Split Ticket in the House and Senate, and the generic-ballot error (poll average − observed national two-party vote) | No directional hypothesis; describe whether δ̂ and the generic-ballot error have the same sign | exploratory |
| H6 | **Across forecasters** (only if ≥ 3 forecasters with final per-unit probabilities): cycle intraclass correlation (ICC) of α−β and δ̂ ≥ 0.5 | Yes: 0.71–0.88 in earlier cycles (internal note §5.50), but with few forecasters | exploratory, conditional |
| H7 | **Ranking** (only if ≥ 5 forecasters in common with 2024): Spearman correlation between the 2024 and 2026 Brier rankings > 0 | Yes: +0.68 (House) and +0.57 (Senate) across earlier cycle pairs (internal note §5.45) | exploratory, conditional |

## 2. Data and outcome (freeze at the time)

- **Main forecast:** Split Ticket / The Argument, files from the "Get the data" button (House: 435 districts; Senate: 35 races). **Interim capture of 2026-10-06** (hashes in §9). The **final capture** will be downloaded on **2026-11-02 or 2026-11-03 (before polls open)**, with its date and hash recorded in an addendum, **before** any result. The evaluation uses the final capture; if it cannot be obtained, the 2026-10-06 capture is used and this is declared. No other version will be used.
- **Expected values:** computed by the frozen script (§9) on the final capture, **without access to results**, and deposited in an addendum. The numbers in §3 are those of the 2026-10-06 capture.
- **Other forecasters (exploratory):** Race to the WH, DDHQ, Cook, Sabato and Inside Elections, **if** their final 2026 probabilities or ratings are obtained from public archives (the JHK database or the Wayback Machine) after the result; ratings are converted with the fixed JHK table (Solid .99, Likely .90, Lean .75, Toss-up .50), **without adjustment**. This is declared as obtained **after** the election.
- **Results:** **certified** state counts (not projections); main source MEDSL, secondary the state election offices; record the URL and date. If a state has not certified by the evaluation date, report with and without it. Races with a runoff after 2026-11-03 (for example Georgia, Louisiana): report with and without them until the final result.
- **Outcome:** y = 1 if the candidate on the **D side of Split Ticket's file** (`dem_name`) wins the seat. **Independents listed as `dem_name` (Nebraska, Montana, South Dakota and Idaho in the Senate; Alaska-AL in the House) count as the D side.** Louisiana (Senate), whose `dem_name` is "Eventual Nominee": the Democratic Party's nominee, whoever runs. The primary analysis uses all contests in the file (435 and 35).
- **Probability:** `win_prob_d` / 100, without recalibration. **The values are integer percentages**: 0 and 100 are treated as certainties (321 of the 435 districts and 16 of the 35 races on 2026-10-06). Sensitivity: only units with 0.05 < p < 0.95.

## 3. Values fixed now

### 3.1 Under calibration (capture of 2026-10-06; script `us_expected_splitticket_2026.py`, seed 57, B = 5000)

π = E[p], α_cal = E[p(1−p)²]/E[p], β_cal = E[(1−p)p²]/E[1−p], BS_cal = E[p(1−p)]. The simulation uses a Gaussian copula: y_i = 1{Φ⁻¹(p_i) + e_i > 0}, e_i = √ρ_n·z_nat + √ρ_s·z_state + √(1−ρ_n−ρ_s)·ε_i, with ρ **fixed now** from earlier cycles (internal note §5.44): **House (0.12; 0.02), Senate (0.005; 0)**.

| | House (435) | Senate (35) |
|---|---|---|
| Sum of p (expected D seats) | 235.3 | 17.5 |
| BS_cal | 0.0259 | 0.0685 |
| α_cal | 0.0254 | 0.0638 |
| β_cal | 0.0264 | 0.0733 |
| **(α−β)_cal** | **−0.0010** | **−0.0095** |
| α−β, **correlated** null [5%; 50%; 95%] | [−0.0356; −0.0018; +0.0351] | [−0.0841; −0.0070; +0.0641] |
| α−β, independent null [5%; 50%; 95%] | [−0.0164; −0.0010; +0.0145] | [−0.0817; −0.0074; +0.0641] |
| BS, correlated null | [0.0190; 0.0254; 0.0345] | [0.0346; 0.0666; 0.1101] |
| BS/BS_cal, correlated null | [0.73; 0.98; 1.33] | [0.51; 0.97; 1.61] |
| D seats, correlated null | [223; 235; 248] | [15; 18; 20] |

### 3.2 Split Ticket's track record (JHK database; script `us_splitticket_history.py`), for reference

| Election | BS | BS_cal | α | β | α−β | (α−β)_cal |
|---|---|---|---|---|---|---|
| House 2022 | 0.033 | 0.042 | 0.049 | 0.018 | +0.031 | +0.007 |
| House 2024 | 0.016 | 0.031 | 0.012 | 0.020 | −0.009 | −0.006 |
| Senate 2022 | 0.029 | 0.057 | 0.055 | 0.010 | +0.044 | +0.030 |
| Senate 2024 | 0.035 | 0.066 | 0.018 | 0.056 | −0.039 | −0.031 |

### 3.3 Fundamentals reference model (House; `us_reference_2026.py`; frozen file `outputs/reference_2026_house_probabilities.csv`)

A probit fitted on 2024 (2024 presidential vote on 2024 lines, incumbent running, seat party; BS 0.016 out of sample), applied to the 2024 presidential vote on 2026 lines with a uniform shift ΔE = (generic-ballot poll average) − (−2.68, the national two-party House vote of 2024). **Fixed environment: weighted generic-ballot average of 2026-10-06 = D +6.98 pp** (RV and LV polls since 2026-06-01, 21-day half-life; VoteHub API, CC BY 4.0), ΔE = +9.66. Fixed values: sum of p = 238.8; 233 districts with P > 0.5; BS_cal = 0.0277; (α−β)_cal = +0.0048; correlation with Split Ticket's 2026-10-06 forecast = 0.982. **The reference is not recomputed** with later information; an "oracle" version (intercept fitted to the realised national vote) is exploratory.

## 4. Statistics and rules

- **Observed:** α_obs, β_obs, α−β, Brier, BS/BS_cal and BBS = (α+β)/2, with the definition of §3 (α over the D-side seats, β over the rest). Position (percentile) of the observed value in the §3 distributions; the independent and correlated nulls are reported side by side.
- **H1:** BS_obs/BS_cal < 1 (report the value and its percentile in the correlated null).
- **H2:** α−β_obs ∈ [−0.0356; +0.0351] (values of the 2026-10-06 capture; if the final capture changes the values, those of the addendum, computed by the same script, apply).
- **H3:** ΔBS = BS(Split Ticket) − BS(reference) < 0; 90% interval by **state-level bootstrap** (B = 5000, seed 58), with no significance threshold. A version with the "oracle" reference is exploratory.
- **δ̂ (H5):** δ̂_win is the δ such that Σ Φ(Φ⁻¹(p_i) + δ) equals the observed number of D-side seats (δ > 0 = the D side did better than forecast); δ̂_dif is the δ that reproduces the observed α−β (script `us_national_shock.py`, function `dif_model`).
- **Sensitivities:** only 0.05 < p < 0.95; excluding units whose result is not yet certified; House without Alaska-AL and without single-candidate districts; Senate without Louisiana.

## 5. Inference

One cycle, correlated error (national share ≈ 12% in the House) and rounded probabilities: **no persistence p-values** and no per-unit confidence intervals as if units were independent. The reading is by **position** in the simulated distribution and by **coverage**. Under its own null the probability of each confirmatory hypothesis is about 90% for H2 and about 50% for H1 (the ratio has median 0.98), so a single coverage result neither validates nor refutes the method. The three confirmatory hypotheses (H1–H3) are all reported, without correction for multiple comparisons, and no hypothesis is changed after the result.

## 6. Interpretation rules (fixed now)

1. H1, H2 and H3 being confirmed or refuted only describes Split Ticket in 2026; they do not generalise to other forecasters or cycles.
2. Inside the correlated interval but outside the independent one: the deviation is consistent with a common national shock and not with forecaster bias (the paper's message). Outside the correlated interval: report as incompatible with calibration even allowing for a national shock.
3. The diagnostic by α, β and α−β remains a **diagnostic, not a prognosis between cycles**; the within-cycle prognosis via (α−β)_cal keeps the scope of internal note §5.48–§5.49 (modest).
4. The 2026 results will not be used to revise ρ, the conversion rule or the reference within this pre-registration; revisions go to a v2 of the US series.

## 7. Declared limitations

- **Third-party data with no known licence:** the Split Ticket files (subscriber content) and The Downballot's are for **local research use**; they are **not republished**, only their hashes. Terms of use were not checked in full.
- **Interim capture:** the 2026-10-06 forecasts may change until 2026-11-03; the numbers in §3 are illustrative and will be replaced by those of the final capture (addendum).
- **Integer-percentage probabilities**, with most units at 0 or 100: α and β depend on few contested units (57 in the House and 13 in the Senate between 0.05 and 0.95).
- **Independence between forecasters:** Split Ticket and VoteHub use the same polling average; comparisons between forecasters are not comparisons of independent errors.
- **Reference:** assumes uniform swing and an unbiased generic ballot (neither tested); few recent polls in the API (11 from July to October); The Downballot margins are rounded to whole points; fitted on one cycle. The House-control simulation of the internal note (§5.52) is **not** used here.
- **Calendar:** certification comes weeks after 2026-11-03; the evaluation is later and recorded in a new version.

## 8. Out of scope

Brazil, economic indicators, likely versus registered voters, 2026 president and governor, the Oswald/TMG forecast, per-candidate analyses, and recalibration of the probabilities.

## 9. Integrity and deposit

- **Intended deposit:** `preregistration_us_v1.md` and `preregistration_us_v1.sha256`, commit and tag `preregistration-us-v1`, **before 2026-11-03**, in a new public repository. The commit timestamp on the hosting server is the evidence of timing.
- **Data files (SHA-256; local, not republished):**
  - Split Ticket House 2026-10-06 (`data/forecasters/splitticket_house_2026-10-06.csv`): `4211698a70b030dd63d9e2f5fcc5df16c6b8dd3ad1a90778d659b721846df45a`
  - Split Ticket Senate 2026-10-06 (`data/forecasters/splitticket_senate_2026-10-06.csv`): `360a1957e2e81d7f46fe8849f7974b44ae0d23bce32e20f54bac906535143306`
  - Split Ticket House 2024 (`data/forecasters/splitticket_house_2024_datawrapper.csv`): `5ba5cd63fdc34c54ad3544c67dd57d8e97ede3be816bc1f4a2cac1f22d43638d`
  - Split Ticket Senate 2024 (`data/forecasters/splitticket_senate_2024_datawrapper.csv`): `db24d9b8d230526d3faace5bcd2c76066d341f17c4787dea6d2655f4c2c6f2a9`
  - The Downballot, 2024 on 2026 lines (`data/downballot/downballot_pres2024_lines2026.csv`): `a3bffa0500b0827c56f66ea40320f3b145e8570864f9b14eee40a5ed3367671a`
  - The Downballot, 2020 and 2024 on 2024 lines (`data/downballot/downballot_pres2020_2024_lines2024.csv`): `b2b8655da31de02efb7e57841fa3676e02711aabf0666567ca510dae841faa72`
  - VoteHub generic ballot (API, CC BY 4.0, captured 2026-10-06; `data/votehub/generic_ballot_2026-10-06.json`): `3d3245b32d1cef31db2d93b2bf4634c3eb18505b6c6cf4ffe9ba723a9269052f`
  - JHK Forecasts (`data/jhk/jhk_output.csv`): `0834c4fc53e9ffc2e1d7f651a6c87fa606bb02db325c41ce42ea8db25a15a67e`
- **Frozen scripts and outputs (SHA-256):**
  - `code/us_common.py`: `758603289d9000c857932a500eb778e3ce4e8cb60f43ff99cc54f70567f9d442`
  - `code/us_expected_splitticket_2026.py`: `ce930a2ebee68fd941fbf4fda486b96f9b1a1c91490027d1203e299274af53ec`
  - `code/us_reference_2024.py`: `c5e91be21c0ebb3353e691d606fd54ce3e802a18a24dac2ab2273cec05c75f77`
  - `code/us_reference_2026.py`: `fa3c7f536d032e4c0f6f925018766a5916d08437d96b6bd63811d6241b4224f2`
  - `code/us_national_shock.py`: `5cc512cfbeba6445de94a7bb0087ca6a707c30a9bf5aa38198fb926e105b1097`
  - `code/us_splitticket_history.py`: `b98be61023c2c8a67ff8221c9bfb9818a16053d11274a24619a7adb0e84dd837`
  - `outputs/reference_2026_house_probabilities.csv`: `a5268e891f7470743c5af9dc2278174474afe85232521a9cefc1da1cce4f5047`
- Any later change is a new version (v2 of the US series), never an edit of this one.
