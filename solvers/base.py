from typing import Protocol, Tuple, List
from definition.board import Board

class Solver(Protocol):
    """
    Solver interface. Each algorithm implements this.
    """
    def solve(self, start: Board) -> Tuple[List[tuple[str,int]], dict]:
        """
        Finds a solution.
        Returns:
            - path: list of (vehicle_id, displacement) moves from start to goal
            - metrics: dict with keys like 'time', 'nodes_expanded', 'max_frontier_size' (group will decide later)
        """
        ...