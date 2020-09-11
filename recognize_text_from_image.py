import pytesseract
from PIL import Image
from multiprocessing import Pool, Manager
import sys
import json
import time

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
for i in range(max_id):
     pool.apply_async(do_recognize_in_process,
                      args=(i,),
                      error_callback=lambda x: print(x))
pool.close()
pool.join()
#print(np.mean(ocr_times), np.std(ocr_times))