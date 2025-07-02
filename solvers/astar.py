import random
from dataclasses import dataclass 
from solvers.base import Solver, Node
from solvers.heuristic import simple_heuristic, recursive_blocking_heuristic
from definition.board import Board
from typing import Tuple, List, Dict, Optional, Callable
import time
import heapq
import tracemalloc

class AStarSolver(Solver):
    def __init__(self, heuristic: Callable[[Board], int] = recursive_blocking_heuristic):

        self.heuristic = heuristic
    
    def solve(self, initial: Board) -> Tuple[List[Tuple[int, int]], Dict]:
        metrics = {
            "search_time": 0,
            "nodes_expanded": 0,
            "memory_usage": 0,
            "path_cost": 0
        }

        start_time = time.time()
        tracemalloc.start()

        solution_node, nodes_expanded = self._astar(initial)

        _, peak = tracemalloc.get_traced_memory()
        metrics["memory_usage"] = peak / 1024 #kb
        tracemalloc.stop()

        metrics["search_time"] = time.time() - start_time
        metrics["nodes_expanded"] = nodes_expanded
        metrics["path_cost"] = solution_node.path_cost if solution_node else 0

        if solution_node is None:
            return [], metrics
        
        return self._get_path(solution_node), metrics

    def _astar(self, initial: Board) -> Tuple[Optional[Node], int]:
       
        start_node = Node(parent=None, state=initial, action=None, path_cost=0)
        if initial.is_goal():
            return start_node, 0

        nodes_expanded = 0
        
        start_h_cost = self.heuristic(initial)
        start_f_cost = start_node.path_cost + start_h_cost 
        
        tie_breaker_id = 0

        frontier: List[Tuple[int, int, Node]] = []
        heapq.heappush(frontier, (start_f_cost, tie_breaker_id, start_node))
        
        reached: Dict[Board, Node] = {initial: start_node} 

        while frontier:
            _, _, node = heapq.heappop(frontier)

            if node.path_cost > reached[node.state].path_cost: 
                continue 
            nodes_expanded += 1

            if node.state.is_goal():
                return node, nodes_expanded
            
            for action in node.state.get_valid_moves():
                child_state = node.state.apply_move(action[0], action[1])
                new_g_cost = node.path_cost + int(node.state.vehicles[action[0]].length)
                
                new_h_cost = self.heuristic(child_state)
                # new_h_cost = 0
                new_f_cost = new_g_cost + new_h_cost
                
                if child_state not in reached or new_g_cost < reached[child_state].path_cost:
                    child_node = Node(parent=node,state=child_state,action=action,path_cost=new_g_cost )
                    
                    reached[child_state] = child_node
                    
                    tie_breaker_id += 1 
                    heapq.heappush(frontier, (new_f_cost, tie_breaker_id, child_node))

        return None, nodes_expanded 

    def _get_path(self, node: Node) -> List[Tuple[int, int]]:
        """
        Reconstructs the path from the goal node to the initial node.
        """
        path = []
        while node.parent is not None:
            path.append(node.action)
            node = node.parent
        return path[::-1] 