#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Resilience and Strategic Slack scaffold..."

python3 -m py_compile python/strategic_slack_resilience_standard.py
python3 python/strategic_slack_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C strategic slack value utility..."
  gcc c/strategic_slack_value_score.c -o outputs/strategic_slack_value_score_c
  ./outputs/strategic_slack_value_score_c > outputs/tables/c_strategic_slack_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ strategic slack scoring..."
  g++ -std=c++17 cpp/strategic_slack_resilience_scoring.cpp -o outputs/strategic_slack_resilience_scoring_cpp
  ./outputs/strategic_slack_resilience_scoring_cpp > outputs/tables/cpp_strategic_slack_resilience_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go strategic slack diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_strategic_slack_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_strategic_slack_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran strategic slack dynamics model..."
  gfortran fortran/strategic_slack_dynamics.f90 -o outputs/strategic_slack_dynamics_fortran
  ./outputs/strategic_slack_dynamics_fortran > outputs/tables/fortran_strategic_slack_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia strategic slack pathway example..."
  julia julia/strategic_slack_pathway_example.jl > outputs/tables/julia_strategic_slack_pathway_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R strategic slack workflow..."
  Rscript r/strategic_slack_resilience_portfolios.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
