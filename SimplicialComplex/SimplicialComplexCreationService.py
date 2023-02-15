import itertools
from math import floor
from typing import List, Set, Tuple


def generate_simplices(file_name: str, top_dim: int = 7, percentage_time=1):
    '''
    top_dim: the largest simplicial order, i.e., the simplicial complex order
    file_name:
    unique_simplices: if to generate the unique simplices, since this dataset contains the same simplex for many times over a certain length of time stamps
        - 'True': we also include the duration of the time stamps of each simplex in the dict value
        - 'False': generate simplices allowed to be duplicate
    '''

    if not file_name:
        return []
    simplex_dim, simplex_vertices = parse_files(file_name)

    simplex_vertices_tupled = get_simplexes(percentage_time, simplex_dim, simplex_vertices)

    list_simplices, freqency = reformat_simplexes(simplex_vertices_tupled, top_dim)

    return list_simplices, freqency


def reformat_simplexes(simplex_vertices_tupled, top_dim):
    """
    Reformats a list of simplices represented as tuples of vertices into a list of sets of tuples, and computes the frequencies of each simplex.
    @param simplex_vertices_tupled: A list of tuples representing the simplices of the simplicial complex, where each tuple contains the indices of its vertices.
    @param top_dim:  The dimension of the top simplex in the simplicial complex.
    @return: A tuple containing two elements:
        - A list of sets, where the k-th set contains the k-simplices of the simplicial complex. The simplices are represented as tuples of vertices.
        - A list of dictionaries, where the k-th dictionary maps the integer ID of a k-simplex to a tuple containing the set representation of the simplex and its frequency.
    """
    list_simplices: List[Set[Tuple[int]]] = [None] * top_dim
    cos = [None] * top_dim
    for k in range(top_dim):
        list_simplices[k] = [sorted(id_vertices) for id_simp, id_vertices in enumerate(simplex_vertices_tupled) if
                             len(id_vertices) == k + 1]
        list_simplices[k].sort()
        freq_simplices = get_frequencies_of_simplexes(k, list_simplices)
        list_simplices[k] = [tuple(list(x)) for x in set(tuple(x) for x in list_simplices[k])]
        list_simplices[k].sort()
        list_simplices[k] = set(list_simplices[k])
        cos[k] = dict(zip(range(len(list_simplices[k])), zip(set(list_simplices[k]), freq_simplices)))
    return list_simplices, cos


def get_frequencies_of_simplexes(k, list_simplices):
    """
    Computes the frequencies of each simplex in a list of simplices in k dimension, and returns a list of integers representing the frequencies.
    @param k: dimension for which simplexes the frequencies are calculated
    @param list_simplices: list of simplicies of the simplicial complex
    @return: list of frequencies of each simplex
    """
    freq_simplices = [len(list(group)) for key, group in itertools.groupby(list_simplices[k])]
    return freq_simplices


def get_simplexes(percentage_time, simplex_dim, simplex_vertices) -> List[List[int]]:
    """
    Group the nodes from the simplex vertices into simplexes
    @param percentage_time: ?
    @param simplex_dim: dimensions of which simplex
    @param simplex_vertices: vertices in the given simplex
    @return: simplexes in the form of their baises
    """
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


def list_faces(list_simplices):
    """
    Computes the faces of a simplicial complex and returns a dictionary of each simplex and its corresponding faces.
    @param list_simplices: simplices of the simplicial complex
    @return:A dictionary containing the simplices and their faces, where each key is an integer index and each value is a
        tuple of two elements: a tuple of face indices and a list of vertex indices.
    """
    list_faces = list_simplices
    for k in range(2, len(list_simplices)):
        for index, simplex_vertices in enumerate(list_simplices[k]):
            face_vertices = (list(itertools.combinations(simplex_vertices, k)))
            face_idx = (
                [face_id for face_id, face_vertex in list_simplices[k - 1].items() if face_vertex[0] in face_vertices])
            list_faces[k][index] = (tuple(face_idx), list_faces[k][index][1])

    return list_faces
