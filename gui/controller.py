import pygame
from gui.views import BoardDrawer, draw_text
from definition.board import Board
import time
from gui.views import Button
from gui.views import AnimatedBoardDrawer

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
        self.solution, self.metrics = solver.solve(board) 
        self.states = [board]
        for move in self.solution:
            self.states.append(self.states[-1].apply_move(*move))
        self.current_step = 0
        self.total_steps = len(self.solution)
        self.current_cost = 0

    def draw_menu_ui(self):
        self.screen.blit(self.background, (0, 0))
        

    def draw_static_ui(self):
        draw_text(self.screen, f" Step: {self.current_step}/{self.total_steps}", (990, 60), font_size=30, color=(0, 0, 0))
        draw_text(self.screen, f" Cost: {self.current_cost}", (990, 100), font_size=30, color=(0, 0, 0))

 
    def run(self):
        i = 1
        paused = False
        while True:
            if i >= len(self.states):
                break
            prev_board = self.states[i-1]
            next_board = self.states[i]
            move = self.solution[i-1]
            i += 1
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
                self.draw_static_ui()
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        paused = not paused
                while paused:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            paused = False
                    self.clock.tick(10)
            self.current_step = i - 1
            if self.solver.__class__.__name__ in ['DFSSolver', 'BFSSolver']:
                self.current_cost += 1  
            else:
                self.current_cost += vehicle.length


        self.draw_menu_ui()
        AnimatedBoardDrawer(next_board, self.vehicles_images).draw(self.screen)

        
       
        self.draw_static_ui()
        draw_text(self.screen, f"Search Time: {self.metrics['search_time']:.6f} s", (990, 200), font_size=30, color=(0,0,0))
        draw_text(self.screen, f"Nodes Expanded: {self.metrics['nodes_expanded']}", (990, 250), font_size=30, color=(0,0,0))
        draw_text(self.screen, f"Memory Usage: {self.metrics['memory_usage']} KB", (990, 300), font_size=30, color=(0,0,0))

        pygame.display.flip()
        pygame.time.delay(100)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.clock.tick(30)