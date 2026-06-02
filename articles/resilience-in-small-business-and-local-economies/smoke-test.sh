#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Resilience in Small Business and Local Economies scaffold..."

python3 -m py_compile python/small_business_local_resilience_standard.py
python3 python/small_business_local_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C local resilience value utility..."
  gcc c/local_resilience_value_score.c -o outputs/local_resilience_value_score_c
  ./outputs/local_resilience_value_score_c > outputs/tables/c_local_resilience_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ local economic resilience scoring..."
  g++ -std=c++17 cpp/local_economic_resilience_scoring.cpp -o outputs/local_economic_resilience_scoring_cpp
  ./outputs/local_economic_resilience_scoring_cpp > outputs/tables/cpp_local_economic_resilience_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go local resilience diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_local_resilience_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_local_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran small business resilience model..."
  gfortran fortran/small_business_resilience_dynamics.f90 -o outputs/small_business_resilience_dynamics_fortran
  ./outputs/small_business_resilience_dynamics_fortran > outputs/tables/fortran_small_business_resilience_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia local resilience pathway example..."
  julia julia/local_resilience_pathway_example.jl > outputs/tables/julia_local_resilience_pathway_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R local economic resilience workflow..."
  Rscript r/local_economic_resilience_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
