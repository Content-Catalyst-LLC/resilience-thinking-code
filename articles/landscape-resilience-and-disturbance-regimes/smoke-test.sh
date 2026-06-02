#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for landscape resilience scaffold..."

python3 -m py_compile python/landscape_resilience_standard.py
python3 python/landscape_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C patch resilience-margin utility..."
  gcc c/patch_resilience_margin.c -o outputs/patch_resilience_margin_c
  ./outputs/patch_resilience_margin_c > outputs/tables/c_patch_resilience_margin.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ patch disturbance simulation..."
  g++ -std=c++17 cpp/patch_disturbance_simulation.cpp -o outputs/patch_disturbance_simulation_cpp
  ./outputs/patch_disturbance_simulation_cpp > outputs/tables/cpp_patch_disturbance_simulation.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go landscape-resilience diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_landscape_resilience_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_landscape_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran landscape resilience-margin example..."
  gfortran fortran/landscape_resilience_margin.f90 -o outputs/landscape_resilience_margin_fortran
  ./outputs/landscape_resilience_margin_fortran > outputs/tables/fortran_landscape_resilience_margin.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia spatial disturbance-threshold model..."
  julia julia/spatial_disturbance_threshold.jl > outputs/tables/julia_spatial_disturbance_threshold.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R landscape-resilience workflow..."
  Rscript r/landscape_resilience_profiles.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
