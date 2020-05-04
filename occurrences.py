import numpy as np
import json
import matplotlib.pyplot as plt
from utils import typography_folders, handwritten_like_typographies, computer_like_typographies
import pygments
from pygments.formatters.terminal import TerminalFormatter
from OCLLexer import OCLLexer
from multiprocessing import Process

lexer = OCLLexer()
formatter = TerminalFormatter()

def do_compute_occurrences_dict(folders, out_file):
    expressions = {}
    for folder in folders:
        matches = json.load(open(folder + "/matches.json"))
        typography_name = folder.rsplit("/", 1)[-1]
        for expression in matches:
            if expression['id'] not in expressions:
                expressions[expression['id']] = {}
            expressions[expression['id']][typography_name] = {}
            rec_expression_tokens = list(pygments.lex(expression['recognized_expression'], lexer))
            gt_expression_tokens = list(pygments.lex(expression['gt_expression'], lexer))
            expressions[expression['id']][typography_name]['recognized_expression_tokens'] = rec_expression_tokens
            expressions[expression['id']][typography_name]['gt_expression_tokens'] = gt_expression_tokens
            expressions[expression['id']][typography_name]['recognized_expression_token_occurrences'] = {}
            expressions[expression['id']][typography_name]['gt_expression_token_occurrences'] = {}
            for token_type, token in rec_expression_tokens:
                token_type = str(token_type)
                if token_type not in expressions[expression['id']][typography_name]['recognized_expression_token_occurrences']:
                    expressions[expression['id']][typography_name]['recognized_expression_token_occurrences'][token_type] = 0
                expressions[expression['id']][typography_name]['recognized_expression_token_occurrences'][token_type] += 1
            for token_type, token in gt_expression_tokens:
                token_type = str(token_type)
                if token_type not in expressions[expression['id']][typography_name]['gt_expression_token_occurrences']:
                    expressions[expression['id']][typography_name]['gt_expression_token_occurrences'][token_type] = 0
                expressions[expression['id']][typography_name]['gt_expression_token_occurrences'][token_type] += 1
    json.dump(expressions, open(out_file, "w"))

p1 = Process(target=do_compute_occurrences_dict, args=(computer_like_typographies, "expressions_computer_like_typographies_occurrences_dict.json"))
p1.start()
p2 = Process(target=do_compute_occurrences_dict, args=(handwritten_like_typographies, "expressions_handwritten_like_typographies_occurrences_dict.json"))
p2.start()
p1.join()
p2.join()