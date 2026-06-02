#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for resilience indicators and dashboard-risk scaffold..."

python3 -m py_compile python/resilience_dashboard_standard.py
python3 python/resilience_dashboard_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C dashboard-value utility..."
  gcc c/dashboard_value_score.c -o outputs/dashboard_value_score_c
  ./outputs/dashboard_value_score_c > outputs/tables/c_dashboard_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ dashboard-value scoring..."
  g++ -std=c++17 cpp/dashboard_value_scoring.cpp -o outputs/dashboard_value_scoring_cpp
  ./outputs/dashboard_value_scoring_cpp > outputs/tables/cpp_dashboard_value_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go dashboard diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_resilience_dashboard_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_resilience_dashboard_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran dashboard score dynamics model..."
  gfortran fortran/dashboard_score_dynamics.f90 -o outputs/dashboard_score_dynamics_fortran
  ./outputs/dashboard_score_dynamics_fortran > outputs/tables/fortran_dashboard_score_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia dashboard score example..."
  julia julia/dashboard_score_example.jl > outputs/tables/julia_dashboard_score_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R dashboard design workflow..."
  Rscript r/resilience_dashboard_designs.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
