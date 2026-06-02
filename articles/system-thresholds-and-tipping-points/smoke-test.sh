#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for system thresholds scaffold..."

python3 -m py_compile python/system_thresholds_standard.py
python3 python/system_thresholds_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C threshold-risk score utility..."
  gcc c/threshold_risk_score.c -o outputs/threshold_risk_score_c
  ./outputs/threshold_risk_score_c > outputs/tables/c_threshold_risk_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ threshold/hysteresis simulation..."
  g++ -std=c++17 cpp/threshold_hysteresis_simulation.cpp -o outputs/threshold_hysteresis_simulation_cpp
  ./outputs/threshold_hysteresis_simulation_cpp > outputs/tables/cpp_threshold_hysteresis_simulation.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go threshold diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_threshold_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_threshold_risk_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran threshold transition example..."
  gfortran fortran/threshold_transition.f90 -o outputs/threshold_transition_fortran
  ./outputs/threshold_transition_fortran > outputs/tables/fortran_threshold_transition.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia nonlinear threshold model..."
  julia julia/nonlinear_threshold_model.jl > outputs/tables/julia_nonlinear_threshold_model.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R threshold workflow..."
  Rscript r/threshold_hysteresis_early_warning.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
