import cStringIO
import ev3dev.ev3 as ev3
from RobotMove import RobotMove
import time
import cv2
import sys
from requests import get, post, codes
from PIL import Image


HOST_IP = 'lowik.sytes.net'
HOST_PORT = 53117


def wait_yes_or_no(timeout_s=5.0):
    start = time.time()
    sleep_s = 0.005
    button = ev3.Button()
    touch = ev3.TouchSensor()
    while timeout_s < 0 or time.time() - start > timeout_s - sleep_s:
        if button.down:
            return 0
        if button.up or touch.is_pressed():
            return 1
        time.sleep(sleep_s)
    return -1


def start_game():
    ev3.Sound.speak("Hello Human. I'm a robot, do you want to play with me").wait()

    n_trys = 0
    while n_trys < 2:
        user_answer = wait_yes_or_no(-1)
        if user_answer == 1:
            ev3.Sound.speak("Cool, let's play!").wait()
            return True
        elif user_answer == 0:
            ev3.Sound.speak("Oh, you're not funny. Bye!").wait()
            return False
        else:
            ev3.Sound.speak("Press up for yes, down for no").wait()
            n_trys += 1

    if n_trys >= 2:
        ev3.Sound.speak("It seems you don't want to play. Bye!").wait()
        return False


def get_image(camera):
    print("Capture image")
    ev3.Sound.speak("I will take a picture in").wait()
    time.sleep(1)
    ev3.Sound.speak("One...").wait()
    time.sleep(1)
    ev3.Sound.speak("Two...").wait()
    time.sleep(1)
    ev3.Sound.speak("Three!").wait()
    return camera.read()


def analyze(image_bgr):
    print("Analyze image")
    host_url = 'http://' + HOST_IP + ':' + str(HOST_PORT)
    url_availability = host_url + '/available'
    url_prediction = host_url + '/predict'

    r = get(url_availability)
    if r.status_code != codes.ok:
        print("Service is not available on this url")
        return

    # Need to convert image to the rigth format to post it on the server.
    image_rgb = image_bgr[:, :, (2, 1, 0)]
    pil_image = Image.fromarray(image_rgb)
    buffer = cStringIO.StringIO()
    pil_image.save(buffer, format='JPEG')
    buffer.seek(0)
    # Post request
    files = {'file': buffer}
    r = post(url_prediction, files=files)
    result = r.json()
    print(result)
    return result["label"]


def give_answer(guess):
    phrase1 = "It looks like a {guess}".format(guess=guess)
    phrase2 = "Is it a {guess}?".format(guess=guess)
    ev3.Sound.speak(phrase1).wait()
    time.sleep(1)
    ev3.Sound.speak(phrase2).wait()


if __name__ == "__main__":
    print("Starting program")
    camera = cv2.VideoCapture(0)
    moves = RobotMove()

    moves.forward(50, 0.2)
    if not start_game():
        sys.exit()

    keep_playing = True
    while keep_playing:
        capture_ok, image = get_image(camera)

        if not capture_ok:
            ev3.Sound.speak("I can not seeee!").wait()
            time.sleep(1)
            sys.exit(1)

        ev3.Sound.speak("Let me guess what it is.").wait()
        guess = analyze(image)

        give_answer(guess)

        ev3.Sound.speak("Is it the right answer?").wait()
        user_answer = wait_yes_or_no(-1)
        if user_answer == 1:
            moves.turn_360()
        else:
            moves.turn_180()
            moves.forward(speed=20, time_ms=1000)

        ev3.Sound.speak("Do you want to play again?").wait()
        user_answer = wait_yes_or_no(-1)
        keep_playing = user_answer == 1
