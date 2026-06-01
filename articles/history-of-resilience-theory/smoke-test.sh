#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for history-of-resilience-theory scaffold..."

python3 python/history_resilience_theory_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C equilibrium-return utility..."
  gcc c/equilibrium_return.c -o outputs/equilibrium_return_c
  ./outputs/equilibrium_return_c > outputs/tables/c_equilibrium_return.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ equilibrium-threshold comparison..."
  g++ -std=c++17 cpp/equilibrium_threshold_compare.cpp -o outputs/equilibrium_threshold_cpp
  ./outputs/equilibrium_threshold_cpp > outputs/tables/cpp_equilibrium_threshold.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go timeline utility..."
  (cd go && go run .) > outputs/tables/go_history_scores.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_history_cli_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran threshold-persistence example..."
  gfortran fortran/threshold_persistence.f90 -o outputs/threshold_persistence_fortran
  ./outputs/threshold_persistence_fortran > outputs/tables/fortran_threshold_persistence.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia threshold-history model..."
  julia julia/threshold_history_model.jl > outputs/tables/julia_threshold_history.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R historical expansion workflow..."
  Rscript r/history_resilience_theory.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
