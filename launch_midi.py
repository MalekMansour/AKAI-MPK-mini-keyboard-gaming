import mido
import json
import threading
import time
import os
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button

# Initialize controllers
keyboard = KeyboardController()
mouse = MouseController()

print("🎹 MIDI Piano Launcher")
print("=========================\n")

# --- STEP 1: Pick MIDI Device ---
devices = mido.get_input_names()
if not devices:
    print("❌ No MIDI devices detected! Plug one in and try again.")
    exit()

print("🎛️ Available MIDI Devices:")
for i, name in enumerate(devices, 1):
    print(f" {i}. {name}")

while True:
    try:
        device_choice = int(input("\nSelect a MIDI device (number): "))
        if 1 <= device_choice <= len(devices):
            input_name = devices[device_choice - 1]
            break
        else:
            print("❌ Invalid choice.")
    except ValueError:
        print("❌ Please enter a number.")

# --- STEP 2: Pick Mapping File ---
keybind_folder = "piano_keybinds"
if not os.path.exists(keybind_folder):
    print(f"❌ Folder '{keybind_folder}' not found! Please create mappings first.")
    exit()

files = [f for f in os.listdir(keybind_folder) if f.endswith(".json")]
if not files:
    print(f"❌ No mapping files found in '{keybind_folder}'!")
    exit()

print("\n📁 Available Keybind Sheets:")
for i, filename in enumerate(files, 1):
    print(f" {i}. {filename}")

while True:
    try:
        file_choice = int(input("\nSelect a keybind sheet (number): "))
        if 1 <= file_choice <= len(files):
            selected_file = os.path.join(keybind_folder, files[file_choice - 1])
            break
        else:
            print("❌ Invalid choice.")
    except ValueError:
        print("❌ Please enter a number.")

# --- STEP 3: Load Mapping ---
with open(selected_file, "r") as f:
    mappings = json.load(f)["done"]

MOUSE_MOVEMENT = mappings.get("mouse_movement", {})
HOLDING_NOTES = set()

MOUSE_BUTTONS = {
    "left_click": Button.left,
    "right_click": Button.right,
    "middle_click": Button.middle
}

print(f"\n✅ Loaded mapping from '{files[file_choice - 1]}'")
print(f"✅ Connected to '{input_name}'")
print("\n🎶 Ready! Press your MIDI keys/pads...\n")

# --- FUNCTIONS ---

def move_mouse_loop(note):
    """Continuously move the mouse while the note is held."""
    speed = 5  # pixels per tick
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

def press_mouse(note_key):
    btn = MOUSE_BUTTONS.get(note_key)
    if btn:
        mouse.press(btn)

def release_mouse(note_key):
    btn = MOUSE_BUTTONS.get(note_key)
    if btn:
        mouse.release(btn)

def handle_note_on(note):
    if note in HOLDING_NOTES:
        return
    HOLDING_NOTES.add(note)

    key = mappings.get(str(note)) or mappings.get(f"cc_{note}")

    if key in MOUSE_BUTTONS:
        press_mouse(key)
    elif note in MOUSE_MOVEMENT.values():
        threading.Thread(target=move_mouse_loop, args=(note,), daemon=True).start()
    elif key:
        try:
            if len(key) == 1:
                keyboard.press(key)
            else:
                keyboard.press(getattr(Key, key))
        except AttributeError:
            keyboard.press(key)

def handle_note_off(note):
    if note in HOLDING_NOTES:
        HOLDING_NOTES.remove(note)

    key = mappings.get(str(note)) or mappings.get(f"cc_{note}")

    if key in MOUSE_BUTTONS:
        release_mouse(key)
    elif key:
        try:
            if len(key) == 1:
                keyboard.release(key)
            else:
                keyboard.release(getattr(Key, key))
        except AttributeError:
            keyboard.release(key)

# --- MAIN LOOP ---
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
            handle_note_on(msg.control)
