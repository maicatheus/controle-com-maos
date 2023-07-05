import cv2
import mediapipe as mp


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    
    frame_color = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    results = hands.process(frame_color)
    print(results.multi_hand_landmarks)

    cv2.imshow('Camera', frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

