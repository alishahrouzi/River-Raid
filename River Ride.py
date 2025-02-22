import pygame
import random

# iniate_setting
pygame.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("River Ride")

bg_y1 = 0
bg_y2 = -HEIGHT

# color
WHITE = (255, 255, 255)
PLANE_COLOR = (255, 0, 0)
FUEL_COLOR = (0, 255, 0)
BULLET_COLOR = (255, 255, 0)
BLACK = (0, 0, 0)

# variable
plane_width, plane_height = 100, 100
plane_x = WIDTH // 2 - plane_width // 2
plane_y = HEIGHT - plane_height - 20

obstacles = []
fuel_items = []
bullets = []
obstacle_speed = 5
fuel_speed = 4
bullet_speed = -10
fuel = 100
score = 0

# image_loading
back_img = pygame.image.load("E:\My Lesson\Bachelor\Projects\Computer Graphic\project\River Raid\Source/26715.jpg")
back_img = pygame.transform.scale(back_img,(WIDTH,HEIGHT))

plane_img = pygame.image.load('E:\My Lesson\Bachelor\Projects\Computer Graphic\project\River Raid\Source/11151.png')
plane_img = pygame.transform.scale(plane_img,(plane_width,plane_height))

obstacle_img = pygame.image.load("E:\My Lesson\Bachelor\Projects\Computer Graphic\project\River Raid\Source/12458.png")
obstacle_img = pygame.transform.scale(obstacle_img,(75,75))

fuel_img = pygame.image.load("E:\My Lesson\Bachelor\Projects\Computer Graphic\project\River Raid\Source/0458.png")
fuel_img = pygame.transform.scale(fuel_img,(60,60))


#voice_loading
shoot_sound = pygame.mixer.Sound("E:\My Lesson\Bachelor\Projects\Computer Graphic\project\River Raid\Source/01.mp3")
explosion_sound = pygame.mixer.Sound("E:\My Lesson\Bachelor\Projects\Computer Graphic\project\River Raid\Source/02.mp3")
fuel_collect_sound = pygame.mixer.Sound("E:\My Lesson\Bachelor\Projects\Computer Graphic\project\River Raid\Source/00.mp3")


clock = pygame.time.Clock()

def spawn_obstacle():
    x = random.randint(100, WIDTH - 150)
    y = -50
    obstacle = pygame.Rect(x, y, 50, 50)
    obstacles.append({"rect": obstacle, "health": 3})  # obstacle with iniate health 3

def spawn_fuel():
    x = random.randint(100, WIDTH - 130)
    y = -30
    fuel_items.append(pygame.Rect(x, y, 30, 30))

def game_over():
    font = pygame.font.SysFont(None, 75)
    text = font.render("Game Over", True, PLANE_COLOR)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

def show_instructions():
    font = pygame.font.SysFont(None, 35)
    screen.fill(WHITE)
    instructions = [
        "Welcome to River Ride!",
        "Move the plane with the mouse.",
        "Avoid obstacles and collect fuel items.",
        "Left-click to shoot bullets.",
        "Obstacles are destroyed after several hits.",
        "Press 'Space' to Start!"
    ]
    for i, line in enumerate(instructions):
        text = font.render(line, True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100 + i * 40))
    pygame.display.flip()

running = True
show_instructions()
waiting = True

while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            waiting = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            waiting = False

while running:
    screen.fill(WHITE)
    bg_y1 += 4
    bg_y2 += 4
    
    if bg_y1 >= HEIGHT:
        bg_y1 = -HEIGHT
    if bg_y2 >= HEIGHT:
        bg_y2 = -HEIGHT
    screen.blit(back_img,(0,bg_y1))
    screen.blit(back_img,(0,bg_y2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click for shoot
            shoot_sound.play()
            bullet = pygame.Rect(plane_x + plane_width // 2 - 5, plane_y, 10, 20)
            bullets.append(bullet)

    # move airplane with mouse
    mouse_x, _ = pygame.mouse.get_pos()
    if 100 <= mouse_x <= WIDTH - plane_width - 100:
        plane_x = mouse_x - plane_width // 2

    # move & present obstacle
    for obstacle in obstacles[:]:
        obs_rect = obstacle["rect"]
        obs_rect.y += obstacle_speed
        screen.blit(obstacle_img, obs_rect)

        # shoot bullet to obstacles
        for bullet in bullets[:]:
            if bullet.colliderect(obs_rect):
                obstacle["health"] -= 1
                bullets.remove(bullet)
                if obstacle["health"] <= 0:
                    explosion_sound.play()
                    obstacles.remove(obstacle)
                    score += 1
                break

        if obs_rect.colliderect(pygame.Rect(plane_x, plane_y, plane_width, plane_height)):
            game_over()
            running = False
        if obs_rect.y > HEIGHT:
            obstacles.remove(obstacle)

    # move & present fuel
    for fuel_item in fuel_items:
        fuel_item.y += fuel_speed
        screen.blit(fuel_img, fuel_item)
        if fuel_item.colliderect(pygame.Rect(plane_x, plane_y, plane_width, plane_height)):
            fuel_collect_sound.play()
            fuel_items.remove(fuel_item)
            fuel = min(fuel + 20, 100)
        elif fuel_item.y > HEIGHT:
            fuel_items.remove(fuel_item)

    # move & present bullet
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        pygame.draw.rect(screen, BULLET_COLOR, bullet)
        if bullet.y < 0:
            bullets.remove(bullet)

    # show score & fuel
    fuel -= 0.05
    fuel_bar_width = int(fuel * 2)
    pygame.draw.rect(screen, BLACK,(20,20,200,20))
    pygame.draw.rect(screen,FUEL_COLOR,(20,20,fuel_bar_width,20))
    if fuel <= 0:
        game_over()
        running = False

    pygame.draw.rect(screen, BLACK, (WIDTH - 150, 15, 180, 60) , border_radius=10)
    pygame.draw.rect(screen, WHITE, (WIDTH - 150, 20, 170, 50) , border_radius=10)
    
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 150, 20))

    # show airplane
    screen.blit(plane_img, (plane_x, plane_y))

    # create new obstacle & fuel
    if random.randint(0, 100) < 2:
        spawn_obstacle()
    if random.randint(0, 100) < 1:
        spawn_fuel()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()