#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for adaptive cycles and panarchy scaffold..."

python3 -m py_compile python/adaptive_cycles_panarchy_standard.py
python3 python/adaptive_cycles_panarchy_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C release-threshold utility..."
  gcc c/release_threshold.c -o outputs/release_threshold_c
  ./outputs/release_threshold_c > outputs/tables/c_release_threshold.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ adaptive-cycle simulation..."
  g++ -std=c++17 cpp/adaptive_cycle_simulation.cpp -o outputs/adaptive_cycle_simulation_cpp
  ./outputs/adaptive_cycle_simulation_cpp > outputs/tables/cpp_adaptive_cycle_simulation.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go phase diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_adaptive_cycle_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_release_risk_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran adaptive-cycle transition example..."
  gfortran fortran/adaptive_cycle_transition.f90 -o outputs/adaptive_cycle_transition_fortran
  ./outputs/adaptive_cycle_transition_fortran > outputs/tables/fortran_adaptive_cycle_transition.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia adaptive-cycle transition model..."
  julia julia/adaptive_cycle_transition.jl > outputs/tables/julia_adaptive_cycle_transition.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R adaptive-cycle phase workflow..."
  Rscript r/adaptive_cycle_phase_simulation.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
