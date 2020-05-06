import re
from ftfy import fix_encoding

chars = {
     "\n": " ",
     "\r": "",
     "\t": " ",
     "\u2018": "'",
     "\u2019": "'",
}

def remove_whitespaces(a):
    return re.sub(" +", " ", a)

def delete_chars(a):
    b = fix_encoding(remove_whitespaces(a))
    for char_to_replace, replace in chars.items():
        b = b.replace(char_to_replace, replace)
    return b

discarded_typographies = [
    "AmaticBold",
    "AmaticRegular",
    "PatrickHandSC",
    "Permanent",
    "RockSalt",
]

handwritten_like_typographies = [
    "DancingScriptBold",
    "DancingScriptRegular",
    "DancingScriptVariable",
    "DeliusSwash",
    "Desyrel",
    "GloriaHallelujah",
    "Handlee",
    "IndieFlower",
    "KalamBold",
    "KalamLight",
    "KalamRegular",
    "Lilly",
    "MarckScript",
    "NoteThis",
    "PatrickHand",
    "Playtime",
    "PlaytimeOblique",
    "ShadowsIntoLight",
    "SueEllenFrancisco",
]

computer_like_typographies = [
    "CourierPrimeBold",
    "CourierPrimeRegular",
    "DejavuMonoSans",
    "DejavuSerif",
    "RobotoItalic",
    "RobotoMedium",
    "RobotoRegular",
    "UbuntuMono",
    "UbuntuRegular"
]

typography_folders = computer_like_typographies.copy()
typography_folders.extend(handwritten_like_typographies)
