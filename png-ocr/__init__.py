import logging
import pytesseract
import azure.functions as func
import io

from PIL import Image

def png_ocr(image_data):
    #Required for local only
    #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    text = ""
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    
    return text

def main(req: func.HttpRequest) -> func.HttpResponse:
    #1
    logging.info('Python HTTP trigger function processed a request.')

    text = ""
    
    for input_file in req.files.values():
        filename = input_file.filename
        contents = input_file.stream.read()

        f = open("test.png","wb")
        f.write(contents)
        f.close()

        text = text + png_ocr(contents)

        logging.info('Filename: %s' % filename)
        logging.info('Contents Length:')
        logging.info(len(text))

    if len(text) > 0:
        return func.HttpResponse(text)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
