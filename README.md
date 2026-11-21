# Gaming Industry Sales Analysis (HCL Training Project)

Practice project built on the same step-by-step structure as the Retail Sales sample.

## Files
- `gaming_sales_raw.csv`          raw, messy practice data (synthetic)
- `make_dataset.py`               regenerates the raw CSV
- `gaming_industry_analysis.py`   main project (21 steps, runs cell-by-cell in VS Code)
- `gaming_sales_cleaned.csv`      output: cleaned data
- `gaming_summary.csv`            output: key metrics
- `charts/`                       output: 4 PNG charts

## Run
1. `pip install pandas numpy matplotlib`
2. Open the folder in VS Code (install Python + Jupyter extensions)
3. Run cells in `gaming_industry_analysis.py`, or `python gaming_industry_analysis.py`

## Data-quality problems injected and how they are handled
| Problem | Fix |
|---|---|
| 2 exact duplicate rows | drop_duplicates |
| Extra spaces / wrong case (" West ", "pc ") | strip + canonical-name mapping |
| Text in a number column ("two") | to_numeric(errors="coerce") |
| Zero units, negative price | set to missing, then row removed |
| Invalid date ("not available") | to_datetime(errors="coerce"), row removed |
| Missing region / units | row removed |
| Missing publisher | filled with "Unknown" |
