
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

# Initialize MediaPipe hands detector
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognition model
model = load_model('mp_hand_gesture')

# Load class names from file
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)  # Print loaded class names (optional)

# Initialize the video capture object (assuming webcam)
cap = cv2.VideoCapture(9)

while True:
    # Read a frame from the webcam
    success, frame = cap.read()

    if not success:  # Check if frame reading failed
        print("Ignoring empty camera frame.")
        # You can add logic here to handle the situation (e.g., break the loop)
        continue

    # Get frame properties (width, height, channels)
    x, y, c = frame.shape

    # Flip the frame vertically (optional)
    frame = cv2.flip(frame, 1)

    # Convert frame to RGB format for MediaPipe processing
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands in the frame using MediaPipe
    result = hands.process(framergb)

    # Initialize class name (empty string)
    className = ''

    # Process the results if hands are detected
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                # Convert landmark coordinates to image coordinates
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([lmx, lmy])

            # Draw hand landmarks on the frame (optional)
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            # Predict gesture using the loaded model
            prediction = model.predict([landmarks])
            classID = np.argmax(prediction)
            className = classNames[classID]

    # Display the predicted class name on the frame
    cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2, cv2.LINE_AA)

    # Display the output frame
    cv2.imshow("Output", frame)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture object and destroy windows
cap.release()
cv2.destroyAllWindows()

print("Program terminated.")
