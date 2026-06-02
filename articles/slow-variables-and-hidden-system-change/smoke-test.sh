#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for slow variables scaffold..."

python3 -m py_compile python/slow_variables_standard.py
python3 python/slow_variables_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C hidden-risk score utility..."
  gcc c/hidden_risk_score.c -o outputs/hidden_risk_score_c
  ./outputs/hidden_risk_score_c > outputs/tables/c_hidden_risk_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ slow-variable simulation..."
  g++ -std=c++17 cpp/slow_variable_simulation.cpp -o outputs/slow_variable_simulation_cpp
  ./outputs/slow_variable_simulation_cpp > outputs/tables/cpp_slow_variable_simulation.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go hidden-risk diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_hidden_risk_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_hidden_risk_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran slow-variable simulation..."
  gfortran fortran/slow_variable_simulation.f90 -o outputs/slow_variable_simulation_fortran
  ./outputs/slow_variable_simulation_fortran > outputs/tables/fortran_slow_variable_simulation.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia slow-variable threshold-distance model..."
  julia julia/slow_variable_threshold_distance.jl > outputs/tables/julia_slow_variable_threshold_distance.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R slow-variable workflow..."
  Rscript r/slow_variables_hidden_change.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
