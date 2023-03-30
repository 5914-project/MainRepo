import cv2

def takePic():
    # Load the default camera
    cap = cv2.VideoCapture(0)

    # Capture a frame
    ret, frame = cap.read()

    # Release the camera
    cap.release()

    # Save the captured image
    cv2.imwrite('captured_image.png', frame)