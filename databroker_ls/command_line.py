from pynput import keyboard
from pynput.keyboard import Key, Controller

from databroker_ls.qt import ls

from databroker import catalog

from databroker_ls.args import get_args

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
            data = object.myOwnPrinting()  # hold the current array of runs without recalling it
            for arr in data[0]:
                print(arr[0], "   ", arr[1], "   ", arr[2])  # how visually spaced out we want to see the data pieces
            if data[1] == "exit":
                # this was from qt.py, means that the data array is empty
                print("No more data in this catalog, exiting...")  # dot dot dot is important because there is a wait time
                return False  # this kicks us out of the listing state
            else:
                print(data[1])  # reminds user of what to do next


def main():
    object = ls(catalog=catalog[get_args().catalog])  # instantiate new ls object
    print("Starting Time          Scan ID      UUID")  # titles for our columns
    data = object.myOwnPrinting() # first time we access data (no user actions necessary after command)
    for arr in data[0]:
        # the first elem in data is the literal output from the catalog
        print(arr[0], "   ", arr[1], "   ", arr[2])  # in the order time, scan_id, uid
    if data[1] == "exit":
        return False  # this kicks us out of the listing state
    else:
        print(data[1])  # second elem in data is the message
    # Collect events until released
    with keyboard.Listener(
        on_press=lambda event: on_press(event, object=object)
    ) as listener:
        listener.join()  # will only join back up with the terminal when we return False


if __name__ == "__main__":
    main()
