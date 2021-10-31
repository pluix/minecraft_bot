import platform
import math
import random
from time import sleep

import keyboard
import mouse
from pynput.mouse import Button, Controller

if platform.system() != "Windows":
    mouse = Controller()

mc_taskbar_location = "5"

forward = "w"
backward = "s"
left = "a"
right = "d"

# # moving:
# # 5 ticks == 1 block
tick = 1 / 20
acceleration = 22
# # falling > 22 blocks == death


secondary_block = "5"
glowstone = "9"

walls = 3


def press_hold(key, tick_count):
    # print(f"Pressing {key} for {tick_count} ticks")
    keyboard.press(key)
    sleep(ticks(tick_count))
    keyboard.release(key)


def random_block():
    return str(random.randint(1, 4))


def ticks(t):
    return tick * t


def place_block(hot_bar_item):
    keyboard.press_and_release(hot_bar_item)
    sleep(tick)

    mouse.right_click()
    sleep(tick)

    mouse.click(button="middle")
    sleep(tick)


def move(key, distance):
    press_hold(key, distance * 5)
    sleep(ticks(10))


def move_jump(direction, distance):
    keyboard.press("space")

    keyboard.press(direction)
    sleep(ticks(3))
    keyboard.release("space")
    sleep(ticks(5))
    keyboard.release(direction)


def jump_place(hot_bar_item, block_count):
    t = block_count
    while t > 0:
        # keyboard.press_and_release(hot_bar_item)

        keyboard.press("space")
        sleep(ticks(3))

        if hot_bar_item == random_block:
            place_block(random_block())
        else:
            place_block(hot_bar_item)

        # mouse.right_click()
        keyboard.release("space")

        sleep(ticks(5))
        t -= 1


def fall(direction, wait_ticks):
    if direction == forward:
        press_hold(forward, 6)
        sleep(ticks(wait_ticks))
        press_hold(backward, 6)
    else:
        press_hold(backward, 6)
        sleep(ticks(wait_ticks))
        press_hold(forward, 6)

    # # eat if fall could hurt
    if wait_ticks > 20:
        keyboard.press("6")
        sleep(ticks(1))
        mouse.press(button="right")
        sleep(3)
        mouse.release(button="right")


def start():
    print("Starting...")
    # keyboard.press("win")
    # keyboard.press_and_release(mc_taskbar_location)
    # keyboard.release("win")
    sleep(tick)
    keyboard.press_and_release("esc")
    sleep(1)


def end():
    print("Ending...")
    keyboard.press_and_release("esc")


if __name__ == "__main__":
    tree_height = 3
    sleep(2)
    start()
    # # switch to axe
    keyboard.press_and_release("2")

    for x in range(0, tree_height+1):
        # # chop 1
        mouse.press("left")
        sleep(ticks(10))
        mouse.release("left")

        # # look up
        mouse.move(0, -10, absolute=False, duration=.5)

        # # chop 2
        mouse.press("left")
        sleep(ticks(10))
        mouse.release("left")

        # # look up
        mouse.move(0, -10, absolute=False, duration=.5)

        # # chop 3
        mouse.press("left")
        sleep(ticks(10))
        mouse.release("left")

        # # look down
        mouse.move(0, 20, absolute=False, duration=.5)

        move_jump(forward, 1)

        if x != 0:
            # # turn around
            mouse.move(-35, 0, absolute=False, duration=0.5)

    end()
    exit(0)
