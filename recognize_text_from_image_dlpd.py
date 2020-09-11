import pytesseract
from PIL import Image
from multiprocessing import Pool, Manager
import sys
import json
from utils import parse_metamodel_keywords
import time
import os

mng = Manager()
sys.argv.append("DejavuMonoSans")
out_path = sys.argv[1]
lang_creation_time = mng.list()
ocr_times = mng.list()

def do_recognize_in_process(index, ecore_file):
    #os.environ['OMP_THREAD_LIMIT'] = "1"
    names = parse_metamodel_keywords(ecore_file)
    with open("wordlistfile.bak") as f:
        out_file_str = f.read() + "\n"
        out_file_str += "\n".join(names)
        with open("wordlistfile%d" % index, "w") as f:
            f.write(out_file_str)
    #print("Processing image #%d" % index)
    #os.system("./create_tessdata_no_lstm.sh %d" % index)
    start_time = time.time()
    os.system("./create_tessdata.sh %d > /dev/null" % index)
    lang_creation_time.append(time.time() - start_time)
    #os.system("rm wordlistfile%d" % index)
    #recognized_text = pytesseract.image_to_string(Image.open(out_path + '/images/%d.png' % index), lang='ocl%d' % index, config="strict")
    #recognized_text = pytesseract.image_to_string(Image.open(out_path + '/images/%d.png' % index), lang='ocl%d' % index, config="-c language_model_penalty_non_dict_word=1")
    #recognized_text = pytesseract.image_to_string(Image.open(out_path + '/images/%d.png' % index), lang='ocl%d' % index, config='--oem 0 -c tessedit_enable_dict_correction=1')
    #recognized_text = pytesseract.image_to_string(Image.open(out_path + '/images/%d.png' % index), lang='eng2', config='--oem 0 -c tessedit_enable_dict_correction=1 -c user_words_file="wordlistfile%d" -c load_system_dawg=0'  % index)
    start_time = time.time()
    recognized_text = pytesseract.image_to_string(Image.open(out_path + '/images/%d.png' % index), lang='ocl%d' % index)
    ocr_times.append(time.time() - start_time)
    os.system("rm /usr/local/share/tessdata/ocl%d.traineddata" % index)
    #os.system("rm wordlistfile%d" % index)
    with open(out_path + "/recognized_text/%d.txt" % index, "w") as f:
        f.write(recognized_text)



matches = json.load(open("loaded_no_duplicated_filtered_expressions.json"))

pool = Pool(1)
for i, match in enumerate(matches):
    pool.apply_async(do_recognize_in_process,
                     args=(i, match['file'],),
                     error_callback=lambda x: print(x))
pool.close()
pool.join()
#print(out_path)
#print(np.mean(lang_creation_time), np.std(lang_creation_time))
#print(np.mean(ocr_times), np.std(ocr_times))
