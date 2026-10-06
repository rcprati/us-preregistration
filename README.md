# US pre-registration v1 (2026 House and Senate)

Pre-registration of an evaluation of probabilistic election forecasters in the 2026 US House and Senate elections, based on the Brier decomposition into **α = E[(1−p)² | Y=1]** and **β = E[p² | Y=0]** and on the expected values of these quantities under calibration with correlated errors.

**Status:** draft prepared on 2026-10-06; **not yet deposited**. It counts as a pre-registration only from the timestamp of the commit that first adds `preregistration_us_v1.md` to the public repository, which must happen **before 2026-11-03** (election day) and before any 2026 result is seen.

## Contents

| Path | What |
|---|---|
| `preregistration_us_v1.md` | the pre-registration (hypotheses, outcome rule, values fixed in advance, interpretation rules, limitations, hashes) |
| `preregistration_us_v1.sha256` | SHA-256 of the pre-registration |
| `code/` | frozen scripts (standard library only, except `us_national_shock.py`, which needs numpy, pandas and scipy) |
| `outputs/reference_2026_house_probabilities.csv` | frozen probabilities of the fundamentals reference model (columns `cd`, `p_ref`; no third-party values) |
| `data/README.md` | the third-party inputs the scripts need, with sources and SHA-256. **The data are not in this repository** |

## Reproducing

Place the inputs listed in `data/README.md` under `data/`, then run from the repository root with `PYTHONPATH=code`:

```bash
PYTHONPATH=code python3 code/us_expected_splitticket_2026.py     # null distributions for Split Ticket 2026 (seed 57)
PYTHONPATH=code python3 code/us_reference_2024.py                # fundamentals reference fitted on 2024
PYTHONPATH=code python3 code/us_reference_2026.py                # 2026 reference (writes outputs/reference_2026_house_probabilities.csv)
PYTHONPATH=code python3 code/us_splitticket_history.py           # Split Ticket 2022/2024 track record from JHK
PYTHONPATH=code python3 code/us_national_shock.py                # latent national shock (needs numpy, pandas, scipy)
```

To verify integrity: `shasum -a 256 -c preregistration_us_v1.sha256`, and compare the hashes listed in §9 of the pre-registration with your files.

## Notes

- The pre-registration cites an internal technical note (v47) for earlier-cycle results used as priors; that note is not part of this repository.
- Third-party data (Split Ticket, The Downballot, JHK Forecasts) are used locally for research and are **not redistributed**; only their hashes appear here. The VoteHub polling API data are CC BY 4.0.
## Licence

The pre-registration text, the code and the outputs written by the author are released under **[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)**; the full legal text is in `LICENSE`. Suggested attribution: *Prati, R., US pre-registration v1 (2026 House and Senate), 2026.* The licence does **not** cover third-party data (Split Ticket, The Downballot, JHK Forecasts), which are not part of this repository and keep their own terms; VoteHub polling API data are CC BY 4.0 under VoteHub's own terms.
