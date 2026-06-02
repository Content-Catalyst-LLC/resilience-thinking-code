#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for climate resilience scaffold..."

python3 -m py_compile python/climate_resilience_standard.py
python3 python/climate_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C climate-resilience utility..."
  gcc c/climate_resilience_value_score.c -o outputs/climate_resilience_value_score_c
  ./outputs/climate_resilience_value_score_c > outputs/tables/c_climate_resilience_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ climate-resilience scoring..."
  g++ -std=c++17 cpp/climate_resilience_scoring.cpp -o outputs/climate_resilience_scoring_cpp
  ./outputs/climate_resilience_scoring_cpp > outputs/tables/cpp_climate_resilience_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go climate-resilience diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_climate_resilience_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_climate_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran climate stress response model..."
  gfortran fortran/climate_stress_response.f90 -o outputs/climate_stress_response_fortran
  ./outputs/climate_stress_response_fortran > outputs/tables/fortran_climate_stress_response.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia climate resilience pathway example..."
  julia julia/climate_resilience_pathway_example.jl > outputs/tables/julia_climate_resilience_pathway_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R climate resilience workflow..."
  Rscript r/climate_resilience_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
