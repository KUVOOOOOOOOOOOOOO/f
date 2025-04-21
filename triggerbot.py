# import time
import pyautogui
import mss
from PIL import Image
import keyboard

# 🎯 Nastavení pro Da Hood (1920x1080 + 120 FOV)
RESOLUTION = (1920, 1080)
FOV = 60  # 120x120 oblast kolem středu
TRIGGER_KEY = 'q'
TARGET_COLOR = (255, 0, 0)  # barva hlavy (červená)
TOLERANCE = 30
CLICK_DELAY = 0.03  # kratší delay pro rychlost

def color_match(c1, c2, tol):
    return all(abs(a - b) <= tol for a, b in zip(c1, c2))

print("=== DA HOOD TRIGGERBOT AKTIVNÍ ===")
print(f"Zastavíš ho klávesou [{TRIGGER_KEY.upper()}]")
time.sleep(1)

with mss.mss() as sct:
    screen_width, screen_height = RESOLUTION
    region = {
        "top": screen_height // 2 - FOV,
        "left": screen_width // 2 - FOV,
        "width": FOV * 2,
        "height": FOV * 2
    }

    while True:
        if keyboard.is_pressed(TRIGGER_KEY):
            print("Triggerbot vypnutý.")
            break

        img = sct.grab(region)
        img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        pixels = img.load()

        for x in range(img.width):
            for y in range(img.height):
                if color_match(pixels[x, y], TARGET_COLOR, TOLERANCE):
                    pyautogui.click()
                    time.sleep(CLICK_DELAY)
                    break
