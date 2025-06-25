from typing import List, Tuple, Dict
from definition.vehicle import Vehicle

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
        moves = [] # List of possible move
        occupied = self.occupied
        for vehicle_id, vehicle in self.vehicles.items():
            coords = vehicle.get_coordinates()
            if vehicle.orientation == 'H':
                row = coords[0][0]
                cols = [c for _, c in coords]
                leftmost, rightmost = min(cols), max(cols)
                # move left 
                if leftmost - 1 >= 0 and occupied[row][leftmost - 1] is None:
                    moves.append((vehicle_id, -1))
                # move right 
                print(rightmost)
                if rightmost + 1 < self.BOARD_WIDTH and occupied[row][rightmost + 1] is None:
                    moves.append((vehicle_id, 1))
            else:
                col = coords[0][1]
                rows = [r for r, _ in coords]
                topmost, bottommost = min(rows), max(rows)
                # move up 
                if topmost - 1 >= 0 and occupied[topmost - 1][col] is None:
                    moves.append((vehicle_id, -1))
                # move down 
                if bottommost + 1 < self.BOARD_HEIGHT and occupied[bottommost + 1][col] is None:
                    moves.append((vehicle_id, 1))
        return moves
                
    
    def apply_move(self, vehicle_id: int, displacement: int) -> 'Board':
        """
        Applies a move to the Board and returns a new Board state.
        vehicle_id: ID of the vehicle to move.
        displacement: Number of cells to move the vehicle (positive for right/down, negative for left/up).
        """
        new_vehicles = {}
        for vehicle_id, vehicle in self.vehicles.items():
            new_vehicle = Vehicle(vehicle.length, vehicle.orientation, vehicle.row, vehicle.col) #may implement clone method in Vehicle
            if vehicle_id == vehicle_id:
                if new_vehicle.orientation == 'H':
                    new_vehicle.col += displacement
                else:
                    new_vehicle.row += displacement
            new_vehicles[vehicle_id] = new_vehicle
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
        # To-do
        raise NotImplementedError
    
    def __eq__(self, other):
        """
        Checks if two Board states are the same.
        """
        # To-do
        raise NotImplementedError