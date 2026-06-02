#!/usr/bin/env python3
from pathlib import Path
try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    raise SystemExit("Missing advanced dependency. Run: pip install -r requirements-advanced.txt") from exc
ROOT = Path(__file__).resolve().parents[1]
OUT_TABLES = ROOT / "outputs/tables"; OUT_FIGURES = ROOT / "outputs/figures"
OUT_TABLES.mkdir(parents=True, exist_ok=True); OUT_FIGURES.mkdir(parents=True, exist_ok=True)
s = pd.read_csv(ROOT / "data/raw/organizational_resilience_strategies.csv")
s["value"] = 0.11*s.anticipation + 0.11*s.absorption + 0.11*s.adaptation + 0.12*s.learning + 0.12*s.memory + 0.11*s.coordination + 0.11*s.governance + 0.12*s.workforce_protection - 0.05*s.workforce_burden - 0.04*s.implementation_burden
s["adjusted_value"] = s.value - 0.06*(8.4-s.learning).clip(lower=0) - 0.06*(8.3-s.memory).clip(lower=0) - 0.08*(8.2-s.workforce_protection).clip(lower=0)
s.sort_values("adjusted_value", ascending=False).to_csv(OUT_TABLES / "advanced_strategy_profiles.csv", index=False)
rng=np.random.default_rng(42); rows=[]
cols=["anticipation","absorption","adaptation","learning","memory","coordination","governance","workforce_protection","workforce_burden","implementation_burden"]
for sim in range(3000):
    x=s.copy()
    for c in cols: x[c]=rng.normal(s[c],0.55).clip(1,10)
    x["sim_value"]=0.11*x.anticipation+0.11*x.absorption+0.11*x.adaptation+0.12*x.learning+0.12*x.memory+0.11*x.coordination+0.11*x.governance+0.12*x.workforce_protection-0.05*x.workforce_burden-0.04*x.implementation_burden
    x=x.sort_values("sim_value", ascending=False).reset_index(drop=True)
    for rank,row in x.iterrows(): rows.append({"simulation_id":sim,"strategy":row.strategy,"rank":rank+1,"value":row.sim_value})
mc=pd.DataFrame(rows)
summary=mc.groupby("strategy").agg(mean_value=("value","mean"), probability_ranked_first=("rank",lambda z:(z==1).mean()*100), probability_top_two=("rank",lambda z:(z<=2).mean()*100)).reset_index().sort_values("probability_ranked_first",ascending=False)
summary.to_csv(OUT_TABLES / "advanced_monte_carlo_summary.csv", index=False)
plt.figure(figsize=(10,6)); plt.bar(summary.strategy, summary.probability_ranked_first); plt.xticks(rotation=25, ha="right"); plt.ylabel("Probability ranked first (%)"); plt.title("Robustness of Organizational Resilience Strategies"); plt.tight_layout(); plt.savefig(OUT_FIGURES / "advanced_probability_ranked_first.png", dpi=160)
print("Advanced organizational resilience workflow complete."); print(summary.round(3))
