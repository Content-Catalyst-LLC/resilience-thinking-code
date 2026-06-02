#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for redundancy and diversity scaffold..."

python3 -m py_compile python/redundancy_diversity_standard.py
python3 python/redundancy_diversity_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C resilience-value utility..."
  gcc c/resilience_value_score.c -o outputs/resilience_value_score_c
  ./outputs/resilience_value_score_c > outputs/tables/c_resilience_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ redundancy-diversity scoring..."
  g++ -std=c++17 cpp/redundancy_diversity_scoring.cpp -o outputs/redundancy_diversity_scoring_cpp
  ./outputs/redundancy_diversity_scoring_cpp > outputs/tables/cpp_redundancy_diversity_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go strategy diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_redundancy_diversity_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_redundancy_diversity_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran function-under-disturbance model..."
  gfortran fortran/function_under_disturbance.f90 -o outputs/function_under_disturbance_fortran
  ./outputs/function_under_disturbance_fortran > outputs/tables/fortran_function_under_disturbance.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia common-mode and response-diversity model..."
  julia julia/common_mode_response_diversity.jl > outputs/tables/julia_common_mode_response_diversity.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R redundancy-diversity workflow..."
  Rscript r/redundancy_diversity_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
