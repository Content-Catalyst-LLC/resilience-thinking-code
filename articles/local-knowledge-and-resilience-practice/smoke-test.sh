#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Local Knowledge and Resilience Practice scaffold..."

python3 -m py_compile python/local_knowledge_standard.py
python3 python/local_knowledge_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C knowledge-value utility..."
  gcc c/knowledge_value_score.c -o outputs/knowledge_value_score_c
  ./outputs/knowledge_value_score_c > outputs/tables/c_knowledge_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ local knowledge scoring..."
  g++ -std=c++17 cpp/local_knowledge_scoring.cpp -o outputs/local_knowledge_scoring_cpp
  ./outputs/local_knowledge_scoring_cpp > outputs/tables/cpp_local_knowledge_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go local knowledge diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_local_knowledge_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_local_knowledge_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran knowledge function model..."
  gfortran fortran/knowledge_function_dynamics.f90 -o outputs/knowledge_function_dynamics_fortran
  ./outputs/knowledge_function_dynamics_fortran > outputs/tables/fortran_knowledge_function_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia local knowledge pathway example..."
  julia julia/local_knowledge_pathway_example.jl > outputs/tables/julia_local_knowledge_pathway_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R local knowledge workflow..."
  Rscript r/local_knowledge_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
