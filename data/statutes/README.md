# Statute Source Files

This directory holds the authoritative text of statutes used as context
for the teacher model. These files are `.gitignore`d because they are
public-domain government text that anyone can fetch.

## Required files

### `co_aia_sb24_205.txt`
Colorado AI Act (SB 24-205), full enacted text.
- Source: https://leg.colorado.gov/bills/sb24-205
- Click "Final Act" PDF, copy text
- Include the delay amendment (SB 25B-004) noting the June 30, 2026 effective date

### `nyc_ll144_dcwp_rules.txt`
NYC Local Law 144 + DCWP Final Rules on AEDTs.
- Statute: https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page
- Final Rules: https://rules.cityofnewyork.us/rule/automated-employment-decision-tools-updated/
- Combine both into one file

### `tx_traiga_hb149.txt` (optional, needed for Case H1)
Texas Responsible AI Governance Act (HB 149), enacted text.
- Source: https://capitol.texas.gov/BillLookup/History.aspx?LegSess=89R&Bill=HB149
- Click "Enrolled" version

## Format

Plain UTF-8 text. Strip headers/footers. Keep section numbers intact.
The teacher prompt concatenates all .txt files in this directory
alphabetically, so file naming matters for ordering.
