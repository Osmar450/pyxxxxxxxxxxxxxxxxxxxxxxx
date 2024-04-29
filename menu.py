import pygame
import sys
from pygame.locals import *
import math

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("BUTTON ForwardTest")

# Definir colores
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE_LIGHT = (173, 216, 230)  # Azul claro

# Estado del juego
class GameState:
    def __init__(self):
        self.menu = True
        self.game_running = False

# Definir clase para el botón circular
class CircularButton:
    def __init__(self, x, y, radius, color, text, font):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.text = text
        self.font = font

    def draw(self, screen):
        # Dibujar el botón circular
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y + 2), self.radius + 2)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # Dibujar el texto en el botón
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)

    def check_click(self, click_pos):
        # Verificar si se hizo clic en el botón
        if ((click_pos[0] - self.x) ** 2 + (click_pos[1] - self.y) ** 2) <= self.radius ** 2:
            return True
        return False

# Función para iniciar el juego
def start_game():
    game_state.menu = False
    game_state.game_running = True

# Función para simular la tecla Enter
def simulate_enter():
    pygame.event.post(pygame.event.Event(KEYDOWN, key=K_RETURN))

# Estado del juego
game_state = GameState()

# Botón para iniciar el juego
start_button = CircularButton(WIDTH - 100, HEIGHT - 100, 40, RED, "A", pygame.font.SysFont(None, 40))

# Bucle principal del juego
clock = pygame.time.Clock()
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state.menu:
                # Verificar clic en el botón para iniciar el juego
                if start_button.check_click(event.pos):
                    start_game()
                    simulate_enter()

    # Limpiar la pantalla
    if game_state.menu:
        screen.fill(ORANGE)  # Cambiar color de fondo a naranja
        # Dibujar el botón circular para iniciar el juego
        start_button.draw(screen)
    elif game_state.game_running:
        screen.fill(BLUE_LIGHT)  # Cambiar color de fondo a azul claro

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de fotogramas
    clock.tick(60)

# Salir del juego
pygame.quit()
sys.exit()
