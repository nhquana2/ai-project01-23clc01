import pygame 

def draw_text(surface, text, pos, font_size=28, color=(0,0,0)):
    font = pygame.font.Font("assets/fonts/Grand9KPixel.ttf", font_size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=pos)
    surface.blit(text_surf, text_rect)

class Selector:
    def __init__(self, items, pos):
        self.items = items
        self.pos = pos
        self.selected = items[0] if items else None

        self.prev_button = pygame.image.load("assets/images/prev_button.png")
        self.prev_button = pygame.transform.scale(self.prev_button, (60, 60))
        self.prev_button_rect = self.prev_button.get_rect(center=(self.pos[0] - 160, self.pos[1]))

        self.next_button = pygame.image.load("assets/images/next_button.png").convert_alpha()
        self.next_button = pygame.transform.scale(self.next_button, (60, 60))
        self.next_button_rect = self.next_button.get_rect(center=(self.pos[0] + 160, self.pos[1]))

    def draw(self, surface):
        surface.blit(self.prev_button, self.prev_button_rect)
        surface.blit(self.next_button, self.next_button_rect)
        draw_text(surface, self.selected, self.pos, 28)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.prev_button_rect.collidepoint(event.pos):
                self.selected = self.items[(self.items.index(self.selected) - 1) % len(self.items)]
            elif self.next_button_rect.collidepoint(event.pos):
                self.selected = self.items[(self.items.index(self.selected) + 1) % len(self.items)]