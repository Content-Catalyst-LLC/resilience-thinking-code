#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Intelligent Infrastructure and Resilience scaffold..."

python3 -m py_compile python/intelligent_infrastructure_resilience_standard.py
python3 python/intelligent_infrastructure_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C intelligent infrastructure value utility..."
  gcc c/intelligent_infrastructure_value_score.c -o outputs/intelligent_infrastructure_value_score_c
  ./outputs/intelligent_infrastructure_value_score_c > outputs/tables/c_intelligent_infrastructure_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ intelligent infrastructure scoring..."
  g++ -std=c++17 cpp/intelligent_infrastructure_scoring.cpp -o outputs/intelligent_infrastructure_scoring_cpp
  ./outputs/intelligent_infrastructure_scoring_cpp > outputs/tables/cpp_intelligent_infrastructure_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go intelligent infrastructure diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_intelligent_infrastructure_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_intelligent_infrastructure_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran intelligent infrastructure dynamics model..."
  gfortran fortran/intelligent_infrastructure_dynamics.f90 -o outputs/intelligent_infrastructure_dynamics_fortran
  ./outputs/intelligent_infrastructure_dynamics_fortran > outputs/tables/fortran_intelligent_infrastructure_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia intelligent infrastructure pathway example..."
  julia julia/intelligent_infrastructure_pathway_example.jl > outputs/tables/julia_intelligent_infrastructure_pathway_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R intelligent infrastructure workflow..."
  Rscript r/intelligent_infrastructure_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
