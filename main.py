from definition.vehicle import Vehicle
from definition.board import Board
from maps import load_map
from solvers.bfs import BFSSolver

def main():

    board = load_map("maps/map2.json")
    board.display_state()
    solver = BFSSolver()
    solution, metrics = solver.solve(board)
    print(solution)
    print(len(solution))
    print(metrics)

if __name__ == "__main__":
    main()



