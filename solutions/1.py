"""
Question
----------
Using Cv2
Create a function that: Reads an image from a path, create a grayscale transformation of the Image. 
Save the image to a folder. 
"""
import os
import sys
import cv2
import webbrowser

main_dir = os.path.dirname(os.path.dirname(__file__))
processed_assets = os.path.join(main_dir, "assets", "processed")
default_example = os.path.join(main_dir, "assets", "raw", "example.jpeg")

def gray_converter(image_path:str) -> str:
    """
    Receives path to an image, converts to greyscale
    Uses webview to open it on browser
    """
    if os.path.exists(image_path):
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        save_to = os.path.join(processed_assets, os.path.basename(image_path))
        cv2.imwrite(save_to,gray_image)
        print("Saving to: ", save_to)
        return save_to
    else:
        sys.exit("Path provided to image does not exist")

if __name__=="__main__":
    # if no picture is provided, use the default pic
    if len(sys.argv) == 1:
        converted = gray_converter(default_example)
    else:
        converted = gray_converter(sys.argv[1])
    # open in a web browser
    webbrowser.open_new_tab(converted)