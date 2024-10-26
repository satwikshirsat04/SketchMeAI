# sketch_model.py
import cv2

def convert_to_sketch(image_path, output_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_image = 255 - gray_image
    blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
    inverted_blurred = 255 - blurred
    sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
    cv2.imwrite(output_path, sketch)
