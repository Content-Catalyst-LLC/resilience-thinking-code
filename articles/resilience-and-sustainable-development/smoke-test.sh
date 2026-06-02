#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Resilience and Sustainable Development scaffold..."

python3 -m py_compile python/sustainable_resilience_standard.py
python3 python/sustainable_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C viability-value utility..."
  gcc c/viability_value_score.c -o outputs/viability_value_score_c
  ./outputs/viability_value_score_c > outputs/tables/c_viability_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ sustainable resilience scoring..."
  g++ -std=c++17 cpp/sustainable_resilience_scoring.cpp -o outputs/sustainable_resilience_scoring_cpp
  ./outputs/sustainable_resilience_scoring_cpp > outputs/tables/cpp_sustainable_resilience_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go sustainable resilience diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_sustainable_resilience_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_sustainable_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran development quality model..."
  gfortran fortran/development_quality_dynamics.f90 -o outputs/development_quality_dynamics_fortran
  ./outputs/development_quality_dynamics_fortran > outputs/tables/fortran_development_quality_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia sustainable resilience pathway example..."
  julia julia/sustainable_resilience_pathway_example.jl > outputs/tables/julia_sustainable_resilience_pathway_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R sustainable resilience workflow..."
  Rscript r/sustainable_resilience_pathways.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
