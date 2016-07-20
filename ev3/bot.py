import ev3dev.ev3 as ev3
import time
import sys


def wait_yes_or_no(timeout_s=5.0):
    sleep_s = 0.005
    yes_or_no = -1

    button = ev3.Button()
    start = time.time()
    while yes_or_no < 0:
        if button.down:
            yes_or_no = 0
        if button.up:
            yes_or_no = 1

        if time.time() - start > timeout_s - sleep_s:
            return yes_or_no
        time.sleep(sleep_s)
    return yes_or_no

def main():
    ev3.Sound.speak("Hello Human. I'm a robot, do you want to play with me").wait()

    wait_user_answer = True
    n_trys = 0
    while wait_user_answer and n_trys < 2:
        user_answer = wait_yes_or_no(10)
        if user_answer == 1:
            ev3.Sound.speak("Cool, let's play!").wait()
            wait_user_answer = False
        elif user_answer == 0:
            ev3.Sound.speak("Oh, you're not funny. Bye!").wait()
            wait_user_answer = False
        else:
            ev3.Sound.speak("Press up for yes, down for no").wait()
            n_trys += 1

    if n_trys > 2:
        ev3.Sound.speak("It seems you don't want to play. Bye!").wait()
        time.sleep(5.0)
        sys.exit()

    time.sleep(5.0)

if __name__ == "__main__":
    main()
