# Local knowledge pathway example.
# Run: julia julia/local_knowledge_pathway_example.jl

using Printf

strategies = [
    ("Participatory Risk Mapping and Action Triggers", 8.7, 8.8, 8.4, 8.2, 8.0, 8.3, 8.5, 3.2),
    ("Indigenous Knowledge Governance Protocol", 8.4, 9.2, 8.8, 8.9, 9.4, 9.0, 8.7, 3.5),
    ("Funded Community Resilience Advisory Council", 9.0, 8.7, 9.1, 8.8, 8.5, 8.9, 9.0, 3.3)
]

function knowledge_value(participation, diversity, influence, trust, protection, reciprocity, accountability, burden)
    return 0.14 * participation +
           0.14 * diversity +
           0.15 * influence +
           0.14 * trust +
           0.14 * protection +
           0.14 * reciprocity +
           0.15 * accountability -
           0.02 * burden
end

println("strategy,knowledge_integration_value,protection_adjusted_value,implementation_burden")

for s in strategies
    name, participation, diversity, influence, trust, protection, reciprocity, accountability, burden = s
    value = knowledge_value(participation, diversity, influence, trust, protection, reciprocity, accountability, burden)
    adjusted = value - 0.08 * max(0, influence - accountability) - 0.08 * max(0, 8.4 - protection)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, adjusted, burden)
end
