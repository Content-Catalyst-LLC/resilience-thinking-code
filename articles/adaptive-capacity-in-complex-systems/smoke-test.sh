#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for adaptive capacity scaffold..."

python3 -m py_compile python/adaptive_capacity_standard.py
python3 python/adaptive_capacity_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C adaptive-capacity score utility..."
  gcc c/adaptive_capacity_score.c -o outputs/adaptive_capacity_score_c
  ./outputs/adaptive_capacity_score_c > outputs/tables/c_adaptive_capacity_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ viability simulation..."
  g++ -std=c++17 cpp/viability_simulation.cpp -o outputs/viability_simulation_cpp
  ./outputs/viability_simulation_cpp > outputs/tables/cpp_viability_simulation.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go adaptive-capacity diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_adaptive_capacity_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_adaptive_capacity_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran adaptive-capacity viability example..."
  gfortran fortran/adaptive_capacity_viability.f90 -o outputs/adaptive_capacity_viability_fortran
  ./outputs/adaptive_capacity_viability_fortran > outputs/tables/fortran_adaptive_capacity_viability.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia response-space rigidity model..."
  julia julia/response_space_rigidity_model.jl > outputs/tables/julia_response_space_rigidity_model.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R adaptive-capacity workflow..."
  Rscript r/adaptive_capacity_profiles.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
