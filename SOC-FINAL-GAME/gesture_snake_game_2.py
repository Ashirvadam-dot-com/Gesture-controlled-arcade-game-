import cv2 as cv
import mediapipe as mp
import pygame
import time
import random 
import sys
from collections import deque

trail_points = deque(maxlen=20)

## MEDIAPIPE SETUP
mp_hands         =  mp.solutions.hands
mp_drawing_tools =  mp.solutions.drawing_utils

hands=mp_hands.Hands(
    static_image_mode         =   False,
    max_num_hands             =   2,
    min_detection_confidence  =   0.7,
    min_tracking_confidence   =   0.5
)

## LANDMARK STYLE 
landmark_style = mp_drawing_tools.DrawingSpec(
    color = (255, 0, 0),
    thickness = -1,
    circle_radius = 5
)

## CONNECTION STYLE 
connection_style = mp_drawing_tools.DrawingSpec(
    color = (255, 255, 255),
    thickness = 3
)



## CORDINATES OF LANDMARKS
def get_cordinates(img, hand_landmark):
    lm_list = []
    h, w = img.shape[:2]
    
    for id , lm in enumerate (hand_landmark.landmark):
        cx = int(lm.x*w)
        cy = int(lm.y*h)
        lm_list.append([id, cx, cy])
    return lm_list

current_point = (0,0)
previous_point = current_point
left_count , right_count , up_count , down_count = 0,0,0,0

## GESTURE CREATOR
def hand_oreo(lm_list , hand_label):
    global gesture , trail_points , current_point, previous_point
    global left_count , right_count , up_count , down_count
    finger_oreo = []
    
    if hand_label == 'Right' :
        finger_oreo.append( 1 if lm_list[2][1] > lm_list[4][1] else 0)
    else :
        finger_oreo.append( 1 if lm_list[2][1] < lm_list[4][1] else 0)
    tips = [8, 12, 16, 20]
    for tip in tips :
        finger_oreo.append( 1 if lm_list[tip-2][2] > lm_list[tip][2] else 0)
        
    count = sum(finger_oreo)
    gesture = 'NONE'

    if count == 0:
        gesture = 'FIST'
    elif count == 5 :
        gesture = 'OPEN PALM'
    elif finger_oreo == [0, 1, 1, 0, 0]:
        gesture = 'PEACE'
    elif finger_oreo==[0,1,0,0,0]:
        gesture= "POINTING"
    elif hand_label == "Right" :
        current_point = lm_list[8][1:]
    
        dx = current_point[0] - previous_point[0]
        dy = current_point[1] - previous_point[1]
        
        previous_point   = current_point
        # horizontal swipe , left and right
        if -20 <= dy <= 20 :
            if dx < 0 :
                left_count +=1
                right_count , up_count , down_count = 0,0,0
            elif dx >=0 :
                right_count +=1
                left_count , up_count , down_count = 0,0,0
        if -15 <= dx <= 15 :
            if dy < 0 :
                up_count +=1
                right_count , left_count , down_count = 0,0,0
            elif dy >= 0 :
                down_count +=1
                left_count , up_count , right_count = 0,0,0    
        gesture = "LEFT" if left_count > 2 else gesture
        gesture = "RIGHT" if right_count > 2 else gesture
        gesture = "UP" if up_count > 2 else gesture
        gesture = "DOWN" if down_count > 2 else gesture
    return gesture
    
        
CELL_SIZE   =   30
GRID_WIDTH  =   30
GRID_HEIGHT =   22
WIDTH       =   CELL_SIZE * GRID_WIDTH
HEIGHT      =   CELL_SIZE * GRID_HEIGHT

# --- Colors ---
BG_COLOR     = (15, 15, 25)
SNAKE_HEAD   = (0, 230, 120)
SNAKE_BODY   = (0, 170, 90)
FOOD_COLOR   = (240, 70, 90)
TEXT_COLOR   = (235, 235, 245)
GRID_COLOR   = (30, 30, 45)

# RANDOM FOOD GENERATOR

def random_food(snake_pos):
    while True:
        pos = ( random.randint(2 , GRID_WIDTH - 3) , random.randint(2 , GRID_HEIGHT - 3) )
        if pos not in snake_pos:
            break
    return pos

def draw_cell(surface , color , pos ):
    X = CELL_SIZE * pos[0]
    Y = CELL_SIZE * pos[1]
    pygame.draw.rect(surface , color , (X, Y, CELL_SIZE, CELL_SIZE) )
    pygame.draw.rect(surface , BG_COLOR , (X, Y, CELL_SIZE, CELL_SIZE) ,1)
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH , HEIGHT))
    pygame.display.set_caption('GESTURE CONTROLLED ACRADE GAME - SNAKE')
    
    SMALL_FONT = pygame.font.SysFont('consolas' , 22)
    MID_FONT   = pygame.font.SysFont('consolas' , 30)
    BIG_FONT   = pygame.font.SysFont('consolas' , 40)
    
    GAME_STARTED = False
    GAME_OVER    = False
    GAME_PAUSED  = False
    HIGH_SCORE   = 0
    
    def reset_game():
        start = ( GRID_WIDTH//2 , GRID_HEIGHT//2 )
        return [start], (1, 0), 0, random_food([start]) 
    
    snake_pos, direction, score, food_pos = reset_game()
    
    MOVE_DELAY_START = 150
    MOVE_DELAY       = MOVE_DELAY_START
    LAST_MOVE_TIME   = pygame.time.get_ticks()
    SPEED_DELAY      = 5
    MOVE_DELAY_MIN   = 80
    
    
    STABLE_GESTURE   = {'Left' :'NONE', 'Right' :'NONE'}
    PREVIOUS_GESTURE = {'Left' :'NONE', 'Right' :'NONE'}
    GESTURE_COUNT    = {'Left' :0 , 'Right' :0}
    STABILITY_FRAMES = 5
    
    cap = cv.VideoCapture(0)
    
    ctime = 0
    ptime = 0
    
    while True:
        success, frame = cap.read()
        if not success:
            print("Camera not found")
            break
        img     = cv.flip(frame, 1)
        rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        
        results = hands.process(rgb_img)
        if results.multi_handedness and results.multi_hand_landmarks :
            for handedness , hand_landmark in zip( results.multi_handedness , results.multi_hand_landmarks ):
                mp_drawing_tools.draw_landmarks(
                    img,
                    hand_landmark,
                    mp_hands.HAND_CONNECTIONS,
                    landmark_style,
                    connection_style   
                )
                
                hand_label = handedness.classification[0].label
                lm_list    = get_cordinates(img, hand_landmark)
                gesture = hand_oreo(lm_list, hand_label)
                
                if gesture == PREVIOUS_GESTURE[hand_label]:
                    GESTURE_COUNT[hand_label] +=1
                else :
                    GESTURE_COUNT[hand_label]    = 1
                    PREVIOUS_GESTURE[hand_label] = gesture
                if GESTURE_COUNT[hand_label] > STABILITY_FRAMES :
                    STABLE_GESTURE[hand_label] = gesture
                    
                for i , point in enumerate (trail_points):
                            radius = max(1, (12-i//2))
                            blue = max(210, 250 - (i*2))
                            green = max(50, 195-(i*8))
                            red = max(10, 140 - (i*7))
                            color = (blue, green, red)
                            cv.circle(img, point , radius , color, -1)
                    
        ##  EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_q :
                    pygame.quit()
                    sys.exit()       
                
        if not GAME_STARTED :
            if STABLE_GESTURE['Left']== 'FIST' :
                GAME_STARTED = True
                STABLE_GESTURE['Left'] = "NONE"
                MOVE_DELAY     = MOVE_DELAY_START
                LAST_MOVE_TIME = pygame.time.get_ticks()
                snake_pos, direction, score, food_pos = reset_game()
                
        elif GAME_OVER :
            if STABLE_GESTURE['Left'] == 'FIST' :
                GAME_OVER , GAME_PAUSED = False, False
                STABLE_GESTURE['Left'] = "NONE"
                MOVE_DELAY     = MOVE_DELAY_START
                LAST_MOVE_TIME = pygame.time.get_ticks()
                snake_pos, direction, score, food_pos = reset_game()
                
        else :
            if not GAME_PAUSED :
                if STABLE_GESTURE['Left'] == 'PEACE' :
                    GAME_PAUSED = True 
                elif STABLE_GESTURE['Right'] == 'UP' and direction != (0, 1):
                    direction = (0, -1)
                elif STABLE_GESTURE['Right'] == 'DOWN' and direction != (0, -1) :
                    direction = (0, 1)
                elif STABLE_GESTURE['Right'] == 'LEFT' and direction != (1, 0) :
                    direction = (-1, 0)
                elif STABLE_GESTURE['Right'] == 'RIGHT' and direction != (-1, 0) :
                    direction = (1, 0)
            else :
                if STABLE_GESTURE['Right'] in ["UP", "DOWN", "LEFT", "RIGHT"]:
                    GAME_PAUSED = False
                    
        current_time = pygame.time.get_ticks()
        
        ## GAME UPDATING
        if GAME_STARTED and not GAME_OVER and not GAME_PAUSED and (current_time - LAST_MOVE_TIME > MOVE_DELAY):
            LAST_MOVE_TIME = current_time
            
            head = snake_pos[0]
            NEW_HEAD = ( head[0]+direction[0] , head[1]+direction[1] )
            
            HIT_WALL = ( NEW_HEAD[0] < 0 or NEW_HEAD[0] >= GRID_WIDTH
                        or NEW_HEAD[1] < 0 or NEW_HEAD[1] >= GRID_HEIGHT)
            HIT_SELF = NEW_HEAD in snake_pos
            
            if HIT_SELF or HIT_WALL :
                GAME_OVER = True 
                HIGH_SCORE = max(score , HIGH_SCORE)
                
            else :
                snake_pos.insert(0, NEW_HEAD)
                if NEW_HEAD == food_pos :
                    score += 1
                    food_pos = random_food(snake_pos)
                    MOVE_DELAY = max(MOVE_DELAY_MIN , MOVE_DELAY - SPEED_DELAY)
                else :
                    snake_pos.pop()
                    
                    
        ## RENDERING 
        screen.fill(BG_COLOR)
        
        if not GAME_STARTED :
            txt1 = BIG_FONT.render('WELCOME to SNAKE GAME', True , SNAKE_HEAD )
            txt2 = MID_FONT.render('Make LEFT FIST to start the game', True , TEXT_COLOR)
            screen.blit(txt1 , (WIDTH//2 - txt1.get_width()//2 , HEIGHT//2 - 40 ))
            screen.blit(txt2 , (WIDTH//2 - txt2.get_width()//2 , HEIGHT//2 + 20 ))
            
        else :
            for c in range(GRID_WIDTH) :
                pygame.draw.line(screen, GRID_COLOR, (c*CELL_SIZE, 0), (c*CELL_SIZE, HEIGHT))
            for r in range(GRID_HEIGHT) :
                pygame.draw.line(screen, GRID_COLOR, (0, r*CELL_SIZE), (WIDTH , r*CELL_SIZE))
                
            draw_cell(screen, FOOD_COLOR , food_pos)
            for i , part in enumerate(snake_pos):
                color = SNAKE_HEAD if i == 0 else SNAKE_BODY
                draw_cell(screen , color , part)
                
            score_surf = SMALL_FONT.render(f"Score: {score} | Gesture: {STABLE_GESTURE}", True, TEXT_COLOR)
            hs_surf = SMALL_FONT.render(f"Best: {HIGH_SCORE}", True, (255, 215, 0))    # gold color
            screen.blit(score_surf, (8, 6))
            screen.blit(hs_surf, (WIDTH - hs_surf.get_width() - 8, 6))    # pin to top right corner


            if GAME_PAUSED and not GAME_OVER:
                pause_surf = BIG_FONT.render("PAUSED", True, TEXT_COLOR)
                sub_surf = MID_FONT.render("Point in any direction to resume", True, TEXT_COLOR)
                screen.blit(
                pause_surf, (WIDTH//2 - pause_surf.get_width()//2, HEIGHT//2 - 40))
                screen.blit(sub_surf, (WIDTH//2 - sub_surf.get_width()//2, HEIGHT//2 + 15))

            if GAME_OVER:
                msg = BIG_FONT.render("GAME OVER", True, FOOD_COLOR)
                sub = MID_FONT.render("Make a FIST to restart", True, TEXT_COLOR)
                screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 40))
                screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 15))  
                
        pygame.display.flip()
        
        cv.putText(img, "LEFT HAND :", (10,30), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0,0,0), 2)
        cv.putText(img, "RIGHT HAND :", (img.shape[1]-260 ,30), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0,0,0), 2)
        cv.putText(img, f"{STABLE_GESTURE['Left']}", (10,70), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
        cv.putText(img, f"{STABLE_GESTURE['Right']}", (img.shape[1]-260, 70), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
        
        ctime = time.time()
        fps = 1/(ctime - ptime)
        ptime = ctime
        cv.putText(img, f"FPS : {int(fps)}", (img.shape[1]//2-50 , img.shape[0]-10 ), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.2, (0, 0, 0), 2)
        cv.imshow('vision tracker ',img)
        
        if cv.waitKey(1) & 0xFF==ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()       
            