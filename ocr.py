

from PIL import Image
import pytesseract
import os
import cv2

# Enhances the image using OpenCV to improve OCR accuracy
def enhance_image(receipt_path):
    # Reads the image in grayscale by removing color.
    receipt_image = cv2.imread(receipt_path, cv2.IMREAD_GRAYSCALE)
    # Applies Gaussian Blur to blur the x-axis more than the y-axes
    # Smooths the image to reduce noise and imperfections for better reading
    receipt_image = cv2.GaussianBlur(receipt_image,(2,2), 0)
    # Converts blurred grayscale image to binary image (black & white) to enhance text contrast.
    #receipt_image = cv2.adaptiveThreshold(receipt_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(receipt_image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=2)

    dilated_inverted = cv2.bitwise_not(dilation)

    # Inverts the image colors to match the optimal input for OCR,
    # depending on whether Tesseract performs better with dark text on a
    # light background or vice versa.

    #receipt_image = cv2.bitwise_not(receipt_image)

    # Transforms the processed OpenCV image (a NumPy array) back to a PIL Image,
    # which is required by pytesseract for OCR.
    final_receipt_image = Image.fromarray(dilated_inverted)
    return final_receipt_image


def process_receipt(image_path):
    receipt = enhance_image(image_path) # enhances image and assigns to receipt
    img_to_text = pytesseract.image_to_string(receipt)  # converts image into strings
    return img_to_text


