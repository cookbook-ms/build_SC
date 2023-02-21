from dataclasses import dataclass
from typing import List, Any


@dataclass
class Node:
    id: int
    attributes: List[Any] = None

    def __hash__(self):
        return hash(Node.id)
