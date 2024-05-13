import pygame
import sys
from paths import cesty
import random

pygame.init()

path = cesty['assets']

screen = pygame.display.set_mode((816,624))
pygame.display.set_caption("Bubble Pop Frenzy - TNejk edition")
clock = pygame.time.Clock()

cannon = pygame.image.load(path.joinpath('cannon.png')).convert_alpha()
cannon = pygame.transform.scale(cannon, (cannon.get_width()*4,cannon.get_height()*4))
red_ball = pygame.image.load(path.joinpath('red_ball.png')).convert_alpha()
red_ball = pygame.transform.scale(red_ball, (red_ball.get_width()*3,red_ball.get_height()*3))
green_ball = pygame.image.load(path.joinpath('green_ball.png')).convert_alpha()
green_ball = pygame.transform.scale(green_ball, (green_ball.get_width()*3,green_ball.get_height()*3))
blue_ball = pygame.image.load(path.joinpath('blue_ball.png')).convert_alpha()
blue_ball = pygame.transform.scale(blue_ball, (blue_ball.get_width()*3,blue_ball.get_height()*3))
yellow_ball = pygame.image.load(path.joinpath('yellow_ball.png')).convert_alpha()
yellow_ball = pygame.transform.scale(yellow_ball, (yellow_ball.get_width()*3,yellow_ball.get_height()*3))

balls = []
player_ball_path = ''

y = 0
for i in range(5):
    x = 0
    for j in range(17):
        ball = random.choice(('red_ball.png','green_ball.png','blue_ball.png','yellow_ball.png'))
        ball_img = pygame.image.load(path.joinpath(ball)).convert_alpha()
        ball_img = pygame.transform.scale(ball_img, (ball_img.get_width() * 3, ball_img.get_height() * 3,))
        ball_rect = ball_img.get_rect(topleft=(x,y))
        balls.append([ball_img,ball_rect,x,y,ball])
        x += 48
    y += 48

numerationsx = []
max_numx = 816
curr_numx = 0
while curr_numx < max_numx:
    numerationsx.append(curr_numx)
    curr_numx += 48

numerationsy = []
max_numy = 624//2
curr_numy = 0
while curr_numy < max_numy:
    numerationsy.append(curr_numy)
    curr_numy += 48

def player_ball_choice():
    global player_ball_path
    player_ball_path = random.choice(('red_ball.png','green_ball.png','blue_ball.png','yellow_ball.png'))
    player_ball = pygame.image.load(path.joinpath(player_ball_path)).convert_alpha()
    player_ball = pygame.transform.scale(player_ball, (player_ball.get_width() * 3, player_ball.get_height() * 3))
    return player_ball

player_ball_img = player_ball_choice()

pygame.mouse.set_pos(816//2, 586)

while True:   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(1)
    

    screen.fill((0,0,0))    

    for ball in balls:
        screen.blit(ball[0],(ball[2],ball[3]))
    
    mx,my = pygame.mouse.get_pos()
    player_ball_rect = player_ball_img.get_rect(center=(mx,my))
    screen.blit(player_ball_img,(mx-(player_ball_img.get_width()/2),my-(player_ball_img.get_height()/2)))

    for ball in balls[:]:
        ball_center = ball[1].center
        distance_squared = (player_ball_rect.centerx - ball_center[0])**2 + (player_ball_rect.centery - ball_center[1])**2
        if distance_squared <= (player_ball_rect.width / 2 + ball[1].width / 2)**2:
            if player_ball_path == ball[4]:
                balls.remove(ball)
            else:
                # Determine the collision point along the x-axis
                if player_ball_rect.centerx < ball[1].left:
                    collision_x = ball[1].left - player_ball_rect.width // 2
                elif player_ball_rect.centerx > ball[1].right:
                    collision_x = ball[1].right + player_ball_rect.width // 2
                else:
                    collision_x = player_ball_rect.centerx

                # Adjust the y-coordinate based on whether the player's ball is above or below the other ball
                y = ball[1].top - player_ball_rect.height if player_ball_rect.centery < ball[1].top else ball[1].bottom

                # Set the x-coordinate of the player's ball to the collision point
                x = collision_x

                # Create a new rectangle for the player's ball at the collision point
                new_rect = player_ball_img.get_rect(top=y, left=x)

                # Append the new position and rectangle to the balls list
                balls.append([player_ball_img, new_rect, x, y, player_ball_path])
                
            pygame.mouse.set_pos(816//2, 586)
            player_ball_img = player_ball_choice()


    pygame.display.update()
    clock.tick(60)