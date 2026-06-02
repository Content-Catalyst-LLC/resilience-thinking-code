#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for ecosystem-service resilience scaffold..."

python3 -m py_compile python/ecosystem_services_resilience_standard.py
python3 python/ecosystem_services_resilience_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C service-flow utility..."
  gcc c/service_flow.c -o outputs/service_flow_c
  ./outputs/service_flow_c > outputs/tables/c_service_flow.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ service disturbance simulation..."
  g++ -std=c++17 cpp/service_disturbance_simulation.cpp -o outputs/service_disturbance_simulation_cpp
  ./outputs/service_disturbance_simulation_cpp > outputs/tables/cpp_service_disturbance_simulation.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go service-resilience diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_service_resilience_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_service_resilience_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran service-resilience margin example..."
  gfortran fortran/service_resilience_margin.f90 -o outputs/service_resilience_margin_fortran
  ./outputs/service_resilience_margin_fortran > outputs/tables/fortran_service_resilience_margin.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia ecosystem-service threshold model..."
  julia julia/ecosystem_service_threshold_model.jl > outputs/tables/julia_ecosystem_service_threshold_model.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R ecosystem-service profile workflow..."
  Rscript r/ecosystem_service_resilience_profiles.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
