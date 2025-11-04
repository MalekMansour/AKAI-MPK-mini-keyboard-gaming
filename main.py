import mido
import pyautogui

# MIDI to keyboard mapping
NOTE_TO_KEY = {
    48: 'w',   # C3
    50: 'a',   # D3
    52: 's',   # E3
    53: 'd',   # F3
    55: 'space',  # G3
    57: 'shift',  # A3
}

# Find your MPK Mini automatically
input_name = None
for name in mido.get_input_names():
    if "mpk" in name.lower():
        input_name = name
        break

if not input_name:
    print("Couldn't find your MPK Mini! Make sure it's plugged in.")
    exit()

print(f"🎹 Connected to {input_name}")
print("Press Ctrl+C to quit.\n")

# Track held notes
held_notes = set()

with mido.open_input(input_name) as port:
    for msg in port:
        if msg.type == 'note_on' and msg.velocity > 0:
            note = msg.note
            if note in NOTE_TO_KEY and note not in held_notes:
                key = NOTE_TO_KEY[note]
                pyautogui.keyDown(key)
                held_notes.add(note)
                print(f"Note {note} pressed → holding '{key}'")
        elif msg.type in ('note_off',) or (msg.type == 'note_on' and msg.velocity == 0):
            note = msg.note
            if note in NOTE_TO_KEY and note in held_notes:
                key = NOTE_TO_KEY[note]
                pyautogui.keyUp(key)
                held_notes.remove(note)
                print(f"Note {note} released → released '{key}'")
