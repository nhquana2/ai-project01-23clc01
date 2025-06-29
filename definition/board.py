from typing import List, Tuple, Dict
from definition.vehicle import Vehicle
import copy

class Board:

    """
    Represents a STATE of the game board for Rush Hour.
    Attributes:
    - vehicles: Dict[id, Vehicle]   # mapping vehicle IDs to Vehicle objects
    - occupied: List[List]          # Occupied matrix, storing vehicle IDs, for fast look-up -> save time 
    """

    BOARD_WIDTH = 6 # Fixed board width 
    BOARD_HEIGHT = 6 # Fixed board height
    TARGET_VEHICLE_ID = 0 # ID of the red vehicle, fixed by default (see FAQ Nguyen Thanh Tinh)

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
                # Horizontal vehicle
                head_row, head_col = vehicle.row, vehicle.col
                tail_col = head_col + vehicle.length - 1
                # move left
                if head_col - 1 >= 0 and occupied[head_row][head_col - 1] is None:
                    moves.append((vehicle_id, -1))
                # move right
                if tail_col + 1 < self.BOARD_WIDTH and occupied[head_row][tail_col + 1] is None:
                    moves.append((vehicle_id, 1))
            else:
                # Vertical vehicle
                head_row, head_col = vehicle.row, vehicle.col
                tail_row = head_row + vehicle.length - 1
                # move up
                if head_row - 1 >= 0 and occupied[head_row - 1][head_col] is None:
                    moves.append((vehicle_id, -1))
                # move down
                if tail_row + 1 < self.BOARD_HEIGHT and occupied[tail_row + 1][head_col] is None:
                    moves.append((vehicle_id, 1))
        return moves
                
    
    def apply_move(self, vehicle_id: int, displacement: int) -> 'Board':
        """
        Applies a move to the Board and returns a new Board state.
        vehicle_id: ID of the vehicle to move.
        displacement: Number of cells to move the vehicle (positive for right/down, negative for left/up).
        """

        board = Board.__new__(Board) # This won't call __init__

        board.vehicles = self.vehicles.copy() # Shallow copy vehicles

        board.occupied = [row[:] for row in self.occupied] # Shallow copy, row[:] is a copy of the row (int, None are immutable)
        # Group members, remember to research on shallow copy and deep copy

        vehicle = Vehicle(
            length=self.vehicles[vehicle_id].length,
            orientation=self.vehicles[vehicle_id].orientation,
            row=self.vehicles[vehicle_id].row,
            col=self.vehicles[vehicle_id].col 
        ) # Construct this and assign to board.vehicles[vehicle_id] later

        if vehicle.orientation == 'H':
            old_row, old_col = vehicle.row, vehicle.col
            if displacement == 1:
                # Move right
                board.occupied[old_row][old_col] = None
                board.occupied[old_row][old_col + vehicle.length] = vehicle_id
            else:
                # Move left
                board.occupied[old_row][old_col + vehicle.length - 1] = None
                board.occupied[old_row][old_col - 1] = vehicle_id
            vehicle.col += displacement
        else:
            old_row, old_col = vehicle.row, vehicle.col
            if displacement == 1:
                # Move down
                board.occupied[old_row][old_col] = None
                board.occupied[old_row + vehicle.length][old_col] = vehicle_id
            else:
                # Move up
                board.occupied[old_row + vehicle.length - 1][old_col] = None
                board.occupied[old_row - 1][old_col] = vehicle_id
            vehicle.row += displacement

        board.vehicles[vehicle_id] = vehicle # Remember assigning back!!

        return board
    
    def is_goal(self) -> bool:
        """
        Checks if the current Board state is a goal state.
        A goal state is defined as the FIXED RED vehicle being in the exit position. (see FAQ Nguyen Thanh Tinh)
        """
        exit_row = 2
        exit_col = self.BOARD_WIDTH - 1

        return self.occupied[exit_row][exit_col] == self.TARGET_VEHICLE_ID
    
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
        