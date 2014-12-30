import pytesser
from PIL import Image


image = Image.open('data2.png')  # Open image object using PIL
print pytesser.image_to_string(image)     # Run tesseract.exe on image
print pytesser.image_file_to_string('data2.png')
