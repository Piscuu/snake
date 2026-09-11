pip install pygame
import pygame, random

pygame.init()
W,H,CELL=600,400,20
screen=pygame.display.set_mode((W,H))
pygame.display.set_caption("Snake")
clock=pygame.time.Clock()
font=pygame.font.SysFont(None,28)
BIG=pygame.font.SysFont(None,48)
BLACK=(20,20,20);GRID=(40,40,40);GREEN=(0,180,0);HEAD=(0,255,0);RED=(220,50,50);WHITE=(240,240,240)
WRAP=True

def food_pos(s):
    while True:
        p=[random.randrange(0,W,CELL),random.randrange(0,H,CELL)]
        if p not in s:return p

best=0

def reset():
    x,y=W//2,H//2
    snake=[[x,y]]
    return snake,[CELL,0],food_pos(snake),0,8

state="menu"
snake,dir,food,score,speed=reset()

while True:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit();raise SystemExit
        if e.type==pygame.KEYDOWN:
            if state=="menu" and e.key==pygame.K_SPACE:
                snake,dir,food,score,speed=reset();state="play"
            elif state=="gameover":
                if e.key==pygame.K_r:
                    snake,dir,food,score,speed=reset();state="play"
                elif e.key==pygame.K_ESCAPE:
                    state="menu"
            elif state=="play":
                if e.key==pygame.K_p: state="pause"
                if e.key==pygame.K_UP and dir[1]==0: dir=[0,-CELL]
                if e.key==pygame.K_DOWN and dir[1]==0: dir=[0,CELL]
                if e.key==pygame.K_LEFT and dir[0]==0: dir=[-CELL,0]
                if e.key==pygame.K_RIGHT and dir[0]==0: dir=[CELL,0]
            elif state=="pause" and e.key==pygame.K_p:
                state="play"

    if state=="play":
        hx,hy=snake[-1]
        hx+=dir[0]; hy+=dir[1]
        if WRAP:
            hx%=W; hy%=H
        elif hx<0 or hx>=W or hy<0 or hy>=H:
            best=max(best,score); state="gameover"
            continue
        head=[hx,hy]
        if head in snake:
            best=max(best,score); state="gameover"; continue
        snake.append(head)
        if head==food:
            score+=1
            speed=min(20,8+score//2)
            food=food_pos(snake)
        else:
            snake.pop(0)

    screen.fill(BLACK)
    if state in ("play","pause","gameover"):
        for x in range(0,W,CELL): pygame.draw.line(screen,GRID,(x,0),(x,H))
        for y in range(0,H,CELL): pygame.draw.line(screen,GRID,(0,y),(W,y))
        pygame.draw.rect(screen,RED,(*food,CELL,CELL))
        for b in snake[:-1]:
            pygame.draw.rect(screen,GREEN,(*b,CELL,CELL))
        pygame.draw.rect(screen,HEAD,(*snake[-1],CELL,CELL))
        screen.blit(font.render(f"Puntaje: {score}  Record: {best}",True,WHITE),(10,10))
    if state=="menu":
        screen.blit(BIG.render("SNAKE",True,WHITE),(240,120))
        screen.blit(font.render("ESPACIO para jugar",True,WHITE),(200,190))
    elif state=="pause":
        screen.blit(BIG.render("PAUSA",True,WHITE),(240,180))
    elif state=="gameover":
        screen.blit(BIG.render("GAME OVER",True,RED),(180,150))
        screen.blit(font.render("R: Reiniciar   ESC: Menu",True,WHITE),(170,220))
    pygame.display.flip()
    clock.tick(speed if state=="play" else 30)
