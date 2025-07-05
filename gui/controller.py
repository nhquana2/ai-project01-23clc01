import pygame
from gui.views import BoardDrawer, draw_text
from definition.board import Board
import time
from gui.views import Button

class AnimatedBoardDrawer:
    def __init__(self, board, images, anim_vehicle=None, anim_offset=(0,0)):
        self.board = board
        self.images = images
        self.anim_vehicle = anim_vehicle  
        self.anim_offset = anim_offset

    def draw(self, surface):
        color_car, max_color_car = 1, 6
        color_truck, max_color_truck = 1, 4
        for vehicle_id, vehicle in self.board.vehicles.items():
            blitting_pos = self._get_blitting_pos(vehicle)
            if vehicle_id == self.anim_vehicle:
                blitting_pos = (blitting_pos[0] + self.anim_offset[0], blitting_pos[1] + self.anim_offset[1])
            if vehicle_id == 0:
                vehicle_image = self._get_vehicle_image(vehicle, 0, 1)
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
        START_POS = (74, 106)
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

class Controller:
    def __init__(
        self, screen, board, solver, speed, vehicles_images
        , algorithms_list, maps_list, speeds_list,
        map_boards, start_button, exit_button
    ):
        self.screen = screen
        self.board = board
        self.solver = solver
        self.speed = speed  
        self.vehicles_images = vehicles_images
        self.background = self.background = pygame.image.load("assets/images/background_scaled.jpeg").convert()
        self.algorithms_list = algorithms_list
        self.maps_list = maps_list
        self.speeds_list = speeds_list
        self.map_boards = map_boards
        self.start_button = start_button
        self.exit_button = exit_button
        self.clock = pygame.time.Clock()
        self.solution, _ = solver.solve(board)
        self.states = [board]
        for move in self.solution:
            self.states.append(self.states[-1].apply_move(*move))

    def draw_menu_ui(self):
        self.screen.blit(self.background, (0, 0))
        #pause button
        
    def run(self):
        for i in range(1, len(self.states)):
            
            prev_board = self.states[i-1]
            next_board = self.states[i]
            move = self.solution[i-1]
            vehicle_id, direction = move
            vehicle = prev_board.vehicles[vehicle_id]
            if vehicle.orientation == 'H':
                dx = direction * 96
                dy = 0
            else:
                dx = 0
                dy = direction * 96
            steps = 24  
            px_per_frame = (dx // steps, dy // steps)
            offset = [0, 0]
            for step in range(steps):
                self.clock.tick(30 * int(self.speed))  
                offset[0] += px_per_frame[0]
                offset[1] += px_per_frame[1]
                self.draw_menu_ui()
                AnimatedBoardDrawer(prev_board, self.vehicles_images, anim_vehicle=vehicle_id, anim_offset=tuple(offset)).draw(self.screen)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
            self.draw_menu_ui()
            AnimatedBoardDrawer(next_board, self.vehicles_images).draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(100)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.clock.tick(30)