# US Pre-registration v1, Addendum 1: definition and recording of the final capture, and interim captures

_DRAFT of 2026-10-26; it counts only once deposited (commit with a server-side timestamp) **before the final capture is taken or opened**, that is, before 2026-11-02 18:00 (-03). It is a **new file**: it does not replace or alter `preregistration_us_v1.md` (SHA-256 `ce202bc0621efb321816…`, commit `9ef0fea8aadf`, tag `preregistration-us-v1`), the frozen scripts or the frozen reference outputs. Hypotheses H1–H7, the outcome rule, the null parameters, the fundamentals reference (generic-ballot environment D +6.98 of 2026-10-06) and the interpretation rules are **unchanged**._

## 1. What this addendum fixes

Section 2 of v1 says that the evaluation uses a "final capture" of Split Ticket's files taken on 2 or 3 November, before polls open, but does not say which version counts when the source updates itself. Since 2026-10-26 we know how the source behaves (Section 3), so the final capture is defined here, before it exists.

## 2. Definition of the final capture

- **Files:** the per-contest House file (435 districts) and the per-contest Senate file (35 races) of Split Ticket / The Argument, obtained through the "Get the data" button of the 2026 model page (columns as in the 2026-10-06 files: `win_prob_d`, `win_prob_r`, `dem_name`, `rep_name`, …).
- **Version that counts:** for each file, the **latest version published before 2026-11-03 11:00 UTC** (the opening of the first polls in the Eastern time zone). The charts refresh about once a day at 18:00 (-03) (≈ 21:00 UTC), so the expected version is the refresh of **2026-11-02 at about 18:00 (-03)**. If a file was last modified earlier than that, or more often than daily near the election, the latest `Last-Modified` before the cut-off is used and this is declared in the addendum that records the capture.
- **Taking the capture:** any time after the refresh of 2 November and before the cut-off. The download must use a **fresh `?v=` parameter** (for example the current epoch time in milliseconds), because without it the content delivery network may return a copy cached up to a day old (observed on 2026-10-26).
- **Verification of each file:** (i) record the chart ID, the full URL used, the download time (-03 and UTC), and the HTTP headers `Last-Modified` and `ETag`; (ii) the server's `ETag` equals the MD5 of the file, so the MD5 of the downloaded file must equal it; if it does not, download again; (iii) record the SHA-256. If two downloads inside the window give different `ETag`s, the later version counts and both are recorded.
- **Which charts:** the current charts at the time of capture, identified from the page. On 2026-10-26 they were `Cy0fK` (House) and `g4hHM` (Senate); the older charts `u9EZf` (House, data of 2026-10-24) and `Hus3x` (Senate, data of 2026-10-14) are still online and are **not** used.
- **Seat-count summaries** (the per-category files, e.g. `2OrV2` for the House and `GhLiF` for the Senate) are informational only and do not enter any statistic.
- **If the final capture cannot be obtained**, the rule of v1 applies: the capture of 2026-10-06 is used and this is declared (the interim capture of 2026-10-26 is **not** a substitute for it).

## 3. What was observed about the source (2026-10-26, for the record)

- Charts are refreshed daily at about 18:00 (-03); the static data URL returns a copy cached for up to a day unless a new `?v=` value is passed; the `?v=` value is not the date of the data.
- Two charts for each chamber were online: the House file downloaded on 2026-10-06 (`u9EZf`) now holds data of 2026-10-24, and the current House chart is `Cy0fK`; the Senate chart `Hus3x` held data of 2026-10-14 and the current one is `g4hHM`.
- Louisiana (Senate): the 2026-10-26 file lists **Jamie Davis** as the Democratic candidate (earlier files: "Eventual Nominee"). The outcome rule of v1 covers both cases (the Democratic Party's nominee, whoever runs).

## 4. Interim captures (exploratory; not used for H1–H3)

| Capture (data date) | File | SHA-256 | Expected D seats (sum of p) | (α−β)_cal |
|---|---|---|---|---|
| House, 2026-10-06 | `splitticket_house_2026-10-06.csv` | `4211698a…` | 235.3 | −0.0010 |
| House, 2026-10-26 (18:00:28 -03) | `splitticket_house_2026-10-26.csv` | `0f918ae3…` | 237.6 | −0.0038 |
| Senate, 2026-10-06 | `splitticket_senate_2026-10-06.csv` | `360a1957…` | 17.5 | −0.0095 |
| Senate, 2026-10-14 | `splitticket_senate_2026-10-14.csv` | `2bdaf2d5…` | 17.7 | −0.0149 |
| Senate, 2026-10-26 (18:00:35 -03) | `splitticket_senate_2026-10-26.csv` | `66a4d9a6…` | 17.6 | −0.0168 |

They give a first look at the within-cycle evolution of (α−β)_cal and are reported as exploratory (main text, Section 5.6). The values for the interim captures were computed with the frozen script (`code/us_expected_splitticket_2026.py`, seed 57) on the files above.

## 5. Expected values for the final capture

Computed with the frozen script on the final files **before any 2026 result is seen**, and deposited in a second addendum with the file hashes. The null parameters (House ρ = (0.12, 0.02), Senate (0.005, 0)) and B = 5000 do not change. The reference model is **not** recomputed.

## 6. Knowledge state at the time of this addendum

No 2026 US election result has been seen. The interim captures of 2026-10-06 (v1), 2026-10-14 (Senate) and 2026-10-26 (both chambers), the House and Senate seat-count summaries (2026-10-23 and 2026-10-26), and the 2026-10-26 observations of Section 3 have been seen.

## 7. Integrity and deposit

- Intended deposit: `preregistration_us_v1_addendum_1.md` and `preregistration_us_v1_addendum_1.sha256` in this repository, commit and tag `preregistration-us-v1-addendum-1`, **before 2026-11-02 18:00 (-03)**.
- Third-party files are not republished; only hashes appear here (Section 4).
- Any later change is a new addendum, never an edit of this file.
