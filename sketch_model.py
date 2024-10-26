# # sketch_model.py
# import cv2

# def convert_to_sketch(image_path, output_path):
#     image = cv2.imread(image_path)
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     inverted_image = 255 - gray_image
#     blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
#     inverted_blurred = 255 - blurred
#     sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
#     cv2.imwrite(output_path, sketch)

from PIL import Image
import cv2

def convert_to_sketch(input_path, output_path):
    # Load the image
    img = cv2.imread(input_path)
    # Convert to gray scale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Invert the image
    inverted_img = 255 - gray_img
    # Blur the image
    blurred_img = cv2.GaussianBlur(inverted_img, (21, 21), sigmaX=0, sigmaY=0)
    # Invert the blurred image
    inverted_blurred_img = 255 - blurred_img
    # Create the sketch image
    sketch_img = cv2.divide(gray_img, inverted_blurred_img, scale=256.0)
    # Save the sketch image
    cv2.imwrite(output_path, sketch_img)

