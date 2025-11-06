# MIDI Keyboard to Mouse & Keyboard Mapper

This project allows you to use your MIDI keyboard or controller (for example, the Akai MPK Mini) as a PC input device. It converts MIDI signals into keyboard and mouse inputs, enabling you to play games or control your computer using your MIDI instrument.


![MIDI Controller Demo](https://medias.audiofanzine.com/images/normal/akai-mpk-mini-2011205.jpg)

## Features

- Use your MIDI keyboard to play PC games.
- Control mouse movement, left and right clicks, and middle mouse button.
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

## How To use

1. Run `midi_keyboard.py` to create your custom keybinds.
   - Choose which connected MIDI keyboard or controller you want to use.
   - Map your keyboard keys and mouse actions to specific MIDI notes or pads.
   - Once finished, save your configuration when prompted.  
     Your keybind file will be saved automatically in the `piano_keybinds` folder.

2. Run `launch_midi.py` to start using your MIDI keyboard as a controller.
   - Select the same MIDI device you configured earlier.
   - Choose which saved keybind file you want to load.
   - Once loaded, your MIDI keys and pads will now function as the mapped keyboard and mouse inputs.

You can create multiple profiles for different games or applications, then easily switch between them by selecting a different saved file.

## Notice
- Some games with anti-input systems may not accept simulated mouse clicks or keyboard presses.
- Works best with windowed or borderless applications.
- Continuous mouse movement uses threading to simulate held input, allowing for smoother control.

## Technologies Used
- Python 3
- mido – for MIDI input/output
- python-rtmidi – for low-level MIDI communication
- pynput – for keyboard and mouse control

## License
This project is open-source and free for personal modification and experimentation. Credit is appreciated if you publish a derived version.
