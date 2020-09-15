import json
import os
import subprocess
from utils import delete_chars
import pyprind

if os.path.isfile("loaded_no_duplicated_filtered_expressions.json"):
    print("Skipping expression loading into USE as 'loaded_no_duplicated_filtered_expressions.json' file already exists")
    exit()

print("Loading exprssions into USE... (this may take a while, please, be patient)")

temp_file = "temp/MM.use"
expressions = json.load(open("filtered_expressions.json"))

conversion_errors = 0
parsing_errors = 0
valid_expressions = []


def load_expression_in_use(mm_path, expression):
    global parsing_errors, conversion_errors
    if os.path.isfile(temp_file):
        os.system("rm " + temp_file)
    a = os.system('./ecore2use.sh "%s" 2> /dev/null' % mm_path)
    if os.path.isfile(temp_file):
        with open(temp_file, "a") as f:
            f.write("\nconstraints\n%s" % expression)
        try:
            result = subprocess.check_output('use-5.2.0/bin/use -c "%s" 2> /dev/null' % temp_file, shell=True)
            return True
        except subprocess.CalledProcessError:
            parsing_errors += 1
            return False
    else:
        conversion_errors += 1
        return False

bar = pyprind.ProgBar(len(expressions), track_time=True, title='Filtering out invalid expressions', bar_char='█', update_interval=1.)
for i, item in enumerate(expressions):
    gt_expression = delete_chars("context %s\ninv %s:\n%s" % (item['context'], item['inv'], item['expression']))
    if load_expression_in_use(item['file'], gt_expression):
        valid_expressions.append(i)
    bar.update()
print("%s parsing errors" % len(valid_expressions))
valid_expressions = [expressions[i] for i in valid_expressions]

print("%s conversion errors" % conversion_errors)
print("%s parsing errors" % parsing_errors)

no_duplicates = {}
duplicates_list = []

for i, expression in enumerate(valid_expressions):
    no_duplicate_key = expression['context'] + "-###-" + expression['inv']
    if no_duplicate_key not in no_duplicates:
        no_duplicates[no_duplicate_key] = expression
    else:
        duplicates_list.append(expression)

new_expressions = list(no_duplicates.values())
json.dump(new_expressions, open("loaded_no_duplicated_filtered_expressions.json", "w"))

print("%s duplicated expressions" % len(duplicates_list))


