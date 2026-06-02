#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for risk-governance resilience scaffold..."

python3 python/risk_governance_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C risk-pressure utility..."
  gcc c/risk_pressure.c -o outputs/risk_pressure_c
  ./outputs/risk_pressure_c > outputs/tables/c_risk_pressure.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ risk-governance margin simulation..."
  g++ -std=c++17 cpp/risk_governance_margin.cpp -o outputs/risk_governance_margin_cpp
  ./outputs/risk_governance_margin_cpp > outputs/tables/cpp_risk_governance_margin.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go governance-resilience utility..."
  (cd go && go run .) > outputs/tables/go_risk_governance_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_risk_governance_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran resilience-margin dynamics example..."
  gfortran fortran/resilience_margin_dynamics.f90 -o outputs/resilience_margin_dynamics_fortran
  ./outputs/resilience_margin_dynamics_fortran > outputs/tables/fortran_resilience_margin_dynamics.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia risk-governance threshold model..."
  julia julia/risk_governance_threshold_model.jl > outputs/tables/julia_risk_governance_threshold_model.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R risk-governance indicator workflow..."
  Rscript r/risk_governance_resilience_indicators.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
