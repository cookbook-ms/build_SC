import itertools
from math import floor
from typing import List, Set, Tuple, Dict

from SimplicialComplex.Simplex import Simplex


def match_simplexes_to_dimension(top_dim: int, simplex_vertices_tupled) -> List[List[Tuple[int]]]:
    list_simplices = [None] * top_dim
    for k in range(top_dim):
        list_simplices[k] = [sorted(id_vertices) for id_simp, id_vertices in enumerate(simplex_vertices_tupled) if
                             len(id_vertices) == k + 1]
        list_simplices[k].sort()
    return list_simplices


def generate_simplices(file_name: str, top_dim: int = 7, percentage_time=1) -> Tuple[List[Set[Simplex]], Dict[Simplex, int]]:
    """
    top_dim: the largest simplicial order, i.e., the simplicial complex order
    file_name:
    unique_simplices: if to generate the unique simplices, since this dataset contains the same simplex for many times over a certain length of time stamps
        - 'True': we also include the duration of the time stamps of each simplex in the dict value
        - 'False': generate simplices allowed to be duplicate
    """

    if not file_name:
        return [], dict()
    simplex_dim, simplex_vertices = parse_files(file_name)

    simplexes = get_simplexes(percentage_time, simplex_dim, simplex_vertices)
    dimensions = match_simplexes_to_dimension(top_dim, simplexes)
    frequencies = get_frequencies(dimensions)
    reformat_simplexes(dimensions)
    return dimensions, frequencies


def reformat_simplexes(dimensions) -> List[Set[Simplex]]:
    for dimension in dimensions:
        dimension = [tuple(list(x)) for x in set(tuple(x) for x in dimension)]
        dimension.sort()
        dimension = set([Simplex(nodes=nodes) for nodes in dimension])
        print(dimension)


def get_frequencies(dimensions):
    """
    Computes the frequencies of each simplex in a list of simplices in k dimension, and returns a list of integers representing the frequencies.
    @param dimensions:
    @return: list of frequencies of each simplex
    """
    freq_simplices: Dict[Simplex, int] = {}
    for dimension in dimensions:
        for simplex in dimension:
            simplex = Simplex(nodes=tuple(simplex))
            if simplex in freq_simplices:
                freq_simplices[simplex] += 1
            else:
                freq_simplices[simplex] = 0
    return freq_simplices


def get_simplexes(percentage_time, simplex_dim, simplex_vertices) -> List[List[int]]:
    """
    Group the nodes from the simplex vertices into simplexes
    @param percentage_time: ?
    @param simplex_dim: dimensions of which simplex
    @param simplex_vertices: vertices in the given simplex
    @return: simplexes in the form of their baises
    """
    if len(simplex_vertices) == 0:
        return []
    simplex_dim = simplex_dim[:floor(percentage_time * len(simplex_dim))]
    start = 0
    simplex_vertices_tupled = []
    for count in simplex_dim:
        end = start + int(count)
        sublist = [int(x) for x in simplex_vertices[start:end]]
        simplex_vertices_tupled.append(sublist)
        start = end
    return simplex_vertices_tupled


def parse_files(file_name: str) -> Tuple[List[str], List[str]]:
    """
    Parse files containing information about dimension of the simplexes and nodes included in which one of them
    @param file_name: first part of the name of the files with information.
    @return: tuple of list of number of nodes in each simplex and list of ids of the nodes in each of the simplexes.
    """
    file_path = './ScHoLP-Data-1.0/' + file_name
    with open(file_path + '/' + file_name + '-nverts.txt') as f:
        simplex_dim: List[str] = [line.rstrip('\n') for line in f]
    with open(file_path + '/' + file_name + '-simplices.txt') as f:
        simplex_vertices: List[str] = [line.rstrip('\n') for line in f]
    return simplex_dim, simplex_vertices
