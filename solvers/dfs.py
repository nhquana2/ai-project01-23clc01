from dataclasses import dataclass
from solvers.base import Solver, Node
from definition.board import Board
from typing import Tuple, List, Dict, Optional, Set
import time
import tracemalloc
import sys

class DFSSolver(Solver):
    def solve(self, initial: Board) -> Tuple[List[Tuple[int, int]], Dict]:
        metrics = {
            "search_time": 0,
            "nodes_expanded": 0,
            "memory_usage": 0,
            "path_cost": 0
        }

        # Increase recursion limit
        sys.setrecursionlimit(10000)

        start_time = time.time()
        tracemalloc.start()
        
        self.nodes_expanded = 0

        # initialize the reached set
        self.reached = {initial}

        # start the dfs search
        solution_node = self._dfs(Node(parent=None, state=initial, action=None, path_cost=0))
        
        current, memory_peak = tracemalloc.get_traced_memory()
        metrics["memory_usage"] = memory_peak / 1024
        tracemalloc.stop()

        metrics["search_time"] = time.time() - start_time
        metrics["nodes_expanded"] = self.nodes_expanded
        metrics["path_cost"] = solution_node.path_cost if solution_node else 0

        return self._get_path(solution_node), metrics

    def _dfs(self, node: Node) -> Optional[Node]:
        if node.state.is_goal():
            return node

        self.nodes_expanded += 1
        
        # recursive dfs instead of an explicit stack
        for action in node.state.get_valid_moves():
            child_state = node.state.apply_move(action[0], action[1])
            
            if child_state not in self.reached:
                self.reached.add(child_state)
                child_node = Node(parent=node, state=child_state, action=action, path_cost=node.path_cost + 1)
                result = self._dfs(child_node)
                if result is not None:
                    return result
                    
        return None

    def _get_path(self, node: Node) -> List[Tuple[int, int]]:
        path = []
        if node is None:
            return path
        while node.parent is not None:
            path.append(node.action)
            node = node.parent
        return path[::-1]
