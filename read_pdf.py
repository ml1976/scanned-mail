## Windows, activation ##
#  C:\path\to\env\Scripts\activate

# https://ocrmypdf.readthedocs.io/en/latest/cookbook.html
# https://github.com/metebalci/pdftitle

from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io
import os

tool = pyocr.get_available_tools()[0]
#lang = tool.get_available_languages()[1]
# print(str(lang))

req_image = []
final_text = []

path_to_pdf = "./scanned_pdf_files/wow6.pdf"
path_to_new_pdf = "./scanned_pdf_files/"
image_pdf = Image(filename=path_to_pdf, resolution=300)
image_jpeg = image_pdf.convert('jpeg')

for img in image_jpeg.sequence:
    img_page = Image(image=img)
    req_image.append(img_page.make_blob('jpeg'))

for img in req_image:
    txt = tool.image_to_string(
        PI.open(io.BytesIO(img)),
        lang="eng",
        builder=pyocr.builders.TextBuilder())
    final_text.append(txt)

with open('./output_text_file/listfile.txt', 'w') as f:
    for item in final_text:
        f.write('%s\n' % item)

print('DONE')

company_name = ['terglau', 'vodeni', 'fors', 'primus',
                'prim usa', 'chegar', 'kecman', 'durisic']


found_company = ''
list_text_file = []

with open('./output_text_file/listfile.txt', 'r') as f:
    list_text_file = f.read().split()

print(list_text_file)


for word in list_text_file:
    if word.lower() in company_name:
        found_company = word.lower()
        break

print(found_company)

# create subject for email

subject_str = found_company.capitalize() + ' mail' + '.pdf'
print(subject_str)
#os.rename(path_to_pdf, path_to_new_pdf + subject_str)


'''
with open('listfile.txt') as file:
  for line in file:
    line = line.lower()
    for word in company_name:
      if word in line:
        found_company = word
        #print('this is the LINE: ' + line)
    if 'billing' in line:
        print(line)

print('this is the company in mail: ' + found_company)
'''
