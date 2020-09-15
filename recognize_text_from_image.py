import pytesseract
from PIL import Image
from multiprocessing import Pool, Manager
import sys
import json
import time
import pyprind
import numpy as np

mng = Manager()
out_path = sys.argv[1]
lang = sys.argv[2]
ocr_times = mng.list()

def do_recognize_in_process(index):
    start_time = time.time()
    recognized_text = pytesseract.image_to_string(Image.open(out_path + '/images/%d.png' % index), lang=lang)
    ocr_times.append(time.time() - start_time)
    with open(out_path + "/recognized_text/%d.txt" % index, "w") as f:
        f.write(recognized_text)


max_id = len(json.load(open("loaded_no_duplicated_filtered_expressions.json")))

pool = Pool(1)
bar = pyprind.ProgBar(max_id, track_time=True, title='Recognizing expressions from images', bar_char='█', update_interval=1.)
for i in range(max_id):
     pool.apply_async(do_recognize_in_process,
                      args=(i,),
                      callback=lambda x: bar.update(),
                      error_callback=lambda x: print(x))
pool.close()
pool.join()

print("\t\t*** Performance in font '%s' ***" % out_path)
print("\t\t\t*** Average time spent on OCR recognition: %s ±%s ***" % (np.mean(ocr_times), np.std(ocr_times)))