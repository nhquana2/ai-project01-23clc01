from definition.vehicle import Vehicle
from definition.board import Board
from maps import load_map
from solvers.bfs import BFSSolver
from solvers.ucs import UCSSolver
from solvers.dfs import DFSSolver
from solvers.astar import AStarSolver
from solvers.heuristic import recursive_blocking_heuristic, simple_heuristic, advanced_heuristic, custom_heuristic

from definition.vehicle import Vehicle
from definition.board import Board
from maps import load_map
from solvers.bfs import BFSSolver
from solvers.ucs import UCSSolver
from solvers.dfs import DFSSolver
from solvers.astar import AStarSolver
import csv
from typing import List

def main():
    #    # Load map5
    # map_name = "map11.json"
    # full_map_path = f"maps/{map_name}"
    # print(f"Loading {full_map_path}...")
    # board = load_map(full_map_path)

    # # Print the board state using display_state
    # print("Initial board state for map5:")
    # board.display_state()

    # # Choose a solver (example: A* with advanced_heuristic)
    # solver = AStarSolver(heuristic=advanced_heuristic)
    # solution, metrics = solver.solve(board)

    # # Print the length of the solution
    # print(f"Length of solution: {len(solution) if solution is not None else 0}")

    # print("Solution metrics:")
    # for key, value in metrics.items():
    #     print(f"{key}: {value}")
   
   
   
    
    maps: List[Board] = []
    map_names: List[str] = [] 

   
    for i in range(1, 15):
        if i < 10:
            map_name = f"map0{i}.json"
        else:   
            map_name = f"map{i}.json"
        full_map_path = f"maps/{map_name}" 
        print(f"Loading {full_map_path}...")
        maps.append(load_map(full_map_path))
        map_names.append(map_name)

    
    solvers = [
        # {"name": "BFS", "instance": BFSSolver()},
        # {"name": "DFS", "instance": DFSSolver()},
        # {"name": "UCS", "instance": UCSSolver()},
        {"name": "A*", "instance": AStarSolver(heuristic=simple_heuristic)}
    ]

    
    csv_file_path = "rs_astart.csv"
    fieldnames = ['map_name','solver_name','solution_length','search_time_sec','nodes_expanded', 'path_cost', 'memory_usage_kb']

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader() 

        for num, board_map in enumerate(maps):
            current_map_name = map_names[num] 
            

            for solver_info in solvers:
                solver_name = solver_info["name"]
                solver_instance = solver_info["instance"]

                solution, metrics = solver_instance.solve(board_map)

                solution_length = len(solution) if solution is not None else 0 


                row_data = {
                    'map_name': current_map_name,
                    'solver_name': solver_name,
                    'solution_length': solution_length,
                    'search_time_sec': metrics.get('search_time', 'N/A'),
                    'nodes_expanded': metrics.get('nodes_expanded', 'N/A'),
                    'path_cost': metrics.get('path_cost', 'N/A'),
                    'memory_usage_kb': metrics.get('memory_usage', 'N/A')
                }
                writer.writerow(row_data)
                csvfile.flush() 

    print(f"Results saved to {csv_file_path}")


if __name__ == "__main__":
    main()






