from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io
import os
from shutil import copy
from rake_nltk import Rake
import pandas as pd
from gensim.summarization import keywords 
import warnings
import re

def start_scanning(file_path):
    tool = pyocr.get_available_tools()[0]
    req_image = []
    final_text = []
    path_to_pdf = file_path
    file_name = path_to_pdf.split('/')[-1]
    print(file_name)
    print('This is path to pdf: ' + path_to_pdf)
    path_to_new_pdf = 'scanned_pdf_for_email'
    image_pdf = Image(filename=path_to_pdf, resolution=300)
    image_jpeg = image_pdf.convert('jpeg')

    for img in image_jpeg.sequence:
        img_page = Image(image=img)
        req_image.append(img_page.make_blob('jpeg'))

    for img in req_image:
        txt = tool.image_to_string(
            PI.open(io.BytesIO(img)), lang='eng', builder=pyocr.builders.TextBuilder())
        final_text.append(txt)

    with open('./output_text_file/listfile.txt', 'w') as f:
        for item in final_text:
            f.write('%s\n' % item)
    
    
    company_name = []

    sender_names = ['triumph']

    found_company = ''
    list_text_file = []

    with open('./output_text_file/listfile.txt', 'r') as f:
        list_text_file = f.read().split()
        
    list_to_string = ' '.join(map(str, list_text_file))

    # uding regex to get all caps words
    result = filter(None, [x.strip() for x in re.findall(r"\b[A-Z\s]+\b", list_to_string)])
    print(*result) # printing the list using * operator separated by space  

    # values = keywords(text=list_to_string, split='\n', scores=True)
    # data = pd.DataFrame(values, columns=['keyword','score'])
    # data = data.sort_values('score', ascending=False)
    # print(data.head(10))
    
    print('this is text in string: ' + list_to_string)


    # r = Rake()
    # r.extract_keywords_from_text(list_to_string)
    # phrases = r.get_ranked_phrases_with_scores()
    # table = pd.DataFrame(phrases, columns=['score', 'Phrase'])
    # table = table.sort_values('score', ascending=False)
    # print(table.head(10))
    
    #print(list_text_file)

    for word in list_text_file:
        if word.lower() in company_name:
            found_company = word.lower()
            break

    subject_str = str(found_company.capitalize()) + ' mail' + '.pdf'
    print(subject_str)
    #os.rename(path_to_pdf, path_to_new_pdf + subject_str)
    copy('./scanned_pdf_files/' + file_name, path_to_new_pdf)
    os.rename(path_to_new_pdf + '/' + file_name,path_to_new_pdf + '/' + subject_str)
    #print('here i am: ' + file_path)


class ExampleHandler(FileSystemEventHandler):
    def on_created(self, event):  # when file is created
        start_scanning(event.src_path)
        # do something, eg. call your function to process the image
        print("Got event for file %s" % event.src_path)


observer = Observer()
event_handler = ExampleHandler()  # create event handler
# set observer to use created handler in directory
observer.schedule(event_handler, path='./scanned_pdf_files/')
observer.start()

# sleep until keyboard interrupt, then stop + rejoin the observer
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
