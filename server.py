from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from ocr import enhance_image, process_receipt
import open_api
import os
import base64
import csv
import io

from open_api import interpret_receipt

app = Flask(__name__)
api = Api(app)


def convert_to_image(received):
    image_path = os.path.join("uploads", "image.jpeg")
    try:
        data = base64.b64decode(received)
        with open(image_path, 'wb') as file:
            file.write(data)
    except Exception as e:
        print(f'Error: {e}')
    return image_path

def append_gpt_lines(writer, gpt_text):
    """
    Splits gpt_text by lines, then splits each line by commas,
    and writes them as CSV rows.
    Example line: "SODA ULT, Soda Ultimate, Soda, $5.99"
    """
    lines = gpt_text.strip().splitlines()
    for line in lines:
        columns = [col.strip() for col in line.split(',')]
        writer.writerow(columns)


class UploadImage(Resource):
    def post(self):
        # Check JSON for image
        data = request.get_json()
        if not data or 'image' not in data:
            return {'error': 'No image files provided'}, 400

        # Convert base64 image to file
        image_base64 = data['image']
        image_path = convert_to_image(image_base64)

        # Run OCR
        ocr_text = process_receipt(image_path)
        print("OCR Output:", ocr_text)
        if not ocr_text.strip():
            return {'error': 'No text found in receipt image'}, 400

        # Interpret OCR
        gpt_output = interpret_receipt(ocr_text)
        for fence in ("```"):
            gpt_output = gpt_output.replace(fence, "")
        print("GPT Output:",gpt_output)

        # Check for existing CSV base64 request
        csv_b64 = data.get('csv')

        if not csv_b64:
            new_bio = io.StringIO()
            writer = csv.writer(new_bio)

            append_gpt_lines(writer, gpt_output)

            new_bio.seek(0)
            new_csv_bytes = new_bio.read().encode('utf-8')
            new_csv_b64 = base64.b64encode(new_csv_bytes).decode('utf-8')

            return {
                'message': 'New CSV created!',
                'updatedCsv': new_csv_b64
            }
        else:
            # _____ Update Existing CSV-File _______
            try:
                csv_raw = base64.b64decode(csv_b64)
            except Exception as e:
                return {'error': f'CSV decode error: {str(e)}'}, 400

            # Load existing CSV into memory
            existing_bio = io.StringIO(csv_raw.decode('utf-8', errors='replace'))
            reader = csv.reader(existing_bio)

            updated_bio = io.StringIO()
            writer = csv.writer(updated_bio)

            for row in reader:
                writer.writerow(row)

            append_gpt_lines(writer, gpt_output)

            updated_bio.seek(0)
            updated_bytes = updated_bio.read().encode('utf-8')
            updated_csv_b64 = base64.b64encode(updated_bytes).decode('utf-8')

            return {
                'message': "Existing CSV updated!",
                'updatedCsv': updated_csv_b64
            }


api.add_resource(UploadImage, '/')

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(host='0.0.0.0', port=5001)
