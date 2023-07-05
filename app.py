import cv2
import mediapipe as mp
import math
import pyautogui
import time


#4,8,12,16,20
def fingers_up(points):
    fingers=[False,False,False,False,False,False]
    if(points[4][0]>points[3][0]):
        fingers[0]=True
    
    if(points[8][1]<points[7][1]):
        fingers[1]=True
    
    if(points[12][1]<points[11][1]):
        fingers[2]=True

    if(points[16][1]<points[15][1]):
        fingers[3]=True
    
    if(points[20][1]<points[19][1]):
        fingers[4]=True
    
    fingers[5] = points[0][1]
    return fingers

def desenhar_retangulo_referencia(imagem,point):
    x_0,y_0 = (point[0] -60),(point[1])
    x , y = (point[0] + 60),(point[1] - 130)
    cv2.rectangle(imagem,(x_0,y_0),(x,y),(0, 255, 0),1)
    

def desenhar_mao(imagem, points):
    for point in points:
        cv2.circle(imagem, point, 5, (0, 255, 0), -1)
    
def distancia_entre_pontos(ponto_origem, ponto):
    return round(math.sqrt(abs((ponto[0] - ponto_origem[0] )**1 + (ponto[1] - ponto_origem[1])**2)),2)

def keyboard_actions(fingers):

    if(not fingers[0] and fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]):
        pyautogui.press('left')
        print("Esquerda")

    if(not fingers[0] and fingers[1] and fingers[2] and not fingers[3] and not fingers[4]):
        pyautogui.press('right')
        print("Direita")
    
    if(fingers[5] < 300):
        pyautogui.press('space')
        print("Pulou")


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
camera = cv2.VideoCapture(0)



while True:
    ret, frame = camera.read()
    
    frame_color = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    results = hands.process(frame_color)

    if results.multi_hand_landmarks:
        for hand_landmarks  in results.multi_hand_landmarks:
            
            hand_points = []
            fingers = [False,False,False,False,False,False]
            for point in hand_landmarks.landmark:
                altura, largura, _ = frame.shape
                x, y = int(point.x * largura), int(point.y * altura)
                hand_points.append((x,y))

            fingers = fingers_up(hand_points)
            
            desenhar_mao(frame,hand_points)
            keyboard_actions(fingers)
            print(fingers)




    print("\n\n\n")
    cv2.imshow('Camera', frame)

    # time.sleep(0.04)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

