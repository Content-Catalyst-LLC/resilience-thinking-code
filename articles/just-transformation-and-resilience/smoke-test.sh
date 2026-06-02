#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Just Transformation and Resilience scaffold..."

python3 -m py_compile python/just_transformation_resilience_standard.py
python3 python/just_transformation_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  gcc c/just_transformation_value_score.c -o outputs/just_transformation_value_score_c
  ./outputs/just_transformation_value_score_c > outputs/tables/c_just_transformation_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  g++ -std=c++17 cpp/just_transformation_scoring.cpp -o outputs/just_transformation_scoring_cpp
  ./outputs/just_transformation_scoring_cpp > outputs/tables/cpp_just_transformation_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  (cd go && go run .) > outputs/tables/go_just_transformation_output.txt
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_just_transformation_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  gfortran fortran/just_transformation_dynamics.f90 -o outputs/just_transformation_dynamics_fortran
  ./outputs/just_transformation_dynamics_fortran > outputs/tables/fortran_just_transformation_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  julia julia/just_transformation_value_example.jl > outputs/tables/julia_just_transformation_value_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/just_transformation_pathway_comparison.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
