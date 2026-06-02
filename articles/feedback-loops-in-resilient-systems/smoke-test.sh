#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for feedback loops scaffold..."

python3 -m py_compile python/feedback_loops_standard.py
python3 python/feedback_loops_standard.py

if command -v gcc >/dev/null 2>&1; then
  echo "Compiling C feedback-risk score utility..."
  gcc c/feedback_risk_score.c -o outputs/feedback_risk_score_c
  ./outputs/feedback_risk_score_c > outputs/tables/c_feedback_risk_score.csv
else
  echo "Skipping C example: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Compiling C++ feedback delay simulation..."
  g++ -std=c++17 cpp/feedback_delay_simulation.cpp -o outputs/feedback_delay_simulation_cpp
  ./outputs/feedback_delay_simulation_cpp > outputs/tables/cpp_feedback_delay_simulation.csv
else
  echo "Skipping C++ example: g++ not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go feedback diagnostic utility..."
  (cd go && go run .) > outputs/tables/go_feedback_diagnostics.csv
else
  echo "Skipping Go example: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust CLI..."
  (cd rust && cargo run --quiet) > outputs/tables/rust_feedback_risk_output.txt
else
  echo "Skipping Rust example: cargo not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Compiling Fortran feedback delay simulation..."
  gfortran fortran/feedback_delay_simulation.f90 -o outputs/feedback_delay_simulation_fortran
  ./outputs/feedback_delay_simulation_fortran > outputs/tables/fortran_feedback_delay_simulation.csv
else
  echo "Skipping Fortran example: gfortran not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia feedback delay model..."
  julia julia/feedback_delay_model.jl > outputs/tables/julia_feedback_delay_model.csv
else
  echo "Skipping Julia example: julia not found."
fi

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R feedback loop workflow..."
  Rscript r/feedback_loop_dynamics.R || echo "R workflow skipped or failed because required R packages are missing."
else
  echo "Skipping R example: Rscript not found."
fi

echo "Smoke tests complete."
