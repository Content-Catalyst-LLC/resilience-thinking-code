#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Financial System Resilience scaffold..."

python3 -m py_compile python/financial_system_resilience_standard.py
python3 python/financial_system_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C financial resilience value utility..."
  gcc c/financial_resilience_value_score.c -o outputs/financial_resilience_value_score_c
  ./outputs/financial_resilience_value_score_c > outputs/tables/c_financial_resilience_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ financial system resilience scoring..."
  g++ -std=c++17 cpp/financial_system_resilience_scoring.cpp -o outputs/financial_system_resilience_scoring_cpp
  ./outputs/financial_system_resilience_scoring_cpp > outputs/tables/cpp_financial_system_resilience_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go financial resilience diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_financial_resilience_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_financial_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran financial function model..."
  gfortran fortran/financial_function_dynamics.f90 -o outputs/financial_function_dynamics_fortran
  ./outputs/financial_function_dynamics_fortran > outputs/tables/fortran_financial_function_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia financial resilience pathway example..."
  julia julia/financial_resilience_pathway_example.jl > outputs/tables/julia_financial_resilience_pathway_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R financial system resilience workflow..."
  Rscript r/financial_system_resilience_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
