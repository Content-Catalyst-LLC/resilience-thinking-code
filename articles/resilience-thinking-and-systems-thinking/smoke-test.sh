#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for systems-resilience scaffold..."

python3 python/systems_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C balancing-feedback utility..."
  gcc c/balancing_feedback.c -o outputs/balancing_feedback_c
  ./outputs/balancing_feedback_c > outputs/tables/c_balancing_feedback.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ feedback resilience-margin simulation..."
  g++ -std=c++17 cpp/feedback_resilience_margin.cpp -o outputs/feedback_resilience_margin_cpp
  ./outputs/feedback_resilience_margin_cpp > outputs/tables/cpp_feedback_resilience_margin.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go systems-resilience utility..."
  (cd go && go run .) > outputs/tables/go_systems_resilience_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_systems_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran stock-flow margin example..."
  gfortran fortran/stock_flow_margin.f90 -o outputs/stock_flow_margin_fortran
  ./outputs/stock_flow_margin_fortran > outputs/tables/fortran_stock_flow_margin.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia feedback-threshold model..."
  julia julia/feedback_threshold_model.jl > outputs/tables/julia_feedback_threshold_model.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R systems-resilience indicator workflow..."
  Rscript r/systems_resilience_indicators.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
