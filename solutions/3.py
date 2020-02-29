"""
Question
---------
Using: OpenCV, Cvlib, Matplotlib, Tensorflow
Create an object detection program that reads an image from the storage, 
    detects only Fruits and displays the image with a bounding box and labels about the detected objects
"""
# CVlib underneath uses YOLOv3 model trained on COCO dataset 
# capable of detecting 80 common objects in context
import os
import sys
import cv2
import matplotlib
import matplotlib.pyplot as plt
import cvlib as cv
import numpy as np
from cvlib.object_detection import draw_bbox
# the backend available on my own system
matplotlib.use('TkAgg')
mng = plt.get_current_fig_manager()
# set plot to full screen
mng.resize(*mng.window.maxsize())

main_dir = os.path.dirname(os.path.dirname(__file__))
processed_assets = os.path.join(main_dir, "assets", "processed")
raw_assets = os.path.join(main_dir, "assets", "raw")
example_image = os.path.join(raw_assets, "example2.jpeg")

def fruitclassifier(image_path:str, confidence:float=0.5) -> np.ndarray :
    """
    Classifies using cvlib
    """
    YOLO_FRUITS = ["banana", "apple", "orange"]
    if not os.path.exists(image_path):
        sys.exit(f"Image does not exist at {image_path}")
    image = cv2.imread(image_path)
    bbox, label, conf = cv.detect_common_objects(image)
    # remove low level confidence objects and non fruits
    for index, (_, lab, con) in enumerate(zip(bbox, label, conf)):
        if not (con > confidence and lab in YOLO_FRUITS):
            bbox.pop(index)
            label.pop(index)
            conf.pop(index)
    output_image = draw_bbox(image, bbox, label, conf)
    save_to = os.path.join(processed_assets, os.path.basename(image_path))
    cv2.imwrite(save_to, output_image)
    print(f"Found {set(label)} as fruit(s) in {image_path}")
    return output_image

if __name__=="__main__":
    if len(sys.argv) == 1 :
        output_image = fruitclassifier(example_image)
    else:
        output_image = fruitclassifier(sys.argv[1])
    # show image, switch back from BGR to RGB
    plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
    print("Opening annotated image ...")
    plt.show()