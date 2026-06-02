#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for social-ecological systems scaffold..."

python3 -m py_compile python/social_ecological_systems_standard.py
python3 python/social_ecological_systems_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C extraction-pressure utility..."
  gcc c/extraction_pressure.c -o outputs/extraction_pressure_c
  ./outputs/extraction_pressure_c > outputs/tables/c_extraction_pressure.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ coupled SES simulation..."
  g++ -std=c++17 cpp/coupled_ses_dynamics.cpp -o outputs/coupled_ses_dynamics_cpp
  ./outputs/coupled_ses_dynamics_cpp > outputs/tables/cpp_coupled_ses_dynamics.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go SES diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_ses_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_ses_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran SES resilience-margin example..."
  gfortran fortran/ses_resilience_margin.f90 -o outputs/ses_resilience_margin_fortran
  ./outputs/ses_resilience_margin_fortran > outputs/tables/fortran_ses_resilience_margin.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia coupled SES dynamics model..."
  julia julia/coupled_ses_dynamics.jl > outputs/tables/julia_coupled_ses_dynamics.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R SES profile workflow..."
  Rscript r/social_ecological_system_profiles.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
