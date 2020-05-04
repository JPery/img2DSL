import numpy as np
import json
import matplotlib.pyplot as plt
from pygments.token import String
from pyparsing import Literal

from utils import handwritten_like_typographies, computer_like_typographies
import pygments
from pygments.formatters.terminal import TerminalFormatter
from OCLLexer import OCLLexer
from multiprocessing import Process, Pool
from Levenshtein import ratio

MAX_ELEMENTS = 20
lexer = OCLLexer()
formatter = TerminalFormatter()

def parse_expression(expression):
    token_type_occurrences = {}
    errors_per_type = {}
    errors_per_token = {}
    tokens = {}
    gt_expression_tokens = list(pygments.lex(expression['gt_expression'], lexer))
    for token_type, token in gt_expression_tokens:
        token_type = str(token_type)
        if token_type not in token_type_occurrences:
            token_type_occurrences[token_type] = 0
        token_type_occurrences[token_type] += 1
        if token not in tokens:
            tokens[token] = {}
            tokens[token]['errors'] = []
            tokens[token]['type'] = token_type
    rec_expression_tokens = list(pygments.lex(expression['recognized_expression'], lexer))
    for token_type, token in rec_expression_tokens:
        token_type = str(token_type)
        if token_type in token_type_occurrences:
            token_type_occurrences[token_type] -= 1
            if token != ' ' and token != '':
                closest_token = max(tokens.keys(), key=lambda x: ratio(x, token))
                # closest_token = max(tokens.keys(), key=lambda x: SequenceMatcher(None, x, token).ratio())
                tokens[closest_token]['errors'].append(token)
    for token_type, value in token_type_occurrences.items():
        if value > 0:
            if token_type not in errors_per_type:
                errors_per_type[token_type] = 0
            errors_per_type[token_type] += value
    return errors_per_type, tokens, errors_per_token


def do_compute_occurrences_dict(folders, out_file):
    for folder in folders:
        matches = json.load(open(folder + "/matches.json"))
        pool = Pool()
        result = pool.map(parse_expression, matches)
        errors_per_type, tokens, errors_per_token = map(list, zip(*result))
        _t = {}
        for t in tokens:
            for key, value in t.items():
                if key not in _t:
                    _t[key] = {
                        'errors': [],
                        'type': value['type']
                    }
                    _t[key]['errors'] = list(filter(lambda x: x != key, value['errors']))
                else:
                    _t[key]['errors'].extend(filter(lambda x: x != key, value['errors']))
        tokens = _t
        tttt = {}
        for key in list(tokens.keys()):
            if len(tokens[key]['errors']) == 0:
                del tokens[key]
                continue
            _type = tokens[key]['type']
            if _type not in tttt:
                tttt[_type] = []
            tttt[_type].append({
                'key': key,
                'errors':  len(tokens[key]['errors'])
            })

        for _type in tttt:
            types, performance = list(zip(*[(x['key'], x['errors']) for x in tttt[_type]]))
            types = [x.replace("$", "\$") for x in list(types)]
            types, performance = list(zip(*list(sorted(zip(types, performance), key=lambda x: x[1], reverse=True))[:MAX_ELEMENTS]))
            plt.rcdefaults()
            fig, ax = plt.subplots()
            y_pos = np.arange(len(types))
            ax.barh(y_pos, performance, align='center')
            ax.set_yticks(y_pos)
            ax.set_yticklabels(types)
            ax.invert_yaxis()
            ax.set_xlabel('Missing tokens in type ' + _type)
            plt.savefig(folder + "/" + "type_" + _type + "_" + out_file, bbox_inches="tight")



p1 = Process(target=do_compute_occurrences_dict, args=(computer_like_typographies, "computer_missing_tokens.png"))
p1.start()
p2 = Process(target=do_compute_occurrences_dict, args=(handwritten_like_typographies, "handwritten_missing_tokens.png"))
#p2 = Process(target=do_compute_occurrences_dict, args=(["UbuntuRegular", "NoteThis"], "handwritten_missing_tokens.png"))
p2.start()
p2.join()
p1.join()
#do_compute_occurrences_dict(computer_like_typographies, "expressions_computer_like_typographies_occurrences_dict.json")
#do_compute_occurrences_dict(handwritten_like_typographies, "expressions_handwritten_like_typographies_occurrences_dict.json")
#do_compute_occurrences_dict(typography_folders, "expressions_all_typographies_occurrences_dict.json")