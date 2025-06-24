from typing import List, Tuple

class Vehicle:
    def __init__(self, id, length, orientation, row, col):
        """
        Initializes a Vehicle instance.
        Attributes:
        - id: Unique ID of the vehicle.
        - length: Length of the vehicle in grid cells.
        - orientation: Orientation of the vehicle ('H' for horizontal or 'V' for vertical).
        - row: Starting row position of the vehicle in the grid.
        - col: Starting column position of the vehicle in the grid.
        """
        self.id = id
        self.length = length
        self.orientation = orientation
        self.row = row
        self.col = col
    
    def get_coordinates(self) -> List[Tuple[int, int]]:
        """
        Returns list of coordinates occupied by the vehicle in the grid.
        Each coordinate is a tuple (row, col).
        """

        # To-do
        raise NotImplementedError