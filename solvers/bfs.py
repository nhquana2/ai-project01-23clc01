from dataclasses import dataclass
from solvers.base import Solver, Node
from definition.board import Board
from typing import Tuple, List, Dict, Optional, Set
import time
from collections import deque
import tracemalloc

class BFSSolver(Solver):
    def _search(self, initial: Board) -> Tuple[Optional[Node], int]:

        nodes_expanded = 0

        start_node = Node(parent=None, state=initial, action=None, path_cost=0)
        if initial.is_goal():
            return start_node, 0

        frontier = deque([start_node])
        reached: Set[Board] = {initial}

        while frontier:
            node = frontier.popleft()
            nodes_expanded += 1
            for action in node.state.get_valid_moves():
                child_state = node.state.apply_move(action[0], action[1])
                child_node = Node(parent=node, state=child_state, action=action, path_cost=node.path_cost + 1)

                if child_state.is_goal():
                    return child_node, nodes_expanded
                    
                if child_state not in reached:
                    reached.add(child_state)
                    frontier.append(child_node)

        return None, nodes_expanded
