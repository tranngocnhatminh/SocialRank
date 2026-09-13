# Modules
import os
from dotenv import load_dotenv
from graph_and_pagerank import Graph, PageRank
from graph_builder import GraphBuilder

# Load API key from environment
load_dotenv()
api_key = os.getenv("XAPI_KEY")
users = ["nminhtn", "Microsoft", "BusinessInsider", "Windows", "GameSpot", "BBCWorld"]

graph = Graph()
builder = GraphBuilder(graph, api_key)
builder.initialize_nodes(users)
builder.add_edges_from_api(users)

print("Graph Adjacency List:")
for node, edges in graph.adjlist.items():
    print(f"{node}: {edges}")

pagerank = PageRank(graph, damping_factor=0.85, tol=1e-6)
page_ranks = pagerank.compute_page_rank()
print("\nPageRank Results:")
for node, rank in page_ranks.items():
    print(f"{node}: {rank:.6f}")
