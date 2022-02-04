import logging
import pytesseract
import azure.functions as func
import io

import asyncio

from PIL import Image

def png_ocr(image_data):
    #Required for local only
    #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text = ""
    byteImgIO = io.BytesIO(image_data)
    byteImgIO.seek(0)
    
    image = Image.open(byteImgIO)
    
    text = pytesseract.image_to_string(image)
    
    return text

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    text = ""
    
    for input_file in req.files.values():
        filename = input_file.filename
        contents = input_file.stream.read()

        text = png_ocr(contents)

        length = len(text)

        logging.info('Filename: %s' % filename)
        logging.info('Contents Length: {length})')

    return func.HttpResponse(text, status_code=200)
