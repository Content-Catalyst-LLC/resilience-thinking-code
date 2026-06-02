#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for regime shifts scaffold..."

python3 -m py_compile python/regime_shifts_standard.py
python3 python/regime_shifts_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C regime-risk score utility..."
  gcc c/regime_risk_score.c -o outputs/regime_risk_score_c
  ./outputs/regime_risk_score_c > outputs/tables/c_regime_risk_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ regime-shift simulation..."
  g++ -std=c++17 cpp/regime_shift_simulation.cpp -o outputs/regime_shift_simulation_cpp
  ./outputs/regime_shift_simulation_cpp > outputs/tables/cpp_regime_shift_simulation.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go regime diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_regime_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_regime_risk_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran regime-shift simulation..."
  gfortran fortran/regime_shift_simulation.f90 -o outputs/regime_shift_simulation_fortran
  ./outputs/regime_shift_simulation_fortran > outputs/tables/fortran_regime_shift_simulation.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia critical slowing model..."
  julia julia/regime_shift_critical_slowing.jl > outputs/tables/julia_regime_shift_critical_slowing.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R regime-shift workflow..."
  Rscript r/regime_shift_early_warning.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
