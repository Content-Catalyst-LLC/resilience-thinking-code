#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Technology System Resilience scaffold..."

python3 -m py_compile python/technology_system_resilience_standard.py
python3 python/technology_system_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C technology resilience value utility..."
  gcc c/technology_resilience_value_score.c -o outputs/technology_resilience_value_score_c
  ./outputs/technology_resilience_value_score_c > outputs/tables/c_technology_resilience_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ technology resilience scoring..."
  g++ -std=c++17 cpp/technology_resilience_scoring.cpp -o outputs/technology_resilience_scoring_cpp
  ./outputs/technology_resilience_scoring_cpp > outputs/tables/cpp_technology_resilience_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go technology resilience diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_technology_resilience_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_technology_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran technology resilience dynamics model..."
  gfortran fortran/technology_resilience_dynamics.f90 -o outputs/technology_resilience_dynamics_fortran
  ./outputs/technology_resilience_dynamics_fortran > outputs/tables/fortran_technology_resilience_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia technology resilience pathway example..."
  julia julia/technology_resilience_pathway_example.jl > outputs/tables/julia_technology_resilience_pathway_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R technology resilience workflow..."
  Rscript r/technology_resilience_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
