from pynput import keyboard
from pynput.keyboard import Key, Controller

from databroker_ls.ls import ls

from databroker import catalog

from databroker_ls.args import get_args
from databroker_ls.catalog import SpecifiedCatalog
"""
This file is a script to actually make the lines load dynamically
"""


def format_printing(data, object):
    for i in range(len(data[0])):
        index = "     "
        if get_args().index:
            index = '{message: <{width}}'.format(message=object.UUIDtoIndex[data[0][i][2][:8]], width=5)
        print(index, data[0][i][0], "   ", data[0][i][1], "   ", data[0][i][2])
    if data[1] == "exit":
        # this was from qt.py, means that the data array is empty
        print("No more data in this catalog, exiting...")  # dot dot dot is important because there is a wait time
        return False  # this kicks us out of the listing state
    else:
        print(data[1])  # reminds user of what to do next


def on_press(key, object):
    """
    Handle key presses: we only care about escape and enter
    """
    if key == keyboard.Key.esc:
        # Stop listener and get out of the loading window, back to regular terminal
        print("exiting...")
        return False
    else:
        if key == keyboard.Key.enter:
            # load the next iteration of the catalog
            data = object.myOwnPrinting()  # hold the current array of runs without recalling it
            return format_printing(data, object)


def main():
    currentCatalog = get_args().catalog
    if currentCatalog == "":
        specifiedCatalog = SpecifiedCatalog()
        specifiedCatalog.query_for_catalog()
        currentCatalog = specifiedCatalog.currentCatalog
    object = ls(catalog=catalog[currentCatalog], fullUID=get_args().all, reverse=get_args().reverse, number=get_args().number)  # instantiate new ls object
    print("     Starting Time          Scan ID      UUID")  # titles for our columns
    data = object.myOwnPrinting() # first time we access data (no user actions necessary after command)
    format_printing(data, object)
    # Collect events until released
    with keyboard.Listener(
        on_press=lambda event: on_press(event, object=object)
    ) as listener:
        listener.join()  # will only join back up with the terminal when we return False


if __name__ == "__main__":
    main()
