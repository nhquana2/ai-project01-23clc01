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
        self.background = pygame.image.load("assets/images/background_scaled.jpeg").convert()
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
        
        # Game control buttons
        self.play_pause_button = Button(
            pygame.image.load("assets/images/buttons/yellow_button.png"), 
            "PAUSE", 
            (990, 400)
        )
        self.reset_button = Button(
            pygame.image.load("assets/images/buttons/gray_button.png"), 
            "RESET", 
            (990, 480)
        )
        self.back_to_menu_button = Button(
            pygame.image.load("assets/images/buttons/red_button.png"), 
            "MENU", 
            (990, 560)
        )
        
        # Game state
        self.paused = False
        self.finished = False
        self.return_to_menu = False
        self.reset_requested = False

    def draw_static_ui(self):
        self.screen.blit(self.background, (0, 0))
        draw_text(self.screen, f" Step: {self.current_step}/{self.total_steps}", (990, 60), font_size=30, color=(0, 0, 0))
        draw_text(self.screen, f" Cost: {self.current_cost}", (990, 100), font_size=30, color=(0, 0, 0))
        
        # Draw "PAUSED" when paused
        if self.paused:
            draw_text(self.screen, "PAUSED", (990, 150), font_size=32, color=(255, 0, 0))
        
        # Draw control buttons - hide play/pause when finished
        if not self.finished:
            self.play_pause_button.draw(self.screen)
        
        self.reset_button.draw(self.screen)
        
        # Only show back to menu when paused or finished
        if self.paused or self.finished:
            self.back_to_menu_button.draw(self.screen)

    def handle_button_events(self, event):
        """Handle button click events"""
        # Disable play/pause button when finished
        if not self.finished and self.play_pause_button.handle_event(event):
            self.paused = not self.paused
            self.play_pause_button.text = "PLAY" if self.paused else "PAUSE"
            return True
            
        if self.reset_button.handle_event(event):
            # Reset game to initial state
            self.current_step = 0
            self.current_cost = 0
            self.paused = True
            self.finished = False
            self.play_pause_button.text = "PLAY"
            self.reset_requested = True  # Flag to indicate reset was requested
            return True
            
        if (self.paused or self.finished) and self.back_to_menu_button.handle_event(event):
            self.return_to_menu = True
            return True
            
        return False

    def run(self):
        i = 1
        
        while True:
            # return to menu condition
            if self.return_to_menu:
                return
                
            # Handle reset - restart from beginning
            if hasattr(self, 'reset_requested') and self.reset_requested: # if reset_button was pressed
                i = 1
                self.reset_requested = False
                # Draw initial state
                self.draw_static_ui()
                AnimatedBoardDrawer(self.states[0], self.vehicles_images).draw(self.screen)
                pygame.display.flip()
                continue
                
            if i >= len(self.states):
                self.finished = True
                
                break
                
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
                
            if self.speed == 1:      # Slow
                steps = 24
            elif self.speed == 2:    # Medium
                steps = 12
            else:                    # Fast
                steps = 6 
                
            px_per_frame = (dx // steps, dy // steps)
            offset = [0, 0]
            
            for step in range(steps):
                self.clock.tick(30 * int(self.speed))  # Control animation speed
                offset[0] += px_per_frame[0]
                offset[1] += px_per_frame[1]
                
                self.draw_static_ui()  # Draw background and static UI
                AnimatedBoardDrawer(prev_board, self.vehicles_images, anim_vehicle=vehicle_id, anim_offset=tuple(offset)).draw(self.screen)
                pygame.display.flip() # Update the display
                
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    else:
                        self.handle_button_events(event)
                
                # Handle pause state
                while self.paused:
                    self.draw_static_ui()
                    AnimatedBoardDrawer(prev_board, self.vehicles_images, anim_vehicle=vehicle_id, anim_offset=tuple(offset)).draw(self.screen)
                    pygame.display.flip()
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return
                        else:
                            self.handle_button_events(event)
                    
                    # After click menu
                    if self.return_to_menu:
                        return
                    
                    # Check if reset was pressed - break out of animation
                    if hasattr(self, 'reset_requested') and self.reset_requested:
                        break
                        
                    self.clock.tick(10)
                
                # Check if reset was pressed during animation
                if hasattr(self, 'reset_requested') and self.reset_requested:
                    break
                    
                # Check if menu button was pressed
                if self.return_to_menu:
                    return
                    
            # If reset was requested, don't update step and cost, restart loop
            if hasattr(self, 'reset_requested') and self.reset_requested:
                continue
                
            # Update step and cost only after completing the move
            self.current_step = i
            if self.solver.__class__.__name__ in ['DFSSolver', 'BFSSolver']:
                self.current_cost += 1  
            else:
                self.current_cost += vehicle.length
                
            # Move to next step
            i += 1
                
            # Draw the final state and metrics after moving
            # self.draw_static_ui()
            # AnimatedBoardDrawer(next_board, self.vehicles_images).draw(self.screen)
            # draw_text(self.screen, f"Search Time: {self.metrics['search_time']:.6f} s", (990, 200), font_size=30, color=(0,0,0))
            # draw_text(self.screen, f"Nodes Expanded: {self.metrics['nodes_expanded']}", (990, 250), font_size=30, color=(0,0,0))
            # draw_text(self.screen, f"Memory Usage: {self.metrics['memory_usage']} KB", (990, 300), font_size=30, color=(0,0,0))

        pygame.display.flip()
        pygame.time.delay(100)
        
        # Game finished - show final state with buttons
        while not self.return_to_menu:
            if self.finished:
                self.draw_static_ui()
                AnimatedBoardDrawer(self.states[-1], self.vehicles_images).draw(self.screen)
                draw_text(self.screen, f"Search Time: {self.metrics['search_time']:.6f} s", (990, 200), font_size=30, color=(0,0,0))
                draw_text(self.screen, f"Nodes Expanded: {self.metrics['nodes_expanded']}", (990, 250), font_size=30, color=(0,0,0))
                draw_text(self.screen, f"Memory Usage: {self.metrics['memory_usage']:.4f} KB", (990, 300), font_size=30, color=(0,0,0))
                draw_text(self.screen, "PUZZLE SOLVED!", (990, 150), font_size=32, color=(0, 128, 0))
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    else:
                        self.handle_button_events(event)
                        
                # Handle reset when game is finished
                if hasattr(self, 'reset_requested') and self.reset_requested:
                    self.finished = False
                    return self.run()  # Restart the game
                        
                self.clock.tick(30)