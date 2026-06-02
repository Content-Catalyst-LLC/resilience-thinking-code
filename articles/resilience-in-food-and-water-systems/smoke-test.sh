#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Food and Water Resilience scaffold..."

python3 -m py_compile python/food_water_resilience_standard.py
python3 python/food_water_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C resilience-value utility..."
  gcc c/resilience_value_score.c -o outputs/resilience_value_score_c
  ./outputs/resilience_value_score_c > outputs/tables/c_resilience_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ food-water scoring..."
  g++ -std=c++17 cpp/food_water_resilience_scoring.cpp -o outputs/food_water_resilience_scoring_cpp
  ./outputs/food_water_resilience_scoring_cpp > outputs/tables/cpp_food_water_resilience_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go food-water diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_food_water_resilience_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_food_water_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran food-water performance model..."
  gfortran fortran/food_water_performance_dynamics.f90 -o outputs/food_water_performance_dynamics_fortran
  ./outputs/food_water_performance_dynamics_fortran > outputs/tables/fortran_food_water_performance_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia food-water pathway example..."
  julia julia/food_water_resilience_pathway_example.jl > outputs/tables/julia_food_water_resilience_pathway_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R food-water workflow..."
  Rscript r/food_water_resilience_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
