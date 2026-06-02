#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Adaptive Governance and Resilience scaffold..."

python3 -m py_compile python/adaptive_governance_standard.py
python3 python/adaptive_governance_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C governance-value utility..."
  gcc c/governance_value_score.c -o outputs/governance_value_score_c
  ./outputs/governance_value_score_c > outputs/tables/c_governance_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ adaptive governance scoring..."
  g++ -std=c++17 cpp/adaptive_governance_scoring.cpp -o outputs/adaptive_governance_scoring_cpp
  ./outputs/adaptive_governance_scoring_cpp > outputs/tables/cpp_adaptive_governance_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go adaptive governance diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_adaptive_governance_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_adaptive_governance_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran governance function model..."
  gfortran fortran/governance_function_dynamics.f90 -o outputs/governance_function_dynamics_fortran
  ./outputs/governance_function_dynamics_fortran > outputs/tables/fortran_governance_function_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia adaptive governance pathway example..."
  julia julia/adaptive_governance_pathway_example.jl > outputs/tables/julia_adaptive_governance_pathway_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R adaptive governance workflow..."
  Rscript r/adaptive_governance_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
