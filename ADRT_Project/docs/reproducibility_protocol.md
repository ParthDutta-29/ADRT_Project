# ADRT Framework: Reproducibility Protocol

## Introduction
This protocol dictates the steps necessary to reproduce the statistical experiments, bounding validations, and comparative metrics used in the formal evaluation of the ADRT distributed pipeline resilience framework.

## 1. Execution Environment
- **Platform:** UPPAAL 4.1+ SMC (Statistical Model Checker)
- **Dependencies:** Python 3.8+, Pandas, Matplotlib, Numpy

## 2. Parameter Configurations & Scripts
The primary experimental bounds are configured via `config/experiment_sweep.json`.

### Reproducing the Statistical Summary
1. Navigate to the `scripts/` directory.
2. Execute the runner:
   `python experiment_runner.py`
3. This orchestrates `experiment_sweep.json` and outputs data into `build/experiments/run_{timestamp}/`.
4. Outputs generated will include:
   - `statistical_summary.csv`
   - `trajectory_statistics.csv`
   - `run_manifest.json` (Includes timestamp, hashes, and parameter states)
   - `experiment_metadata.json`

### Regenerating Publication Plots
1. Once the experiment runner has generated the CSVs, execute the plot generator:
   `python plot_results.py --exp_dir ../build/experiments/run_{timestamp}`
2. This parses `trajectory_statistics.csv` to compute 95% Confidence Intervals (CI) and generate bound-filled trajectory plots.
3. Outputs are stored in `build/experiments/run_{timestamp}/plots/`.

## 3. Formal Bounded-State Verification
To guarantee the model lacks infinite loops, out-of-bound variables, or underflows:
1. Re-bundle the XML:
   `python merge_xml.py --modular`
2. Run formal safety queries:
   `python phase9_formal_verification.py`
3. Any warnings regarding dynamic decrements MUST be manually resolved using the guaranteed saturating pattern `(x >= y) ? x - y : 0`. `max(0, x-y)` is strictly forbidden.

## 4. Query Re-Validation
The file `validation/experimental_queries.q` contains all queries.
Run it natively inside the UPPAAL GUI or via the UPPAAL command line tool (`verifyta`) utilizing `build/main_system.xml`.
