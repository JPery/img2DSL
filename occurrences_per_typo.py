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

lexer = OCLLexer()
formatter = TerminalFormatter()

def parse_expression(expression):
    token_type_occurrences = {}
    token_occurrences = {}
    errors_per_type = {}
    errors_per_token = {}
    tokens = {}
    gt_expression_tokens = list(pygments.lex(expression['gt_expression'], lexer))
    for token_type, token in gt_expression_tokens:
        token_type = str(token_type)
        if token_type not in token_type_occurrences:
            token_type_occurrences[token_type] = 0
        if token_type != 'Token.Literal.String' and 'Token.Comment' not in token_type:
            if token not in token_occurrences:
                token_occurrences[token] = 0
            token_occurrences[token] += 1
        token_type_occurrences[token_type] += 1
        if token not in tokens:
            tokens[token]  ={}
            tokens[token]['errors'] = []
            tokens[token]['type'] = token_type
    rec_expression_tokens = list(pygments.lex(expression['recognized_expression'], lexer))
    for token_type, token in rec_expression_tokens:
        token_type = str(token_type)
        if token_type not in token_type_occurrences:
            token_type_occurrences[token_type] = 0
        token_type_occurrences[token_type] -= 1
        if token in token_occurrences:
            token_occurrences[token] -= 1
        if token != ' ' and token != '':
            closest_token = max(tokens.keys(), key=lambda x: ratio(x, token))
            # closest_token = max(tokens.keys(), key=lambda x: SequenceMatcher(None, x, token).ratio())
            tokens[closest_token]['errors'].append(token)
    for token_type, value in token_type_occurrences.items():
        if value > 0:
            if token_type not in errors_per_type:
                errors_per_type[token_type] = 0
            errors_per_type[token_type] += value
    for token, value in token_occurrences.items():
        if value > 0:
            if token not in errors_per_token:
                errors_per_token[token] = 0
            errors_per_token[token] += value
    return errors_per_type, tokens, errors_per_token


def do_compute_occurrences_dict(folders, out_file):
    total_errors_per_type = {}
    for folder in folders:
        matches = json.load(open(folder + "/matches.json"))
        pool = Pool()
        result = pool.map(parse_expression, matches)
        errors_per_type, tokens, errors_per_token = map(list, zip(*result))
        _e = {}
        for e in errors_per_type:
            for key, value in e.items():
                if key not in _e:
                    _e[key] = value
                else:
                    _e[key] += value
        errors_per_type = _e
        _e = {}
        for e in errors_per_token:
            for key, value in e.items():
                if key not in _e:
                    _e[key] = value
                else:
                    _e[key] += value
        errors_per_token = _e
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
        for key in list(tokens.keys()):
            if len(tokens[key]['errors']) == 0:
                del tokens[key]

        token_types = list(errors_per_type.keys())
        y_pos = np.arange(len(token_types))
        performance = list(errors_per_type.values())
        _tokens, performance = zip(*sorted(zip(token_types, performance), key=lambda x: x[1], reverse=True))
        json.dump(tokens, open(folder + "_tokens.json", "w"))
        plt.rcdefaults()
        fig, ax = plt.subplots()
        ax.barh(y_pos, performance, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(token_types)
        ax.invert_yaxis()
        ax.set_xlabel('Missing token types')
        plt.savefig(folder + "/" + "per_type_" + out_file, bbox_inches="tight")

        MAX_ELEMENTS = 20
        _tokens = [x.replace("$", "\$") for x in list(errors_per_token.keys())][:MAX_ELEMENTS]
        y_pos = np.arange(len(_tokens))
        performance = list(errors_per_token.values())[:MAX_ELEMENTS]
        _tokens, performance = zip(*sorted(zip(_tokens, performance), key=lambda x: x[1], reverse=True))
        #json.dump(tokens, open(folder + "_tokens.json", "w"))
        plt.rcdefaults()
        fig, ax = plt.subplots()
        ax.barh(y_pos, performance, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(_tokens)
        ax.invert_yaxis()
        ax.set_xlabel('Missing tokens')
        plt.savefig(folder + "/" + "per_token_" + out_file, bbox_inches="tight")

    token_types = list(total_errors_per_type.keys())
    y_pos = np.arange(len(token_types))
    performance = list(total_errors_per_type.values())

    plt.rcdefaults()
    fig, ax = plt.subplots()
    ax.barh(y_pos, performance, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(token_types)
    ax.invert_yaxis()
    ax.set_xlabel('Missing tokens')
    plt.savefig(out_file, bbox_inches="tight")


p1 = Process(target=do_compute_occurrences_dict, args=(computer_like_typographies, "computer_missing_tokens.png"))
p1.start()
p2 = Process(target=do_compute_occurrences_dict, args=(handwritten_like_typographies, "handwritten_missing_tokens.png"))
p2.start()
p2.join()
p1.join()
#do_compute_occurrences_dict(computer_like_typographies, "expressions_computer_like_typographies_occurrences_dict.json")
#do_compute_occurrences_dict(handwritten_like_typographies, "expressions_handwritten_like_typographies_occurrences_dict.json")
#do_compute_occurrences_dict(typography_folders, "expressions_all_typographies_occurrences_dict.json")