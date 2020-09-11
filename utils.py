import re
import json
from ftfy import fix_encoding
from lxml import etree

chars = {
     "\n": " ",
     "\r": "",
     "\t": " ",
     "\u2018": "'",
     "\u2019": "'",
}

def apply_duplicated_filter(list_2_filter):
    filter_elements = json.load(open("no_duplicated_filter.json"))
    return [list_2_filter[i] for i in filter_elements]

def remove_whitespaces(a):
    return re.sub(" +", " ", a)

def delete_chars(a):
    b = fix_encoding(remove_whitespaces(a))
    for char_to_replace, replace in chars.items():
        b = b.replace(char_to_replace, replace)
    return b

def parse_metamodel_keywords(ecore_file):
    doc = etree.XML(open(ecore_file, "r").read().encode("utf8"))
    e = doc.findall('.//*[@name]')
    names = [x.attrib['name'] for x in e]
    return set(names)

discarded_typographies = [
    "AmaticBold",
    "AmaticRegular",
    "PatrickHandSC",
    "Permanent",
    "RockSalt",
]

handwritten_like_typographies = [
    "DeliusSwash",
    "Handlee"
]

computer_like_typographies = [
    "CourierPrimeBold",
    "CourierPrimeRegular",
    "DejavuMonoSans",
    "DejavuSerif",
    "RobotoMedium",
    "RobotoRegular",
    "UbuntuMono",
    "UbuntuRegular"
]

typography_folders = computer_like_typographies.copy()
typography_folders.extend(handwritten_like_typographies)
