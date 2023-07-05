import cv2
import mediapipe as mp
import math



def desenhar_retangulo_referencia(imagem,point):
    x_0,y_0 = (point[0] -60),(point[1])
    x , y = (point[0] + 60),(point[1] - 130)
    cv2.rectangle(imagem,(x_0,y_0),(x,y),(0, 255, 0),1)

def desenhar_mao(imagem, points):
    for i in range(0,21,4):
        cv2.circle(imagem, points[i], 5, (0, 255, 0), -1)
    
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
            for point in hand_landmarks.landmark:
                altura, largura, _ = frame.shape
                x, y = int(point.x * largura), int(point.y * altura)
                hand_points.append((x,y))

            desenhar_retangulo_referencia(frame,hand_points[0])
            print(distancia_entre_pontos(hand_points[0],hand_points[4]), end=" ")
            print(distancia_entre_pontos(hand_points[0],hand_points[8]), end=" ")
            print(distancia_entre_pontos(hand_points[0],hand_points[12]), end=" ")
            print(distancia_entre_pontos(hand_points[0],hand_points[16]), end=" ")
            print(distancia_entre_pontos(hand_points[0],hand_points[20]), end="\n")
            desenhar_mao(frame,hand_points)



    print("\n\n\n")
    cv2.imshow('Camera', frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

