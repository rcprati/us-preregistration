# Inputs (not included)

The scripts read these files under `data/`. They are third-party data and are not redistributed here; SHA-256 values are in §9 of `preregistration_us_v1.md`.

| Path | Source | Notes |
|---|---|---|
| `forecasters/splitticket_house_2026-10-06.csv`, `forecasters/splitticket_senate_2026-10-06.csv` | Split Ticket / The Argument, 2026 midterm model page, "Get the data" button | interim captures of 2026-10-06; subscriber content; local research use only |
| `forecasters/splitticket_house_2024_datawrapper.csv`, `forecasters/splitticket_senate_2024_datawrapper.csv` | Split Ticket, 2024 forecast pages (Datawrapper chart data) | validated against the JHK database (House 435/435, Senate 34/34) |
| `downballot/downballot_pres2024_lines2026.csv`, `downballot/downballot_pres2020_2024_lines2024.csv` | The Downballot (sponsored by Grassroots Analytics), public Google Sheets exported to CSV on 2026-10-06 | integer percentages; no licence stated |
| `votehub/generic_ballot_2026-10-06.json` | VoteHub polling API, `GET /polls?poll_type=generic-ballot` (https://api.votehub.com), captured 2026-10-06 | CC BY 4.0 |
| `jhk/jhk_output.csv` | JHK Forecasts, forecast-history database (https://projects.jhkforecasts.com/forecast-history) | 33 forecasters, 2016–2024; no licence stated |
