from PIL import Image, ImageDraw, ImageFont
import json
from multiprocessing import Pool
import re
import sys
import os

out_path = sys.argv[1]
font_path = sys.argv[2]

font = ImageFont.truetype(font_path, size=20)

def text_wrap(text, font, max_width):
    lines = []

    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        regexp = "[ =()[\]{}>\n]"
        l = re.findall(regexp, text)
        l.append("")
        words = [x+y for x,y in zip(re.split(regexp, text), l)]
        i = 0
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i]
                i += 1
                if '\n' in words[i-1]:
                    break
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines


def do_create_image_from_expression(expression, file_name, padding=20):
    if os.path.isfile(file_name):
        #print("%s already exists" % file_name)
        return
    expression = expression.replace("\r", "")
    img = Image.new('RGB', (1680, 1050), (255, 255, 255))
    text = expression
    lines = text_wrap(text, font, img.size[0] - padding)
    line_height = font.getsize('hg')[1]

    draw = ImageDraw.Draw(img)
    x = padding
    y = padding
    for line in lines:
        draw.text((x, y), line, fill=(0,0,0), font=font)
        y = y + line_height
    img.save(file_name)

i = 0

pool = Pool()
for item in json.load(open("loaded_no_duplicated_filtered_expressions.json")):
    pool.apply_async(do_create_image_from_expression,
                     args=("context %s\ninv %s:\n%s" % (item['context'], item['inv'], item['expression']), out_path + "/images/%d.png" % i),
                     error_callback=lambda x: print(x))
    i+=1
pool.close()
pool.join()