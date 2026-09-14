# Modules
import requests
from typing import List
from graph_and_pagerank import Graph

# GraphBuilder to construct the graph from API data
class GraphBuilder:
    def __init__(self, graph: Graph, api_key: str):
        self.graph = graph
        self.api_key = api_key

    # Build the graph from a list of users and their follow relationships using the API
    def initialize_nodes(self, users: List[str]):
        # Add each user as a node in the graph
        for user in users:
            self.graph.add_node(user)

    def check_follow_relationship(self, source_user: str, target_user: str) -> bool:
        # Check if source_user follows target_user using the API
        url = "https://api.getxapi.com/twitter/user/check_follow_relationship"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        params = {
            "source_user_name": source_user,
            "target_user_name": target_user,
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['data'].get("sourceFollowsTarget", False)
        else:
            print(f"API request failed with status code {response.status_code} for users {source_user} -> {target_user} due to their privacy settings")
            return False

    def add_edges_from_api(self, users: List[str]):
        # For each pair of users, check if one follows the other using the API and add edges accordingly
        for source_user in users:
            for target_user in users:
                if source_user != target_user:
                    if self.check_follow_relationship(source_user, target_user):
                        self.graph.add_edge(source_user, target_user)