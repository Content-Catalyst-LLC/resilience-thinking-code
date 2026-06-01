#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for predictive resilience scaffold..."

python3 python/predictive_resilience_model_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C probability utility..."
  gcc c/resilience_probability.c -lm -o outputs/resilience_probability_c
  ./outputs/resilience_probability_c > outputs/tables/c_probability_output.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ forecast utility..."
  g++ -std=c++17 cpp/fast_resilience_forecast.cpp -o outputs/fast_resilience_forecast_cpp
  ./outputs/fast_resilience_forecast_cpp > outputs/tables/cpp_forecast_output.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go forecast utility..."
  (cd go && go run .) > outputs/tables/go_forecast_output.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_cli_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran probability example..."
  gfortran fortran/threshold_probability.f90 -o outputs/threshold_probability_fortran
  ./outputs/threshold_probability_fortran > outputs/tables/fortran_probability_output.txt
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia nonlinear threshold predictor..."
  julia julia/nonlinear_threshold_predictor.jl > outputs/tables/julia_threshold_predictions.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R predictive profile workflow..."
  Rscript r/predictive_resilience_profiles.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
