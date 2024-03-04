from PySimpleGUI import Image, Button, Window, WIN_CLOSED

def popup_image(image, title='Popup with Image'):
    layout = [
        [Image(data=image)],
        [Button("OK")]
    ]

    # Create the Window
    window = Window(title, layout, element_justification='c')

    # Event Loop
    while True:
        event, values = window.read()
        if event == "OK" or event == WIN_CLOSED:
            break

    # Close the window
    window.close()