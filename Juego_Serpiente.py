# Juego de la Serpiente con pygame-ce
import pygame
import random
import sys

pygame.init()

# ---------------- Configuración de la ventana ----------------
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de la Serpiente")

# ---------------- Definición de colores ----------------
GREEN_HEAD = (0, 200, 0)
GREEN_BODY = (0, 255, 100)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = (170, 215, 81)
BORDER_COLOR = (0, 100, 0)

# ---------------- Área jugable ----------------
PLAY_X = CELL_SIZE
PLAY_Y = 50
PLAY_WIDTH = (WIDTH - 2 * CELL_SIZE) // CELL_SIZE * CELL_SIZE
PLAY_HEIGHT = (HEIGHT - CELL_SIZE - 50) // CELL_SIZE * CELL_SIZE

# ---------------- Variables del juego ----------------
snake = [(PLAY_X + CELL_SIZE * 10, PLAY_Y + CELL_SIZE * 5),
         (PLAY_X + CELL_SIZE * 9, PLAY_Y + CELL_SIZE * 5),
         (PLAY_X + CELL_SIZE * 8, PLAY_Y + CELL_SIZE * 5)]
snake_dir = (CELL_SIZE, 0)

def generate_food():
    """Genera comida alineada a la cuadrícula dentro del área jugable."""
    x = random.randint(0, (PLAY_WIDTH // CELL_SIZE) - 1) * CELL_SIZE + PLAY_X
    y = random.randint(0, (PLAY_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE + PLAY_Y
    return (x, y)

food = generate_food()
score = 0
high_score = 0

clock = pygame.time.Clock()

# ---------------- Pantalla de inicio ----------------
def start_screen():
    font_big = pygame.font.SysFont("Arial", 60)
    font_small = pygame.font.SysFont("Arial", 30)

    title = font_big.render("Juego de la Serpiente", True, GREEN_HEAD)
    play_text = font_small.render("Presiona ENTER para jugar", True, WHITE)
    quit_text = font_small.render("Presiona Q para salir", True, WHITE)

    while True:
        draw_background()
        window.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 100)))
        window.blit(play_text, play_text.get_rect(center=(WIDTH//2, HEIGHT//2)))
        window.blit(quit_text, quit_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50)))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# ---------------- Funciones auxiliares ----------------
def draw_background():
    colors = [(170, 215, 81), (162, 209, 73)]
    window.fill(BG_COLOR)
    for y in range(PLAY_Y, PLAY_Y + PLAY_HEIGHT, CELL_SIZE):
        for x in range(PLAY_X, PLAY_X + PLAY_WIDTH, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            color = colors[((x // CELL_SIZE) + (y // CELL_SIZE)) % 2]
            pygame.draw.rect(window, color, rect)
    pygame.draw.rect(window, BORDER_COLOR, (PLAY_X, PLAY_Y, PLAY_WIDTH, PLAY_HEIGHT), 4)

def draw_snake():
    for i, pos in enumerate(snake):
        color = GREEN_HEAD if i == 0 else GREEN_BODY
        rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(window, color, rect)
        if i == 0:
            eye_radius = max(2, CELL_SIZE // 6)
            pygame.draw.circle(window, WHITE, (pos[0] + eye_radius*2, pos[1] + eye_radius*2), eye_radius)
            pygame.draw.circle(window, (0,0,0), (pos[0] + eye_radius*2, pos[1] + eye_radius*2), eye_radius//2)
            pygame.draw.circle(window, WHITE, (pos[0] + CELL_SIZE - eye_radius*2, pos[1] + eye_radius*2), eye_radius)
            pygame.draw.circle(window, (0,0,0), (pos[0] + CELL_SIZE - eye_radius*2, pos[1] + eye_radius*2), eye_radius//2)

def draw_food():
    center = (food[0] + CELL_SIZE//2, food[1] + CELL_SIZE//2)
    radius = CELL_SIZE//2 - 2
    pygame.draw.circle(window, RED, center, radius)

def show_score():
    font = pygame.font.SysFont("Arial", 24)
    pygame.draw.rect(window, BORDER_COLOR, (0, 0, WIDTH, 40))
    score_text = font.render(f"Puntuación: {score}", True, WHITE)
    record_text = font.render(f"Récord: {high_score}", True, WHITE)
    window.blit(score_text, (10, 8))
    window.blit(record_text, (200, 8))

def reset_game():
    global snake, snake_dir, food, score
    snake = [(PLAY_X + CELL_SIZE * 10, PLAY_Y + CELL_SIZE * 5),
             (PLAY_X + CELL_SIZE * 9, PLAY_Y + CELL_SIZE * 5),
             (PLAY_X + CELL_SIZE * 8, PLAY_Y + CELL_SIZE * 5)]
    snake_dir = (CELL_SIZE, 0)
    food = generate_food()
    score = 0

def game_over():
    global high_score, score
    if score > high_score:
        high_score = score
    font_big = pygame.font.SysFont("Arial", 40)
    font_mid = pygame.font.SysFont("Arial", 25)
    font_small = pygame.font.SysFont("Arial", 20)
    text = font_big.render("GAME OVER", True, RED)
    score_text = font_mid.render(f"Puntuación final: {score}", True, WHITE)
    record_text = font_mid.render(f"Récord: {high_score}", True, WHITE)
    restart_text = font_small.render("Presiona R para reiniciar o Q para salir", True, WHITE)
    window.fill((30, 30, 30))
    window.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2 - 60)))
    window.blit(score_text, score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))
    window.blit(record_text, record_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))
    window.blit(restart_text, restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60)))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def change_direction(new_dir):
    global snake_dir
    if (new_dir[0] != -snake_dir[0]) and (new_dir[1] != -snake_dir[1]):
        snake_dir = new_dir

# ---------------- Ejecución ----------------
start_screen()

# ---------------- Bucle principal ----------------
while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            change_direction((0, -CELL_SIZE))
        elif keys[pygame.K_DOWN]:
            change_direction((0, CELL_SIZE))
        elif keys[pygame.K_LEFT]:
            change_direction((-CELL_SIZE, 0))
        elif keys[pygame.K_RIGHT]:
            change_direction((CELL_SIZE, 0))

        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        snake.insert(0, new_head)

        # ✅ Detección robusta de comida
        head_rect = pygame.Rect(new_head[0], new_head[1], CELL_SIZE, CELL_SIZE)
        food_rect = pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE)
        if head_rect.colliderect(food_rect):
            food = generate_food()
            score += 1
        else:
            snake.pop()

        # ✅ Colisiones robustas
        if (new_head[0] < PLAY_X or new_head[0] >= PLAY_X + PLAY_WIDTH or
            new_head[1] < PLAY_Y or new_head[1] >= PLAY_Y + PLAY_HEIGHT or
            new_head in snake[1:]):
            if not game_over():
                break

        draw_background()
        draw_snake()
        draw_food()
        show_score()
        pygame.display.flip()
        clock.tick(15)
        
    except Exception as e:
        print(f"Error inesperado: {e}")
        pygame.quit()
        sys.exit()
