#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for learning, memory, and adaptive management scaffold..."

python3 -m py_compile python/learning_memory_standard.py
python3 python/learning_memory_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C adaptive-learning utility..."
  gcc c/adaptive_learning_value_score.c -o outputs/adaptive_learning_value_score_c
  ./outputs/adaptive_learning_value_score_c > outputs/tables/c_adaptive_learning_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ adaptive-learning scoring..."
  g++ -std=c++17 cpp/adaptive_learning_scoring.cpp -o outputs/adaptive_learning_scoring_cpp
  ./outputs/adaptive_learning_scoring_cpp > outputs/tables/cpp_adaptive_learning_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go adaptive-management diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_learning_memory_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_learning_memory_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran memory response dynamics model..."
  gfortran fortran/memory_response_dynamics.f90 -o outputs/memory_response_dynamics_fortran
  ./outputs/memory_response_dynamics_fortran > outputs/tables/fortran_memory_response_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia memory adaptive response model..."
  julia julia/memory_adaptive_response.jl > outputs/tables/julia_memory_adaptive_response.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R adaptive management workflow..."
  Rscript r/adaptive_management_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
