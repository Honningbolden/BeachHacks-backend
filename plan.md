# Plan

### Backend
1. Receive HTTP Request
2. Preprocess
   - Tweak settings for higher of text visibility
   - Slice image horizontally to group lines -> Resulting in multiple image slices
3. Perform OCR
   - Group strings by image slice (as single string <- Comma separated)
   - Use Tesseract to perform OCR
   - Return all strings as list
4. Send to OpenAI API (or DAIN AI)
   - Parse all list items as text lines
   - Make HTTP Request to OpenAI API
   - Use response.json to get data
5. Return response to FrontEnd (or upload to Google Sheet using Google Sheet API)

### Frontend
1. Take image
2. Convert image to base64
3. Make HTTP request to backend

# Links
- **Geeks for Geeks: Text Detection and Extraction using OpenCV and OCR:** https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/
- **Geeks for Geeks: OpenCV Tutorial in Python:** https://www.geeksforgeeks.org/opencv-python-tutorial/
- **DataCamp: Getting Started with Python HTTP Requests for REST APIs:** https://www.datacamp.com/tutorial/making-http-requests-in-python
- **Medium: Tesseract OCR: Understanding the Contents of Documents, Beyond Their Text:** https://medium.com/geekculture/tesseract-ocr-understanding-the-contents-of-documents-beyond-their-text-a98704b7c655
  - Very good way to understand how Tessaract OCR reads text layouts!
- **Geeks for Geeks: Build a Python REST API using Flask:** https://www.geeksforgeeks.org/python-build-a-rest-api-using-flask/

#### Techniques
- **OpenCV:** Use this library to preprocess images before performing OCR
- **Tesseract:** OCR library
- **OpenAI Text Generation API:** Send OCR output to this API and receive a structured response (structured output)