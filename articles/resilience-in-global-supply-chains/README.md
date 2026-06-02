# Resilience in Global Supply Chains

Companion repository folder for the article **Resilience in Global Supply Chains**.

This directory provides reproducible workflows for global supply chain resilience strategy comparison, redundancy and flexibility analysis, visibility and dependency mapping, coordination review, climate and infrastructure exposure analysis, equity and labor safeguard diagnostics, implementation-burden analysis, cascading-risk simulation, and uncertainty-aware supply chain planning.

## Correct article directory

```text
articles/resilience-in-global-supply-chains/
```

## Purpose

This scaffold supports a professional supply chain resilience modeling workflow:

1. Define supply chain resilience strategies across redundancy, flexibility, visibility, coordination, adaptive capacity, equity safeguards, infrastructure continuity, systemic exposure, and implementation burden.
2. Compare strategies under balanced, redundancy-first, flexibility-first, visibility-first, coordination-first, climate-infrastructure, equity-first, exposure-sensitive, and implementation-aware priorities.
3. Simulate network flow performance under supplier failure, port congestion, climate disruption, cyber outage, logistics chokepoints, labor disruption, demand surge, critical-goods stress, and compound disruption.
4. Estimate equity-adjusted, infrastructure-adjusted, and implementation-adjusted supply chain resilience value.
5. Diagnose redundancy gaps, visibility gaps, infrastructure-continuity gaps, equity and labor safeguard gaps, cyber and digital-dependency exposure, climate exposure, systemic exposure, and implementation-burden triggers.
6. Model uncertainty using Monte Carlo simulation.
7. Support responsible interpretation across global supply chains, economic resilience, infrastructure resilience, climate resilience, food and water systems, healthcare supply chains, labor rights, human rights, public governance, and critical goods planning.
8. Provide multi-language examples in Python, R, Julia, SQL, Rust, Go, C, C++, and Fortran.
9. Export reproducible tables, figures, documentation, and notebook placeholders.

## Responsible-use note

The data are synthetic and the models are methodological examples. They are intended for learning, reproducible article companions, dashboard prototyping, resilience strategy comparison, supply-network stress testing, and professional workflow design. Real supply chain resilience analysis requires multi-tier supplier data, infrastructure data, labor and human-rights due diligence, climate-risk mapping, cyber-risk review, public governance analysis, competition-law awareness, confidentiality safeguards, and affected-stakeholder participation.

Do not use these examples to justify exploitation, hide labor or environmental harm behind resilience scores, expose confidential supplier data, automate procurement decisions without review, ignore affected workers and communities, or treat flow continuity as sufficient if risk is shifted onto vulnerable people.

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/global_supply_chain_resilience_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/global_supply_chain_resilience_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```
