from definition.vehicle import Vehicle
from definition.board import Board
from maps import load_map
from solvers.bfs import BFSSolver
from solvers.ucs import UCSSolver
from solvers.dfs import DFSSolver
from solvers.astar import AStarSolver
from solvers.heuristic import recursive_blocking_heuristic, simple_heuristic

def main():

    board = load_map("maps/map8.json")
    board.display_state()
    # solver = UCSSolver()
    # solver = BFSSolver()
    # solver = DFSSolver()
    # solution, metrics = solver.solve(board)
    # print(solution)
    # print(len(solution))
    # print(metrics)

    solver = AStarSolver(heuristic=simple_heuristic)
    solver2 = AStarSolver(heuristic=recursive_blocking_heuristic)
    solver3 = UCSSolver()

    solution, metrics = solver.solve(board)
    print("A* simple")
    print(solution)
    print(len(solution))
    print(metrics)

    print("A* recursive")
    solution2, metrics2 = solver2.solve(board)
    print(solution2)
    print(len(solution2))
    print(metrics2)

    print("UCS")
    solution3, metrics3 = solver3.solve(board)
    print(solution3)
    print(len(solution3))
    print(metrics3)

    # board = load_map("maps/map2.json")

    # board.display_state()

    # new_board = board.apply_move(1, 1)

    # board.display_state()
    # new_board.display_state()

    # print(board.vehicles[1])
    # print(new_board.vehicles[1])

if __name__ == "__main__":
    main()


