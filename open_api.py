import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from ocr import enhance_image, process_receipt

def interpret_receipt(receipt_lines):
    print("receipt_lines", receipt_lines)
    env_path = Path('.env')
    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("OPENAI_API_KEY")
    system_prompt = ("Given a string of raw text taken from a receipt, return a formatted "
                     "csv file that "
                     "labels each item by category. The text might be missing some text or some characters, "
                     "so you'd need to fill in the blanks. The formatting should look like this soda: 3.99. Only "
                     "return pure csv formatting. The headers are as follows: specific item name, general item name, "
                     "category, price. An example of a correct output is 'DR PEPP ZERO,Dr. Pepper, Soda, "
                     "$2.99'). Don't use quotations, and don't return headers as part of the CSV. Please remove "
                     "repetitive words. Be sure to split lines so the outline is multiple lines!!")

    client = OpenAI(api_key = api_key)
    response = client.responses.create(
      model="gpt-4o-mini",
      instructions=system_prompt,
      input=receipt_lines
    )

    print("gpt output", response.output_text)

    return response.output_text