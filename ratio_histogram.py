import matplotlib.pyplot as plt
import numpy as np
import json
from PIL import Image
import sys

out_path = sys.argv[1]

ratios = ["ratio", "fuzzy_ratio", "lev_ratio"]

for ratio in ratios:
    matches = json.load(open(out_path + "/matches.json"))
    a = [x[ratio] for x in matches]
    # An "interface" to matplotlib.axes.Axes.hist() method
    n, bins, patches = plt.hist(x=a, bins=16, alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel(ratio)
    #plt.yscale('log')
    #plt.xscale('log')
    plt.ylabel('Expressions')
    plt.title('Per expression match ratio')
    maxfreq = n.max()
    # Set a clean upper y-axis limit.
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    plt.xlim(xmin=0, xmax=1)
    plt.savefig(out_path + '/%s.png' % ratio)
    plt.clf()
    # Poor match in regular expressions
    # Filter images from regular expressions with: '.matches(' not in x['gt_expression']
    """
    for match in filter(lambda x: x[ratio] < 0.2 and '.matches(' not in x['gt_expression'], matches):
        Image.open(out_path + '/images/%d.png' % match['id']).show()
        print(match)
    """
