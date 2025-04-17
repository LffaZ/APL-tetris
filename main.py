import pygame
import random
import sys
from constants import BACKGROUND_COLOR
from board import Board
from bricks import IShape, OShape, TShape, SShape, ZShape

class Game:
    def __init__(self):
        # Setup pygame
        pygame.init()

        # Game window size and settings
        self.screen_width = 510
        self.screen_height = 600
        self.block_size = 30
        self.board_width = 10
        self.board_height = 20

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Tetris')

        # Initialize the board
        self.board = Board(self.board_width, self.board_height, self.block_size)

        # Initialize the first shape
        self.board.spawn_new_brick()

        self.last_fall_time = pygame.time.get_ticks()  # Time of the last brick fall
        self.fall_delay = 500  # Set delay for falling speed (milliseconds)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        now = pygame.time.get_ticks()

        # Movement cooldowns
        move_delay = 100  # ms
        drop_delay = 80   # ms

        # Geser kiri
        if keys[pygame.K_LEFT]:
            if now - getattr(self, 'last_move_left', 0) > move_delay:
                self.board.move_current_brick(-1)
                self.last_move_left = now

        # Geser kanan
        if keys[pygame.K_RIGHT]:
            if now - getattr(self, 'last_move_right', 0) > move_delay:
                self.board.move_current_brick(1)
                self.last_move_right = now

        # Soft drop
        if keys[pygame.K_DOWN]:
            if now - getattr(self, 'last_soft_drop', 0) > drop_delay:
                self.board.soft_drop()
                self.last_soft_drop = now

    def game_loop(self):
        """Main game loop"""
        while True:
            self.screen.fill(BACKGROUND_COLOR)
            self.handle_input()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.board.rotate_current_brick()
                        # self.rotate_pressed = False
                    elif event.key == pygame.K_SPACE:
                        self.board.hard_drop()
                


            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Check if it's time for the next fall
            current_time = pygame.time.get_ticks()
            if current_time - self.last_fall_time >= self.fall_delay:
                # Update the board (falling logic)
                self.board.update()

                # Update the time of the last fall
                self.last_fall_time = current_time

            # Draw the board and the current brick
            self.board.draw(self.screen)
            self.board.draw_ghost(self.screen)

            font = pygame.font.SysFont(None, 36)
            text = font.render("Next", True, (80, 80, 80))
            self.screen.blit(text, (self.board_width * self.block_size + 50, 130))
            self.board.draw_next_bricks(self.screen)

            # Cek game over
            if self.board.game_over:
                print("GAME OVER")
                pygame.quit()
                sys.exit()

            # Update display
            pygame.display.update()

# Create a Game instance and start the game loop
if __name__ == "__main__":
    game = Game()
    game.game_loop()
