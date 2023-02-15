from typing import Tuple, Set

from SimplicialComplex.SimplicialComplexCreationService import generate_simplices, list_faces


class SimplicialComplex:
    def __init__(self, file_name: str, top_dim: int = 7, percentage_time: int = 1):
        self.simplexes, self.frequency_of_simplex = generate_simplices(file_name, top_dim=top_dim,
                                                                       percentage_time=percentage_time)
        self.faces: Set[Tuple[int]] = list_faces(self.simplexes)