import pytesseract
import cv2

# Ruta fija a Tesseract en Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image_path: str) -> str:

    image = cv2.imread(image_path)

    if image is None:
        raise Exception("No se pudo leer la imagen")

    # Rotación fija (tu documento viene girado)
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        2
    )

    # OCR SOLO EN INGLES (estable)
    text = pytesseract.image_to_string(gray, lang="eng")

    return text
