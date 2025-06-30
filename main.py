from definition.vehicle import Vehicle
from definition.board import Board
from maps import load_map
from solvers.bfs import BFSSolver
from solvers.ucs import UCSSolver
from solvers.dfs import DFSSolver
from solvers.astar import AStarSolver

def main():

    board = load_map("maps/map2.json")
    board.display_state()
    # solver = UCSSolver()
    # solver = BFSSolver()
    # solver = DFSSolver()
    # solution, metrics = solver.solve(board)
    # print(solution)
    # print(len(solution))
    # print(metrics)

    solver = AStarSolver()
    solver2 = UCSSolver()

    solution, metrics = solver.solve(board)
    print("A*")
    print(solution)
    print(len(solution))
    print(metrics)

    print("UCS")
    solution2, metrics2 = solver2.solve(board)
    print(solution2)
    print(len(solution2))
    print(metrics2)

    # board = load_map("maps/map2.json")

    # board.display_state()

    # new_board = board.apply_move(1, 1)

    # board.display_state()
    # new_board.display_state()

    # print(board.vehicles[1])
    # print(new_board.vehicles[1])

if __name__ == "__main__":
    main()



