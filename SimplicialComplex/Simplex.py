import itertools
from dataclasses import dataclass
from typing import Set, Tuple

from SimplicialComplex.Node import Node


@dataclass
class Simplex:
    nodes: Tuple[int] = None

    def __hash__(self):
        return hash(self.nodes)

    def __iter__(self):
        return self.nodes.__iter__()

    @property
    def get_faces(self):
        return list(itertools.combinations(self.nodes, len(self.nodes)))

