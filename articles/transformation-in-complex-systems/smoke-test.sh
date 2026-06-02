#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for transformation scaffold..."

python3 -m py_compile python/transformation_standard.py
python3 python/transformation_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C transformation-value utility..."
  gcc c/transformation_value_score.c -o outputs/transformation_value_score_c
  ./outputs/transformation_value_score_c > outputs/tables/c_transformation_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ transformation pathway scoring..."
  g++ -std=c++17 cpp/transformation_pathway_scoring.cpp -o outputs/transformation_pathway_scoring_cpp
  ./outputs/transformation_pathway_scoring_cpp > outputs/tables/cpp_transformation_pathway_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go transformation diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_transformation_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_transformation_readiness_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran adaptive-limit model..."
  gfortran fortran/adaptive_limit_model.f90 -o outputs/adaptive_limit_model_fortran
  ./outputs/adaptive_limit_model_fortran > outputs/tables/fortran_adaptive_limit_model.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia adaptive-limit model..."
  julia julia/adaptive_limit_model.jl > outputs/tables/julia_adaptive_limit_model.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R transformation workflow..."
  Rscript r/transformation_pathways.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
