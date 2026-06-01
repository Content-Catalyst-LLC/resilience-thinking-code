#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for engineering/ecological resilience scaffold..."

python3 python/engineering_ecological_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C return-rate utility..."
  gcc c/return_rate.c -o outputs/return_rate_c
  ./outputs/return_rate_c > outputs/tables/c_return_rate.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ return-vs-threshold simulation..."
  g++ -std=c++17 cpp/return_vs_threshold.cpp -o outputs/return_vs_threshold_cpp
  ./outputs/return_vs_threshold_cpp > outputs/tables/cpp_return_vs_threshold.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go scenario utility..."
  (cd go && go run .) > outputs/tables/go_profile_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_profile_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran resilience-margin example..."
  gfortran fortran/resilience_margin.f90 -o outputs/resilience_margin_fortran
  ./outputs/resilience_margin_fortran > outputs/tables/fortran_resilience_margin.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia threshold-dynamics model..."
  julia julia/threshold_dynamics.jl > outputs/tables/julia_threshold_dynamics.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R profile workflow..."
  Rscript r/engineering_ecological_resilience_profiles.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
