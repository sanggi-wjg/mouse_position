import json
import os
import threading
import time

import pyautogui
from pyhooked import Hook, MouseEvent

"""
pyinstaller -F -n mouse_positions  create_mouse_positions.py
"""

# Setup stop event
thread_stop = threading.Event()
positions = []


# Setup hot key handler
def left_click(event):
    if isinstance(event, MouseEvent):
        if event.current_key == 'RButton' and event.event_type == 'key down':
            x, y = pyautogui.position()
            positions.append({ 'x': x, 'y': y })
            print(positions)

            if len(positions) == 4:
                hook.unhook_mouse()
                thread_stop.set()


# Create Json file
def create_json():
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'positions.json')

    with open(filepath, 'w+') as json_file:
        json.dump(positions, json_file)

    print(filepath, '생성 완료.')


if __name__ == '__main__':
    print('프로그램 시작.')
    print('현재 마우스 좌표 저장 : 마우스 오른쪽 클릭!')

    # Start hot key thread
    hook = Hook()
    hook.handler = left_click
    thread = threading.Thread(name = 'mouse', target = hook.hook, daemon = True)
    thread.start()

    # Main loop
    while not thread_stop.is_set():
        time.sleep(1)

    create_json()
    print('프로그램 종료.')
