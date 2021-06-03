import cv2
import mediapipe as mp
import pygame
import imutils
import sys
import random
import  time
from threading import Thread
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
drawingModule = mp.solutions.drawing_utils
handsModule = mp.solutions.hands
FPS = 60
WIN_WIDTH = 640
WIN_HEIGHT = 480
WHITE = (255, 255, 255)
ORANGE = (255, 150, 100)

clock = pygame.time.Clock()
sc = pygame.display.set_mode(
    (WIN_WIDTH, WIN_HEIGHT))
start_time = time.time()
r = 30
x = 0 - r
y = WIN_HEIGHT // 2
radius = 10
kruzki = []
def func1():
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            clock.tick(FPS)
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = hands.process(image)

            # Draw the hand annotations on the image.
            imageHeight, imageWidth, _ = image.shape
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks != None:
                for handLandmarks in results.multi_hand_landmarks:
                    for point in handsModule.HandLandmark:
                        mp_drawing.draw_landmarks(
                            image, handLandmarks, mp_hands.HAND_CONNECTIONS)
                        normalizedLandmark = handLandmarks.landmark[point]
                        pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                                  normalizedLandmark.y,
                                                                                                  imageWidth,
                                                                                                  imageHeight)

                        #print(point)
                        #print(pixelCoordinatesLandmark)
                        #print(normalizedLandmark)
            cv2.imshow('MediaPipe Hands', image)
            sc.fill(WHITE)
            global start_time
            global kruzki
            global radius
            if time.time() - start_time >=3:
                x, y = random.randint(100, 700), random.randint(100, 700)
                r = random.randint(20, 100)
                kruzki.append([sc,ORANGE,x,y,r])
                start_time = time.time()
            try:
                pygame.draw.circle(sc, ORANGE,(int(pixelCoordinatesLandmark[0])-100,int(pixelCoordinatesLandmark[1])), radius)
                for i in kruzki:
                    pygame.draw.circle(i[0], i[1], (i[2], i[3]), i[4])
            except:
                print("/")

            pygame.display.update()
            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
func1()