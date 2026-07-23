import cv2 as cv
import mediapipe as mp
import pygame
import time
import random 
import sys
import math
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


## CORDINATES OF LANDMARKS
def get_cordinates(img, hand_landmark):
    lm_list = []
    h, w = img.shape[:2]
    
    for id , lm in enumerate (hand_landmark.landmark):
        cx = int(lm.x*w)
        cy = int(lm.y*h)
        lm_list.append([id, cx, cy])
    return lm_list

def normalised_distance(lm_list,p1,p2):
    x1,y1=lm_list[p1][1],lm_list[p1][2]
    x2,y2=lm_list[p2][1],lm_list[p2][2]
    
    distance=math.hypot(x2-x1,y2-y1)
    
    ref=math.hypot(lm_list[0][1]-lm_list[9][1],lm_list[0][2]-lm_list[9][2])
    
    if ref==0:
        return distance
    else:
        return distance/ref


## GESTURE CREATOR
def finger_oreo_hand(lm_list,hand_label):
    tips=[8,12,16,20] # except thumb

    # normalised distance
    distance=normalised_distance(lm_list,4,8)

    Orientation=[]
    if hand_label=="Right":
        Orientation.append(1 if lm_list[3][1]>lm_list[4][1] else 0)
    else :
        Orientation.append(1 if lm_list[3][1]<lm_list[4][1] else 0)
    for tip in tips :
        Orientation.append(1 if lm_list[tip][2]<lm_list[tip-2][2] else 0)
        
    # orientation list has been created with 0's and 1's 
    gesture="NONE"
    if Orientation==[0,0,0,0,0]:
        gesture= "FIST"
    elif Orientation==[1,1,1,1,1]:
        gesture= "OPEN PALM"
    elif Orientation==[0,1,0,0,0]:
        gesture= "POINTING"
    elif Orientation==[0,1,1,0,0]:
        gesture= "PEACE"
    elif Orientation==[1,0,1,1,1]  and distance <0.25:
        gesture ="PINCH"
    
    return gesture

current_point = (0,0)
previous_point = current_point
left_count , right_count , up_count , down_count = 0,0,0,0
swipe = 'NONE'
def dynamic_gesture( lm_list) :
    global trail_points , current_point, previous_point, swipe
    global left_count , right_count , up_count , down_count
    
    current_point = lm_list[8][1:]
    
    dx = current_point[0] - previous_point[0]
    dy = current_point[1] - previous_point[1]
    
    previous_point   = current_point
    trail_points.appendleft(current_point)
    
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
    swipe = "LEFT" if left_count > 1 else swipe
    swipe = "RIGHT" if right_count > 1 else swipe
    swipe = "UP" if up_count > 1 else swipe
    swipe = "DOWN" if down_count > 1 else swipe
    
    return swipe
    
        
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
    
    
    cap = cv.VideoCapture(0)
    
    ctime = 0
    ptime = 0
    
    GESTURE   = {'Left' :'NONE', 'Right' :'NONE'}
    PREVIOUS_GESTURE = {'Left' :'NONE', 'Right' :'NONE'}
    GESTURE_COUNT    = {'Left' :0 , 'Right' :0}
    STABILITY_FRAMES = 5
    swipe_gesture = {'Left' :'NONE', 'Right' :'NONE'}
    while True:
        success, frame = cap.read()
        if not success:
            print("Camera not found")
            break
        img     = cv.flip(frame, 1)
        rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        
        results = hands.process(rgb_img)
        hands_present_this_frame = []
        
        if results.multi_handedness and results.multi_hand_landmarks :
            for handedness , hand_landmark in zip( results.multi_handedness , results.multi_hand_landmarks ):             
                hand_label = handedness.classification[0].label
                lm_list    = get_cordinates(img, hand_landmark)
                gesture = finger_oreo_hand(lm_list, hand_label)
                hands_present_this_frame.append(hand_label)
                
                if gesture == PREVIOUS_GESTURE[hand_label]:
                    GESTURE_COUNT[hand_label] +=1
                else :
                    GESTURE_COUNT[hand_label]    = 1
                    PREVIOUS_GESTURE[hand_label] = gesture
                if GESTURE_COUNT[hand_label] > STABILITY_FRAMES :
                    GESTURE[hand_label] = gesture
                
                if hand_label == "Right" :
                    swipe_gesture[hand_label] = dynamic_gesture(lm_list)
                
                    
                for i , point in enumerate (trail_points):
                            radius = max(1, (12-i//2))
                            blue = max(210, 250 - (i*2))
                            green = max(50, 195-(i*8))
                            red = max(10, 140 - (i*7))
                            color = (blue, green, red)
                            cv.circle(img, point , radius , color, -1)
                            
            if "Left" not in hands_present_this_frame:
                GESTURE['Left'] = 'NONE'
                PREVIOUS_GESTURE['Left'] = 'NONE'
                GESTURE_COUNT['Left'] = 0
                
            if "Right" not in hands_present_this_frame:
                GESTURE['Right'] = 'NONE'
                PREVIOUS_GESTURE['Right'] = 'NONE'
                GESTURE_COUNT['Right'] = 0
                swipe_gesture['Right'] = 'NONE'
                trail_points.clear()
        else : 
            trail_points.clear()
            swipe_gesture = {'Left' :'NONE', 'Right' :'NONE'}
            GESTURE   = {'Left' :'NONE', 'Right' :'NONE'}
            
            
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
            if GESTURE['Left']== 'FIST' :
                GAME_STARTED = True
                GESTURE['Left'] = "NONE"
                MOVE_DELAY     = MOVE_DELAY_START
                LAST_MOVE_TIME = pygame.time.get_ticks()
                snake_pos, direction, score, food_pos = reset_game()
                
        elif GAME_OVER :
            if GESTURE['Left'] == 'FIST' :
                GAME_OVER , GAME_PAUSED = False, False
                GESTURE['Left'] = "NONE"
                MOVE_DELAY     = MOVE_DELAY_START
                LAST_MOVE_TIME = pygame.time.get_ticks()
                snake_pos, direction, score, food_pos = reset_game()
                
        else :
            if not GAME_PAUSED :
                if GESTURE['Left'] == 'OPEN PALM' :
                    GAME_PAUSED = True 
                elif swipe_gesture['Right'] == 'UP' and direction != (0, 1):
                    direction = (0, -1)
                elif swipe_gesture['Right'] == 'DOWN' and direction != (0, -1) :
                    direction = (0, 1)
                elif swipe_gesture['Right'] == 'LEFT' and direction != (1, 0) :
                    direction = (-1, 0)
                elif swipe_gesture['Right'] == 'RIGHT' and direction != (-1, 0) :
                    direction = (1, 0)
            else :
                if GESTURE['Left'] == "FIST":
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
                
            score_surf = SMALL_FONT.render(f"Score: {score} | Swipe gesture: {swipe_gesture['Right']}", True, TEXT_COLOR)
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
                sub = MID_FONT.render("Make a LEFT FIST to restart", True, TEXT_COLOR)
                screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 40))
                screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 15))  
                
        pygame.display.flip()
        
        cv.putText(img, "LEFT HAND :", (10,30), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0,0,0), 2)
        cv.putText(img, "Gesture :", (10,70), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0,0,0), 2)
        cv.putText(img, f"{GESTURE['Left']}", (180,70), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255,0,0), 2)
        cv.putText(img, "Swipe     :", (10,110), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0,0,0), 2)
        cv.putText(img, f"{swipe_gesture['Left']}", (180,110), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255,0,0), 2)
        
        cv.putText(img, "RIGHT HAND :", (img.shape[1]-400 ,30), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0,0,0), 2)
        cv.putText(img, "Gesture :", (img.shape[1]-400,70), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0,0,0), 2)
        cv.putText(img, f"{GESTURE['Right']}", (img.shape[1]-230,70), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255,0,0), 2)
        cv.putText(img, "Swipe     :", (img.shape[1]-400,110), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0,0,0), 2)
        cv.putText(img, f"{swipe_gesture['Right']}", (img.shape[1]-230,110), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255,0,0), 2)
        
        
        
        ctime = time.time()
        fps = 1/(ctime - ptime)
        ptime = ctime
        cv.putText(img, f"FPS : {int(fps)}", (img.shape[1]//2-50 , img.shape[0]-10 ), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.2, (0, 0, 0), 2)
        img = cv.resize(img, (640, 480))
        cv.imshow('vision tracker ',img)
        
        if cv.waitKey(1) & 0xFF==ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()       
            