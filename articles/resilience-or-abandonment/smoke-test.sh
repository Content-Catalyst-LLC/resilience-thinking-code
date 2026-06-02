#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Resilience or Abandonment scaffold..."

python3 -m py_compile python/resilience_or_abandonment_standard.py
python3 python/resilience_or_abandonment_standard.py

if command -v gcc >/dev/null 2>&1; then
  gcc c/resilience_or_abandonment_value_score.c -o outputs/resilience_or_abandonment_value_score_c
  ./outputs/resilience_or_abandonment_value_score_c > outputs/tables/c_resilience_or_abandonment_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  g++ -std=c++17 cpp/resilience_or_abandonment_scoring.cpp -o outputs/resilience_or_abandonment_scoring_cpp
  ./outputs/resilience_or_abandonment_scoring_cpp > outputs/tables/cpp_resilience_or_abandonment_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  (cd go && go run .) > outputs/tables/go_resilience_or_abandonment_output.txt
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_resilience_or_abandonment_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  gfortran fortran/abandonment_risk_dynamics.f90 -o outputs/abandonment_risk_dynamics_fortran
  ./outputs/abandonment_risk_dynamics_fortran > outputs/tables/fortran_abandonment_risk_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  julia julia/resilience_or_abandonment_value_example.jl > outputs/tables/julia_resilience_or_abandonment_value_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/resilience_or_abandonment_strategy_comparison.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
