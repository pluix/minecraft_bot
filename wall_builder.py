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
tick = 1/20
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
    return tick*t


def place_block(hot_bar_item):
    keyboard.press_and_release(hot_bar_item)
    sleep(tick)

    mouse.right_click()
    sleep(tick)

    mouse.click(button="middle")
    sleep(tick)


def move(key, distance):
    press_hold(key, distance*5)
    sleep(ticks(10))


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
    if wait_ticks > 20:
        keyboard.press("6")
        sleep(ticks(1))
        mouse.press(button="right")
        sleep(3)
        mouse.release(button="left")


def start():
    print("Starting...")
    keyboard.press("win")
    keyboard.press_and_release(mc_taskbar_location)
    keyboard.release("win")
    sleep(tick)
    keyboard.press_and_release("esc")
    sleep(1)


def end():
    print("Ending...")
    keyboard.press_and_release("esc")


if __name__ == "__main__":
    wall_height = 8
    wall_width = 7
    pillar_width = 1
    buffer = 1
    floor = 1

    wall_section_width = wall_width - (2*buffer + 2*pillar_width)
    wall_section_height = wall_height - (2*buffer + floor)
    
    wall_count = 0

    sleep(1)
    start()

    # first layer (floor)
    for blocks in range(0, (wall_width - pillar_width) * walls):
        jump_place(random_block, floor)
        fall(forward, (5*floor)+1)
    for blocks in range(0, pillar_width):
        if blocks + 1 < pillar_width:
            jump_place(random_block, floor)
            fall(forward, (5*floor)+1)
        else:
            jump_place(random_block, floor)

    # # second layer (buffer)
    for blocks in range(0, (wall_width - pillar_width) * walls):
        jump_place(random_block, buffer)
        fall(backward, (5*buffer)+1)

    for blocks in range(0, pillar_width):
        if blocks + 1 < pillar_width:
            jump_place(random_block, buffer)
            fall(backward, (5*buffer)+1)
        else:
            jump_place(random_block, buffer)

    # # third layer (wall section)
    for x in range(0, walls):

        for blocks in range(0, pillar_width):
            jump_place(random_block, wall_section_height)
            fall(forward, (5*wall_section_height)+1)
        for blocks in range(0, buffer):
            jump_place(random_block, wall_section_height)
            fall(forward, (5*wall_section_height)+1)

        for blocks in range(0, wall_section_width):
            if blocks != math.floor(wall_section_width/2):
                jump_place(secondary_block, wall_section_height)
                fall(forward, (5*wall_section_height)+1)
            else:
                middle_bottom = math.floor(wall_section_height/2)
                jump_place(secondary_block, middle_bottom)
                jump_place(glowstone, 1)
                jump_place(secondary_block, middle_bottom)
                fall(forward, (5*wall_section_height)+1)

        for blocks in range(0, buffer):
            jump_place(random_block, wall_section_height)
            fall(forward, (5*wall_section_height)+1)

    for blocks in range(0, pillar_width):
        if blocks + 1 < pillar_width:
            jump_place(random_block, wall_section_height)
            fall(forward, (5*wall_section_height)+1)
        else:
            jump_place(random_block, wall_section_height)

    # # fourth layer (buffer)
    for blocks in range(0, (wall_width - pillar_width) * walls):
        jump_place(random_block, buffer)
        fall(backward, (5*buffer)+1)

    for blocks in range(0, pillar_width):
        if blocks + 1 < pillar_width:
            jump_place(random_block, buffer)
            fall(backward, (5*buffer)+1)
        else:
            jump_place(random_block, buffer)

    # # fifth layer (floor)
    for blocks in range(0, (wall_width - pillar_width) * walls):
        jump_place(random_block, floor)
        fall(forward, (5*floor)+1)
    for blocks in range(0, pillar_width):
        if blocks + 1 < pillar_width:
            jump_place(random_block, floor)
            fall(forward, (5*floor)+1)
        else:
            jump_place(random_block, floor)

    # # first pillar
    fall(forward, (5*wall_height+1))
    move(backward, 1)
    move(left, 1)
    move(backward, 1)
    move(right, 1)
    jump_place(random_block, wall_height+floor)

    # # other pillars
    for x in range(0, walls):
        if x < walls:
            fall(forward, (5 * wall_height + 1))
            move(backward, 1)
            move(left, 1)
            move(backward, wall_width-1)
            move(right, 1)
            jump_place(random_block, wall_height+floor)

    # # build overhang
    keyboard.press("shift")
    keyboard.press("a")
    keyboard.press("s")
    mouse.move(18, -18, absolute=False, duration=.5)
    sleep(1)
    keyboard.release("s")

    overhang_num = walls*6
    overhang_count = 0
    sleep(ticks(5))

    for x in range(0, overhang_num):
        # print(overhang_count, overhang_count % 6)
        if overhang_count != wall_width-(2*pillar_width):
            mouse.right_click()
            overhang_count += 1
        else:
            overhang_count = 0
        sleep(1.10)

    keyboard.release("shift")
    keyboard.release("a")

    sleep(1)
    end()
    exit(0)
