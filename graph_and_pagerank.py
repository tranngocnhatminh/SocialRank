# Modules
import numpy as np
from typing import Dict, List

# Graph Representation: Adjacency List
class Graph:
    # Basic graph structure using an adjacency list to represent nodes and edges
    def __init__(self):
        self.adjlist = {}

    def add_node(self, u):
        if u not in self.adjlist:
            self.adjlist[u] = []

    def add_edge(self, u, v):
        self.adjlist[u].append(v)

    def get_nodes(self) -> List:
        return list(self.adjlist.keys())

# PageRank Algorithm Implementation Based on Linear Algebra
class PageRank:
    def __init__(self, graph: Graph, damping_factor: float = 0.85, tol: float = 1e-6):
        # Initialize basic parameters for PageRank computation
        self.graph = graph
        self.damping_factor = damping_factor
        self.tol = tol
        self.page_rank = {node: 1 / len(graph.get_nodes()) for node in graph.get_nodes()}

    def create_transition_matrix(self) -> np.ndarray:
        # Build the transition matrix from the graph's adjacency list
        nodes = self.graph.get_nodes()
        n = len(nodes)
        transition_matrix = np.zeros((n, n))
        for i, u in enumerate(nodes):
            out_degree = len(self.graph.adjlist[u])
            if out_degree == 0:
                # Handle dangling nodes by redistributing their rank uniformly
                transition_matrix[:, i] = 1 / n
            for v in self.graph.adjlist[u]:
                j = nodes.index(v)
                transition_matrix[j][i] = 1 / out_degree
        
        # Modify the transition matrix to include the damping factor and return it
        transition_matrix = self.damping_factor * transition_matrix + (1 - self.damping_factor) / n * np.ones((n, n))
        return transition_matrix

    def compute_page_rank(self) -> Dict:
        # Iteratively compute PageRank with mofified transition matrix until convergence
        nodes = self.graph.get_nodes()
        n = len(nodes)
        transition_matrix = self.create_transition_matrix()
        curr_page_rank = np.array(list(self.page_rank.values()))
        prev_page_rank = np.zeros(n)
        while np.linalg.norm(curr_page_rank - prev_page_rank) > self.tol:
            prev_page_rank = curr_page_rank.copy()
            curr_page_rank = np.matmul(transition_matrix, curr_page_rank)

        # Update the PageRank values in the dictionary and return result
        for i, node in enumerate(nodes):
            self.page_rank[node] = curr_page_rank[i]
        return self.page_rank
