# MIDI Keyboard to Mouse & Keyboard Mapper

This project allows you to use your MIDI keyboard or controller (for example, the Akai MPK Mini) as a PC input device. It converts MIDI signals into keyboard and mouse inputs, enabling you to play games or control your computer using your MIDI instrument.

---

## Features

- Use your MIDI keyboard to play PC games.
- Control mouse movement, left and right clicks, and even the middle mouse button.
- Map MIDI notes, pads, and knobs to keyboard keys.
- Continuous mouse movement while a key is held.
- Create and save multiple custom keybind profiles for different games.

---

## How It Works

- The program listens for MIDI input using the `mido` library.
- Each MIDI note, pad, or knob can be assigned to a computer key or mouse action.
- The configuration is stored in JSON format inside a `piano_keybinds` folder.
- The `launch_midi.py` script reads your selected profile and runs the key mappings in real time.

---

## Example Use Cases

| Game | Example Use |
|------|--------------|
| Valorant | Map WASD to pads, left/right click to shoot, knobs for camera movement |
| Minecraft | Control player movement, place/break blocks, open inventory |
| Coding | Assign macros like copy/paste, undo, or run scripts |
| DAWs | Use pads for transport controls or effect toggles |

---

## Setup and Usage

### 1. Install Dependencies

Make sure Python 3 is installed, then run:

```bash
pip install mido python-rtmidi pynput
