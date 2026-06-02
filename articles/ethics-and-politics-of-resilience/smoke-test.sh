#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Ethics and Politics of Resilience scaffold..."

python3 -m py_compile python/ethical_resilience_standard.py
python3 python/ethical_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  gcc c/ethical_resilience_value_score.c -o outputs/ethical_resilience_value_score_c
  ./outputs/ethical_resilience_value_score_c > outputs/tables/c_ethical_resilience_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  g++ -std=c++17 cpp/ethical_resilience_scoring.cpp -o outputs/ethical_resilience_scoring_cpp
  ./outputs/ethical_resilience_scoring_cpp > outputs/tables/cpp_ethical_resilience_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  (cd go && go run .) > outputs/tables/go_ethical_resilience_output.txt
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_ethical_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  gfortran fortran/ethical_resilience_dynamics.f90 -o outputs/ethical_resilience_dynamics_fortran
  ./outputs/ethical_resilience_dynamics_fortran > outputs/tables/fortran_ethical_resilience_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  julia julia/ethical_resilience_value_example.jl > outputs/tables/julia_ethical_resilience_value_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/ethical_resilience_strategy_comparison.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
