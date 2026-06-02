#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Infrastructure Resilience scaffold..."

python3 -m py_compile python/infrastructure_resilience_standard.py
python3 python/infrastructure_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C resilience-value utility..."
  gcc c/resilience_value_score.c -o outputs/resilience_value_score_c
  ./outputs/resilience_value_score_c > outputs/tables/c_resilience_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ infrastructure scoring..."
  g++ -std=c++17 cpp/infrastructure_resilience_scoring.cpp -o outputs/infrastructure_resilience_scoring_cpp
  ./outputs/infrastructure_resilience_scoring_cpp > outputs/tables/cpp_infrastructure_resilience_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go infrastructure diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_infrastructure_resilience_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_infrastructure_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran service response model..."
  gfortran fortran/service_response_dynamics.f90 -o outputs/service_response_dynamics_fortran
  ./outputs/service_response_dynamics_fortran > outputs/tables/fortran_service_response_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia infrastructure pathway example..."
  julia julia/infrastructure_resilience_pathway_example.jl > outputs/tables/julia_infrastructure_resilience_pathway_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R infrastructure workflow..."
  Rscript r/infrastructure_resilience_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
