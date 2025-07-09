from dataclasses import dataclass
from solvers.base import Solver, Node
from definition.board import Board
from typing import Tuple, List, Dict, Optional, Set
import sys

class DFSSolver(Solver):
    def __init__(self):
        super().__init__()
        # Increase recursion limit
        sys.setrecursionlimit(500000)

    def _search(self, initial: Board) -> Tuple[Optional[Node], int]:
        """DFS implementation using recursion"""
        self.nodes_expanded = 0
        self.reached: Set[Board] = {initial}
        
        solution_node = self._dfs_recursive(
            Node(parent=None, state=initial, action=None, path_cost=0)
        )
        
        return solution_node, self.nodes_expanded

    def _dfs_recursive(self, node: Node) -> Optional[Node]:
        """
        Recursive DFS helper function
        """
        if node.state.is_goal():
            return node

        self.nodes_expanded += 1
        
        for action in node.state.get_valid_moves():
            child_state = node.state.apply_move(action[0], action[1])
            
            if child_state not in self.reached:
                self.reached.add(child_state)
                child_node = Node(parent=node, state=child_state, action=action, path_cost=node.path_cost + 1)
                result = self._dfs_recursive(child_node)
                if result is not None:
                    return result
                    
        return None
