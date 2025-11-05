import mido
import json

print("🎛️ MIDI Key Mapper Setup")
print("Make sure your AKAI MPK Mini is plugged in!\n")

# Auto-detect your MPK Mini
input_name = None
for name in mido.get_input_names():
    if "mpk" in name.lower():
        input_name = name
        break

if not input_name:
    print("❌ Couldn't find your MPK Mini! Plug it in and try again.")
    exit()

print(f"✅ Connected to {input_name}\n")

NOTE_TO_KEY = {}

print("First, assign piano keys to mouse movement directions (up/down/left/right).")
mouse_keys = {}

with mido.open_input(input_name) as port:
    for direction in ["up", "down", "left", "right"]:
        print(f"\n🎹 Press the piano key you want to move the mouse {direction}:")
        while True:
            msg = port.receive()
            if msg.type == 'note_on' and msg.velocity > 0:
                note = msg.note
                mouse_keys[direction] = note
                print(f"✅ {direction.capitalize()} mapped to piano key {note}")
                break

print("\nNow map the rest of your piano keys/knobs to computer keys.")
print("Press a piano key/pad or move a knob, then type the computer key it should trigger.")
print("When you're done, type 'done' and hit Enter.\n")

with mido.open_input(input_name) as port:
    while True:
        msg = port.receive()

        if msg.type == 'note_on' and msg.velocity > 0:
            note = msg.note
            print(f"\n🎹 You pressed MIDI note {note}.")
            key = input("→ Enter the computer key for this note (or 'done' to finish): ").strip().lower()

            if key == "done":
                break
            elif key:
                NOTE_TO_KEY[note] = key
                print(f"✅ Mapped note {note} to key '{key}'")

        elif msg.type == 'control_change':
            print(f"\n🎚️ You moved knob/control {msg.control}.")
            key = input("→ Enter the computer key for this control (or 'done' to finish): ").strip().lower()
            if key == "done":
                break
            elif key:
                NOTE_TO_KEY[f"cc_{msg.control}"] = key
                print(f"✅ Mapped control {msg.control} to key '{key}'")

# Add mouse movement mappings
NOTE_TO_KEY["mouse_movement"] = mouse_keys

# Ask for a name for this mapping
mapping_name = input("\nEnter a name for this mapping (saved in JSON): ").strip()
data_to_save = {mapping_name: NOTE_TO_KEY}

print("\n💾 Saving mappings...")
with open("midi_mapping.json", "w") as f:
    json.dump(data_to_save, f, indent=4)

print("✅ Saved! You can now use this mapping in your MIDI keyboard script.")
