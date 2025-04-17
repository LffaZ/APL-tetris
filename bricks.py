from brick import Brick
from constants import I_COLOR, O_COLOR, T_COLOR, S_COLOR, Z_COLOR, J_COLOR, L_COLOR

class IShape(Brick):
    def __init__(self, block_size, x, y):
        super().__init__(block_size, I_COLOR, x, y)
        # Shape coordinates for the I shape (vertical line)
        self.shape = [(0, 0), (1, 0), (2, 0), (3, 0)]


class OShape(Brick):
    def __init__(self, block_size, x, y):
        super().__init__(block_size, O_COLOR, x, y)
        # Shape coordinates for the O shape (square)
        self.shape = [(0, 0), (0, 1), (1, 0), (1, 1)]


class TShape(Brick):
    def __init__(self, block_size, x, y):
        super().__init__(block_size, T_COLOR, x, y)
        # Shape coordinates for the T shape (T)
        self.shape = [(0, 0), (1, 0), (2, 0), (1, 1)]


class SShape(Brick):
    def __init__(self, block_size, x, y):
        super().__init__(block_size, S_COLOR, x, y)
        # Shape coordinates for the S shape (S)
        self.shape = [(1, 0), (2, 0), (0, 1), (1, 1)]


class ZShape(Brick):
    def __init__(self, block_size, x, y):
        super().__init__(block_size, Z_COLOR, x, y)
        # Shape coordinates for the Z shape (Z)
        self.shape = [(0, 0), (1, 0), (1, 1), (2, 1)]

class JShape(Brick):
    def __init__(self, block_size, x, y):
        super().__init__(block_size, J_COLOR, x, y)  # Warna biru untuk J
        # Koordinat shape untuk J (mirip huruf J)
        self.shape = [(0, 0), (1, 0), (2, 0), (2, 1)]

class LShape(Brick):
    def __init__(self, block_size, x, y):
        super().__init__(block_size, L_COLOR, x, y)  # Warna oranye untuk L
        # Koordinat shape untuk L (mirip huruf L)
        self.shape = [(0, 0), (1, 0), (2, 0), (0, 1)]
