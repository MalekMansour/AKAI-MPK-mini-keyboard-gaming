import mido
import json
import threading
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button
import time

# Controllers
keyboard = KeyboardController()
mouse = MouseController()

# Load mapping
with open("midi_mapping.json", "r") as f:
    mappings = json.load(f)["done"]

MOUSE_MOVEMENT = mappings.get("mouse_movement", {})
HOLDING_NOTES = set()

# Map string names to actual mouse buttons
MOUSE_BUTTONS = {
    "left_click": Button.left,
    "right_click": Button.right
}

# Detect MIDI input
input_name = None
for name in mido.get_input_names():
    if "mpk" in name.lower():
        input_name = name
        break

if not input_name:
    print("❌ MPK Mini not found! Connect it and try again.")
    exit()

print(f"✅ Connected to {input_name}")
print("Ready! Press your MIDI keys/pads...")

# Mouse movement loop
def move_mouse_loop(note):
    speed = 5  # pixels per step
    while note in HOLDING_NOTES:
        if note == MOUSE_MOVEMENT.get("up"):
            mouse.move(0, -speed)
        elif note == MOUSE_MOVEMENT.get("down"):
            mouse.move(0, speed)
        elif note == MOUSE_MOVEMENT.get("left"):
            mouse.move(-speed, 0)
        elif note == MOUSE_MOVEMENT.get("right"):
            mouse.move(speed, 0)
        time.sleep(0.01)

# Mouse button functions
def press_mouse(note_key):
    btn = MOUSE_BUTTONS.get(note_key)
    if btn:
        mouse.press(btn)

def release_mouse(note_key):
    btn = MOUSE_BUTTONS.get(note_key)
    if btn:
        mouse.release(btn)

# Handle note_on
def handle_note_on(note):
    if note in HOLDING_NOTES:
        return
    HOLDING_NOTES.add(note)

    key = mappings.get(str(note)) or mappings.get(f"cc_{note}")

    # Mouse clicks
    if key in MOUSE_BUTTONS:
        press_mouse(key)

    # Mouse movement
    elif note in MOUSE_MOVEMENT.values():
        threading.Thread(target=move_mouse_loop, args=(note,), daemon=True).start()

    # Keyboard keys
    elif key:
        try:
            if len(key) == 1:
                keyboard.press(key)
            else:
                keyboard.press(getattr(Key, key))
        except AttributeError:
            keyboard.press(key)

# Handle note_off
def handle_note_off(note):
    if note in HOLDING_NOTES:
        HOLDING_NOTES.remove(note)

    key = mappings.get(str(note)) or mappings.get(f"cc_{note}")

    # Mouse clicks
    if key in MOUSE_BUTTONS:
        release_mouse(key)

    # Keyboard keys
    elif key:
        try:
            if len(key) == 1:
                keyboard.release(key)
            else:
                keyboard.release(getattr(Key, key))
        except AttributeError:
            keyboard.release(key)

# Main loop
with mido.open_input(input_name) as port:
    for msg in port:
        if msg.type == "note_on":
            if msg.velocity > 0:
                handle_note_on(msg.note)
            else:
                handle_note_off(msg.note)
        elif msg.type == "note_off":
            handle_note_off(msg.note)
        elif msg.type == "control_change":
            # Optional: treat knobs as keys
            handle_note_on(msg.control)

