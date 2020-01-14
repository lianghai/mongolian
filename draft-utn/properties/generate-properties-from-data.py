import unicodedata, zipfile
from collections import OrderedDict, defaultdict

LETTER_NAME_TO_CODE_POINT = OrderedDict()
with open("../data/phonetic-letters.txt") as f:
    for line in f.read().splitlines():
        letter_name, code_point = line.partition("  # ")[0].split(", ")[:2]
        LETTER_NAME_TO_CODE_POINT[letter_name] = code_point

LETTER_NAME_TO_VARIANT_GROUPS = defaultdict(list)
with open("../data/variants.txt") as f:
    for line in f.readlines():
        line = line.strip()
        if line:
            letter_name, _, rest = line.partition(": ")
            variants = [field[1:] for field in rest.split()]
            LETTER_NAME_TO_VARIANT_GROUPS[letter_name].append(variants)

with open("./Mongolian_Written_Forms.txt", "w") as f:
    for letter_name, code_point in sorted(
        LETTER_NAME_TO_CODE_POINT.items(),
        key=lambda x: int(x[1], 16),
    ):
        character_name = unicodedata.name(chr(int(code_point, 16)))
        for i, variant_group in enumerate(LETTER_NAME_TO_VARIANT_GROUPS[letter_name]):
            fields = [code_point]
            fields.append(str(i + 1))
            fields.extend(" ".join(variant).ljust(5) for variant in variant_group)
            f.write(" ; ".join(fields) + " # " + character_name + "\n")

with zipfile.ZipFile("properties.zip", "w", compression=zipfile.ZIP_DEFLATED) as f:
    for filename in [
        "Mongolian_Syllabic_Category.txt",
        "Mongolian_Written_Forms.txt",
    ]:
        f.write(filename)
