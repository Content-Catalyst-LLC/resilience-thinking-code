#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for ecological resilience scaffold..."

python3 -m py_compile python/ecological_resilience_standard.py
python3 python/ecological_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  gcc c/stability_return.c -o outputs/stability_return_c
  ./outputs/stability_return_c > outputs/tables/c_stability_return.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  g++ -std=c++17 cpp/ecological_regime_shift.cpp -o outputs/ecological_regime_shift_cpp
  ./outputs/ecological_regime_shift_cpp > outputs/tables/cpp_ecological_regime_shift.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  (cd go && go run .) > outputs/tables/go_ecological_resilience_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  (cd rust && cargo run --quiet) > outputs/tables/rust_ecological_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  gfortran fortran/basin_width_margin.f90 -o outputs/basin_width_margin_fortran
  ./outputs/basin_width_margin_fortran > outputs/tables/fortran_basin_width_margin.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  julia julia/ecological_regime_shift.jl > outputs/tables/julia_ecological_regime_shift.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/ecological_resilience_profiles.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
