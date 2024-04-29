import pygame
import sys
import math
from pygame.locals import *

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Joystick Test")

# Definir colores
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Integración del joystick
class Joystick:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color_outer = GRAY  # Color del borde del joystick (gris metálico)
        self.color_inner = RED  # Color del círculo interior del joystick (rojo)
        self.shadow_color = (0, 0, 0, 128)  # Color de la sombra
        self.max_offset = size / 2
        self.offset = 0
        self.angle = 0
        self.magnitude = 0

    def draw(self, screen):
        # Draw joystick outer circle with black outline and shadow
        pygame.draw.circle(screen, BLACK, (self.x, self.y + 2), self.size)
        pygame.draw.circle(screen, self.shadow_color, (self.x, self.y + 2), self.size - 2)
        pygame.draw.circle(screen, BLACK, (self.x, self.y - 2), self.size)
        pygame.draw.circle(screen, self.shadow_color, (self.x, self.y - 2), self.size - 2)
        pygame.draw.circle(screen, self.color_outer, (self.x, self.y), self.size - 2)

        # Draw joystick handle as red circle with shadow
        handle_x = self.x + int(math.cos(self.angle) * self.offset)
        handle_y = self.y + int(math.sin(self.angle) * self.offset)
        pygame.draw.circle(screen, BLACK, (handle_x, handle_y + 2), self.size // 3)
        pygame.draw.circle(screen, self.shadow_color, (handle_x, handle_y + 2), self.size // 3 - 1)
        pygame.draw.circle(screen, BLACK, (handle_x, handle_y - 2), self.size // 3)
        pygame.draw.circle(screen, self.shadow_color, (handle_x, handle_y - 2), self.size // 3 - 1)
        pygame.draw.circle(screen, self.color_inner, (handle_x, handle_y), self.size // 3 - 1)

    def update(self, touch_pos):
        # Calculate distance between joystick center and touch position
        dx = touch_pos[0] - self.x
        dy = touch_pos[1] - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
         # Calculate joystick offset and angle
        if distance <= self.max_offset:
            self.offset = distance
            self.angle = math.atan2(dy, dx)
        else:
            self.offset = self.max_offset
            self.angle = math.atan2(dy, dx)

        # Normalize magnitude to be between 0 and 1
        self.magnitude = min(distance / self.max_offset, 1)

# Integrar joystick
joystick = Joystick(100, HEIGHT - 100, 60)  # Ajustar tamaño del joystick

# Definir clase para el jugador
class Player:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color_outer = BLACK  # Color del borde del jugador (negro)
        self.color_inner = RED  # Color del círculo interior del jugador (rojo)
        self.speed = 5  # Ajustar velocidad del jugador

    def draw(self, screen):
        # Draw the player with transparent fill and black outline
        pygame.draw.circle(screen, (255, 255, 255, 128), (self.x, self.y), self.size)
        pygame.draw.circle(screen, self.color_outer, (self.x, self.y), self.size, 2)
        pygame.draw.circle(screen, self.color_inner, (self.x, self.y), self.size // 2)

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        # Verificar si la nueva posición del jugador no choca con la palanca
        if not (joystick.x - joystick.size <= new_x <= joystick.x + joystick.size and
                joystick.y - joystick.size <= new_y <= joystick.y + joystick.size):
            self.x = new_x
            self.y = new_y

        # Verificar si la nueva posición del jugador no choca con los bordes de la ventana
        self.x = max(self.size, min(self.x, WIDTH - self.size))
        self.y = max(self.size, min(self.y, HEIGHT - self.size))

# Crear al jugador
player = Player(WIDTH // 2, HEIGHT // 2, 20)  # Ajustar tamaño del jugador

# Definir clase para el botón circular
class CircularButton:
    def __init__(self, x, y, radius, color, text, font, action):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.text = text
        self.font = font
        self.action = action

    def draw(self, screen):
        # Dibujar el botón circular
        pygame.draw.circle(screen, BLACK, (self.x, self.y + 2), self.radius + 2)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # Dibujar el texto en el botón
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)

    def check_click(self, click_pos):
        # Verificar si se hizo clic en el botón
        if math.sqrt((click_pos[0] - self.x) ** 2 + (click_pos[1] - self.y) ** 2) <= self.radius:
            self.action()

# Función para iniciar el juego
def start_game():
    print("Comenzar juego...")

# Función para salir del juego
def quit_game():
    pygame.quit()
    sys.exit()

# Crear botón circular para iniciar el juego
start_button = CircularButton(WIDTH - 100, HEIGHT - 100, 40, RED, "A", pygame.font.SysFont(None, 40), start_game)

# Bucle principal del juego
clock = pygame.time.Clock()
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar clic en el botón para iniciar el juego
            start_button.check_click(event.pos)

    # Actualizar el joystick
    joystick.update(pygame.mouse.get_pos())

    # Mover al jugador con el joystick
    player.move(int(math.cos(joystick.angle) * joystick.magnitude * player.speed),
                int(math.sin(joystick.angle) * joystick.magnitude * player.speed))

    # Limpiar la pantalla
    screen.fill(ORANGE)  # Cambiar color de fondo a naranja

    # Dibujar el joystick
    joystick.draw(screen)

    # Dibujar al jugador
    player.draw(screen)

    # Dibujar el botón circular para iniciar el juego
    start_button.draw(screen)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de fotogramas
    clock.tick(60)

# Salir del juego
pygame.quit()
sys.exit()
