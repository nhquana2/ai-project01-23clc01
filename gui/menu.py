import pygame
from gui.views import draw_text
from gui.views import Selector

class Menu:
    def __init__(self, screen, algorithms_list, maps_list, speeds_list):
        self.screen = screen
        self.algorithms_list = Selector(algorithms_list, (990, 142))
        self.maps_list = Selector(maps_list, (990, 350))
        self.speeds_list = Selector(speeds_list, (990, 550))
        
    def run(self):
        while True:

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                self.algorithms_list.handle_event(event)
                self.maps_list.handle_event(event)
                self.speeds_list.handle_event(event)
            
            # Background 
            background = pygame.image.load("assets/images/background.png").convert()
            background = pygame.transform.scale(background, (1280, 720))
            self.screen.blit(background, (0, 0))

            # Text 
            draw_text(self.screen, "Choose searching algorithm", (990, 30))
            draw_text(self.screen, "Choose map", (990, 240))
            draw_text(self.screen, "Choose speed", (990, 450))

            # List selectors
            self.algorithms_list.draw(self.screen)
            self.maps_list.draw(self.screen)
            self.speeds_list.draw(self.screen)

            pygame.display.flip()