from typing import Tuple, List, Optional, Dict, Optional
from definition.board import Board
from dataclasses import dataclass
from abc import ABC, abstractmethod
import time
import tracemalloc

@dataclass
class Node:
    state: Board
    action: Tuple[int, int] | None # (vehicle_id, displacement)
    parent: Optional["Node"] = None
    path_cost: int = 0


class Solver(ABC):
    """
    Solver interface. Each algorithm implements this.
    """
    def solve(self, initial: Board) -> Tuple[List[Tuple[int, int]], Dict]:

        metrics = {
            "search_time": 0.0,
            "nodes_expanded": 0,
            "memory_usage": 0.0,
            "path_cost": 0
        }

        start_time = time.time()
        tracemalloc.start()
        solution_node, nodes_expanded = self._search(initial)

        current, memory_peak = tracemalloc.get_traced_memory()
        metrics["memory_usage"] = memory_peak / 1024
        tracemalloc.stop()

        metrics["search_time"] = time.time() - start_time
        metrics["nodes_expanded"] = nodes_expanded
        metrics["path_cost"] = solution_node.path_cost if solution_node else 0

        return self._get_path(solution_node), metrics

    @abstractmethod
    def _search(self, initial: Board) -> Tuple[Optional[Node], int]:
        """
        Abstract method that each solver must implement, to execute the search algorithm.
        Returns: (solution_node, nodes_expanded)
        """
        pass

    def _get_path(self, node: Node | None) -> List[Tuple[int, int]]:
        """
        Reconstructs the path from the goal node to the initial node.
        """
        path = []
        if node is None:
            return path
        while node.parent is not None:
            path.append(node.action)
            node = node.parent
        return path[::-1] 