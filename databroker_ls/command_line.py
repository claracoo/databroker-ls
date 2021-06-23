from pynput import keyboard
from pynput.keyboard import Key, Controller

from databroker_ls.qt import ls

"""
This file is a script to actually make the lines load dynamically
"""

def on_press(key, object):
    """
    Handle key presses: we only care about escape and enter
    """
    if key == keyboard.Key.esc:
        # Stop listener and get out of the loading window, back to regular terminal
        return False
    else:
        if key == keyboard.Key.enter:
            # load the next iteration of the catalog
            print(object.myOwnPrinting())
            # if (object.myOwnPrinting() == "exit"):
            #     return False

def main():
    object = ls() # instantiate new ls object
    print("Starting Time          Scan ID      UUID")
    print(object.myOwnPrinting()) # start by loading the first set of entries
    # Collect events until released
    with keyboard.Listener(on_press=lambda event: on_press(event, object=object)) as listener:
        listener.join() # will only join back up with the terminal when we return False


if __name__ == '__main__':
    main()