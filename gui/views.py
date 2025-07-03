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
        self.selected: str | None = items[0] if items else None

        self.prev_button = pygame.image.load("assets/images/buttons/prev_button.png")
        self.prev_button = pygame.transform.scale(self.prev_button, (60, 60))
        self.prev_button_rect = self.prev_button.get_rect(center=(self.pos[0] - 160, self.pos[1]))

        self.next_button = pygame.image.load("assets/images/buttons/next_button.png").convert_alpha()
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

class Button:
    def __init__(self, image, text, pos):
        self.image = image
        self.image = pygame.transform.smoothscale(self.image, (258, 74))
        self.text = text
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        draw_text(surface, self.text, (self.pos[0], self.pos[1] - 8), 24, color=(255, 255, 255))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class BoardDrawer:
    def __init__(self, board, images):
        self.board = board
        self.images = images
    
    def draw(self, surface):
        color_car, max_color_car = 1, 6
        color_truck, max_color_truck = 1, 4

        for vehicle_id, vehicle in self.board.vehicles.items():
            blitting_pos = self._get_blitting_pos(vehicle)
            if vehicle_id == 0:
                vehicle_image = self._get_vehicle_image(vehicle, 0, color_truck)
            else:
                vehicle_image = self._get_vehicle_image(vehicle, color_car, color_truck)

            surface.blit(vehicle_image, blitting_pos)

            if vehicle.length == 2 and vehicle_id != 0:
                color_car = color_car + 1
                if color_car > max_color_car:   
                    color_car = 1
            elif vehicle.length == 3:
                color_truck = color_truck + 1
                if color_truck > max_color_truck:
                    color_truck = 1

    def _get_blitting_pos(self, vehicle):
        START_POS = (74, 106) # (0, 0) blitting position on the screen
        return (START_POS[0] + vehicle.col * 96, START_POS[1] + vehicle.row * 96)

    def _get_vehicle_image(self, vehicle, color_car, color_truck):
        image_name = ""

        if vehicle.length == 2:
            image_name = "car" + str(color_car) + ".png"
        else:
            image_name = "truck" + str(color_truck) + ".png"
    
        image = self.images[image_name]
        
        if vehicle.length == 2:
            image = pygame.transform.smoothscale(image, (83, 179))
        else:
            image = pygame.transform.smoothscale(image, (83, 275))
        
        if vehicle.orientation == "H":
            image = pygame.transform.rotate(image, -90)

        return image

