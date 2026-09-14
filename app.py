# Modules
import os
from pathlib import Path
from flask import Flask, jsonify, request, send_file
from dotenv import load_dotenv
from graph_and_pagerank import Graph, PageRank
from graph_builder import GraphBuilder

# Load API key from environment
load_dotenv()
app = Flask(__name__)
api_key = os.getenv("XAPI_KEY")
BASE_DIR = Path(__file__).resolve().parent

# Load home page and static files
@app.get("/")
def home():
    return send_file(BASE_DIR / "index.html")

# Load CSS stylesheet
@app.get("/style.css")
def stylesheet():
    return send_file(BASE_DIR / "style.css", mimetype="text/css")

# API endpoint to analyze the social graph and compute PageRank
@app.post("/api/analyze")
def analyze():
    data = request.get_json()
    usernames = data.get("usernames", [])
    # Obtain a clean list of usernames by stripping whitespace and leading '@' symbols
    usernames = [
        username.strip().lstrip("@")
        for username in usernames
        if username.strip()
    ]
    # Error handling for empty username list
    if not usernames:
        return jsonify({"error": "Enter at least one username."}), 400
    # Running the graph building and PageRank computation
    graph = Graph()
    builder = GraphBuilder(graph, api_key)
    builder.initialize_nodes(usernames)
    builder.add_edges_from_api(usernames)
    rankings = PageRank(graph).compute_page_rank()
    # Return the graph structure and PageRank results as JSON
    return jsonify({
        "edges": [
            {"source": source, "target": target}
            for source, targets in graph.adjlist.items()
            for target in targets
        ],
        "rankings": [
            {"username": username, "score": float(score)}
            for username, score in sorted(
                rankings.items(),
                key=lambda item: item[1],
                reverse=True
            )
        ]
    })

if __name__ == "__main__":
    app.run(debug=True)