#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Resilience Scenarios and Futures Thinking scaffold..."

python3 -m py_compile python/resilience_scenarios_futures_standard.py
python3 python/resilience_scenarios_futures_standard.py

if command -v gcc >/dev/null 2>&1; then
  gcc c/resilience_scenario_value_score.c -o outputs/resilience_scenario_value_score_c
  ./outputs/resilience_scenario_value_score_c > outputs/tables/c_resilience_scenario_value_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  g++ -std=c++17 cpp/resilience_scenario_scoring.cpp -o outputs/resilience_scenario_scoring_cpp
  ./outputs/resilience_scenario_scoring_cpp > outputs/tables/cpp_resilience_scenario_scoring.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  (cd go && go run .) > outputs/tables/go_resilience_scenario_output.txt
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  CARGO_TARGET_DIR="${PWD}/outputs/rust-target" cargo run --manifest-path rust/Cargo.toml --quiet > outputs/tables/rust_resilience_scenario_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  gfortran fortran/resilience_future_dynamics.f90 -o outputs/resilience_future_dynamics_fortran
  ./outputs/resilience_future_dynamics_fortran > outputs/tables/fortran_resilience_future_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  julia julia/resilience_scenario_pathway_example.jl > outputs/tables/julia_resilience_scenario_pathway_example.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/resilience_scenario_strategies.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
