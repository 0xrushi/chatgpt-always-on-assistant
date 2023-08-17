from pynput import keyboard

# Track the state of the Ctrl key and Ctrl+N combination
ctrl_pressed = False
ctrl_n_pressed = False

def on_press(key):
    global ctrl_pressed, ctrl_n_pressed

    if key == keyboard.Key.ctrl:
        ctrl_pressed = True
    elif key == keyboard.KeyCode.from_char('n') and ctrl_pressed:
        ctrl_n_pressed = True
        
    if ctrl_pressed and ctrl_n_pressed:
        print("Ctrl+N pressed!")

def on_release(key):
    global ctrl_pressed, ctrl_n_pressed

    if key == keyboard.Key.ctrl:
        ctrl_pressed = False
    elif key == keyboard.KeyCode.from_char('n') and ctrl_pressed:
        ctrl_n_pressed = False

    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
