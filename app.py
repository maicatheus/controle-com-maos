import cv2
import mediapipe as mp
import math

def ponto_em_poligono(ponto, poligono):
    x, y = ponto

    intersecoes = 0
    n = len(poligono)

    for i in range(n):
        x1, y1 = poligono[i]
        x2, y2 = poligono[(i + 1) % n]

        if y > min(y1, y2):
            if y <= max(y1, y2):
                if x <= max(x1, x2):
                    if y1 != y2:
                        x_intersecao = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                        if x1 == x2 or x <= x_intersecao:
                            intersecoes += 1

    return intersecoes % 2 == 0


def verificar_dedos_levantados(poligono,pontos):
    dedos_levantados = 0
    for i in range(0,21,4):
        if ponto_em_poligono(pontos[i],poligono):
            dedos_levantados += 1
    
    return dedos_levantados

    
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

            x_0,y_0 = (hand_points[0][0] - 60),(hand_points[0][1])
            x , y = (hand_points[0][0] + 60),(hand_points[0][1] - 130)
            poligono =[(x_0,y_0),(x_0,y),(x,y),(x,y_0)]
            desenhar_retangulo_referencia(frame,hand_points[0])
            desenhar_mao(frame,hand_points)
            
            print(f"Dedos levantados: {verificar_dedos_levantados(poligono,hand_points)}")



    print("\n\n\n")
    cv2.imshow('Camera', frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

