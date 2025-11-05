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
print("Press a key/pad on your MPK Mini, then type the computer key it should trigger.")
print("Example: if you press a pad, type 'space' or 'shift' etc.")
print("When you're done, type 'done' and hit Enter.\n")

NOTE_TO_KEY = {}

with mido.open_input(input_name) as port:
    while True:
        msg = port.receive()

        if msg.type == 'note_on' and msg.velocity > 0:
            note = msg.note
            print(f"\n🎹 You pressed MIDI note {note}.")
            key = input("→ Enter the computer key for this note (or leave blank to skip): ").strip().lower()

            if key == "done":
                break
            elif key:
                NOTE_TO_KEY[note] = key
                print(f"✅ Mapped note {note} to key '{key}'")

        elif msg.type == 'control_change':
            print(f"\n🎚️ You moved knob/control {msg.control}.")
            key = input("→ Enter the computer key for this control (or leave blank to skip): ").strip().lower()
            if key == "done":
                break
            elif key:
                NOTE_TO_KEY[f"cc_{msg.control}"] = key
                print(f"✅ Mapped control {msg.control} to key '{key}'")

print("\n💾 Saving mappings to midi_mapping.json...")
with open("midi_mapping.json", "w") as f:
    json.dump(NOTE_TO_KEY, f, indent=4)

print("✅ Saved! You can now run `midi_keyboard.py` to use your custom mappings.")

