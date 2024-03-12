from PIL import Image 
from pytesseract import pytesseract 
  
# for image
path_to_tesseract = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
image_path = r"download.jpg"
  

img = Image.open(image_path) 
  

pytesseract.tesseract_cmd = path_to_tesseract 

text = pytesseract.image_to_string(img) 
print(text)


from pypdf import PdfReader 
  

reader = PdfReader('example.pdf') 
  
 
print(len(reader.pages)) 
  

page = reader.pages[0] 
  

text = page.extract_text() 
print(text) 