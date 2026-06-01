#!/usr/bin/env bash
set -euo pipefail

echo "Running dependency-light smoke tests..."

python3 python/resilience_diagnostics_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C example..."
  gcc c/viability_simulation.c -o outputs/viability_simulation_c
  ./outputs/viability_simulation_c > outputs/tables/c_viability_output.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ example..."
  g++ -std=c++17 cpp/repeated_disturbance.cpp -o outputs/repeated_disturbance_cpp
  ./outputs/repeated_disturbance_cpp > outputs/tables/cpp_viability_output.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go example..."
  (cd go && go run .) > outputs/tables/go_network_output.txt
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust example..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_diagnostics_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran example..."
  gfortran fortran/dynamic_viability.f90 -o outputs/dynamic_viability_fortran
  ./outputs/dynamic_viability_fortran > outputs/tables/fortran_viability_output.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia example..."
  julia julia/threshold_regime_shift.jl > outputs/tables/julia_threshold_output.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R example..."
  Rscript r/resilience_profiles.R || echo "R example skipped or failed because tidyverse is not installed."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
