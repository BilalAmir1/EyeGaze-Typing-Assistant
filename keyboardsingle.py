import cv2
import numpy as np
import dlib
from math import hypot
import pyglet
import time
import pyttsx3


#sounds
sound = pyglet.media.load("bubble_pop.wav", streaming=False)


cap = cv2.VideoCapture(0)
#size of board for text
board = np.zeros((300, 1350), np.uint8)
board[:] = 255


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# keyboard settings
keyboard = np.zeros((405, 802, 3), np.uint8) #keyboard size

keys_set_1 = {0: "Q", 1: "W", 2: "E", 3: "R", 4: "T", 5: "Y", 6: "U", 7: "I",
              8: "O", 9: "P", 10: "A", 11: "S", 12: "D", 13: "F", 14: "G", 15: "H",
              16: "J",17: "K",18: "L",19: "Z",20: "X",21: "C",22: "V",23: "B",
              24: "N",25: "M",26: " YES ",27: " NO ",28: " EAT ",29: " REST "}
messages = []
def add_message(message):
  messages.append(message)

def save_messages():
  with open("messages.txt", "+w") as f:
    for message in messages:
      f.write(message + "\n")

def read_messages():
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    with open("messages.txt", "r") as f:
        for line in f:
            # Remove leading/trailing whitespace and newline characters
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Print the line to the console
            print(line)

            # Convert the line to speech
            engine.say(line)

    # Play the speech
    engine.runAndWait()
def letter(letter_index, text, letter_light):
    # Keys
    if letter_index == 0:
        x=0
        y=0
    elif letter_index == 1:
        x=100
        y=0
    elif letter_index == 2:
        x=200
        y=0
    elif letter_index == 3:
        x=300
        y=0
    elif letter_index == 4:
        x=400
        y=0
    elif letter_index == 5:
        x=500
        y=0
    elif letter_index == 6:
        x=600
        y=0
    elif letter_index == 7:
        x=700
        y=0
    elif letter_index == 8:
        x=0
        y=100
    elif letter_index == 9:
        x=100
        y=100
    elif letter_index == 10:
        x=200
        y=100
    elif letter_index == 11:
        x=300
        y=100
    elif letter_index == 12:
        x=400
        y=100
    elif letter_index == 13:
        x=500
        y=100
    elif letter_index == 14:
        x=600
        y=100
    elif letter_index == 15:
        x=700
        y=100
    elif letter_index == 16:
        x=0
        y=200
    elif letter_index == 17:
        x=100
        y=200
    elif letter_index == 18:
        x=200
        y=200
    elif letter_index == 19:
        x=300
        y=200
    elif letter_index == 20:
        x=400
        y=200
    elif letter_index == 21:
        x=500
        y=200
    elif letter_index == 22:
        x=600
        y=200
    elif letter_index == 23:
        x=700
        y=200
    elif letter_index == 24:
        x=0
        y=300
    elif letter_index == 25:
        x=100
        y=300
    elif letter_index == 26:
        x=225
        y=300
    elif letter_index == 27:
        x=353
        y=300
    elif letter_index == 28:
        x=475
        y=300
    elif letter_index == 29:
        x=650
        y=300



    width = 100
    height =100
    th = 2  # thickness

    # Text settings
    font_letter = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 1
    font_th = 2
    text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y
    cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (255, 0, 0), font_th)

    if letter_light is True:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
        cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
    else:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (51, 51, 51), -1)
        cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (255, 255, 255), font_th)



def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

font = cv2.FONT_HERSHEY_SIMPLEX




def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_lenght / ver_line_lenght
    return ratio

def eyes_contour_points(facial_landmarks):
    left_eye = []
    right_eye = []
    for n in range(36, 42):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        left_eye.append([x, y])
    for n in range(42, 48):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        right_eye.append([x, y])
    left_eye = np.array(left_eye, np.int32)
    right_eye = np.array(right_eye, np.int32)
    return left_eye, right_eye

def get_gaze_ratio(eye_points, facial_landmarks):
    # Code for Gaze detection
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)

    # code for the Mask around the eye
    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    # Gaze tracking
    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])

    gray_eye = eye[min_y: max_y, min_x: max_x]
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)

    right_side_threshold = threshold_eye[0: height, int(width / 2): width]
    right_side_white = cv2.countNonZero(right_side_threshold)

    if left_side_white == 0:
        gaze_ratio = 1
    elif right_side_white == 0:
        gaze_ratio = 5
    else:
        gaze_ratio = left_side_white / right_side_white
    return gaze_ratio

# Counters
frames = 0
letter_index = 0
blinking_frames = 0
frames_to_blink = 6
frames_active_letter = 8
start_time = time.time()

# Text and keyboard settings
text = ""
keyboard_selected = "left"
last_keyboard_selected = "left"
select_keyboard_menu = True
keyboard_selection_frames = 0
background = cv2.imread("pic.jpg")
background = cv2.resize(background, (1780, 720))


while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, (590, 400))
    rows, cols, _ = frame.shape
    keyboard[:] = (26,26,26)
    frames += 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # Draw a white space for loading bar
    frame[rows - 50: rows, 0: cols] = (255, 255, 255)



        # Keyboard selected

    keys_set = keys_set_1
    active_letters = keys_set[letter_index]

    #face detection
    faces = detector(gray)
    for face in faces:
        #x, y = face.left(), face.top()
        #x1, y1 = face.right(), face.bottom()
        #cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
        landmarks = predictor(gray, face)

        left_eye, right_eye = eyes_contour_points(landmarks)

        #Code for Detecting Blinking
        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
        if blinking_ratio > 5.7:
            eyes_closed = True
        else:
            eyes_closed = False

        # Eyes color
        cv2.polylines(frame, [left_eye], True, (0, 0, 255), 2)
        cv2.polylines(frame, [right_eye], True, (0, 0, 255), 2)


        if select_keyboard_menu is True:
            # Detecting gaze to select Left or Right keybaord
            gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
            gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
            gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2

            if gaze_ratio <= 0.9:
                keyboard_selected = "right"
                keyboard_selection_frames += 1

                # If Kept gaze on one side more than 15 frames, move to keyboard
                if keyboard_selection_frames == 15:
                    select_keyboard_menu = False
                    print("right")

                    # Set frames count to 0 when keyboard selected
                    frames = 0
                    keyboard_selection_frames = 0
                if keyboard_selected != last_keyboard_selected:
                    last_keyboard_selected = keyboard_selected
                    keyboard_selection_frames = 0
            else:
                keyboard_selected = "left"
                keyboard_selection_frames += 1
                # If Kept gaze on one side more than 15 frames, move to keyboard
                if keyboard_selection_frames == 15:
                    select_keyboard_menu = False

                    # Set frames count to 0 when keyboard selected
                    frames = 0
                if keyboard_selected != last_keyboard_selected:
                    last_keyboard_selected = keyboard_selected
                    keyboard_selection_frames = 0

        else:
            # Detect the blinking to select the key that is lighting up
            if blinking_ratio > 5:
                # cv2.putText(frame, "BLINKING", (50, 150), font, 4, (255, 0, 0), thickness=3)
                blinking_frames += 1
                frames -= 1

                # Show green eyes when closed
                cv2.polylines(frame, [left_eye], True, (0, 255, 0), 2)
                cv2.polylines(frame, [right_eye], True, (0, 255, 0), 2)

                # Typing letter
                if blinking_frames == frames_to_blink:
                    if active_letters != "<" and active_letters != "_":
                        text += active_letters
                    if active_letters == "_":
                        text += " "
                    #saving what is written on a file named message.txt
                    add_message(text)
                    save_messages()
                    sound.play()

                    # time.sleep(1)

            else:
                blinking_frames = 0

                # # active letter location using gaze
                # gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
                # gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
                # gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2
                #
                # if gaze_ratio <= 0.9:
                #     for i in range(30):
                #         if i == 8:
                #             light = True
                #         else:
                #             light = False
                #         letter(i, keys_set[i], light)
                #     print("right")
                # elif gaze_ratio >= 1.9:
                #     for i in range(30):
                #         if i == 8:
                #             light = True
                #         else:
                #             light = False
                #         letter(i, keys_set[i], light)
                #         print("left")
            # Display active-letters on the keyboard
            if frames == frames_active_letter:
                letter_index += 1
                frames = 0
            if letter_index == 30:
                letter_index = 0
            for i in range(30):
                if i == letter_index:
                    light = True
                else:
                    light = False
                letter(i, keys_set[i], light)

            # Show the text we're writing on the board
        cv2.putText(board, text, (10, 50), font, 1, 0, 2)

        elapsed_time = time.time() - start_time
        cv2.putText(frame, "Time passed in sec: {:.2f}".format(elapsed_time), (5, 20), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 1)

        # Blinking loading bar
        percentage_blinking = blinking_frames / frames_to_blink
        loading_x = int(cols * percentage_blinking)
        cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (51, 51, 51), -1)


        # cv2.imshow("Frame", frame)
        # cv2.imshow("Board", board)
        #cv2.imshow("Virtual keyboard", keyboard)
        # adjusting the video frame in the background
        background[5:5 + 400, 810:810 + 590] = frame
        # adjusting the board in the background
        board_color = cv2.cvtColor(board, cv2.COLOR_GRAY2BGR)
        background[410:410+board_color.shape[0], 5:5+board_color.shape[1]] = board_color
        # adjusting the video frame in the background
        background[5:5 + 405, 5:5 + 802] = keyboard
        # background size = 1780, 720
        cv2.imshow("Adjusted Frames", background)


    key = cv2.waitKey(1)
    if key == 27:
        break
read_messages()
# sys.exit()
cap.release()
cv2.destroyAllWindows()