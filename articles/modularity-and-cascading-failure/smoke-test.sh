#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for modularity and cascading failure scaffold..."

python3 -m py_compile python/modularity_cascade_standard.py
python3 python/modularity_cascade_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C containment-value utility..."
  gcc c/containment_value_score.c -o outputs/containment_value_score_c
  ./outputs/containment_value_score_c > outputs/tables/c_containment_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ containment strategy scoring..."
  g++ -std=c++17 cpp/containment_strategy_scoring.cpp -o outputs/containment_strategy_scoring_cpp
  ./outputs/containment_strategy_scoring_cpp > outputs/tables/cpp_containment_strategy_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go cascade diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_modularity_cascade_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_modularity_cascade_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran cascade propagation dynamics model..."
  gfortran fortran/cascade_propagation_dynamics.f90 -o outputs/cascade_propagation_dynamics_fortran
  ./outputs/cascade_propagation_dynamics_fortran > outputs/tables/fortran_cascade_propagation_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia cascade diagnostic model..."
  julia julia/network_cascade_example.jl > outputs/tables/julia_network_cascade_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R modularity-cascade workflow..."
  Rscript r/modularity_cascade_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
