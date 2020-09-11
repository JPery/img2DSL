import json
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
import Levenshtein
import sys
from utils import delete_chars

out_path = sys.argv[1]

i = 0

matches = []

matcher = SequenceMatcher()
perfect_expressions = []
for item in json.load(open("loaded_no_duplicated_filtered_expressions.json")):
    gt_expression = delete_chars("context %s\ninv %s:\n%s" % (item['context'], item['inv'], item['expression']))
    recognized_expression = delete_chars(open(out_path + "/recognized_text/%d.txt" % i).read())
    ratio = SequenceMatcher(None, gt_expression, recognized_expression).ratio()
    fuzzy_ratio = fuzz.ratio(gt_expression, recognized_expression)/100
    # lev_ratio = Levenshtein.ratio(gt_expression, recognized_expression)
    lev_distance = Levenshtein.distance(gt_expression, recognized_expression)

    lev_ratio = 1  - (lev_distance/max(len(gt_expression), len(recognized_expression)))
    expression = {
        'id': i,
        'gt_expression': gt_expression,
        'recognized_expression': recognized_expression,
        'ratio': ratio,
        'fuzzy_ratio': fuzzy_ratio,
        'lev_ratio': lev_ratio,
        'lev_distance': lev_distance,
        'file': item['file']
    }
    if lev_ratio == 1:
        perfect_expressions.append(expression)
    matches.append(expression)
    i+=1

#print(out_path, len(perfect_expressions))
json.dump(matches, open(out_path + "/matches.json", "w"))