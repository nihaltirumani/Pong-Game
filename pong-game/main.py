import pygame, random, math
from sys import exit

class Pong:
    def __init__(self, size, x, y):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = 7
        self.dir = random.randint(0, 90) - 45
        self.velx = self.speed * math.cos(self.dir)
        self.vely = self.speed * math.sin(self.dir)

    def draw(self, screen):
        pygame.draw.circle(screen, PRIMARY_COLOR, self.rect.center, self.size / 2)
    
    def update(self):
        global player1_score, player2_score
        if self.rect.left < 0 : 
            self.reset()
            player1_score += 1
        if self.rect.right > WIDTH:
            self.reset()
            player2_score += 1

        if self.rect.top < 0 or self.rect.bottom > HEIGHT: self.vely *= -1
        if self.rect.colliderect(player1) or self.rect.colliderect(player2): self.velx *= -1
        
        self.rect.x += self.velx
        self.rect.y += self.vely

    def reset(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.dir = random.randint(0, 90) - 45
        self.velx = self.speed * math.cos(self.dir)
        self.vely = self.speed * math.sin(self.dir)

pygame.init()

WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")
clock = pygame.time.Clock()
game_mode = 0

PRIMARY_COLOR = (46, 230, 46)
BG_COLOR = (0, 0, 35)

font1 = pygame.font.Font("Micro5-Regular.ttf", 100)

title = font1.render("PONG GAME", 0, PRIMARY_COLOR)
title_rect = title.get_rect(center=(WIDTH / 2, 100))

play_button_text = font1.render("PLAY", 0, BG_COLOR)
play_button_text_rect = play_button_text.get_rect(center=(WIDTH / 2, HEIGHT / 4 * 3))
play_button_rect = pygame.Rect(play_button_text_rect.topleft[0] - 10, play_button_text_rect.topleft[1], play_button_text_rect.width + 10, play_button_text_rect.height)

p2_button_text = font1.render("2 PLAYERS", 0, BG_COLOR)
p2_button_text_rect = p2_button_text.get_rect(center=(WIDTH / 4, HEIGHT / 2))
p2_button_rect = pygame.Rect(p2_button_text_rect.topleft[0] - 10, p2_button_text_rect.topleft[1], p2_button_text_rect.width + 10, p2_button_text_rect.height)

p1_button_text = font1.render("1 PLAYER", 0, BG_COLOR)
p1_button_text_rect = p1_button_text.get_rect(center=(WIDTH / 4 * 3, HEIGHT / 2))
p1_button_rect = pygame.Rect(p1_button_text_rect.topleft[0] - 10, p1_button_text_rect.topleft[1], p1_button_text_rect.width + 10, p1_button_text_rect.height)

score1 = font1.render("0", 0, PRIMARY_COLOR)
score1_rect = score1.get_rect(midtop=(WIDTH / 4, 40))
score2 = font1.render("0", 0, PRIMARY_COLOR)
score2_rect = score2.get_rect(midtop=(WIDTH / 4 * 3, 40))

player1 = pygame.Rect(WIDTH - 30 - 15, HEIGHT / 2, 15, 75)
player1_speed = 3
player1_score = 0

player2 = pygame.Rect(30, HEIGHT / 2, 15, 75)
player2_speed = 3
player2_score = 0

pong = Pong(30, WIDTH / 2, HEIGHT / 2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(BG_COLOR)

    mouse_pos = pygame.mouse.get_pos()
    mouse = pygame.mouse.get_pressed()

    if game_mode > 1:

        pong.draw(screen)
        pong.update()

        # player 1 controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player1.top >= player1_speed :
            player1.y -= player1_speed
        if keys[pygame.K_DOWN] and player1.bottom <= HEIGHT - player1_speed :
            player1.y += player1_speed

        # player 2 (AI)
        if game_mode == 2:
            if pong.velx < 0:
                if player2.top > pong.rect.top:
                    player2.y -= player2_speed
                if player2.bottom < pong.rect.bottom:
                    player2.y += player2_speed
        elif game_mode == 3:
            if keys[pygame.K_w] and player2.top >= player2_speed :
                player2.y -= player2_speed
            if keys[pygame.K_s] and player2.bottom <= HEIGHT - player2_speed :
                player2.y += player2_speed
        
        pygame.draw.rect(screen, PRIMARY_COLOR, player1)
        pygame.draw.rect(screen, PRIMARY_COLOR, player2)

        score1 = font1.render(str(player2_score), 0, PRIMARY_COLOR)
        score1_rect = score1.get_rect(midtop=(WIDTH / 4, 40))

        score2 = font1.render(str(player1_score), 0, PRIMARY_COLOR)
        score2_rect = score2.get_rect(midtop=(WIDTH / 4 * 3, 40))

        screen.blit(score1, score1_rect)
        screen.blit(score2, score2_rect)

    elif game_mode == 0:
        if play_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]) and not mouse[0] and old_mouse[0]:
                game_mode = 1
        old_mouse = mouse

        screen.blit(title, title_rect)
        pygame.draw.rect(screen, PRIMARY_COLOR, play_button_rect)
        screen.blit(play_button_text, play_button_text_rect)
    
    elif game_mode == 1:
        if p1_button_text_rect.collidepoint(mouse_pos[0], mouse_pos[1]) and not mouse[0] and old_mouse[0]:
                game_mode = 2
        if p2_button_text_rect.collidepoint(mouse_pos[0], mouse_pos[1]) and not mouse[0] and old_mouse[0]:
                game_mode = 3
        old_mouse = mouse

        pygame.draw.rect(screen, PRIMARY_COLOR, p1_button_rect)
        screen.blit(p1_button_text, p1_button_text_rect)
        pygame.draw.rect(screen, PRIMARY_COLOR, p2_button_rect)
        screen.blit(p2_button_text, p2_button_text_rect)

    pygame.display.update()
    clock.tick(60)