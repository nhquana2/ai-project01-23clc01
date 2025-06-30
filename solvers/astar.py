import random
from dataclasses import dataclass 
from solvers.base import Solver, Node
from definition.board import Board
from typing import Tuple, List, Dict, Optional
import time
import heapq
import tracemalloc

class AStarSolver(Solver):
    def solve(self, initial: Board) -> Tuple[List[Tuple[int, int]], Dict]:
        metrics = {
            "search_time": 0,
            "nodes_expanded": 0,
            "memory_usage": 0
        }

        start_time = time.time()
        tracemalloc.start()

        solution_node, nodes_expanded = self._astar(initial)

        _, peak = tracemalloc.get_traced_memory()
        metrics["memory_usage"] = peak / 1024 #kb
        tracemalloc.stop()

        metrics["search_time"] = time.time() - start_time
        metrics["nodes_expanded"] = nodes_expanded

        if solution_node is None:
            return [], metrics
        
        return self._get_path(solution_node), metrics
    
    def _h(self, state: Board) -> int:
        """        
        1. Direct distance: red car (ID 0) to the exit
        2. Blocking vehicles: Number of vehicles blocking the path to exit
        """
        # Target vehicle (red car)
        target_vehicle = state.vehicles[state.TARGET_VEHICLE_ID]
            
        # Calculate direct distance to exit
        target_row = 2  # Fixed exit row defined in Board
        target_col = state.BOARD_WIDTH - 1  # Exit column
            
        # Distance from target vehicle's rightmost position to exit
        right_pos = target_vehicle.col + target_vehicle.length - 1
        direct_distance = target_col - right_pos
        
        # Count blocking vehicles
        blocking_count = 0
        for col in range(right_pos + 1, target_col + 1):
            if state.occupied[target_row][col] is not None:
                blocking_count += 1
                
        # Each blocking vehicle needs at least 1 move to clear
        # Add this to the direct distance the red car needs to move
        print(f"blocking_count in h: {blocking_count}")
        return direct_distance + blocking_count

    def _count_blocking_recursively(self, state: Board, vehicle_id: int, visited: set) -> int:
        """
        Returns the total number of vehicles that must move in the blocking chain.
        """
        if vehicle_id in visited:
            return 0
        
        visited.add(vehicle_id)
        vehicle = state.vehicles[vehicle_id]
        count = 1  # Count this vehicle itself
        
        # Check if this vehicle can move in any direction
        can_move_directly = False
        
        if vehicle.orientation == 'V':
            # Check vertical movement possibilities
            top_row = vehicle.row
            bottom_row = vehicle.row + vehicle.length - 1
            col = vehicle.col
            
            # Move up
            if top_row > 0 and state.occupied[top_row - 1][col] is None:
                can_move_directly = True
            # Move down
            elif bottom_row < state.BOARD_HEIGHT - 1 and state.occupied[bottom_row + 1][col] is None:
                can_move_directly = True
            
            # If can't move directly, check what's blocking it
            if not can_move_directly:
                # Check what's blocking upward movement
                if top_row > 0:
                    blocker_up = state.occupied[top_row - 1][col]
                    if blocker_up is not None and blocker_up not in visited:
                        count += self._count_blocking_recursively(state, blocker_up, visited.copy())
                
                # Check what's blocking downward movement
                if bottom_row < state.BOARD_HEIGHT - 1:
                    blocker_down = state.occupied[bottom_row + 1][col]
                    if blocker_down is not None and blocker_down not in visited:
                        count += self._count_blocking_recursively(state, blocker_down, visited.copy())
                        
        else:  # Horizontal vehicle
            # Check horizontal movement possibilities
            left_col = vehicle.col
            right_col = vehicle.col + vehicle.length - 1
            row = vehicle.row
            
            # Can move left?
            if left_col > 0 and state.occupied[row][left_col - 1] is None:
                can_move_directly = True
            # Can move right?
            elif right_col < state.BOARD_WIDTH - 1 and state.occupied[row][right_col + 1] is None:
                can_move_directly = True
            
            # If can't move directly, check what's blocking it
            if not can_move_directly:
                # Check what's blocking leftward movement
                if left_col > 0:
                    blocker_left = state.occupied[row][left_col - 1]
                    if blocker_left is not None and blocker_left not in visited:
                        count += self._count_blocking_recursively(state, blocker_left, visited.copy())
                
                # Check what's blocking rightward movement
                if right_col < state.BOARD_WIDTH - 1:
                    blocker_right = state.occupied[row][right_col + 1]
                    if blocker_right is not None and blocker_right not in visited:
                        count += self._count_blocking_recursively(state, blocker_right, visited.copy())
        
        return count

    def _h2(self, state: Board) -> int:
        """
        heuristic that recursively counts blocking cars.
        Starts from cars between red car and exit, then recursively counts
        all vehicles that need to move to clear the path.
        """
        # Target vehicle (red car)
        target_vehicle = state.vehicles[state.TARGET_VEHICLE_ID]
        
        # Calculate direct distance to exit
        target_row = 2  # Fixed exit row defined in Board
        target_col = state.BOARD_WIDTH - 1  # Exit column
        
        # Distance from target vehicle's rightmost position to exit
        right_pos = target_vehicle.col + target_vehicle.length - 1
        direct_distance = target_col - right_pos
        
        # If already at exit, no moves needed
        if direct_distance <= 0:
            return 0
        
        # Recursively count all vehicles that need to move
        total_blocking_count = 0
        global_visited = set()
        
        # Start from each car directly blocking the red car's path
        for col in range(right_pos + 1, target_col + 1):
            blocker_id = state.occupied[target_row][col]
            if blocker_id is not None and blocker_id not in global_visited:
                # Recursively count this blocking chain
                blocking_chain_count = self._count_blocking_recursively(state, blocker_id, set())
                total_blocking_count += blocking_chain_count
                global_visited.add(blocker_id)
        
        print(f"total_blocking_count in h2: {total_blocking_count}")
        # Total heuristic: direct distance + total vehicles that need to move
        return direct_distance + total_blocking_count

    def _astar(self, initial: Board) -> Tuple[Optional[Node], int]:
       
        start_node = Node(parent=None, state=initial, action=None, path_cost=0)
        if initial.is_goal():
            return start_node, 0

        nodes_expanded = 0
        
        start_h_cost = self._h2(initial)
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
                
                new_h_cost = self._h2(child_state)
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