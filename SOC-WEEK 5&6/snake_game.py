import pygame
import random
import sys

CELL_SIZE   =   30
GRID_WIDTH  =   30
GRID_HEIGHT =   25
WIDTH       =   CELL_SIZE*GRID_WIDTH
HEIGHT      =   CELL_SIZE*GRID_HEIGHT

WHITISH      =   (235 ,235,245)
BG_COLOR     =   (22,53,36)
GRID_TILES   =   (54 ,112,77)
SNAKE_HEAD   =   (255,191,0)
SNAKE_BODY   =   (211,175,55)
FOOD_COLOR   =   (241,75,75)

def random_food(snake):
    while True:
        pos=(random.randint(2,GRID_WIDTH-3),random.randint(2,GRID_HEIGHT-3))
        if pos not in snake:
            return pos
        
class draw:
    def __init__(self,surface):
        self.surface=surface
    def circle(self,pos,color):
        self.pos=pos
        self.color=color
        x   = CELL_SIZE*pos[0]
        y   = CELL_SIZE*pos[1]
        r=CELL_SIZE/2
        pygame.draw.circle(self.surface,self.color,(x+r,y+r),r)
        pygame.draw.circle(self.surface,BG_COLOR,(x+r,y+r),r,1)
    def rectangle(self,pos,color):
        self.pos=pos
        self.color=color
        x   = CELL_SIZE*pos[0]
        y   = CELL_SIZE*pos[1]
        pygame.draw.rect(self.surface,self.color,(x,y,CELL_SIZE,CELL_SIZE))
        pygame.draw.rect(self.surface,BG_COLOR,(x,y,CELL_SIZE,CELL_SIZE),1)
        
def main():
    pygame.init()
    screen=pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("SNAKE GAME")
    
    FONT      =   pygame.font.SysFont('consolas',22)
    BIG_FONT  =   pygame.font.SysFont('consolas',40,bold=True)
    MEDIUM_FONT=  pygame.font.SysFont('consolas',45,bold=True)
    
    GAME_STARTED    = False
    GAME_OVER       = False
    GAME_PAUSED     = False
    HIGH_SCORE      = 0
    
    MOVE_DELAY_START=200
    MOVE_DELAY_MIN=80
    SPEED_STEP=5
    LAST_MOVE_TIME=pygame.time.get_ticks()
    MOVE_DELAY=MOVE_DELAY_START
    
    
    def reset_game():
        start=(GRID_WIDTH//2,GRID_HEIGHT//2)
        return [start],(1,0),random_food([start]),0
    
    snake_pos,direction,food_pos,score=reset_game()
    
    while True:
        for button in pygame.event.get():
            if button.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if button.type==pygame.KEYDOWN:
                if button.key==pygame.K_q:
                    pygame.quit()
                    sys.exit()
                    
                if not GAME_STARTED:
                    if button.key==pygame.K_SPACE:
                        GAME_STARTED    =True
                        snake_pos,direction,food_pos,score=reset_game()
                        MOVE_DELAY      =MOVE_DELAY_START
                        LAST_MOVE_TIME  =pygame.time.get_ticks()
                
                elif GAME_OVER:
                    if button.key==pygame.K_SPACE:
                        GAME_OVER       =False
                        GAME_PAUSED     =False
                        snake_pos,direction,food_pos,score=reset_game()
                        MOVE_DELAY      =MOVE_DELAY_START
                        LAST_MOVE_TIME  =pygame.time.get_ticks()
                        
                else:
                    if button.key==pygame.K_p:
                        GAME_PAUSED =not GAME_PAUSED
                        
                    if not GAME_PAUSED:
                        if button.key==pygame.K_UP and direction !=(0,1):
                            direction=(0,-1)
                        elif button.key==pygame.K_DOWN and direction !=(0,-1):
                            direction=(0,1)
                        elif button.key==pygame.K_LEFT and direction !=(1,0):
                            direction=(-1,0)
                        elif button.key==pygame.K_RIGHT and direction !=(-1,0):
                            direction=(1,0)
        
        current_time=pygame.time.get_ticks()
        if GAME_STARTED and not GAME_PAUSED and not GAME_OVER and (current_time-LAST_MOVE_TIME>MOVE_DELAY):
            LAST_MOVE_TIME=current_time
            head=snake_pos[0]
            new_head=(head[0]+direction[0],head[1]+direction[1]) 
            
            hit_wall=(new_head[0]<0 or new_head[0]>=GRID_WIDTH
                      or new_head[1]<0 or new_head[1]>=GRID_HEIGHT)
            
            hit_self=new_head in snake_pos
            
            if hit_wall or hit_self :
                GAME_OVER=True
                HIGH_SCORE=max(HIGH_SCORE,score)
                
            else:
                snake_pos.insert(0,new_head)
                if new_head==food_pos:
                    score+=1
                    MOVE_DELAY=max(MOVE_DELAY_MIN,MOVE_DELAY-SPEED_STEP)
                    food_pos=random_food(snake_pos)
                else:
                    snake_pos.pop()
                    
        
        screen.fill(BG_COLOR)
        
        if not GAME_STARTED:
            text1=BIG_FONT.render('WELCOME',True,WHITISH)
            text2=MEDIUM_FONT.render('SNAKE GAME', True , WHITISH)      
            text3=FONT.render('Press SPACE to START', True , WHITISH)  
            screen.blit(text1, (WIDTH//2-text1.get_width()//2,8*CELL_SIZE))
            screen.blit(text2, (WIDTH//2 - text2.get_width()//2 , 14*CELL_SIZE))
            screen.blit(text3, (WIDTH//2 - text3.get_width()//2 , 17*CELL_SIZE))
            
        else :
            for x in range(GRID_WIDTH):
                pygame.draw.line(screen,GRID_TILES,(x*CELL_SIZE,0),(x*CELL_SIZE,HEIGHT))
            for y in range(GRID_HEIGHT):
                pygame.draw.line(screen,GRID_TILES,(0,y*CELL_SIZE),(WIDTH,y*CELL_SIZE))    
                    
            painter=draw(screen)
            painter.rectangle(food_pos,FOOD_COLOR)
            for index, pos in enumerate(snake_pos):
                color=SNAKE_HEAD if index==0 else SNAKE_BODY
                painter.circle(pos,color)
            
            score_text=FONT.render(f'Score : {score}',True,WHITISH)
            best_text=FONT.render(f'Best : {HIGH_SCORE}',True,WHITISH)
            screen.blit(score_text,(6,6))
            screen.blit(best_text,(6,score_text.get_height() + 8))
            
            if GAME_PAUSED:
                pause_text1= MEDIUM_FONT.render('GAME IS PAUSED' , True , WHITISH )
                pause_text2= FONT.render('Press p to RESUME', True , WHITISH)
                
                screen.blit(pause_text1 , (WIDTH//2 - pause_text1.get_width()//2 , HEIGHT//2 - 40))
                screen.blit(pause_text2 , (WIDTH//2 - pause_text2.get_width()//2 , HEIGHT//2 + 20))
                
            if GAME_OVER:
                over_text1=MEDIUM_FONT.render('GAME IS OVER' , True , WHITISH)
                over_text2 = FONT.render('Press SPACE to RESTART | q to QUIT', True , WHITISH )
                
                screen.blit(over_text1 , (WIDTH//2 - over_text1.get_width()//2 , HEIGHT//2 - 40))
                screen.blit(over_text2 , (WIDTH//2 - over_text2.get_width()//2 , HEIGHT//2 + 20))
        
        pygame.display.flip()
        
if __name__ == '__main__':
    main()


