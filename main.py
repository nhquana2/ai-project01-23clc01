from definition.vehicle import Vehicle
from definition.board import Board
from maps import load_map

def main():

    board = load_map("maps/map1.json")
    moves = board.get_valid_moves()
    print(board.vehicles.values())
    board.display_state()
    board_new = board.apply_move(2, -1)
    board_new.display_state()
    print(board_new.get_valid_moves())
    board.display_state()

if __name__ == "__main__":
    main()



