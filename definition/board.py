from typing import List, Tuple, Dict

class Board:
    """
    Represents a STATE of the game board for Rush Hour.
    Attributes:
    - vehicles: Dict[id, Vehicle]   # mapping vehicle IDs to Vehicle objects
    - size: int                     # board width/height (square), in our project, fixed = 6
    """

    def __init__(self, vehicles: dict, size: int = 6):
        self.vehicles = vehicles
        self.size = size
    
    def get_valid_moves(self) -> List[Tuple[id, int]]:
        """
        Generates all valid moves.
        Returns a list of (vehicle_id, displacement).
        """
        # To-do
        raise NotImplementedError
    
    def apply_move(self, vehicle_id: int, displacement: int) -> 'Board':
        """
        Applies a move to the Board and returns a new Board state.
        vehicle_id: ID of the vehicle to move.
        displacement: Number of cells to move the vehicle (positive for right/down, negative for left/up).
        """
        # To-do
        raise NotImplementedError
    
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
        raise NotImplementedError
    
    def __eq__(self, other):
        """
        Checks if two Board states are the same.
        """
        raise NotImplementedError