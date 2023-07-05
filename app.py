import cv2
import mediapipe as mp


def desenhar_mao(imagem, points):
    for i in range(0,21,4):
        cv2.circle(imagem, points[i], 5, (0, 255, 0), -1)
   

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
            
            print(hand_points)
            desenhar_mao(frame,hand_points)



    print("\n\n\n")
    cv2.imshow('Camera', frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

