# Technology resilience pathway example.
# Run: julia julia/technology_resilience_pathway_example.jl

using Printf

strategies = [
    ("Graceful Degradation and Fallback Architecture", 9.2, 8.8, 8.4, 8.2, 7.8, 8.3, 8.4, 8.5, 8.0, 3.0, 3.4),
    ("Cyber Recovery and Tested Backup Program", 8.0, 8.9, 8.5, 9.2, 8.4, 8.1, 8.6, 8.0, 7.9, 3.2, 3.5),
    ("Data Integrity and Lineage Governance", 8.0, 7.8, 8.6, 8.1, 9.3, 8.2, 8.8, 8.2, 7.8, 3.0, 3.4),
    ("Technical Debt and Maintainability Program", 8.4, 7.8, 8.2, 8.2, 8.0, 9.2, 8.5, 8.3, 7.8, 2.6, 3.7)
]

function tech_value(architecture, redundancy, observability, cybersecurity, data_integrity, maintainability, governance, human, vendor, debt, implementation)
    return 0.10 * architecture +
           0.10 * redundancy +
           0.10 * observability +
           0.11 * cybersecurity +
           0.11 * data_integrity +
           0.11 * maintainability +
           0.11 * governance +
           0.11 * human +
           0.10 * vendor -
           0.03 * debt -
           0.02 * implementation
end

println("strategy,technology_resilience_value,adjusted_value,technical_debt_risk")

for s in strategies
    name, architecture, redundancy, observability, cybersecurity, data_integrity, maintainability, governance, human, vendor, debt, implementation = s
    value = tech_value(architecture, redundancy, observability, cybersecurity, data_integrity, maintainability, governance, human, vendor, debt, implementation)
    adjusted = value - 0.06 * max(0, 8.3 - maintainability) - 0.06 * max(0, 8.3 - governance) - 0.07 * max(0, 8.2 - human) - 0.05 * max(0, 8.0 - vendor)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, adjusted, debt)
end
