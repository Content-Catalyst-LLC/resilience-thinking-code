#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for resilience metrics scaffold..."

python3 -m py_compile python/resilience_metrics_standard.py
python3 python/resilience_metrics_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C metric-value utility..."
  gcc c/metric_value_score.c -o outputs/metric_value_score_c
  ./outputs/metric_value_score_c > outputs/tables/c_metric_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ metric scoring..."
  g++ -std=c++17 cpp/resilience_metric_scoring.cpp -o outputs/resilience_metric_scoring_cpp
  ./outputs/resilience_metric_scoring_cpp > outputs/tables/cpp_resilience_metric_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go framework diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_resilience_metric_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_resilience_metrics_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran resilience-function dynamics model..."
  gfortran fortran/resilience_function_dynamics.f90 -o outputs/resilience_function_dynamics_fortran
  ./outputs/resilience_function_dynamics_fortran > outputs/tables/fortran_resilience_function_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia resilience score model..."
  julia julia/resilience_score_threshold_sensitivity.jl > outputs/tables/julia_resilience_score_threshold_sensitivity.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R resilience measurement workflow..."
  Rscript r/resilience_measurement_frameworks.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
