from collections import OrderedDict, defaultdict
import unicodedata

LETTER_NAME_TO_CODE_POINT = OrderedDict()
with open("data/phonetic-letters.txt") as f:
    for line in f.readlines():
        letter_name, code_point = line.strip().split(", ")[:2]
        LETTER_NAME_TO_CODE_POINT[letter_name] = code_point

LETTER_NAME_TO_VARIANT_GROUPS = defaultdict(list)
with open("data/variant-set/draft-utn.txt") as f:
    for line in f.readlines():
        line = line.strip()
        if line:
            letter_name, _, rest = line.partition(": ")
            variants = [field[1:] for field in rest.split()]
            LETTER_NAME_TO_VARIANT_GROUPS[letter_name].append(variants)

with open("data/Mongolian_Written_Forms.txt", "w") as f:
    for letter_name, code_point in LETTER_NAME_TO_CODE_POINT.items():
        character_name = unicodedata.name(chr(int(code_point, 16)))
        for i, variant_group in enumerate(LETTER_NAME_TO_VARIANT_GROUPS[letter_name]):
            fields = [code_point]
            fields.append(str(i + 1))
            fields.extend(" ".join(variant).ljust(5) for variant in variant_group)
            f.write(" ; ".join(fields) + " # " + character_name + "\n")
