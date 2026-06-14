import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 10) 
GREEN = (50, 255, 50)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 0)
PURPLE = (200, 50, 255)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WAVES DEFENDER")
clock = pygame.time.Clock()


font_small = pygame.font.SysFont("Arial", 20, bold=True)
font_large = pygame.font.SysFont("Arial", 60, bold=True)
font_title = pygame.font.SysFont("Impact", 80)


class Player:
    def __init__(self):
        self.width = 50
        self.height = 30
        self.exact_x = float(WIDTH // 2 - self.width // 2)
        self.exact_y = float(HEIGHT - 50)
        self.speed = 7
        self.rect = pygame.Rect(int(self.exact_x), int(self.exact_y), self.width, self.height)
        self.cooldown = 0
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.exact_x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.exact_x += self.speed
        
        self.rect.x = int(self.exact_x)
            
    def draw(self, surface):
        pygame.draw.rect(surface, YELLOW, self.rect, border_radius=5)
        canon_rect = pygame.Rect(self.rect.centerx - 6, self.rect.top - 12, 12, 12)
        pygame.draw.rect(surface, GREEN, canon_rect)
        pygame.draw.polygon(surface, BLUE, [(self.rect.left - 10, self.rect.bottom), 
                                              (self.rect.left, self.rect.top + 10),
                                              (self.rect.left, self.rect.bottom)])
        pygame.draw.polygon(surface, BLUE, [(self.rect.right + 10, self.rect.bottom), 
                                              (self.rect.right, self.rect.top + 10),
                                              (self.rect.right, self.rect.bottom)])

class Bullet:
    def __init__(self, x, y):
        self.exact_y = float(y - 15)
        self.rect = pygame.Rect(x - 3, int(self.exact_y), 6, 20)
        self.speed = 10
        
    def move(self):
        self.exact_y -= self.speed
        self.rect.y = int(self.exact_y)
        
    def draw(self, surface):
        pygame.draw.rect(surface, YELLOW, self.rect, border_radius=3)

class Enemy:
    def __init__(self, x, y, speed_x):
        self.exact_x = float(x)
        self.exact_y = float(y)
        self.rect = pygame.Rect(int(self.exact_x), int(self.exact_y), 40, 30)
        self.speed_x = speed_x
        
    def move(self, direction):
        self.exact_x += self.speed_x * direction
        self.rect.x = int(self.exact_x)
        
    def drop(self):
        self.exact_y += 25
        self.rect.y = int(self.exact_y)
        
    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, (self.rect.x + 8, self.rect.y + 8, 8, 8))
        pygame.draw.rect(surface, WHITE, (self.rect.x + 24, self.rect.y + 8, 8, 8))
        pygame.draw.rect(surface, BLACK, (self.rect.x + 10, self.rect.y + 10, 4, 4))
        pygame.draw.rect(surface, BLACK, (self.rect.x + 26, self.rect.y + 10, 4, 4))

#BACKGROUND 
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(0.5, 2.5)
        self.size = random.randint(1, 3)
        
    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
            
    def draw(self, surface):
        color = (200, 200, 255) 
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

def draw_text(surface, text, font, color, x, y, center=False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def show_menu(title, subtitle, score=None):
    stars = [Star() for _ in range(50)]
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

        screen.fill(BLACK)
        
        for star in stars:
            star.move()
            star.draw(screen)
            
        draw_text(screen, title, font_title, YELLOW, WIDTH//2, HEIGHT//3, center=True)
        draw_text(screen, subtitle, font_small, WHITE, WIDTH//2, HEIGHT//2, center=True)
        
        if score is not None:
            draw_text(screen, f"Puntuación Final: {score}", font_large, GREEN, WIDTH//2, HEIGHT//2 + 80, center=True)
            
        pygame.display.flip()

def main():
    show_menu("WAVES DEFENDER", "PRESS SPACE TO START")
    

    score = 0
    level = 1
    lives = 3
    
    player = Player()
    bullets = []
    enemies = []
    stars = [Star() for _ in range(80)]
    

    enemy_direction = 1 
    base_enemy_speed = 2.0
    
    def spawn_enemies():
        nonlocal enemy_direction
        enemies.clear()
        enemy_direction = 1
        rows = 4
        cols = 8

        current_speed = base_enemy_speed + (level - 1) * 0.6
        
        for row in range(rows):
            for col in range(cols):
                enemy_x = 100 + col * 60
                enemy_y = 50 + row * 50
                enemies.append(Enemy(enemy_x, enemy_y, current_speed))

    spawn_enemies()
    
    running = True
    while running:
        clock.tick(FPS) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        keys = pygame.key.get_pressed()
        player.move(keys)
        
        if player.cooldown > 0:
            player.cooldown -= 1
            
        if keys[pygame.K_SPACE] and player.cooldown == 0:
            bullets.append(Bullet(player.rect.centerx, player.rect.top))
            player.cooldown = 10 
            
        
        for star in stars:
            star.move()
            
        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)
                
        move_down = False
        for enemy in enemies:
            enemy.move(enemy_direction)
            if enemy.rect.right >= WIDTH - 10 or enemy.rect.left <= 10:
                move_down = True
                
        if move_down:
            for enemy in enemies:
                enemy.move(-enemy_direction)
                enemy.drop()
            enemy_direction *= -1
                
#COLISSIONS
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if enemy in enemies:
                        enemies.remove(enemy)
                    score += 10 * level #POINTS FOR LEVEL
                    break 
                    
        for enemy in enemies:
            if enemy.rect.colliderect(player.rect) or enemy.rect.bottom >= HEIGHT:
                lives -= 1
                if lives <= 0:
                    show_menu("GAME OVER", "PRESS SPACE TO TRY AGAIN", score)
                    score = 0
                    level = 1
                    lives = 3
                    player = Player()
                    bullets.clear()
                    spawn_enemies()
                else:
                    bullets.clear()
                    player = Player()
                    spawn_enemies()
                break
                
        if len(enemies) == 0:
            level += 1
            bullets.clear()
            spawn_enemies()
            
        screen.fill(BLACK)
        
        for star in stars:
            star.draw(screen)
            
        player.draw(screen)
        
        for bullet in bullets:
            bullet.draw(screen)
            
        for enemy in enemies:
            enemy.draw(screen)
            
        draw_text(screen, f"POINTS: {score}", font_small, WHITE, 20, 20)
        draw_text(screen, f"LEVEL: {level}", font_small, YELLOW, WIDTH - 120, 20)
        draw_text(screen, f"LIVES: {lives}", font_small, RED, WIDTH // 2, 20, center=True)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
