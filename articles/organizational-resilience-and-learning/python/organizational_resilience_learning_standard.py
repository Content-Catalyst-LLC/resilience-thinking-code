#!/usr/bin/env python3
from __future__ import annotations
import csv, random
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "tables"
PROC = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)
PROC.mkdir(parents=True, exist_ok=True)
BENEFITS = ["anticipation", "absorption", "adaptation", "learning", "memory", "coordination", "governance", "workforce_protection"]

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path, rows):
    if not rows: return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

def val(row, key): return float(row[key])

def resilience_value(row):
    return (0.11*val(row,"anticipation") + 0.11*val(row,"absorption") + 0.11*val(row,"adaptation") +
            0.12*val(row,"learning") + 0.12*val(row,"memory") + 0.11*val(row,"coordination") +
            0.11*val(row,"governance") + 0.12*val(row,"workforce_protection") -
            0.05*val(row,"workforce_burden") - 0.04*val(row,"implementation_burden"))

def score(row, scenario):
    return (val(scenario,"anticipation_weight")*val(row,"anticipation") + val(scenario,"absorption_weight")*val(row,"absorption") +
            val(scenario,"adaptation_weight")*val(row,"adaptation") + val(scenario,"learning_weight")*val(row,"learning") +
            val(scenario,"memory_weight")*val(row,"memory") + val(scenario,"coordination_weight")*val(row,"coordination") +
            val(scenario,"governance_weight")*val(row,"governance") + val(scenario,"workforce_protection_weight")*val(row,"workforce_protection") -
            val(scenario,"workforce_burden_weight")*val(row,"workforce_burden") - val(scenario,"implementation_burden_weight")*val(row,"implementation_burden"))

def diagnostic(row):
    if val(row,"workforce_burden") >= 3.4: return "workforce-burden review needed"
    if val(row,"implementation_burden") >= 3.5: return "implementation-burden review needed"
    if val(row,"learning") < 8.0: return "learning-system review needed"
    if val(row,"memory") < 8.0: return "institutional-memory review needed"
    if val(row,"workforce_protection") < 8.0: return "workforce-protection review needed"
    return "promising but requires stress testing"

def strategy_profiles(strategies):
    rows = []
    for r in strategies:
        base = resilience_value(r)
        adjusted = base - 0.06*max(0, 8.4-val(r,"learning")) - 0.06*max(0, 8.3-val(r,"memory")) - 0.08*max(0, 8.2-val(r,"workforce_protection"))
        rows.append({"strategy_id": r["strategy_id"], "strategy": r["strategy"], "domain": r["domain"], "organizational_resilience_value": round(base, 5), "adjusted_value": round(adjusted, 5), "workforce_adjusted_value": round(base * (0.72 + 0.028*val(r,"workforce_protection") - 0.010*val(r,"workforce_burden")), 5), "diagnostic": diagnostic(r), "critical_function": r["critical_function"]})
    return sorted(rows, key=lambda x: x["adjusted_value"], reverse=True)

def scenario_rankings(strategies, scenarios):
    rows = []
    for s in scenarios:
        ranked = sorted([(score(r, s), r) for r in strategies], reverse=True, key=lambda x: x[0])
        for rank, (v, r) in enumerate(ranked, 1):
            rows.append({"scenario": s["scenario"], "rank": rank, "strategy_id": r["strategy_id"], "strategy": r["strategy"], "organizational_resilience_value": round(v, 5)})
    return rows

def simulate(org, events, seed=42, steps=90):
    rng = random.Random(seed)
    function = val(org,"baseline_function"); learning = val(org,"learning_capacity"); memory = val(org,"memory_capacity"); strain = val(org,"workforce_strain")
    anticipation = val(org,"anticipation_capacity"); absorption = val(org,"absorptive_capacity"); adaptation = val(org,"adaptive_capacity")
    coordination = val(org,"coordination_capacity"); governance = val(org,"governance_capacity"); ethics = val(org,"ethical_burden_sensitivity")
    schedule = {10:events[0], 24:events[1], 38:events[2], 52:events[3], 66:events[4], 78:events[5]}
    rows = []
    for t in range(steps):
        e = schedule.get(t)
        if e:
            shock=val(e,"shock_intensity"); operational=val(e,"operational_disruption"); staffing=val(e,"staffing_stress"); knowledge=val(e,"knowledge_loss"); coord_stress=val(e,"coordination_stress"); digital=val(e,"digital_disruption"); reputation=val(e,"reputational_pressure"); burden=val(e,"ethical_burden"); opportunity=val(e,"learning_opportunity"); name=e["event_name"]
        else:
            shock=0.05+rng.random()*0.02; operational=staffing=coord_stress=0.10; knowledge=0.08+0.001*t; digital=0.09; reputation=0.08; burden=0.20; opportunity=0.18; name="background organizational pressure"
        load = 0.12*shock + 0.14*operational + 0.14*staffing + 0.13*knowledge + 0.13*coord_stress + 0.12*digital + 0.11*reputation + 0.11*burden
        adaptive = min(1, max(0, 0.13*anticipation + 0.13*absorption + 0.16*adaptation + 0.15*learning + 0.14*memory + 0.13*coordination + 0.10*governance + 0.06*(1-strain)))
        strain = min(1, max(0, strain + 0.18*load + 0.08*max(0, load-absorption) - 0.08*governance - 0.08*ethics))
        function = min(1, max(0, function - 0.32*load + 0.24*adaptive + 0.08*coordination + 0.06*governance - 0.18*strain))
        review_quality = 0.30*governance + 0.25*coordination + 0.25*ethics + 0.20*anticipation
        learning = min(1, max(0, learning + 0.10*opportunity*review_quality - (0.015 + 0.045*strain + 0.020*knowledge)))
        memory = min(1, max(0, memory + 0.05*(0.30*memory + 0.22*learning + 0.20*governance + 0.18*coordination + 0.10*ethics) - 0.04*strain - 0.03*knowledge))
        score_value = min(1, max(0, 0.20*function + 0.16*learning + 0.16*memory + 0.16*adaptive + 0.12*coordination + 0.10*governance + 0.10*(1-strain)))
        rows.append({"organization": org["organization"], "time": t, "event": name, "disruption_load": round(load,5), "function": round(function,5), "adaptive_response": round(adaptive,5), "learning_stock": round(learning,5), "memory_stock": round(memory,5), "workforce_strain": round(strain,5), "resilience_score": round(score_value,5)})
    return rows

def summarize_dynamic(rows):
    out=[]
    for org in sorted({r["organization"] for r in rows}):
        sub=[r for r in rows if r["organization"]==org]
        out.append({"organization": org, "mean_function": round(mean(float(r["function"]) for r in sub),5), "minimum_function": round(min(float(r["function"]) for r in sub),5), "final_function": sub[-1]["function"], "final_learning_stock": sub[-1]["learning_stock"], "final_memory_stock": sub[-1]["memory_stock"], "maximum_workforce_strain": round(max(float(r["workforce_strain"]) for r in sub),5), "final_resilience_score": sub[-1]["resilience_score"]})
    return sorted(out, key=lambda x: x["final_resilience_score"], reverse=True)

def monte_carlo(strategies, scenario, n=2000):
    rng=random.Random(42); rows=[]
    for i in range(n):
        scored=[]
        for r in strategies:
            sampled=dict(r)
            for c in BENEFITS + ["workforce_burden", "implementation_burden"]:
                sampled[c]=str(max(1,min(10,val(r,c)+rng.gauss(0,0.55))))
            scored.append((score(sampled,scenario),r))
        scored.sort(reverse=True,key=lambda x:x[0])
        for rank,(v,r) in enumerate(scored,1):
            rows.append({"simulation_id":i,"strategy_id":r["strategy_id"],"strategy":r["strategy"],"rank":rank,"organizational_resilience_value":round(v,5)})
    summary=[]; k=len(strategies)
    for r in strategies:
        sub=[x for x in rows if x["strategy_id"]==r["strategy_id"]]
        ranks=[int(x["rank"]) for x in sub]; vals=[float(x["organizational_resilience_value"]) for x in sub]
        summary.append({"strategy_id":r["strategy_id"],"strategy":r["strategy"],"mean_value":round(mean(vals),5),"median_value":round(median(vals),5),"probability_ranked_first":round(100*sum(x==1 for x in ranks)/n,2),"probability_top_two":round(100*sum(x<=2 for x in ranks)/n,2),"probability_bottom_two":round(100*sum(x>=k-1 for x in ranks)/n,2)})
    return rows, sorted(summary, key=lambda x: x["probability_ranked_first"], reverse=True)

def main():
    strategies=read_csv(ROOT/"data/raw/organizational_resilience_strategies.csv")
    scenarios=read_csv(ROOT/"data/raw/organizational_resilience_scenarios.csv")
    orgs=read_csv(ROOT/"data/raw/organizational_profiles.csv")
    events=read_csv(ROOT/"data/raw/organizational_disruption_events.csv")
    profiles=strategy_profiles(strategies)
    dynamic=[]
    for i,org in enumerate(orgs): dynamic.extend(simulate(org, events, seed=100+i))
    mc, mc_summary=monte_carlo(strategies, scenarios[0])
    write_csv(OUT/"organizational_resilience_strategy_profiles_standard.csv", profiles)
    write_csv(OUT/"organizational_resilience_strategy_rankings_standard.csv", scenario_rankings(strategies, scenarios))
    write_csv(OUT/"organizational_resilience_dynamic_simulation_standard.csv", dynamic)
    write_csv(OUT/"organizational_resilience_dynamic_summary_standard.csv", summarize_dynamic(dynamic))
    write_csv(OUT/"organizational_resilience_monte_carlo_standard.csv", mc)
    write_csv(OUT/"organizational_resilience_robustness_summary_standard.csv", mc_summary)
    write_csv(PROC/"organizational_resilience_strategy_profiles_standard.csv", profiles)
    print("Organizational resilience and learning workflow complete.")
    print(f"Wrote outputs to: {OUT}")
    for row in profiles:
        print(f"  {row['strategy']}: adjusted={row['adjusted_value']} diagnostic={row['diagnostic']}")
if __name__ == "__main__": main()
