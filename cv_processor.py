import PyPDF2
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from config import load_config

class CVProcessor:
    def __init__(self):
        self.config = load_config()

    def extract_text_from_pdf(self, pdf_path):
        start_time = time.time()
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(reader.pages)):
                    text += reader.pages[page_num].extract_text()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            text = None
        end_time = time.time()
        print(f"Time taken to extract text from PDF: {end_time - start_time} seconds")
        return text

    def extract_text_azure(self, image_path):
        start_time = time.time()
        try:
            subscription_key = self.config['AZURE_VISION_KEY']
            endpoint = self.config['AZURE_VISION_ENDPOINT']

            client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

            with open(image_path, "rb") as image_file:
                read_response = client.read_in_stream(image_file, raw=True)

            read_operation_location = read_response.headers["Operation-Location"]
            operation_id = read_operation_location.split("/")[-1]

            while True:
                read_result = client.get_read_result(operation_id)
                if read_result.status not in ['notStarted', 'running']:
                    break

            if read_result.status == OperationStatusCodes.succeeded:
                text = ""
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        text += line.text + "\n"
            else:
                text = None
        except Exception as e:
            print(f"Error extracting text from image: {e}")
            text = None
        end_time = time.time()
        print(f"Time taken to extract text from image: {end_time - start_time} seconds")
        return text

    def extract_text(self, image_or_pdf_path):
        start_time = time.time()
        if image_or_pdf_path.endswith('.pdf'):
            text = self.extract_text_from_pdf(image_or_pdf_path)
        else:
            text = self.extract_text_azure(image_or_pdf_path)
        end_time = time.time()
        print(f"Time taken to extract text: {end_time - start_time} seconds")
        return text