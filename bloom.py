import cv2
import numpy as np
from typing import Tuple
import COLORS as colors

def apply_blooming(image):
    #Apply a blooming effect to the image
    image = cv2.GaussianBlur(image, ksize=(3, 3), sigmaX=2, sigmaY=2)
    image = cv2.blur(image, ksize=(5, 5))
    return image

def create_border(image, margin, thickness, color):
    #Draw a rectangular border around the image
    height, width = image.shape[:2]
    cv2.rectangle(image, (margin, margin), (width - margin, height - margin), color, thickness)
    return image

def glowing_border(image, margin, thickness, color):
    #Create a glowing border effect by applying a border and then adding a blooming effect.
    image = create_border(image, margin, thickness, color)

    image = apply_blooming(image)
    return image

def glowing_text(image, text, color):
    #Image Dimensions
    height, width = image.shape[:2]
    
    # Size text
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    font_scale = 3
    thickness = 2
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
    
    x_pos = (width - text_width) // 2
    y_pos = (height + text_height) // 2
    
    #Create text
    image = cv2.putText(image, text, (x_pos, y_pos), font, font_scale, color, thickness)
    
    return image


