import pytesseract
from PIL import Image
import io

def extract_text_from_image(file_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(file_bytes))
    text = pytesseract.image_to_string(image)
    return text

# import pytesseract
# from PIL import Image, ImageEnhance, ImageFilter
# import numpy as np
# import cv2
# import io

# def preprocess_image(image: Image.Image) -> Image.Image:
#     # Convert PIL Image to OpenCV format
#     open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
#     # Convert to grayscale
#     gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    
#     # Apply GaussianBlur to reduce noise and improve thresholding
#     gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
#     # Apply adaptive thresholding
#     gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                  cv2.THRESH_BINARY, 11, 2)
    
#     # Use morphological operations to remove noise
#     kernel = np.ones((1, 1), np.uint8)
#     gray = cv2.erode(gray, kernel, iterations=1)
#     gray = cv2.dilate(gray, kernel, iterations=1)
    
#     # Detect edges
#     edges = cv2.Canny(gray, 100, 200)
    
#     # Find contours and straighten the image
#     contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#     if contours:
#         largest_contour = max(contours, key=cv2.contourArea)
#         rect = cv2.minAreaRect(largest_contour)
#         box = cv2.boxPoints(rect)
#         box = np.int0(box)
        
#         width = int(rect[1][0])
#         height = int(rect[1][1])
        
#         src_pts = box.astype("float32")
#         dst_pts = np.array([[0, height-1],
#                             [0, 0],
#                             [width-1, 0],
#                             [width-1, height-1]], dtype="float32")
        
#         M = cv2.getPerspectiveTransform(src_pts, dst_pts)
#         warped = cv2.warpPerspective(gray, M, (width, height))
        
#         gray = warped
    
#     # Convert back to PIL Image
#     processed_image = Image.fromarray(gray)
    
#     return processed_image

# def extract_text_from_image(file_bytes: bytes) -> str:
#     try:
#         image = Image.open(io.BytesIO(file_bytes))
#         processed_image = preprocess_image(image)
#         processed_image.save("processed_image.png")  # Save the processed image for debugging
#         text = pytesseract.image_to_string(processed_image, lang='eng')
#         return text
#     except Exception as e:
#         raise RuntimeError(f"Error processing image: {e}")