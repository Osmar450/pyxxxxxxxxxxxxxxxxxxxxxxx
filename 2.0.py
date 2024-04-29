import pygame
import sys
import math
import random
from pygame.locals import *

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 1200, 800
SCREEN_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Forwardpy")

# Cargar música de fondo
pygame.mixer.music.load('mine.mp3')
pygame.mixer.music.play(-1)  # Reproducir en bucle

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)  # Nuevo color para Coins y Level
ORANGE = (255, 165, 0)  # Nuevo color para Game Over


# Cargar imágenes y ajustar al tamaño de pantalla
def load_and_scale_image(filename, size):
    image = pygame.image.load(filename).convert_alpha()
    return pygame.transform.scale(image, size)


player_image = load_and_scale_image('1.png', (int(WIDTH * 0.03), int(HEIGHT * 0.05)))
enemy_image = load_and_scale_image('enemy.png', (int(WIDTH * 0.03), int(HEIGHT * 0.05)))
ground_image = load_and_scale_image('background.png', SCREEN_SIZE)
sword_image = load_and_scale_image('sword.png', (int(WIDTH * 0.03), int(HEIGHT * 0.05)))
heart_image = load_and_scale_image('heart.png', (int(WIDTH * 0.015), int(HEIGHT * 0.025)))
coin_image = load_and_scale_image('coin.png', (int(WIDTH * 0.025), int(HEIGHT * 0.0375)))
game_over_background = load_and_scale_image('dead.png', SCREEN_SIZE)
pause_menu_background = load_and_scale_image('background.png', SCREEN_SIZE)

# Cargar imágenes para los diferentes fondos de escenario
backgrounds = {
    "0": load_and_scale_image('b1.png', SCREEN_SIZE),
    "1": load_and_scale_image('b1.png', SCREEN_SIZE),
    "2": load_and_scale_image('b1.png', SCREEN_SIZE),
    "3": load_and_scale_image('b1.png', SCREEN_SIZE),
    "4": load_and_scale_image('b1.png', SCREEN_SIZE),
    "5": load_and_scale_image('b2.png', SCREEN_SIZE),
    "6": load_and_scale_image('b2.png', SCREEN_SIZE),
    "7": load_and_scale_image('b2.png', SCREEN_SIZE),
    "8": load_and_scale_image('b2.png', SCREEN_SIZE),
    "9": load_and_scale_image('b2.png', SCREEN_SIZE),
    "10": load_and_scale_image('b3.png', SCREEN_SIZE),
    "11": load_and_scale_image('b3.png', SCREEN_SIZE),
    "12": load_and_scale_image('b3.png', SCREEN_SIZE),
    "13": load_and_scale_image('b3.png', SCREEN_SIZE),
    "14": load_and_scale_image('b3.png', SCREEN_SIZE),
    "15": load_and_scale_image('b4.png', SCREEN_SIZE),
    "16": load_and_scale_image('b4.png', SCREEN_SIZE),
    "17": load_and_scale_image('b4.png', SCREEN_SIZE),
    "18": load_and_scale_image('b4.png', SCREEN_SIZE),
    "19": load_and_scale_image('b5.png', SCREEN_SIZE),
    "20": load_and_scale_image('b1.png', SCREEN_SIZE)  # Fondo predeterminado para nivel 20 y posteriores
}

# Definir la imagen de fondo
background_image = backgrounds["0"]


# Definir clase para representar al jugador
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = player_image.get_width()
        self.height = player_image.get_height()
        self.health = 3  # Vida del jugador
        self.attack_damage = 1  # Daño de ataque
        self.has_sword = False  # Indica si el jugador tiene el arma
        self.inventory = [None, None, None]  # Inventario con 3 celdas
        self.coins = 0  # Número de monedas recolectadas
        self.level = 1  # Nivel del jugador
        self.paused = False  # Indica si el juego está en pausa

    def draw(self):
        screen.blit(player_image, (self.x, self.y))
        # Dibujar la barra de vida del jugador
        for i in range(self.health):
            screen.blit(heart_image, (10 + i * (heart_image.get_width() + 5), 10))
        # Dibujar el puntaje del jugador
        coins_text = font.render("Coins: " + str(self.coins), True, YELLOW)
        screen.blit(coins_text, (10, 40))
        # Dibujar el nivel del jugador
        level_text = font.render("Level: " + str(self.level), True, YELLOW)
        screen.blit(level_text, (10, 70))

    def attack(self, enemy):
        # Verificar colisión entre el jugador y el enemigo
        if (self.x < enemy.x + enemy.width and self.x + self.width > enemy.x and self.y
                < enemy.y + enemy.height and self.y + self.height > enemy.y):
            enemy.health -= self.attack_damage
            # Verificar si el enemigo ha muerto
            if enemy.health <= 0:
                enemy.reset_position()

    def pickup_sword(self):
        pass

    def drop_sword(self):
        pass


# Definir clase para representar al enemigo
class Enemy:
    def __init__(self, x, y):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = enemy_image.get_width()
        self.height = enemy_image.get_height()
        self.health = 3  # Vida del enemigo
        self.speed = random.uniform(0.2, 0.4) + 0.2 * (player.level - 1)  # Velocidad aumenta con el nivel

    def draw(self):
        screen.blit(enemy_image, (self.x, self.y))

    def move_towards_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance

    def reset_position(self):
        self.x = random.randint(50, WIDTH - self.width - 50)
        self.y = random.randint(50, HEIGHT - self.height - 50)
        self.health = 3
        self.speed = random.uniform(0.2, 0.5) + 0.2 * (player.level - 1)


# Definir clase para representar las monedas
class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = coin_image.get_width()
        self.height = coin_image.get_height()

    def draw(self):
        screen.blit(coin_image, (self.x, self.y))


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

    def draw(self):
        # Draw joystick outer circle with black outline and shadow
        outer_circle_radius = self.size
        inner_circle_radius = self.size // 3
        joystick_pos = (100, HEIGHT-100)

        # Draw outer circle with black outline
        pygame.draw.circle(screen, BLACK, joystick_pos, outer_circle_radius)
        pygame.draw.circle(screen, self.shadow_color, joystick_pos, outer_circle_radius - 2)

        # Draw inner circle
        pygame.draw.circle(screen, self.color_outer, joystick_pos, outer_circle_radius - 2)

        # Draw joystick handle as red circle with shadow
        handle_x = 100 + int(math.cos(self.angle) * self.offset)
        handle_y = (HEIGHT-100) + int(math.sin(self.angle) * self.offset)
        handle_pos = (handle_x, handle_y)

        # Draw handle outer circle with black outline
        pygame.draw.circle(screen, BLACK, handle_pos, inner_circle_radius)
        pygame.draw.circle(screen, self.shadow_color, handle_pos, inner_circle_radius - 1)

        # Draw handle inner circle
        pygame.draw.circle(screen, self.color_inner, handle_pos, inner_circle_radius - 1)

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


# Función para mostrar el menú principal
def show_menu():
    menu_font = pygame.font.SysFont(None, 60)
    title_text = menu_font.render("Forward PROJECT", True, WHITE)
    instruction_text = menu_font.render("[Press ENTER to Start]", True, GREEN)
    screen.blit(background_image, (0, 0))  # Mostrar imagen de fondo
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, HEIGHT // 3))
    screen.blit(instruction_text, ((WIDTH - instruction_text.get_width()) // 2, HEIGHT // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False


# Función para mostrar la pantalla de Game Over
def show_game_over(elapsed_time):
    menu_font = pygame.font.SysFont(None, 60)
    game_over_text = menu_font.render("Game Over", True, RED)
    score_text = menu_font.render("Coins: " + str(player.coins), True, ORANGE)
    level_text = menu_font.render("Level: " + str(player.level), True, ORANGE)
    time_text = menu_font.render("Time Survived: " + format_time(elapsed_time), True,
                                 RED)  # Mostrar tiempo transcurrido
    retry_text = menu_font.render("Press TAB to Retry", True, GREEN)
    screen.blit(game_over_background, (0, 0))  # Usar nueva imagen de fondo para Game Over
    screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 3))
    screen.blit(score_text, ((WIDTH - score_text.get_width()) // 2, HEIGHT // 2))
    screen.blit(level_text,
                ((WIDTH - level_text.get_width()) // 2, HEIGHT // 2 + 60))  # Mostrar nivel debajo de las monedas
    screen.blit(time_text, ((WIDTH - time_text.get_width()) // 2, HEIGHT // 2 + 120))  # Mostrar tiempo debajo del nivel
    screen.blit(retry_text, ((WIDTH - retry_text.get_width()) // 2, HEIGHT // 2 + 180))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    waiting = False
                    reiniciar_juego()


def reiniciar_juego():
    # Aquí reseteas todas las variables del juego a su estado inicial
    # Por ejemplo:
    player.x = WIDTH // 2
    player.y = HEIGHT // 2
    player.health = 3
    player.coins = 0
    player.level = 1
    enemies.clear()
    coins.clear()
    enemies.extend([Enemy(random.randint(50, WIDTH - enemy_image.get_width() - 50),
                          random.randint(50, HEIGHT - enemy_image.get_height() - 50)) for _ in range(10)])
    coins.extend([Coin(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)) for _ in range(5)])
    global game_over
    game_over = False


# Función para mostrar el menú de pausa
def show_pause_menu():
    menu_font = pygame.font.SysFont(None, 60)
    pause_text = menu_font.render("Paused", True, WHITE)
    continue_text = menu_font.render("Press ESC to Continue", True, GREEN)
    screen.blit(pause_menu_background, (0, 0))  # Usar nueva imagen de fondo para menú de pausa
    screen.blit(pause_text, ((WIDTH - pause_text.get_width()) // 2, HEIGHT // 3))
    screen.blit(continue_text, ((WIDTH - continue_text.get_width()) // 2, HEIGHT // 2))
    pygame.display.flip()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False


# Formatear el tiempo en segundos a un formato de tiempo legible
def format_time(milliseconds):
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds %= 60
    return "{:02}:{:02}".format(minutes, seconds)


# Mostrar el menú principal
show_menu()

# Crear al jugador y a los enemigos
player = Player(WIDTH // 2, HEIGHT // 2)
enemies = [Enemy(random.randint(50, WIDTH - enemy_image.get_width() - 50),
                 random.randint(50, HEIGHT - enemy_image.get_height() - 50)) for _ in range(10)]

joystick = Joystick(WIDTH // 2, HEIGHT // 2, 60)

# Crear monedas
coins = [Coin(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)) for _ in range(5)]

# Velocidad de movimiento del jugador
player_speed = 5

# Definir fuente para texto
font = pygame.font.SysFont(None, 30)

# Bucle principal del juego
clock = pygame.time.Clock()
running = True
game_over = False
start_time = pygame.time.get_ticks()  # Tiempo de inicio del juego
# joystick


while running:
    # Calcular el tiempo transcurrido desde el inicio del juego
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and game_over:
                # Reiniciar el juego
                reiniciar_juego()
                start_time = pygame.time.get_ticks()  # Reiniciar el tiempo de inicio del juego
            elif event.key == pygame.K_ESCAPE and not game_over:
                # Mostrar el menú de pausa
                player.paused = True
                show_pause_menu()
                player.paused = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                touch_pos = pygame.mouse.get_pos()
                joystick.update(touch_pos)
        elif event.type == pygame.MOUSEMOTION:
            touch_pos = pygame.mouse.get_pos()
            joystick.update(touch_pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            joystick.offset = 0
            joystick.magnitude = 0

    # Dibujar el fondo
    screen.fill(WHITE)

    if not game_over and not player.paused:
        # Obtener las teclas presionadas
        keys = pygame.key.get_pressed()

        # Get joystick magnitude and angle
        joystick_magnitude = joystick.magnitude
        joystick_angle = joystick.angle

        # Calculate player movement based on joystick input
        player.x += int(joystick_magnitude * player_speed * math.cos(joystick_angle))
        player.y += int(joystick_magnitude * player_speed * math.sin(joystick_angle))

        # Ensure player stays within screen boundaries
        player.x = max(0, min(player.x, WIDTH - player.width))
        player.y = max(0, min(player.y, HEIGHT - player.height))

        # Guardar la posición anterior del jugador
        prev_x, prev_y = player.x, player.y

        # Mover al jugador según las teclas presionadas
        if keys[K_w] or keys[K_UP]:
            player.y -= player_speed
        if keys[K_s] or keys[K_DOWN]:
            player.y += player_speed
        if keys[K_a] or keys[K_LEFT]:
            player.x -= player_speed
        if keys[K_d] or keys[K_RIGHT]:
            player.x += player_speed

        # Verificar los límites del suelo para el jugador
        player.x = max(0, min(player.x, WIDTH - player.width))
        player.y = max(0, min(player.y, HEIGHT - player.height))

        # Mover a los enemigos hacia el jugador
        for enemy in enemies:
            enemy.move_towards_player(player)

        # Verificar colisiones entre el jugador y los enemigos
        for enemy in enemies:

            if (player.x < enemy.x + enemy.width and player.x + player.width > enemy.x and player.y < enemy.y +
                    enemy.height and player.y + player.height > enemy.y):
                player.health -= 1
                if player.health <= 0:
                    game_over = True

                player.health -= 1
                if player.health <= 0:
                    game_over = True

        # Verificar colisiones entre el jugador y las monedas
        for coin in coins:
            if (player.x < coin.x + coin.width and player.x + player.width > coin.x and player.y < coin.y +
                    coin.height and player.y + player.height > coin.y):
                player.coins += 1
                coins.remove(coin)  # Quitar la moneda recolectada

        # Verificar si el jugador ha avanzado al siguiente nivel
        if player.coins >= 5 * player.level:
            player.level += 1
            # Eliminar enemigos anteriores y agregar nuevos enemigos
            enemies.clear()
            enemies.extend([Enemy(random.randint(50, WIDTH - enemy_image.get_width() - 50),
                                  random.randint(50, HEIGHT - enemy_image.get_height() - 50)) for _ in
                            range(player.level * 2)])
            # Eliminar monedas anteriores y agregar nuevas monedas
            coins.clear()
            coins.extend([Coin(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)) for _ in range(5)])

    # Dibujar el fondo
    screen.blit(background_image, (0, 0))

    # Dibujar al jugador
    player.draw()

    # Dibujar el Joystick
    joystick.draw()

    # Dibujar a los enemigos
    for enemy in enemies:
        enemy.draw()

    # Dibujar las monedas
    for coin in coins:
        coin.draw()

    if game_over:
        # Mostrar pantalla de Game Over
        show_game_over(elapsed_time)

    # Actualizar la pantalla
    pygame.display.flip()

    # Limitar la velocidad de fotogramas
    clock.tick(60)

# Salir del juego
pygame.quit()
sys.exit()
