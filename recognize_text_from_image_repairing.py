import json
import traceback
import pytesseract
import re
from Levenshtein._levenshtein import distance
from PIL import Image
from multiprocessing import Pool, Manager
import sys
import time
from utils import parse_metamodel_keywords
import pyprind
import numpy as np

sys.argv.append("DejavuMonoSans")
sys.argv.append("eng")
out_path = sys.argv[1]
lang = sys.argv[2]

mng = Manager()
ocr_times = mng.list()
pp_times = mng.list()

def recognize_and_replace_with_keywords(recognized_text, keywords):
    symbol = recognized_text
    #matches = re.findall("\( *[a-zA-Z0-9$_]+ *\|", symbol)
    words_regex = '[a-zA-Z0-9$_€¥®]+'
    matches = re.finditer("\(( *[a-zA-Z0-9$_]+( *:\n* *[a-zA-Z0-9$_]+)?( *,)*)+ *\|", symbol)
    for word in matches:
        word = word.string[word.start():word.end()]
        var_matches = re.findall(words_regex, word)
        for var in var_matches:
            keywords.add(var.strip())

    matches = re.findall("let +[a-zA-Z0-9$_]+", symbol)
    for word in matches:
        keywords.add(word.rsplit(" ",1 )[-1])
    token_escape_sequence = "#####"
    token_list = []
    matches = re.findall(words_regex, symbol)
    keywords = sorted(keywords, key=lambda x: len(x))

    for i, word in enumerate(matches):
        if i == 3:
            symbol = symbol.replace(word, token_escape_sequence, 1)
            token_list.append(word)
            continue
        symbol = symbol.replace(word, token_escape_sequence, 1)
        last_ratio = 0
        best_match = word
        for keyword in keywords:
            if abs(len(word) - len(keyword)) <= 2:
                #r = ratio(word, keyword)
                r = 1 - (distance(word, keyword) / max(len(word), len(keyword)))
                #if r > 0.75 and r > last_ratio:
                if r > last_ratio:
                    last_ratio = r
                    best_match = keyword
        token_list.append(best_match)
    try:
        recognized_text = symbol.replace(token_escape_sequence, "%s")
        recognized_text = recognized_text % tuple(token_list)
        return recognized_text
    except Exception as e:
        traceback.print_exc()

def do_recognize_in_process(index, ecore_file, gt_expression):
    #os.environ['OMP_THREAD_LIMIT'] = "1"
    keywords = parse_metamodel_keywords(ecore_file)
    with open("wordlistfile.bak") as f:
        keywords.update(f.read().split("\n"))

    start_time = time.time()
    prev_recognized_text = pytesseract.image_to_string(Image.open(out_path + '/images/%d.png' % index), lang=lang)
    ocr_times.append(time.time() - start_time)
    #r1 = ratio(prev_recognized_text, gt_expression)
    start_time = time.time()
    recognized_text = recognize_and_replace_with_keywords(prev_recognized_text, keywords)
    pp_times.append(time.time() - start_time)
    #r2 = ratio(recognized_text, gt_expression)
    #if r2 < r1:
    #    print(index)
    with open(out_path + "/recognized_text/%d.txt" % index, "w") as f:
        f.write(recognized_text)
    return index

matches = json.load(open("loaded_no_duplicated_filtered_expressions.json"))

oid = 0
pool = Pool(1)
bar = pyprind.ProgBar(len(matches), track_time=True, title='Recognizing expressions from images', bar_char='█', update_interval=1.)
for i, match in enumerate(matches[oid:], start=oid):
#for i, match in enumerate(matches[oid:], start=oid):
     pool.apply_async(do_recognize_in_process,
                      args=(i, match['file'], "context %s\ninv %s:\n%s" % (match['context'], match['inv'], match['expression'])),
                      callback=lambda x: bar.update(),
                      error_callback=lambda x: print(x))#, callback=lambda x : print(x))
pool.close()
pool.join()

print("\t\t*** Performance in font '%s' ***" % out_path)
print("\t\t\t*** Average time spent in post-processing: %s ±%s ***" % (np.mean(pp_times), np.std(pp_times)))
print("\t\t\t*** Average time spent on OCR recognition: %s ±%s ***" % (np.mean(ocr_times), np.std(ocr_times)))