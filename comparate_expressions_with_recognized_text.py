import json
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
import Levenshtein
import sys

out_path = sys.argv[1]

i = 0
chars = {
     "\n": " ",
     "\r": "",
     "\t": " "
}


def delete_chars(a):
    b = a
    for char_to_replace, replace in chars.items():
        b = b.replace(char_to_replace, replace)
    return b

matches = []

matcher = SequenceMatcher()
for item in json.load(open("expressions_v2.json")):
    gt_expression = delete_chars("context %s\ninv %s\n%s" % (item['context'], item['inv'], item['expression']))
    recognized_expression = delete_chars(open(out_path + "/recognized_text/%d.txt" % i).read())
    ratio = SequenceMatcher(None, gt_expression, recognized_expression).ratio()
    fuzzy_ratio = fuzz.ratio(gt_expression, recognized_expression)/100
    lev_ratio = Levenshtein.ratio(gt_expression, recognized_expression)
    matches.append({
        'id': i,
        'gt_expression': gt_expression,
        'recognized_expression': recognized_expression,
        'ratio': ratio,
        'fuzzy_ratio': fuzzy_ratio,
        'lev_ratio': lev_ratio
    })
    i+=1

json.dump(matches, open(out_path + "/matches.json", "w"))