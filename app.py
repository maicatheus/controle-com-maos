import cv2
import mediapipe as mp
import math


#4,8,12,16,20
def fingers_up(points):
    fingers=[0,0,0,0,0]
    if(points[4][0]>points[3][0]):
        fingers[0]=1
    
    if(points[8][1]<points[7][1]):
        fingers[1]=1
    
    if(points[12][1]<points[11][1]):
        fingers[2]=1

    if(points[16][1]<points[15][1]):
        fingers[3]=1
    
    if(points[20][1]<points[19][1]):
        fingers[4]=1

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
            fingers = [0,0,0,0,0]
            for point in hand_landmarks.landmark:
                altura, largura, _ = frame.shape
                x, y = int(point.x * largura), int(point.y * altura)
                hand_points.append((x,y))

            fingers = fingers_up(hand_points)

            desenhar_mao(frame,hand_points)
            
            print(fingers)




    print("\n\n\n")
    cv2.imshow('Camera', frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

