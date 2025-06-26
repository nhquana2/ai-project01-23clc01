from typing import List, Tuple, Dict
from definition.vehicle import Vehicle
import copy

class Board:
    BOARD_WIDTH = 6 # Fixed board width 
    BOARD_HEIGHT = 6 # Fixed board height
    """
    Represents a STATE of the game board for Rush Hour.
    Attributes:
    - vehicles: Dict[id, Vehicle]   # mapping vehicle IDs to Vehicle objects
    - occupied: List[List]          # Occupied matrix, storing vehicle IDs, for fast look-up -> save time 
    """

    def __init__(self, vehicles: dict):
        self.vehicles = vehicles
        self.occupied = [[None for _ in range(self.BOARD_WIDTH)] for _ in range(self.BOARD_HEIGHT)]
        for vehicle_id, vehicle in self.vehicles.items():
            for x, y in vehicle.get_coordinates():
                if self.occupied[x][y] is not None:
                    raise ValueError(f"Vehicles collision detected")
                self.occupied[x][y] = vehicle_id

    # ATTENTION !! All these below method, please check using occupied matrix and also remember to update the vehicle's coordinates. @nhquan

    def get_occupied(self) -> List[List]:
        return self.occupied

    def get_valid_moves(self) -> List[Tuple[id, int]]:
        """
        Generates all valid moves.
        Returns a list of (vehicle_id, displacement).
        """
        moves = []
        occupied = self.occupied
        for vehicle_id, vehicle in self.vehicles.items():
            # compute head and tail positions directly
            if vehicle.orientation == 'H':
                head_row = vehicle.row
                head_col = vehicle.col
                tail_row = head_row
                tail_col = head_col - vehicle.length + 1
                # move left
                if tail_col - 1 >= 0 and occupied[tail_row][tail_col - 1] is None:
                    moves.append((vehicle_id, -1))
                # move right
                if head_col + 1 < self.BOARD_WIDTH and occupied[head_row][head_col + 1] is None:
                    moves.append((vehicle_id, 1))
            else:
                head_col = vehicle.col
                head_row = vehicle.row
                tail_col = head_col
                tail_row = head_row - vehicle.length + 1
                # move up
                if tail_row - 1 >= 0 and occupied[tail_row - 1][tail_col] is None:
                    moves.append((vehicle_id, -1))
                # move down
                if head_row + 1 < self.BOARD_HEIGHT and occupied[head_row + 1][head_col] is None:
                    moves.append((vehicle_id, 1))
        return moves
                
    
    def apply_move(self, vehicle_id: int, displacement: int) -> 'Board':
        """
        Applies a move to the Board and returns a new Board state.
        vehicle_id: ID of the vehicle to move.
        displacement: Number of cells to move the vehicle (positive for right/down, negative for left/up).
        """
        new_vehicles = self.vehicles.copy()
        moved = copy.copy(new_vehicles[vehicle_id])
        if moved.orientation == 'H':
            moved.col += displacement
        else:
            moved.row += displacement
        new_vehicles[vehicle_id] = moved
        return Board(new_vehicles)
    
    def is_goal(self) -> bool:
        """
        Checks if the current Board state is a goal state.
        A goal state is defined as the FIXED RED vehicle being in the exit position. (see FAQ Nguyen Thanh Tinh)
        """
        # To-do
        raise NotImplementedError
    
    def __hash__(self):
        """
        Returns a hash of the Board state (for checking reached states).
        """
        return hash(tuple(tuple(row) for row in self.occupied))
    
    def __eq__(self, other):
        """
        Checks if two Board states are the same.
        """
        if not isinstance(other, Board):
            return False
        return self.occupied == other.occupied        
    
    def display_state(self):
        """
        Prints the Board state.
        """
        for row in self.occupied:
            print(' '.join(str(cell) if cell is not None else '.' for cell in row))
        print()
