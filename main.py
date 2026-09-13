from graph_and_pagerank import Graph
from graph_and_pagerank import PageRank

graph = Graph()

graph.add_node("A")
graph.add_node("B")
graph.add_node("C")

graph.add_edge("A", "B")
graph.add_edge("B", "C")
#graph.add_edge("C", "B")

pagerank = PageRank(graph)

result = pagerank.compute_page_rank()

print(result)