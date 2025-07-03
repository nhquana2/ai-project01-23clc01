from dataclasses import dataclass
from solvers.base import Solver, Node
from definition.board import Board
from typing import Tuple, List, Dict, Optional
import time
from collections import deque
import tracemalloc

class BFSSolver(Solver):
    def solve(self, initial: Board) -> Tuple[List[Tuple[int, int]], Dict]:

        metrics = {
            "search_time": 0.0,
            "nodes_expanded": 0,
            "memory_usage": 0.0,
            "path_cost": 0
        }

        start_time = time.time()
        tracemalloc.start()
        solution_node, nodes_expanded = self._bfs(initial)

        current, memory_peak = tracemalloc.get_traced_memory()
        metrics["memory_usage"] = memory_peak / 1024
        tracemalloc.stop()

        metrics["search_time"] = time.time() - start_time
        metrics["nodes_expanded"] = nodes_expanded
        metrics["path_cost"] = solution_node.path_cost if solution_node else 0

        return self._get_path(solution_node), metrics
    
    def _bfs(self, initial: Board) -> Tuple[Optional[Node], int]:

        nodes_expanded = 0

        start_node = Node(parent=None, state=initial, action=None, path_cost=0)
        if initial.is_goal():
            return start_node, 0

        frontier = deque([start_node])
        reached = {initial: start_node}

        while frontier:
            node = frontier.popleft()
            nodes_expanded += 1
            for action in node.state.get_valid_moves():
                child_state = node.state.apply_move(action[0], action[1])
                child_node = Node(parent=node, state=child_state, action=action, path_cost=node.path_cost + 1)
                if child_state.is_goal():
                    return child_node, nodes_expanded
                if child_state not in reached:
                    reached[child_state] = child_node
                    frontier.append(child_node)
        return None, nodes_expanded

    def _get_path(self, node: Node | None) -> List[Tuple[int, int]]:
        path = []
        if node is None:
            return path
        while node.parent is not None:
            path.append(node.action)
            node = node.parent
        return path[::-1]