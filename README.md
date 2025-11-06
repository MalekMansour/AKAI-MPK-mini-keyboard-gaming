# 🎹 Piano Controller – Turn Your MIDI Keyboard Into a Game Controller

## 🧠 What This Project Is
Piano Controller is a Python-based tool that lets you **turn any MIDI piano or pad controller** (like the AKAI MPK Mini) into a **fully functional game controller or keyboard emulator**.

Instead of pressing WASD on your keyboard, you can use your **piano keys or pads to move**, **click the mouse**, **jump**, or even **aim**. It’s completely customizable — every piano key, knob, or pad can be mapped to a keyboard or mouse action.

This means you can literally **play games, browse the web, or even make music and code using your MIDI piano**.

---

## ✨ Features
- 🎛️ **Fully Customizable Keybinds**  
  Choose which piano keys or knobs control your keyboard and mouse actions.
  
- 🖱️ **Mouse & Keyboard Support**  
  Control both mouse movement and clicks, or emulate keyboard presses.

- 🎹 **Multi-Device Support**  
  Works with any connected MIDI keyboard or controller — pick which one to use.

- 💾 **Keybind Profiles**  
  Save multiple keybind setups as `.json` files inside the `piano_keybinds` folder.  
  Quickly switch between them for different games or use cases.

- 🔁 **Real-Time Response**  
  Your MIDI input instantly translates to key presses or mouse movements.

---

## 🕹️ What You Can Do With It

You can use your piano as a controller for:

| Category | Example Games |
|-----------|----------------|
| 🎯 FPS / Shooters | Valorant, CS2, Overwatch *(for movement, jumping, and some aiming)* |
| 🧩 Platformers | Celeste, Hollow Knight, Cuphead |
| 🚗 Racing | Need for Speed, Forza Horizon |
| 🎶 Rhythm & Fun | Beat Saber (PC), OSU!, StepMania |
| 💻 General Use | Controlling the mouse, shortcuts, or macros |

While **some games with strict anti-cheat systems (like Valorant)** may block external input emulation, most indie, single-player, and creative software works perfectly.

---

## ⚙️ How It Works
1. Your MIDI keyboard sends **note_on**, **note_off**, and **control_change** signals.  
2. The program listens to those signals using the `mido` library.  
3. Each MIDI note or control is mapped to a corresponding **keyboard or mouse action** using `pynput`.  
4. You can save these mappings in a `.json` file and reload them later.

---

## 🧩 Files Overview
| File | Description |
|------|--------------|
| `setup_mapping.py` | Interactive setup script to create or edit your piano keybinds. |
| `launch_midi.py` | Launch your chosen MIDI device with a saved keybind profile. |
| `piano_keybinds/` | Folder containing your saved keybind sheets in JSON format. |

---

## 🚀 How to Use

### 1️⃣ Install Dependencies
Make sure you have Python 3.10+ installed, then run:

pip install mido python-rtmidi pynput


