from definition.vehicle import Vehicle
from definition.board import Board
from maps import load_map
from solvers.bfs import BFSSolver
from solvers.ucs import UCSSolver
from solvers.astar import AStartSolver

def main():

    board = load_map("maps/map3.json")
    board.display_state()
    solver = UCSSolver()
    #solver = BFSSolver()
    solution, metrics = solver.solve(board)
    print(solution)
    print(len(solution))
    print(metrics)

    #solver = UCSSolver()
    solver = AStartSolver()
    solution, metrics = solver.solve(board)
    print(solution)
    print(len(solution))
    print(metrics)

    # board = load_map("maps/map2.json")

    # board.display_state()

    # new_board = board.apply_move(1, 1)

    # board.display_state()
    # new_board.display_state()

    # print(board.vehicles[1])
    # print(new_board.vehicles[1])

if __name__ == "__main__":
    main()



