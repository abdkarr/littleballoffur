import random
import networkx as nx
from littleballoffur.sampler import Sampler

class HybridNodeEdgeSampler(Sampler):
    r"""An implementation of hybrid node-edge sampling.

    Args:
        number_of_edges (int): Number of edges. Default is 100.
        seed (int): Random seed. Default is 42.
        p (float): Hybridization probability. Default is 0.8.
    """
    def __init__(self, number_of_edges=100, seed=42, p=0.8):
        self.number_of_edges = number_of_edges
        self.seed = seed
        self.p = p
        self._set_seed()

    def _create_initial_edge_set(self):
        """
        Choosing initial edges.
        """
        self._sampled_edges = set()
        edges = [edge for edge in self._graph.edges()]
        while len(self._sampled_edges) < self.number_of_edges:
            score = random.uniform(0,1)
            if score < self.p:
                source_node = random.choice(range(self._graph.number_of_nodes()))
                target_node = random.choice([node for node in self._graph.neighbors(source_node)])
                edge = sorted([source_node, target_node])
                edge = tuple(edge)
            else:
                edge = random.choice(edges)
            self._sampled_edges.add(edge)

    def sample(self, graph):
        """
        Sampling edges randomly from randomly sampled nodes or sampling random edges.

        Arg types:
            * **graph** *(NetworkX graph)* - The graph to be sampled from.

        Return types:
            * **new_graph** *(NetworkX graph)* - The graph of sampled edges.
        """
        self._check_graph(graph)
        self._check_number_of_edges(graph)
        self._graph = graph
        self._create_initial_edge_set()
        new_graph = nx.from_edgelist(self._sampled_edges)
        return new_graph