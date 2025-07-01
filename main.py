from definition.vehicle import Vehicle
from definition.board import Board
from maps import load_map
from solvers.bfs import BFSSolver
from solvers.ucs import UCSSolver
from solvers.dfs import DFSSolver
from solvers.astar import AStarSolver
import pygame
from pathlib import Path
from gui.menu import Menu
#from gui.controller import Controller

CONFIG = {
    "algorithms": {
        "DFS": DFSSolver(),
        "BFS": BFSSolver(),
        "UCS": UCSSolver(),
        "A*": AStarSolver(),
    },
    "maps_dir": Path("maps"),
    "speeds": {
        "Slow": 1,
        "Medium": 2,
        "Fast": 3,
    }
}

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Rush Hour - 23CLC01")
    clock = pygame.time.Clock()

    menu = Menu(screen, list(CONFIG["algorithms"].keys()), [f.name for f in CONFIG["maps_dir"].glob("*.json")], list(CONFIG["speeds"].keys()))

    while True:
        choice = menu.run()

        if choice is None: # User quit
            break 

        algorithm_name, map_name, speed = choice

        board = load_map(CONFIG['maps_dir'] / map_name)
        solver = CONFIG["algorithms"][algorithm_name]
        #controller = Controller(screen, board, solver, speed)
        #controller.run()
    
    pygame.quit()


