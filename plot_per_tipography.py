import numpy as np
import json
import matplotlib.pyplot as plt
from utils import typography_folders, handwritten_like_typographies, computer_like_typographies


def do_plot(folders, out_file):
    lev_avgs = []
    lev_stddevs = []
    typographies = []
    for folder in folders:
        matches = json.load(open(folder + "/matches.json"))
        lev_avg = np.average([x['lev_ratio'] for x in matches])
        lev_stddev = np.std([x['lev_ratio'] for x in matches])
        typography_name = folder.rsplit("/", 1)[-1]
        typographies.append(typography_name)
        lev_avgs.append(lev_avg)
        lev_stddevs.append(lev_stddev)

    fig, ax = plt.subplots()
    for i, typo in enumerate(typographies):
        x = lev_avgs[i]
        y = lev_stddevs[i]
        ax.scatter(x, y, label=typo, alpha=0.5, edgecolors='none')
    chartBox = ax.get_position()
    ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.7, chartBox.height])
    ax.legend(loc='upper center', bbox_to_anchor=(1.7, 0.975), ncol=2)
    ax.grid(True)
    plt.title("Levensthein ratio")
    plt.ylabel('Std Dev')
    plt.xlabel('Avg')
    plt.savefig(out_file, bbox_inches="tight")

do_plot(computer_like_typographies, "computer_like_typographies_lev_ratio.png")
do_plot(handwritten_like_typographies, "handwritten_like_typographies_lev_ratio.png")
do_plot(typography_folders, "all_typographies_lev_ratio.png")