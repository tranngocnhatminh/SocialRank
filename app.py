# Modules
import os
from dotenv import load_dotenv
from graph_and_pagerank import Graph, PageRank
from graph_builder import GraphBuilder

# Load API key from environment
load_dotenv()
api_key = os.getenv("XAPI_KEY")
users = ["nminhtn", "Microsoft"]

