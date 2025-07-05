from definition.board import Board
from typing import Dict, List, Tuple, Optional, Set


def simple_heuristic(state: Board) -> int:
    """        
    1. Direct distance: red car (ID 0) to the exit
    2. Blocking vehicles: Sum of lengths of vehicles blocking the path to exit
    """
    # Target vehicle (red car)
    target_vehicle = state.vehicles[state.TARGET_VEHICLE_ID]
        
    # Calculate direct distance to exit
    target_row = 2  # Fixed exit row defined in Board
    target_col = state.BOARD_WIDTH - 1  # Exit column
        
    # Distance from target vehicle's rightmost position to exit
    right_pos = target_vehicle.col + target_vehicle.length - 1
    direct_distance = target_col - right_pos
    
    # Sum lengths of blocking vehicles
    blocking_cost = 0
    for col in range(right_pos + 1, target_col + 1):
        blocker_id = state.occupied[target_row][col]
        if blocker_id is not None:
            blocking_cost += state.vehicles[blocker_id].length
            
    # Each blocking vehicle's cost is its length
    # Add this to the direct distance the red car needs to move
    # print(f"blocking_cost in h: {blocking_cost}")
    return direct_distance + blocking_cost

def custom_heuristic(state: Board) -> int:
    # --- Direct distance component ---------------------------------------
    target_vehicle = state.vehicles[state.TARGET_VEHICLE_ID]
    target_row = 2                      # Exit row (fixed)
    target_col = state.BOARD_WIDTH - 1  # Exit column

    right_pos = target_vehicle.col + target_vehicle.length - 1
    direct_distance = target_col - right_pos

    # --- Blocking cost component -----------------------------------------
    blocking_cost = 0
    for col in range(right_pos + 1, target_col + 1):
        blocker_id = state.occupied[target_row][col]
        if blocker_id is not None:
            if state.vehicles[blocker_id].orientation == 'V':
                if state.vehicles[blocker_id].length == 2:
                    blocking_cost += 2
                    head_blocker = state.vehicles[blocker_id].row
                    tail_blocker = state.vehicles[blocker_id].row + state.vehicles[blocker_id].length - 1
                    if state.occupied[head_blocker - 1][col] is not None:
                        blocking_cost += state.vehicles[state.occupied[head_blocker - 1][col]].length
                    if state.occupied[tail_blocker + 1][col] is not None:
                        blocking_cost += state.vehicles[state.occupied[tail_blocker + 1][col]].length
                else:
                    head_blocker = state.vehicles[blocker_id].row
                    tail_blocker = state.vehicles[blocker_id].row + state.vehicles[blocker_id].length - 1
                    target_blocker_row = 3
                    blocking_cost += 3 * (target_blocker_row - head_blocker)
                    if state.occupied[tail_blocker + 1][col] is not None:
                        blocking_cost += state.vehicles[state.occupied[tail_blocker + 1][col]].length
                    if state.occupied[head_blocker - 1][col] is not None:
                        blocking_cost += state.vehicles[state.occupied[head_blocker - 1][col]].length
            else:
                return 0
    return direct_distance + blocking_cost 

def advanced_heuristic(state: Board) -> int:
    """
    Advanced heuristic that counts the number of blocking vehicles and their lengths.
    """
    # Target vehicle (red car)
    target_vehicle = state.vehicles[state.TARGET_VEHICLE_ID]
        
    # Calculate direct distance to exit
    target_row = 2  # Fixed exit row defined in Board
    target_col = state.BOARD_WIDTH - 1  # Exit column
        
    # Distance from target vehicle's rightmost position to exit
    right_pos = target_vehicle.col + target_vehicle.length - 1
    direct_distance = target_col - right_pos
    
    # Sum lengths of blocking vehicles
    blocking_cost = 0
    for col in range(right_pos + 1, target_col + 1):
        blocker_id = state.occupied[target_row][col]
        if blocker_id is not None:
            if state.vehicles[blocker_id].orientation == 'V':
                if state.vehicles[blocker_id].length == 2: # case length of blocking car = 2
                    blocking_cost += 2
                    head_blocker = state.vehicles[blocker_id].row
                    tail_blocker = state.vehicles[blocker_id].row + state.vehicles[blocker_id].length - 1
                    head_cost = 0
                    tail_cost = 0
                    if state.occupied[head_blocker - 1][col] is not None and state.occupied[tail_blocker + 1][col] is not None:
                        head_cost = state.vehicles[state.occupied[head_blocker - 1][col]].length
                        tail_cost = state.vehicles[state.occupied[tail_blocker + 1][col]].length
                        blocking_cost += (head_cost + tail_cost)
                    elif state.occupied[head_blocker - 1][col] is None and state.occupied[tail_blocker + 1][col] is not None:
                        tail_cost = state.vehicles[state.occupied[tail_blocker + 1][col]].length
                        blocking_cost += tail_cost
                    elif state.occupied[head_blocker - 1][col] is not None and state.occupied[tail_blocker + 1][col] is None:
                        head_cost = state.vehicles[state.occupied[head_blocker - 1][col]].length
                        blocking_cost += head_cost
                    else:
                        blocking_cost += 0

                else: # case length of blocking car > 3
                    head_blocker = state.vehicles[blocker_id].row
                    tail_blocker = state.vehicles[blocker_id].row + state.vehicles[blocker_id].length - 1
                    target_blocker_row = 3
                    blocking_cost += 3 * (target_blocker_row - head_blocker)
                    tail_cost = 0
                    head_cost = 0

                    if state.occupied[head_blocker - 1][col] is not None and state.occupied[tail_blocker + 1][col] is not None:
                        head_cost = state.vehicles[state.occupied[head_blocker - 1][col]].length
                        tail_cost = state.vehicles[state.occupied[tail_blocker + 1][col]].length
                        blocking_cost += (tail_cost)
                    elif state.occupied[head_blocker - 1][col] is None and state.occupied[tail_blocker + 1][col] is not None:
                        tail_cost = state.vehicles[state.occupied[tail_blocker + 1][col]].length
                        blocking_cost += tail_cost
                    elif state.occupied[head_blocker - 1][col] is not None and state.occupied[tail_blocker + 1][col] is None:
                        head_cost = state.vehicles[state.occupied[head_blocker - 1][col]].length
                        blocking_cost += head_cost
                    else:
                        blocking_cost += 0
            else:
                return 0
            
    return direct_distance + blocking_cost

def count_blocking_recursively(state: Board, vehicle_id: int, visited: set) -> int:
    """
    Returns the total cost (sum of lengths) of vehicles that must move in the blocking chain.
    """
    if vehicle_id in visited:
        return 0
    
    visited.add(vehicle_id)
    vehicle = state.vehicles[vehicle_id]
    cost = vehicle.length  # Cost is the length of this vehicle
    
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
                    cost += count_blocking_recursively(state, blocker_up, visited)
            
            # Check what's blocking downward movement
            if bottom_row < state.BOARD_HEIGHT - 1:
                blocker_down = state.occupied[bottom_row + 1][col]
                if blocker_down is not None and blocker_down not in visited:
                    cost += count_blocking_recursively(state, blocker_down, visited)
                    
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
                    cost += count_blocking_recursively(state, blocker_left, visited)
            
            # Check what's blocking rightward movement
            if right_col < state.BOARD_WIDTH - 1:
                blocker_right = state.occupied[row][right_col + 1]
                if blocker_right is not None and blocker_right not in visited:
                    cost += count_blocking_recursively(state, blocker_right, visited)
    
    return cost

def recursive_blocking_heuristic(state: Board) -> int:
    """
    heuristic that recursively counts blocking cars with their lengths as costs.
    Starts from cars between red car and exit, then recursively counts
    all vehicles that need to move to clear the path, weighted by their lengths.
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
    
    # Recursively count all vehicles that need to move, weighted by their lengths
    total_blocking_cost = 0
    global_visited = set()
    
    # Start from each car directly blocking the red car's path
    for col in range(right_pos + 1, target_col + 1):
        blocker_id = state.occupied[target_row][col]
        if blocker_id is not None and blocker_id not in global_visited:
            # Recursively count this blocking chain with length-based costs
            blocking_chain_cost = count_blocking_recursively(state, blocker_id, global_visited)
            total_blocking_cost += blocking_chain_cost
    
    # print(f"total_blocking_cost in h2: {total_blocking_cost}")
    # Total heuristic: direct distance + total cost of vehicles that need to move
    return direct_distance + total_blocking_cost 
