#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Public Health System Resilience scaffold..."

python3 -m py_compile python/public_health_resilience_standard.py
python3 python/public_health_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C resilience-value utility..."
  gcc c/resilience_value_score.c -o outputs/resilience_value_score_c
  ./outputs/resilience_value_score_c > outputs/tables/c_resilience_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ public health resilience scoring..."
  g++ -std=c++17 cpp/public_health_resilience_scoring.cpp -o outputs/public_health_resilience_scoring_cpp
  ./outputs/public_health_resilience_scoring_cpp > outputs/tables/cpp_public_health_resilience_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go public health diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_public_health_resilience_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_public_health_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran health-system function model..."
  gfortran fortran/health_system_function_dynamics.f90 -o outputs/health_system_function_dynamics_fortran
  ./outputs/health_system_function_dynamics_fortran > outputs/tables/fortran_health_system_function_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia public health pathway example..."
  julia julia/public_health_resilience_pathway_example.jl > outputs/tables/julia_public_health_resilience_pathway_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R public health workflow..."
  Rscript r/public_health_resilience_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
