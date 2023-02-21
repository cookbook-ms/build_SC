import itertools
from typing import Tuple, Set, Dict, List

from SimplicialComplex.Simplex import Simplex
from SimplicialComplex.SimplicialComplexCreationService import generate_simplices


class SimplicialComplex:
    def __init__(self, file_name: str, top_dim: int = 7, percentage_time: int = 1):
        self._simplexes, self._frequency_of_simplex = generate_simplices(file_name, top_dim=top_dim,
                                                                         percentage_time=percentage_time)

    @property
    def simplexes(self) -> List[Set[Simplex]]:
        return self._simplexes

    @property
    def frequency_of_simplex(self) -> Dict[Simplex, int]:
        return self._frequency_of_simplex

    def get_simplexes_with_face(self, simplex: Simplex) -> Set[Simplex]:
        return set(
            [sim for dimension in self._simplexes for sim in dimension if set(simplex.nodes).issubset(sim.nodes)])

    def get_frequency_of_simplex(self, simplex: Simplex) -> int:
        return self._frequency_of_simplex[simplex]
