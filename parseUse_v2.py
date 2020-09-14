import json
import os
import subprocess
import sys
import pyprind

temp_file = "temp/MM.use"


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

font = sys.argv[1]

matches = json.load(open("%s/matches.json" % font))
bar = pyprind.ProgBar(len(matches), track_time=True, title='Loading expressions', bar_char='█', update_interval=1.)
for item in matches:
    if load_expression_in_use(item['file'], item['recognized_expression']):
        valid_expressions.append(item['id'])
    bar.update()
print("Valid expressions in '%s': %s" %(font, len(valid_expressions)))


