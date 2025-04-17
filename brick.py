import pygame
from constants import GRID_COLOR, WHITE, OUTLINE

class Brick:
    def __init__(self, block_size, color, x, y):
        self.block_size = block_size
        self.color = color
        self.x = x  # Initial x position
        self.y = y  # Initial y position
        self.shape = []  # Shape coordinates will be defined in child classes

    def draw(self, screen):
        """Draw the blocks for the shape."""
        for x, y in self.shape:
            rect = pygame.Rect((x + self.x) * self.block_size, 
                               (y + self.y) * self.block_size, 
                               self.block_size, self.block_size)
            pygame.draw.rect(screen, self.color, rect)  # Drawing brick blocks
            pygame.draw.rect(screen, OUTLINE, rect, 2)  # Outline for the blocks

    def move_down(self):
        """Move the brick down by one unit."""
        self.y += 1  # Move the brick down by one row

    def get_positions(self):
        """Return the absolute positions of the brick blocks."""
        return [(self.x + dx, self.y + dy) for dx, dy in self.shape]
    

