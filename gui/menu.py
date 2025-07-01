import pygame
from gui.views import draw_text

class Menu:
    def __init__(self, screen, algorithms, maps):
        self.screen = screen
        self.algorithms = algorithms
        self.maps = maps
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
            self.screen.fill((255, 255, 255))
            background = pygame.image.load("assets/images/background.png").convert()
            background = pygame.transform.scale(background, (1280, 720))
            self.screen.blit(background, (0, 0))
            draw_text(self.screen, "Choose searching algorithm", (750, 10))
            pygame.display.flip()