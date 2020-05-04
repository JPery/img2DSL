import json
import os
import glob

# Test 1 -> Couldn't transform 698 ecores
# Test 2 -> Couldn't open 2991 use files

temp_file = "temp/MM.use"
expressions = json.load(open("expressions_v2.json"))

conversion_errors = 0
parsing_errors = 0
valid_expressions = []
for i in glob.glob("UbuntuMono/recognized_text/*.txt"):
    if os.path.isfile(temp_file):
        os.system("rm " + temp_file)
    print(i)
    expression_index = int(i.rsplit("/")[-1].rsplit(".")[0])
    item = expressions[expression_index]
    a = os.system('./ecore2use.sh "%s"' % item['file'])
    if os.path.isfile(temp_file):
        #with  open(temp_file, "a") as f:
        #    with open(i) as f2:
        #        text = f2.read()
        #        f.write("\nconstraints\n%s" % text)
        result = os.system("use-5.2.0/bin/use -c " + temp_file)
        if result:
            parsing_errors+=1
        else:
            valid_expressions.append(expression_index)
    else:
        conversion_errors+=1
        print("Couldn't convert to use")

json.dump(valid_expressions, open("valid_expressions.json", "w"))
print("Couldn't transform %d ecores" % conversion_errors)
print("Couldn't open %d use files" % parsing_errors)