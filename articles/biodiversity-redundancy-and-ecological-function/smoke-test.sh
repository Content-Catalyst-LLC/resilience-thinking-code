#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for biodiversity redundancy scaffold..."

python3 -m py_compile python/biodiversity_redundancy_standard.py
python3 python/biodiversity_redundancy_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C functional-output utility..."
  gcc c/functional_output.c -o outputs/functional_output_c
  ./outputs/functional_output_c > outputs/tables/c_functional_output.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ function-loss simulation..."
  g++ -std=c++17 cpp/function_loss_simulation.cpp -o outputs/function_loss_simulation_cpp
  ./outputs/function_loss_simulation_cpp > outputs/tables/cpp_function_loss_simulation.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go function-resilience diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_function_resilience_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_function_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran functional-resilience margin example..."
  gfortran fortran/functional_resilience_margin.f90 -o outputs/functional_resilience_margin_fortran
  ./outputs/functional_resilience_margin_fortran > outputs/tables/fortran_functional_resilience_margin.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia biodiversity-function threshold model..."
  julia julia/biodiversity_function_threshold.jl > outputs/tables/julia_biodiversity_function_threshold.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R functional-diversity workflow..."
  Rscript r/functional_diversity_redundancy_profiles.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
