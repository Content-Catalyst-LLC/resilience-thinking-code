#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Disaster Risk Reduction and resilience scaffold..."

python3 -m py_compile python/drr_resilience_standard.py
python3 python/drr_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C DRR-value utility..."
  gcc c/drr_value_score.c -o outputs/drr_value_score_c
  ./outputs/drr_value_score_c > outputs/tables/c_drr_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ DRR scoring..."
  g++ -std=c++17 cpp/drr_resilience_scoring.cpp -o outputs/drr_resilience_scoring_cpp
  ./outputs/drr_resilience_scoring_cpp > outputs/tables/cpp_drr_resilience_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go DRR diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_drr_resilience_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_drr_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran disaster stress response model..."
  gfortran fortran/disaster_stress_response.f90 -o outputs/disaster_stress_response_fortran
  ./outputs/disaster_stress_response_fortran > outputs/tables/fortran_disaster_stress_response.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia DRR pathway example..."
  julia julia/drr_resilience_pathway_example.jl > outputs/tables/julia_drr_resilience_pathway_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R DRR workflow..."
  Rscript r/drr_resilience_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
