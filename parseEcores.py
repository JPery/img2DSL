import glob
import lxml.etree
import os
import json
import re

if os.path.isfile("filtered_expressions.json"):
    print("filtered_expressions file already exists")
    exit()


OCL_EXPRESSIONS = []

ecore_files = list(glob.glob("ocl-dataset/dataset/repos/**/*.ecore", recursive=True))

for ecore_file in ecore_files:
    if os.path.isfile(ecore_file):
        try:
            doc = lxml.etree.XML(open(ecore_file, "r").read().encode("utf8"))
            e=doc.findall('eClassifiers/eAnnotations/[@source="http://www.eclipse.org/emf/2002/Ecore/OCL/Pivot"]/details')

            for expression in e:
                context = expression.getparent().getparent().attrib['name'].strip()
                inv = expression.attrib['key'].strip()
                expression = re.sub("([\t\n ])+", " ", expression.attrib['value'].strip())
                OCL_EXPRESSIONS.append({
                                           'context': context,
                                           'inv': inv,
                                           'expression': expression,
                                           'file': ecore_file
                                       })
        except Exception as _e:
            pass

json.dump(OCL_EXPRESSIONS, open("filtered_expressions.json", "w"))
