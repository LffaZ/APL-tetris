# tetris.py
import pygame
import sys
from constants import BACKGROUND_COLOR
from board import Board
from bricks import IShape, OShape, TShape, SShape, ZShape

# Setup pygame
pygame.init()

# Ukuran layar dan board
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30  # Ukuran tiap petak di board
BOARD_WIDTH = 10  # 10 kolom
BOARD_HEIGHT = 20  # 20 baris

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

# Inisialisasi board
board = Board(BOARD_WIDTH, BOARD_HEIGHT, BLOCK_SIZE)
i_shape = IShape(BLOCK_SIZE)
o_shape = OShape(BLOCK_SIZE)
t_shape = TShape(BLOCK_SIZE)
s_shape = SShape(BLOCK_SIZE)
z_shape = ZShape(BLOCK_SIZE)

# Game loop
def game_loop():
    while True:
        screen.fill(BACKGROUND_COLOR)  # Set background color

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the board
        board.draw(screen)

        i_shape.draw(screen, 3, 0)  # Position the I shape at (3, 0)
        o_shape.draw(screen, 5, 2)  # Position the O shape at (5, 2)
        t_shape.draw(screen, 2, 5)  # Position the T shape at (2, 5)
        s_shape.draw(screen, 7, 5)  # Position the S shape at (7, 5)
        z_shape.draw(screen, 4, 7)

        # Update display
        pygame.display.update()

# Jalankan game
game_loop()
