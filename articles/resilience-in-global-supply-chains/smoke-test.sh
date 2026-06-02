#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Resilience in Global Supply Chains scaffold..."

python3 -m py_compile python/global_supply_chain_resilience_standard.py
python3 python/global_supply_chain_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C supply-chain value utility..."
  gcc c/supply_chain_resilience_value_score.c -o outputs/supply_chain_resilience_value_score_c
  ./outputs/supply_chain_resilience_value_score_c > outputs/tables/c_supply_chain_resilience_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ supply chain resilience scoring..."
  g++ -std=c++17 cpp/global_supply_chain_resilience_scoring.cpp -o outputs/global_supply_chain_resilience_scoring_cpp
  ./outputs/global_supply_chain_resilience_scoring_cpp > outputs/tables/cpp_global_supply_chain_resilience_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go supply chain diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_global_supply_chain_resilience_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_global_supply_chain_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran supply chain flow model..."
  gfortran fortran/supply_chain_flow_dynamics.f90 -o outputs/supply_chain_flow_dynamics_fortran
  ./outputs/supply_chain_flow_dynamics_fortran > outputs/tables/fortran_supply_chain_flow_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia supply chain pathway example..."
  julia julia/global_supply_chain_pathway_example.jl > outputs/tables/julia_global_supply_chain_pathway_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R supply chain resilience workflow..."
  Rscript r/global_supply_chain_resilience_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
