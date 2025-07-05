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
from gui.controller import Controller
import os
from typing import Tuple

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Rush Hour - 23CLC01")

CONFIG = {
    "algorithms": {
        "DFS": DFSSolver(),
        "BFS": BFSSolver(),
        "UCS": UCSSolver(),
        "A*": AStarSolver(),
    },
    "maps_dir": Path("maps"),
    "map_names": [f.name for f in Path("maps").glob("*.json")],
    "speeds": {
        "Slow": 1,
        "Medium": 2,
        "Fast": 3,
    },
    "map_boards": {map_name: load_map("maps/" + map_name) for map_name in [f.name for f in Path("maps").glob("*.json")]},
    "vehicles_images": {image_name: pygame.image.load("assets/images/vehicles/" + image_name).convert_alpha() for image_name in os.listdir("assets/images/vehicles/")}
}

if __name__ == "__main__":

    menu = Menu(
        screen,
        list(CONFIG["algorithms"].keys()),
        CONFIG["map_names"],
        list(CONFIG["speeds"].keys()),
        CONFIG["map_boards"],
        CONFIG["vehicles_images"]
    )

    while True:
        choice: Tuple | None = menu.run()

        if choice is None:  # User quit
            break

        algorithm_name, map_name, speed = choice

        board = load_map(CONFIG['maps_dir'] / map_name)
        solver = CONFIG["algorithms"][algorithm_name]

        controller = Controller(
            screen,
            board,
            solver,
            CONFIG["speeds"][speed],
            CONFIG["vehicles_images"],
            menu.algorithms_list,
            menu.maps_list,
            menu.speeds_list,
            CONFIG["map_boards"],
            menu.start_button,
            menu.exit_button
        )
        controller.run()

    pygame.quit()


