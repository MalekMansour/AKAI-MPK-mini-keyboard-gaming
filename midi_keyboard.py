import mido
import json
import os
import keyboard as kb  # to detect Ctrl+F to finish
from datetime import datetime

print("🎛️ MIDI Key Mapper Setup")
print("Make sure your MIDI device is plugged in!\n")

# --- Step 1: List all connected MIDI devices ---
devices = mido.get_input_names()
if not devices:
    print("❌ No MIDI devices found! Plug one in and try again.")
    exit()

print("🎹 Available MIDI Devices:")
for i, name in enumerate(devices, 1):
    print(f" {i}. {name}")

# Let user pick
while True:
    try:
        choice = int(input("\nSelect your MIDI device (number): "))
        if 1 <= choice <= len(devices):
            input_name = devices[choice - 1]
            break
        else:
            print("❌ Invalid choice. Try again.")
    except ValueError:
        print("❌ Please enter a number.")

print(f"\n✅ Connected to {input_name}\n")

NOTE_TO_KEY = {}
mouse_keys = {}

# Helper to get a MIDI input message
def get_note_input(port):
    while True:
        msg = port.receive()
        if msg.type == 'note_on' and msg.velocity > 0:
            return msg.note
        elif msg.type == 'control_change':
            return f"cc_{msg.control}"

# --- Step 2: Main Menu ---
def main_menu():
    print("\n===== MAIN MENU =====")
    print("1️⃣  Bind Keyboard Keys")
    print("2️⃣  Bind Mouse Controls")
    print("3️⃣  Save Keybind Sheet")
    print("4️⃣  Quit")
    choice = input("\nSelect an option (1-4): ").strip()
    return choice

# --- Step 3: Bind mouse controls ---
def bind_mouse_controls(port):
    print("\n🖱️ Let's bind mouse controls.")
    print("Press the piano key you want to use for each action.\n")

    for direction in ["up", "down", "left", "right"]:
        print(f"🎹 Press piano key for MOUSE MOVE {direction.upper()}:")
        mouse_keys[direction] = get_note_input(port)
        print(f"✅ Bound mouse {direction} to note {mouse_keys[direction]}")

    for click in ["left_click", "right_click", "middle_click"]:
        print(f"\n🎹 Press piano key for {click.replace('_', ' ').title()}:")
        note = get_note_input(port)
        NOTE_TO_KEY[str(note)] = click
        print(f"✅ Bound {click} to note {note}")

    NOTE_TO_KEY["mouse_movement"] = mouse_keys
    print("\n✅ Finished binding mouse controls!")

# --- Step 4: Bind keyboard keys ---
def bind_keyboard_keys(port):
    print("\n⌨️ Binding keyboard keys.")
    print("Press a key on your COMPUTER keyboard, then press a key on your MIDI keyboard.")
    print("When you're done, press Ctrl + F to finish.\n")

    while True:
        if kb.is_pressed("ctrl+f"):
            print("✅ Finished keyboard binding!")
            break

        try:
            key = input("→ Type the computer key you want to bind (ex: w, space, shift): ").strip().lower()
            if not key:
                continue

            print("🎹 Now press the piano key you want to map to that key...")
            note = get_note_input(port)
            NOTE_TO_KEY[str(note)] = key
            print(f"✅ Bound MIDI note {note} → '{key}'\n")

        except KeyboardInterrupt:
            print("\n✅ Finished keyboard binding.")
            break

# --- Step 5: Save mappings ---
def save_mappings():
    os.makedirs("piano_keybinds", exist_ok=True)
    name = input("\n💾 Enter a name for this keybind sheet: ").strip()
    if not name:
        name = f"mapping_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    path = os.path.join("piano_keybinds", f"{name}.json")

    with open(path, "w") as f:
        json.dump({"done": NOTE_TO_KEY}, f, indent=4)

    print(f"✅ Saved mapping to {path}")

# --- Step 6: Main Loop ---
with mido.open_input(input_name) as port:
    while True:
        choice = main_menu()

        if choice == "1":
            bind_keyboard_keys(port)
        elif choice == "2":
            bind_mouse_controls(port)
        elif choice == "3":
            save_mappings()
        elif choice == "4":
            print("\n👋 Exiting setup. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")
