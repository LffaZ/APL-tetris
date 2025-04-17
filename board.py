import pygame
import random
from constants import BOARD_COLOR, WHITE, OUTLINE, PREVIEW_COLOR, PREVIEW_OUTLINE, HOLD_COLOR
from bricks import IShape, OShape, TShape, SShape, ZShape,  JShape, LShape

class Board:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]  # Initialize an empty grid
        self.current_brick = None
        self.game_over = False
        self.next_bricks = [self.generate_random_brick() for _ in range(5)]
        self.hold_brick = None
        self.hold_used = False  # Lock hold per brick

    def hold_current_brick(self):
        if self.hold_used or not self.current_brick:
            return  

        temp = self.hold_brick
        self.hold_brick = self.current_brick.__class__  

        if temp:
            # Ada hold sebelumnya → tukar
            self.current_brick = temp(self.block_size, self.width // 2 - 1, 0)
        else:
            # Belum ada hold → ambil dari next
            self.current_brick = self.next_bricks.pop(0)
            self.current_brick.x = self.width // 2 - 1
            self.current_brick.y = 0
            self.next_bricks.append(self.generate_random_brick())

        self.hold_used = True  # 🔒 Gak bisa hold lagi sebelum brick ini jatuh


    def generate_random_brick(self):
        brick_types = [IShape, OShape, TShape, SShape, ZShape, JShape, LShape]
        brick_class = random.choice(brick_types)
        center_x = self.width // 2 - 1
        return brick_class(self.block_size, center_x, 0)

    def can_fall(self):
        """Check if the current brick can fall further down."""
        if not self.current_brick:
            return False

        for dx, dy in self.current_brick.get_positions():
            # Check if the brick has reached the bottom or if there's another brick below it
            if dy + 1 >= self.height or self.grid[dy + 1][dx] != 0:
                return False
        return True

    def spawn_new_brick(self):
        # Ambil tipe dari next_brick (class-nya)
        brick_class = self.next_bricks.pop(0).__class__

        # Buat current brick baru dengan posisi awal
        self.current_brick = brick_class(self.block_size, self.width // 2 - 1, 0)

        # Cek game over
        if self.is_game_over(self.current_brick):
            self.current_brick = None
            self.game_over = True
        else:
            self.next_bricks.append(self.generate_random_brick())

    def draw_next_brick(self, screen):
        """Tampilkan preview dari next brick di area kanan"""
        if not self.next_brick:
            return

        # Offset posisi preview di kanan layar
        preview_x = self.width * self.block_size + 50
        preview_y = 100

        for dx, dy in self.next_brick.shape:
            rect = pygame.Rect(
                preview_x + dx * self.block_size,
                preview_y + dy * self.block_size,
                self.block_size,
                self.block_size
            )
            pygame.draw.rect(screen, self.next_brick.color, rect)
            pygame.draw.rect(screen, (115, 87, 81), rect, 2)

    def draw_next_bricks(self, screen):
        """Tampilkan 5 preview brick berikutnya"""
        preview_x = self.width * self.block_size + 50
        start_y = 170
        spacing = 80  # Jarak antar preview

        for i, brick in enumerate(self.next_bricks):
            offset_y = start_y + i * spacing
            for dx, dy in brick.shape:
                rect = pygame.Rect(
                    preview_x + dx * self.block_size,
                    offset_y + dy * self.block_size,
                    self.block_size,
                    self.block_size
                )
                pygame.draw.rect(screen, brick.color, rect)
                pygame.draw.rect(screen, (115, 87, 81), rect, 2)


    def update(self):
        """Update the position of the current brick."""
        if self.can_fall():
            # Move the current brick down by 1
            self.current_brick.move_down()  # Move down if possible
        else:
            # Lock the current brick into the grid
            for dx, dy in self.current_brick.get_positions():
                self.grid[dy][dx] = self.current_brick.color  # Store the color in the grid
            pygame.mixer.Sound("sfx/drop.wav").play()
            self.clear_lines()
            self.spawn_new_brick()
            self.hold_used = False

    def move_current_brick(self, dx):
        """Geser current brick ke kiri (-1) atau kanan (+1)"""
        if not self.current_brick:
            return
        new_x = self.current_brick.x + dx
        # Validasi biar ga nabrak tembok/grid
        if all(0 <= new_x + x < self.width and self.grid[self.current_brick.y + y][new_x + x] == 0
               for x, y in self.current_brick.shape if 0 <= self.current_brick.y + y < self.height):
            self.current_brick.x = new_x

    def rotate_current_brick(self):
        """Putar current brick searah jarum jam (rotasi 90 derajat)"""
        if not self.current_brick:
            return
        # Rotasi manual: (x, y) -> (-y, x)
        new_shape = [(-y, x) for x, y in self.current_brick.shape]
        # Cek apakah posisi baru valid
        if all(0 <= self.current_brick.x + x < self.width and 
               0 <= self.current_brick.y + y < self.height and 
               self.grid[self.current_brick.y + y][self.current_brick.x + x] == 0
               for x, y in new_shape):
            self.current_brick.shape = new_shape

    def soft_drop(self):
        """Turunin brick 1 step ke bawah"""
        if self.can_fall():
            self.current_brick.move_down()
        else:
            self.update()  # brick dikunci dan spawn baru

    def hard_drop(self):
        """Langsung jatuhin sampai mentok"""
        while self.can_fall():
            self.current_brick.move_down()
        self.update()
        
    def is_game_over(self, brick):
        """Cek apakah posisi awal brick nabrak brick lain"""
        for x, y in brick.get_positions():
            if y >= 0 and self.grid[y][x] != 0:
                return True
        return False

    def clear_lines(self):
        """Hapus baris yang penuh dan geser sisanya ke bawah"""
        new_grid = []
        lines_cleared = 0

        for row in self.grid:
            if 0 not in row:
                lines_cleared += 1  # Hitung berapa baris yang dihapus
            else:
                new_grid.append(row)  # Simpan baris yang gak penuh

        # Tambah baris kosong di atas (buat ganti baris yang dihapus)
        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(self.width)])

        self.grid = new_grid

        if lines_cleared > 0:
            pygame.mixer.Sound("sfx/line_clr.wav").play()

    def draw(self, screen):
        """Draw the board and bricks on the screen."""
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)

                # Draw the background for the board (board color)
                # pygame.draw.rect(screen, BOARD_COLOR, rect)

                # Draw the outline of each square
                pygame.draw.rect(screen, BOARD_COLOR, rect, 2)
                pygame.draw.rect(screen, WHITE, rect, 1)
                pygame.draw.rect(screen, BOARD_COLOR, rect, 2)
                # pygame.draw.rect(screen, WHITE, rect, 1)
                pygame.draw.rect(screen, WHITE, rect, 1)

                # If there's a brick (color not zero), draw it
                if self.grid[y][x] != 0:
                    pygame.draw.rect(screen, self.grid[y][x], rect)  # Draw the brick with its color
                    pygame.draw.rect(screen, OUTLINE, rect, 2)
        if self.current_brick:
            self.current_brick.draw(screen)

    def draw_ghost(self, screen):
        """Gambar bayangan posisi jatuh current_brick"""
        if not self.current_brick:
            return

        # Buat salinan posisi brick
        ghost_y = self.current_brick.y
        while True:
            # Coba turunkan 1 langkah
            next_y = ghost_y + 1
            positions = [(self.current_brick.x + dx, next_y + dy) for dx, dy in self.current_brick.shape]
            
            # Cek apakah nabrak atau sampai bawah
            if any(
                y >= self.height or (y >= 0 and self.grid[y][x] != 0)
                for x, y in positions
            ):
                break
            ghost_y += 1

        # Gambar bayangan di posisi ghost_y
        for dx, dy in self.current_brick.shape:
            x = self.current_brick.x + dx
            y = ghost_y + dy
            if y >= 0:
                rect = pygame.Rect(x * self.block_size, y * self.block_size,
                                self.block_size, self.block_size)
                pygame.draw.rect(screen, PREVIEW_COLOR, rect)  # Gambar warna bayangan
                pygame.draw.rect(screen, PREVIEW_OUTLINE, rect, 2)

    def draw_hold_brick(self, screen):
        if not self.hold_brick:
            return

        preview_x = self.width * self.block_size + 50
        preview_y = 50  # Turun dari next

        temp_brick = self.hold_brick(self.block_size, 0, 0)
        for dx, dy in temp_brick.shape:
            rect = pygame.Rect(
                preview_x + dx * self.block_size,
                preview_y + dy * self.block_size,
                self.block_size, self.block_size
            )
            # pygame.draw.rect(screen, temp_brick.color, rect)
            pygame.draw.rect(screen, HOLD_COLOR, rect) 
            pygame.draw.rect(screen, (115, 87, 81), rect, 2)


