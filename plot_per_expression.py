import numpy as np
import json
import matplotlib.pyplot as plt
from utils import typography_folders, handwritten_like_typographies, computer_like_typographies


def do_plot(folders, out_file):
    expressions = {}
    for folder in folders:
        matches = json.load(open(folder + "/matches.json"))
        for expression in matches:
            if expression['id'] not in expressions:
                expressions[expression['id']] = {}
            if 'ratios' not in expressions[expression['id']]:
                expressions[expression['id']]['lev_ratios'] = []
            expressions[expression['id']]['lev_ratios'].append(expression['lev_ratio'])

    fig, ax = plt.subplots()
    for key, value in expressions.items():
        x = np.average(value['lev_ratios'])
        y = np.std(value['lev_ratios'])
        ax.scatter(x, y, label=key, alpha=0.5, edgecolors='none')
    ax.grid(True)
    plt.title("Per expression Levensthein ratio")
    plt.ylabel('Std Dev')
    plt.xlabel('Avg')
    plt.savefig(out_file, bbox_inches="tight")


do_plot(computer_like_typographies, "expressions_computer_like_typographies_lev_ratio.png")
do_plot(handwritten_like_typographies, "expressions_handwritten_like_typographies_lev_ratio.png")
do_plot(typography_folders, "expressions_all_typographies_lev_ratio.png")