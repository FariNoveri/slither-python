import pygame
import math
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slither.io Style Snake")
clock = pygame.time.Clock()

# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Snake config
SEGMENT_RADIUS = 8
SEGMENT_SPACING = 5
SNAKE_LENGTH = 10  # Start shorter
speed = 3.5

# Snake state
trail = []
head_pos = [WIDTH / 2, HEIGHT / 2]
last_dir = [1, 0]  # Default start direction: right

# Apple
apple_radius = 10
apple_pos = [random.randint(apple_radius, WIDTH - apple_radius),
             random.randint(apple_radius, HEIGHT - apple_radius)]

score = 0
font = pygame.font.SysFont(None, 36)
game_active = True

def draw_snake(trail):
    for i in range(0, len(trail), 4):  # Skip for spacing
        pygame.draw.circle(screen, GREEN, (int(trail[i][0]), int(trail[i][1])), SEGMENT_RADIUS)

def draw_apple():
    pygame.draw.circle(screen, RED, (int(apple_pos[0]), int(apple_pos[1])), apple_radius)

def check_self_collision(trail):
    head = trail[0]
    for segment in trail[15:]:  # Jarak aman agar tidak terlalu sensitif
        if math.hypot(head[0] - segment[0], head[1] - segment[1]) < SEGMENT_RADIUS * 0.9:
            return True
    return False

def show_score():
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def game_over_screen():
    screen.fill(BLACK)
    text1 = font.render("You Died!", True, WHITE)
    text2 = font.render(f"Final Score: {score}", True, WHITE)
    text3 = font.render("Press R to Restart or ESC to Exit", True, WHITE)
    screen.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//2 - 60))
    screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 - 20))
    screen.blit(text3, (WIDTH//2 - text3.get_width()//2, HEIGHT//2 + 20))
    pygame.display.update()

def reset_game():
    global trail, head_pos, SNAKE_LENGTH, score, apple_pos, game_active, last_dir
    trail = []
    head_pos = [WIDTH / 2, HEIGHT / 2]
    last_dir = [1, 0]  # Reset direction to right
    SNAKE_LENGTH = 10  # Start shorter
    score = 0
    apple_pos = [random.randint(apple_radius, WIDTH - apple_radius),
                 random.randint(apple_radius, HEIGHT - apple_radius)]
    game_active = True

# Game loop
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False

    if game_active:
        # Movement
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - head_pos[0]
        dy = mouse_y - head_pos[1]
        dist = math.hypot(dx, dy)

        if dist > 10:  # Mouse bergerak, update arah
            dx /= dist
            dy /= dist
            last_dir = [dx, dy]  # Simpan arah terakhir
        else:  # Mouse diam, teruskan gerakan sebelumnya
            dx, dy = last_dir  # Gunakan arah terakhir saat mouse diam

        # Pastikan ular terus bergerak sesuai dengan arah sebelumnya
        head_pos[0] += dx * speed
        head_pos[1] += dy * speed

        # Ular tetap berada di layar
        if head_pos[0] < 0:
            head_pos[0] = WIDTH
        elif head_pos[0] > WIDTH:
            head_pos[0] = 0

        if head_pos[1] < 0:
            head_pos[1] = HEIGHT
        elif head_pos[1] > HEIGHT:
            head_pos[1] = 0

        trail.insert(0, list(head_pos))
        if len(trail) > SNAKE_LENGTH * SEGMENT_SPACING:
            trail.pop()

        # Collision with apple
        if math.hypot(head_pos[0] - apple_pos[0], head_pos[1] - apple_pos[1]) < SEGMENT_RADIUS + apple_radius:
            score += 1
            SNAKE_LENGTH += 2  # Pertumbuhan yang lebih sedikit setiap makan apel
            apple_pos = [random.randint(apple_radius, WIDTH - apple_radius),
                         random.randint(apple_radius, HEIGHT - apple_radius)]

        # Self collision
        if check_self_collision(trail):
            game_active = False

        # Draw everything
        draw_apple()
        draw_snake(trail)
        show_score()

        pygame.display.update()
    else:
        game_over_screen()

pygame.quit()
sys.exit()
