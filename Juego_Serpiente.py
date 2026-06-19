# Juego de la Serpiente 🐍

# Librerías
import pygame   # Librería para gráficos, sonido y control de eventos
import random   # Librería estándar para generar números aleatorios
import sys      # Librería estándar para cerrar el programa de forma controlada

# Inicializar pygame (obligatorio antes de usarlo)
pygame.init()

# ---------------- Configuración de la ventana ----------------
WIDTH, HEIGHT = 600, 400  # Tamaño de la ventana
window = pygame.display.set_mode((WIDTH, HEIGHT))  # Crear ventana
pygame.display.set_caption("Juego de la Serpiente 🐍")  # Título de la ventana

# ---------------- Definición de colores ----------------
BLACK = (0, 0, 0)   # Fondo negro
GREEN = (0, 255, 0) # Color de la serpiente
RED = (255, 0, 0)   # Color de la comida
WHITE = (255, 255, 255) # Texto

# ---------------- Variables del juego ----------------
snake = [(100, 50), (90, 50), (80, 50)]  # Lista de posiciones de la serpiente
snake_dir = (10, 0)  # Dirección inicial (mueve hacia la derecha)
food = (random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10))  # Posición aleatoria de la comida
score = 0  # Puntuación inicial

# ---------------- Funciones auxiliares ----------------
def draw_snake():
    """Dibuja cada parte de la serpiente en pantalla"""
    for pos in snake:
        pygame.draw.rect(window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

def draw_food():
    """Dibuja la comida en pantalla"""
    pygame.draw.rect(window, RED, pygame.Rect(food[0], food[1], 10, 10))

def show_score():
    """Muestra la puntuación en la esquina superior izquierda"""
    font = pygame.font.SysFont("Arial", 20)
    score_text = font.render(f"Puntuación: {score}", True, WHITE)
    window.blit(score_text, (10, 10))

def game_over():
    """Pantalla de Game Over con opción de reinicio"""
    font = pygame.font.SysFont("Arial", 40)
    text = font.render("GAME OVER", True, RED)
    score_text = pygame.font.SysFont("Arial", 25).render(f"Puntuación final: {score}", True, WHITE)
    restart_text = pygame.font.SysFont("Arial", 20).render("Presiona R para reiniciar o Q para salir", True, WHITE)

    window.fill(BLACK)
    window.blit(text, (WIDTH//2 - 100, HEIGHT//2 - 40))
    window.blit(score_text, (WIDTH//2 - 120, HEIGHT//2))
    window.blit(restart_text, (WIDTH//2 - 180, HEIGHT//2 + 40))
    pygame.display.flip()

    # Espera a que el jugador decida
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar
                    return True
                if event.key == pygame.K_q:  # Salir
                    pygame.quit()
                    sys.exit()

# ---------------- Bucle principal del juego ----------------
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Capturar teclas para cambiar dirección
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_dir != (0, 10): snake_dir = (0, -10)
    if keys[pygame.K_DOWN] and snake_dir != (0, -10): snake_dir = (0, 10)
    if keys[pygame.K_LEFT] and snake_dir != (10, 0): snake_dir = (-10, 0)
    if keys[pygame.K_RIGHT] and snake_dir != (-10, 0): snake_dir = (10, 0)

    # Actualizar posición de la serpiente
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    snake.insert(0, new_head)

    # Verificar si come la comida
    if new_head == food:
        food = (random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10))
        score += 1
    else:
        snake.pop()

    # Verificar colisiones (paredes o cuerpo)
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake[1:]):
        if not game_over():  # Mostrar pantalla de Game Over
            break
        else:
            # Reiniciar variables
            snake = [(100, 50), (90, 50), (80, 50)]
            snake_dir = (10, 0)
            food = (random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10))
            score = 0

    # Dibujar todo en pantalla
    window.fill(BLACK)
    draw_snake()
    draw_food()
    show_score()
    pygame.display.flip()
    clock.tick(15)  # Controla la velocidad del juego
