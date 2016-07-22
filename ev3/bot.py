import ev3dev.ev3 as ev3
import time
import cv2
import sys
import requests
import flask


def wait_yes_or_no(timeout_s=5.0):
    start = time.time()
    sleep_s = 0.005
    button = ev3.Button()
    while time.time() - start > timeout_s - sleep_s:
        if button.down:
            return 0
        if button.up:
            return 1
        time.sleep(sleep_s)
    return -1


def start_game():
    ev3.Sound.speak("Hello Human. I'm a robot, do you want to play with me").wait()

    n_trys = 0
    while n_trys < 2:
        user_answer = wait_yes_or_no(5.0)
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
    ev3.Sound.speak("I will take a picture in").wait()
    time.sleep(1)
    ev3.Sound.speak("One...").wait()
    time.sleep(1)
    ev3.Sound.speak("Two...").wait()
    time.sleep(1)
    ev3.Sound.speak("Three!").wait()
    return camera.read()


def analyze(image):
    return "Banana"


def give_answer(guess):
    phrase1 = "It looks like a {guess}".format(guess=guess)
    phrase2 = "Is it a {guess}?".format(guess=guess)
    ev3.Sound.speak(phrase1).wait()
    time.sleep(1)
    ev3.Sound.speak(phrase2).wait()


if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    if not start_game():
        sys.exit()

    capture_ok, image = get_image(camera)

    if not capture_ok:
        ev3.Sound.speak("I can not seeee!").wait()
        time.sleep(1)
        sys.exit(1)

    ev3.Sound.speak("Let me guess what it is.").wait()
    guess = analyze(image)

    give_answer(guess)
