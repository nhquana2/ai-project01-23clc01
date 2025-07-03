from typing import Protocol, Tuple, List, Optional, Dict, Optional
from definition.board import Board
from dataclasses import dataclass

@dataclass
class Node:
    state: Board
    action: Tuple[int, int] | None # (vehicle_id, displacement)
    parent: Optional["Node"] = None
    path_cost: int = 0

# Notice: This is a PROTOCOL 
class Solver(Protocol):
    """
    Solver interface. Each algorithm implements this.
    """
    def solve(self, initial: Board) -> Tuple[List[Tuple[int, int]], Dict]:
        """
        Finds a solution.
        Returns:
            - path: list of (vehicle_id, displacement) moves from initial to goal state
            - metrics: dict with keys like 'search_time', 'nodes_expanded', 'memory_usage' (group will decide later)
        """
        ...