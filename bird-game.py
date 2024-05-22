import pygame
import random
import os

print("Current working directory:", os.getcwd())
print("Files in the directory:", os.listdir())

# Pygame'i başlatma
pygame.init()

# Oyun penceresi
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Renkler
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (100, 100, 100)

# FPS ve Saat
clock = pygame.time.Clock()
fps = 60

# Dosyaların varlığını kontrol etme
if not os.path.exists("bird.png") or not os.path.exists("pipe.png"):
    print("Hata: 'bird.png' ve/veya 'pipe.png' dosyaları mevcut değil.")
    print("Current working directory:", os.getcwd())
    print("Files in the directory:", os.listdir())
    pygame.quit()
    exit()

# Kuş Resmi
bird_image = pygame.image.load("bird.png")
bird_width, bird_height = 50, 50
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))

# Boru Resmi
pipe_image = pygame.image.load("pipe.png")
pipe_image = pygame.transform.scale(pipe_image, (80, 500))

# Kuş Değişkenleri
bird_x = 50
bird_y = 50
bird_velocity = 0
gravity = 0.5

# Boru Değişkenleri
pipe_gap = 150
pipe_velocity = 3
pipe_frequency = 1500  # Boruların oluşturulma süresi (ms)
last_pipe = pygame.time.get_ticks() - pipe_frequency
pipes = []

# Skor
score = 0
font = pygame.font.SysFont(None, 35)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def reset_game():
    global bird_x, bird_y, bird_velocity, pipes, score, last_pipe
    bird_x = 50
    bird_y = 30
    bird_velocity = 0
    pipes = []
    score = 0
    last_pipe = pygame.time.get_ticks() - pipe_frequency

# Oyun Döngüsü
running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -7

    # Kuşu hareket ettirme
    bird_velocity += gravity
    bird_y += bird_velocity

    # Kuşun yere düşmesini engelleme
    if bird_y > screen_height - bird_height:
        bird_y = screen_height - bird_height
        bird_velocity = 0
    elif bird_y < 0:
        bird_y = 0
        bird_velocity = 0

    # Boruları oluşturma
    time_now = pygame.time.get_ticks()
    if time_now - last_pipe > pipe_frequency:
        pipe_height = random.randint(-100, 100)
        btm_pipe = pipe_image.get_rect(midtop=(screen_width, screen_height / 2 + pipe_height + pipe_gap / 2))
        top_pipe = pipe_image.get_rect(midbottom=(screen_width, screen_height / 2 + pipe_height - pipe_gap / 2))
        pipes.append((top_pipe, btm_pipe))
        last_pipe = time_now

    # Boruları hareket ettirme ve silme
    for i in range(len(pipes) - 1, -1, -1):
        pipes[i][0].centerx -= pipe_velocity
        pipes[i][1].centerx -= pipe_velocity

        if pipes[i][0].right < 0:
            pipes.pop(i)
            score += 1

    # Çarpışma kontrolü
    bird_rect = pygame.Rect(bird_x, bird_y, bird_width-20, bird_height-20)
    for pipe in pipes:
        if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
            reset_game()

    # Ekranı temizleme
    screen.fill(blue)

    # Kuşu çizme
    screen.blit(bird_image, (bird_x, bird_y))

    # Kuşun hitbox'ını çizme (debugging amacıyla)
    pygame.draw.rect(screen, red, bird_rect, 1)

    # Boruları çizme
    for pipe in pipes:
        screen.blit(pipe_image, pipe[0])
        screen.blit(pipe_image, pipe[1])

    # Skoru çizme
    draw_text(f"Skor: {score}", font, white, 10, 10)

    # Ekranı güncelleme
    pygame.display.update()

pygame.quit()
