import itertools
import time
from itertools import groupby
from math import floor
from typing import List, Set, Tuple, Dict
from simplicial import *
from pymemcache.client import base

client = base.Client(('localhost', 11211))


def generate_simplices(top_dim=7, file_name='email-Enron', unique_simplices=False, percentage_time=1):
    '''
    top_dim: the largest simplicial order, i.e., the simplicial complex order
    file_name:
    unique_simplices: if to generate the unique simplices, since this dataset contains the same simplex for many times over a certain length of time stamps
        - 'True': we also include the duration of the time stamps of each simplex in the dict value
        - 'False': generate simplices allowed to be duplicate
    '''
    cached_simplex = client.get(file_name)
    if cached_simplex:
        c = cached_simplex
    else:
        c: SimplicialComplex = SimplicialComplex()
        file_path: str = './ScHoLP-Data-1.0/' + file_name
        with open(file_path + '/' + file_name + '-nverts.txt') as f:
            simplex_dim: List[str] = [line.rstrip('\n') for line in f]
        with open(file_path + '/' + file_name + '-simplices.txt') as f:
            simplex_vertices: List[str] = [line.rstrip('\n') for line in f]
        with open(file_path + '/' + file_name + '-node-labels.txt') as f:
            number_of_nodes: int = len([line.rstrip('\n') for line in f])

        current_position_in_vertex_list: int = 0
        for simplex in simplex_dim:
            if int(simplex) > top_dim:
                continue
            bases_of_the_simplex: List[str] = simplex_vertices[
                                              current_position_in_vertex_list: current_position_in_vertex_list + int(
                                                  simplex)]
            try:
                c.addSimplexWithBasis(bases_of_the_simplex)
            except (KeyError, ValueError) as error:
                pass
            current_position_in_vertex_list += int(simplex)
        client.set(file_name, c)
    return c


if __name__ == "__main__":
    start = time.time()
    complex = generate_simplices(top_dim=4, unique_simplices=True, percentage_time=1)
    end = time.time()
    print((end - start) / 60)
