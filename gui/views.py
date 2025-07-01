import pygame 

def draw_text(surface, text, pos, font_size=28, color=(0,0,0)):
    font = pygame.font.Font("assets/fonts/Grand9KPixel.ttf", font_size)
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, pos)