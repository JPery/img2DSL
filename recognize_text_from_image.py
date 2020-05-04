import pytesseract
from PIL import Image
from multiprocessing import Pool
import sys

out_path = sys.argv[1]

def do_recognize_in_process(index):
    recognized_text = pytesseract.image_to_string(Image.open(out_path + '/images/%d.png' % index))
    with open(out_path + "/recognized_text/%d.txt" % index, "w") as f:
        f.write(recognized_text)


max_id = 4773

pool = Pool(4)
for i in range(max_id+1):
     pool.apply_async(do_recognize_in_process,
                      args=(i,),
                      error_callback=lambda x: print(x))
pool.close()
pool.join()
