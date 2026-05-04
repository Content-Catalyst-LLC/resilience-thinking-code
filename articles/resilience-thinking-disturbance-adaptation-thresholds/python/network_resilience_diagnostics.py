"""
Network resilience diagnostics for resilience thinking.
"""

from __future__ import annotations

import pandas as pd
import networkx as nx


def build_supply_network() -> nx.Graph:
    edges = [
        ("Supplier A", "Factory 1"),
        ("Supplier B", "Factory 1"),
        ("Supplier C", "Factory 2"),
        ("Factory 1", "Distribution Hub"),
        ("Factory 2", "Distribution Hub"),
        ("Distribution Hub", "Region 1"),
        ("Distribution Hub", "Region 2"),
        ("Region 1", "Local Service A"),
        ("Region 2", "Local Service B"),
        ("Backup Supplier", "Factory 2")
    ]

    graph = nx.Graph()
    graph.add_edges_from(edges)
    return graph


def network_diagnostics(graph: nx.Graph) -> pd.DataFrame:
    centrality = nx.degree_centrality(graph)
    betweenness = nx.betweenness_centrality(graph)

    return pd.DataFrame({
        "node": list(graph.nodes()),
        "degree": [graph.degree(node) for node in graph.nodes()],
        "degree_centrality": [centrality[node] for node in graph.nodes()],
        "betweenness": [betweenness[node] for node in graph.nodes()]
    }).sort_values("betweenness", ascending=False)


def main() -> None:
    graph = build_supply_network()
    diagnostics = network_diagnostics(graph)

    print(diagnostics)
    diagnostics.to_csv("../outputs/network_resilience_diagnostics.csv", index=False)


if __name__ == "__main__":
    main()
