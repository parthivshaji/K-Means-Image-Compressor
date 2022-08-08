import kmeansalgorithm
from PIL import Image
import PySimpleGUI as gui
from os import path

main_column = [
    [
        gui.Text("Image File"),
        gui.In(size=(45,1), enable_events=True, key="-IMAGE-"),
        gui.FileBrowse(),
    ],
    [
        gui.Text("Number of colors in final image (Recommended Value: 16)"),
        gui.In(size=(5,1), enable_events=True, key="-K-"),
        gui.Button('Compress Image',disabled=True)
    ]
]

layout = [
    [
        gui.Column(main_column),
    ]
]

window = gui.Window("K-Means Image Compressor", layout)
image_provided = False
K = -1

while True:
    event, values = window.read()
    if event == "Exit" or event == gui.WIN_CLOSED:
        break

    if event == "-IMAGE-":
        image_path = values["-IMAGE-"]
        image_provided = True
        window['Compress Image'].update(disabled=False)
    
    if event == "Compress Image":
        K = int(values["-K-"])
        if K > 0:
            kmeansalgorithm.runAlgorithm(image_path, K)
            gui.popup('Image Compressed! Check program directory')
            img = Image.open("compressed_{}".format(path.basename(image_path)))
            img.show()
        else:
            gui.popup('Enter K value greater than 0')

window.close()