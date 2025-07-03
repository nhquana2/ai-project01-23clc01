import pygame
from gui.views import draw_text
from gui.views import Selector
from gui.views import BoardDrawer
from gui.views import Button
from maps import load_map
import os
from typing import Tuple

class Menu:
    def __init__(self, screen, algorithms_list, maps_list, speeds_list, map_boards, vehicles_images):
        self.screen = screen
        self.algorithms_list: Selector = Selector(algorithms_list, (990, 130))
        self.maps_list: Selector = Selector(maps_list, (990, 320))
        self.speeds_list: Selector = Selector(speeds_list, (990, 500))
        self.map_boards = map_boards
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("assets/images/background.png").convert()
        self.background = pygame.transform.scale(self.background, (1280, 720))
        self.vehicles_images = vehicles_images
        self.start_button = Button(pygame.image.load("assets/images/buttons/gray_button.png"), "START", (840, 640))
        self.exit_button = Button(pygame.image.load("assets/images/buttons/red_button.png"), "EXIT", (1135, 640))

    def run(self) -> Tuple | None:
        while True:
            self.clock.tick(60)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                self.algorithms_list.handle_event(event)
                self.maps_list.handle_event(event)
                self.speeds_list.handle_event(event)
                if self.start_button.handle_event(event):
                    return (self.algorithms_list.selected, self.maps_list.selected, self.speeds_list.selected)
                if self.exit_button.handle_event(event):
                    return None

            # Background 
            self.screen.blit(self.background, (0, 0))

            # Text 
            draw_text(self.screen, "Choose searching algorithm", (990, 40))
            draw_text(self.screen, "Choose map", (990, 230))
            draw_text(self.screen, "Choose speed", (990, 410))

            # List selectors
            self.algorithms_list.draw(self.screen)
            self.maps_list.draw(self.screen)
            self.speeds_list.draw(self.screen)

            # Board drawer
            board_drawer = BoardDrawer(self.map_boards[self.maps_list.selected], self.vehicles_images)
            board_drawer.draw(self.screen)

            # Buttons
            self.start_button.draw(self.screen)
            self.exit_button.draw(self.screen)

            pygame.display.flip()