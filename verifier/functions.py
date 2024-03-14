import asyncio
import re
from io import BytesIO

import aiohttp
import requests
from PIL import Image
from pytesseract import pytesseract

path_to_tesseract = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
image_path = r"C:/Ved/Academic/Coding/Projects/lifeflow_backend/verifier/image.png"

patterns = r'(\w+)\s+(hospital|blood\s*bank|bloodbank|clinic|pharmacy|medical\s*centre)'  

# def get_image_local(image_path) -> str:
#     img =  Image.open(image_path) 

#     pytesseract.tesseract_cmd = path_to_tesseract 

#     text =  pytesseract.image_to_string(img) 
#     matches =  re.findall(patterns, text, re.IGNORECASE)
#     for match in matches:
#         if match[0].lower() in ["speciality", "super"]:
#             index = text.find(match[0])
#             if index > 0:
#                 prev_word_match = re.search(r'\b(\w+)\b', text[:index])
#                 if prev_word_match:
#                     concatenated_word = prev_word_match.group(1) + ' ' + match[0] + ' ' + match[1]
#                     return (concatenated_word)
#         else:
#             concatenated_word = match[0] + ' ' + match[1]
#             return (concatenated_word)
#     return ""

# print(get_image_local(image_path))

async def get_image_remote(image_url) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                img_content = await response.read()
                img = Image.open(BytesIO(img_content))
                pytesseract.tesseract_cmd = path_to_tesseract 
                text = pytesseract.image_to_string(img)
                matches = re.findall(patterns, text, re.IGNORECASE)
                for match in matches:
                    if match[0].lower() in ["speciality", "super"]:
                        index = text.find(match[0])
                        if index > 0:
                            prev_word_match = re.search(r'\b(\w+)\b', text[:index])
                            if prev_word_match:
                                concatenated_word = prev_word_match.group(1) + ' ' + match[0] + ' ' + match[1]
                                return concatenated_word
                    else:
                        concatenated_word = match[0] + ' ' + match[1]
                        return concatenated_word
            return ""

# async def main():
#     image_url = "https://image.slidesharecdn.com/5156041-5950-150621072950-lva1-app6891/75/max-hospital-shalimar-bagh-doctors-prescription-1-2048.jpg"
#     result = await get_image_remote(image_url)
#     print(result)
