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
        pygame.mixer.init()

        self.sfx_move = pygame.mixer.Sound("sfx/move.wav")
        self.sfx_rotate = pygame.mixer.Sound("sfx/rotate.wav")
        self.sfx_drop = pygame.mixer.Sound("sfx/drop.wav")
        self.sfx_line_clear = pygame.mixer.Sound("sfx/line_clr.wav")

        self.last_move_sound = 0
        self.move_sound_delay = 100

        # Game window size and settings
        self.screen_width = 510
        self.screen_height = 600
        self.block_size = 30
        self.board_width = 10
        self.board_height = 20
        self.hold_pressed = False

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
            if now - self.last_move_sound > self.move_sound_delay:
                self.sfx_move.play()
                self.last_move_sound = now

        # Geser kanan
        if keys[pygame.K_RIGHT]:
            if now - getattr(self, 'last_move_right', 0) > move_delay:
                self.board.move_current_brick(1)
                self.last_move_right = now
            if now - self.last_move_sound > self.move_sound_delay:
                self.sfx_move.play()
                self.last_move_sound = now

        # Soft drop
        if keys[pygame.K_DOWN]:
            if now - getattr(self, 'last_soft_drop', 0) > drop_delay:
                self.board.soft_drop()
                self.last_soft_drop = now
                
        if keys[pygame.K_c] and not self.hold_pressed:
            self.hold_pressed = True
            self.board.hold_current_brick()

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
                        self.sfx_rotate.play()
                        self.board.rotate_current_brick()  # Rotasi brick ketika tombol atas ditekan
                    elif event.key == pygame.K_SPACE:
                        self.board.hard_drop()  # Hard drop ketika tombol spasi ditekan
                    elif event.key == pygame.K_c:  # Tombol C untuk hold
                        if not self.board.hold_used and self.board.current_brick:  # Hanya boleh hold sekali per turn
                            self.board.hold_current_brick()  # Menyimpan brick saat tombol C ditekan
                            self.hold_used = True  # Menandakan sudah digunakan


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

            font = pygame.font.SysFont(None, 30)
            text = font.render("Next", True, (80, 80, 80))
            self.screen.blit(text, (self.board_width * self.block_size + 50, 140))
            self.board.draw_next_bricks(self.screen)

            self.board.draw_hold_brick(self.screen)

            font = pygame.font.SysFont(None, 30)
            hold_label = font.render("Hold", True, (80, 80, 80))
            self.screen.blit(hold_label, (self.board_width * self.block_size + 50, 20))


            # Cek game over
            if self.board.game_over:
                print("GAME OVER")
                pygame.quit()
                sys.exit()

            # Update display
            pygame.display.update()

    def __del__(self):
        pygame.mixer.quit()
        print("Audio resources released")

# Create a Game instance and start the game loop
if __name__ == "__main__":
    game = Game()
    game.game_loop()
    del game
