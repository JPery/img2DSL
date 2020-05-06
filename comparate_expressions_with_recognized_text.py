import json
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
import Levenshtein
import sys
from utils import delete_chars

out_path = sys.argv[1]
#out_path = "UbuntuRegular"

i = 0

matches = []

matcher = SequenceMatcher()
perfect_expressions = []
for item in json.load(open("filtered_expressions_v2.json")):
    gt_expression = delete_chars("context %s\ninv %s:\n%s" % (item['context'], item['inv'], item['expression']))
    recognized_expression = delete_chars(open(out_path + "/recognized_text/%d.txt" % i).read())
    ratio = SequenceMatcher(None, gt_expression, recognized_expression).ratio()
    fuzzy_ratio = fuzz.ratio(gt_expression, recognized_expression)/100
    lev_ratio = Levenshtein.ratio(gt_expression, recognized_expression)
    expression = {
        'id': i,
        'gt_expression': gt_expression,
        'recognized_expression': recognized_expression,
        'ratio': ratio,
        'fuzzy_ratio': fuzzy_ratio,
        'lev_ratio': lev_ratio
    }
    if lev_ratio == 1:
        perfect_expressions.append(expression)
    matches.append(expression)
    i+=1
print(len(perfect_expressions))
json.dump(matches, open(out_path + "/matches.json", "w"))