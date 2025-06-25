from definition.vehicle import Vehicle
from definition.board import Board

# For debug testing only
def pretty_print(grid):
    width = 6
    for row in grid:
        print(" ".join(f"{str(x):>{width}}" for x in row))

def main():
    # Test Vehicle class
    vehicle = Vehicle(length=3, orientation='V', row=4, col=2)
    vehicle2 = Vehicle(length=2, orientation='H', row=5, col = 5)
    vehicle3 = Vehicle(length=2, orientation='H', row=5, col = 4)
    print(vehicle.get_coordinates())
    # Test Board
    board = Board(vehicles={4: vehicle, 1: vehicle2, 3: vehicle3})
    pretty_print(board.get_occupied())

main()