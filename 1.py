import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLUE_SKY = (135, 206, 235)
GREEN_GRASS = (34, 139, 34)
METALLIC_GRAY = (169, 169, 169)  # Color metálico para los obstáculos

# Configuración de la ventana
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumping Ball")

# Definir la pelota
ball_radius = 20
ball_vel_y = 0
ball_vel_x = 0  # Velocidad horizontal
jumping = False
double_jump = False  # Agregar variable para el doble salto
# Cargar la skin de la pelota y ajustar su tamaño
ball_image = pygame.image.load('1.png').convert_alpha()
ball_image = pygame.transform.scale(ball_image, (ball_radius * 2, ball_radius * 2))
ball_rect = ball_image.get_rect()

# Cargar skin de la llave
key_image = pygame.image.load('llave.png').convert_alpha()
key_image = pygame.transform.scale(key_image, (ball_radius + 20, ball_radius + 20))  # Hacer la llave más grande

# Cargar skin de los pinchos
spike_image = pygame.Surface((ball_radius * 2, ball_radius * 2))
spike_image.fill((255, 0, 0))  # Rojo
pygame.draw.polygon(spike_image, (0, 0, 0), [(0, 0), (ball_radius * 2, 0), (ball_radius, ball_radius * 2)])

# Cargar música de fondo
pygame.mixer.music.load("poumusic.mp3")
pygame.mixer.music.play(-1)  # Reproducir música de fondo en bucle

# Definir la gravedad
gravity = 0.1

# Definir el marcador
score = 0
font = pygame.font.SysFont(None, 36)

# Lista de plataformas y llaves por nivel
levels = []

# Generar plataformas y llave para los niveles
for i in range(10):  # Generar 10 niveles
    platforms = []
    last_platform = pygame.Rect(0, HEIGHT - 20, 0, 0)
    for _ in range(random.randint(5, 10)):
        platform_width = random.randint(100, 300)
        platform_height = 20
        platform_x = random.randint(0, WIDTH - platform_width)
        platform_y = last_platform.top - random.randint(50, 150)
        platform_rect = pygame.Rect(platform_x, platform_y, platform_width, platform_height)
        platforms.append(platform_rect)
        last_platform = platform_rect

    key_x = random.randint(0, WIDTH - ball_radius)
    key_y = last_platform.top - random.randint(20, 50)
    key_pos = (key_x, key_y)

    levels.append({"platforms": platforms, "key_pos": key_pos})

# Añadir pinchos al principio de cada nivel
for level in levels:
    first_platform = level["platforms"][0]
    spike_rect = spike_image.get_rect(midtop=(first_platform.centerx, first_platform.top))
    level["spike_rect"] = spike_rect

# Índice del nivel actual
current_level = 0
key_collected = False  # Indica si se ha recogido la llave del nivel actual

# Función para mostrar el marcador
def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Bucle principal del juego
clock = pygame.time.Clock()
running = True
game_over = False
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jumping:
                ball_vel_y = -10
                jumping = True
                # Incrementar el marcador cuando se realiza un salto
                score += 1
            elif (event.key == pygame.K_SPACE and jumping) and not double_jump:
                ball_vel_y = -10
                double_jump = True
                score += 1
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                ball_vel_x = -5
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                ball_vel_x = 5
            elif event.key == pygame.K_RETURN and game_over:
                # Reiniciar el juego
                ball_vel_x = 0
                ball_vel_y = 0
                ball_rect.topleft = (WIDTH // 2, HEIGHT // 4)
                jumping = False
                double_jump = False
                score = 0
                current_level = 0
                game_over = False
                key_collected = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT or event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                ball_vel_x = 0

    if not game_over:
        # Aplicar la gravedad
        ball_vel_y += gravity
        ball_rect.y += ball_vel_y
        ball_rect.x += ball_vel_x  # Mover la pelota horizontalmente

        # Si la pelota cae al vacío, mostrar pantalla de Game Over
        if ball_rect.top > HEIGHT:
            game_over = True

        # Detección de colisiones con las plataformas
        on_platform = False
        for platform in levels[current_level]["platforms"]:
            if ball_rect.colliderect(platform):
                if ball_vel_y > 0:  # Si la pelota está cayendo
                    ball_rect.bottom = platform.top
                    ball_vel_y = 0
                    jumping = False
                    on_platform = True
                elif ball_vel_y < 0:  # Si la pelota está subiendo
                    ball_rect.top = platform.bottom
                    ball_vel_y = 0

        # Si el jugador no está en una plataforma, establecer jumping en Verdadero
        if not on_platform:
            jumping = True

        # Detección de colisión con la llave
        if not key_collected and ball_rect.colliderect(
                pygame.Rect(*levels[current_level]["key_pos"], ball_radius, ball_radius)):
            key_collected = True

        # Si se recoge la llave, avanzar al siguiente nivel
        if key_collected:
            current_level += 1
            key_collected = False
            if current_level >= len(levels):
                game_over = True

    # Dibujar el fondo de día soleado
    screen.fill(BLUE_SKY)

    # Dibujar las plataformas del nivel actual
    for platform in levels[current_level]["platforms"]:
        pygame.draw.rect(screen, GREEN_GRASS, platform)

    # Dibujar pinchos del nivel actual
    screen.blit(spike_image, levels[current_level]["spike_rect"].topleft)

    # Dibujar la llave del nivel actual si no ha sido recogida
    if not key_collected:
        screen.blit(key_image, levels[current_level]["key_pos"])

    # Dibujar la pelota
    screen.blit(ball_image, ball_rect.topleft)

    # Dibujar el marcador
    draw_score()

    # Si el juego ha terminado, mostrar pantalla de Game Over
    if game_over:
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2))
        retry_text = font.render("Press ENTER to Retry", True, WHITE)
        screen.blit(retry_text, ((WIDTH - retry_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2 + 50))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de cuadros
    clock.tick(60)

# Salir de Pygame 
pygame.quit()
sys.exit()
