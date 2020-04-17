# encoding: UTF-8

import unicodedata

with open("data.txt") as f:
    lines = f.readlines()

WRITING_SYSTEM_NAMES = ["Hudum", "Todo", "Sibe", "Manchu"]

data = {
    "Hudum":  [],
    "Todo":   [],
    "Sibe":   [],
    "Manchu": [],
}
for line in lines:
    id, usage = line.strip().split()[:2]
    codepoint = int(id) + 0x1800
    for i, digit in enumerate(usage):
        if int(digit):
            data[WRITING_SYSTEM_NAMES[i]].append(codepoint)

def make_unicode_scalar(codepoint):
    return "U+" + hex(codepoint)[2:].upper()

for writing_system_name in WRITING_SYSTEM_NAMES:
    codepoints = data[writing_system_name]
    ranges = []
    temp = []
    for c in codepoints:
        if temp:
            if c - temp[-1] == 1:
                temp.append(c)
            else:
                if len(temp) < 3:
                    ranges.extend(make_unicode_scalar(i) for i in temp)
                else:
                    ranges.append(make_unicode_scalar(temp[0]) + ".." + make_unicode_scalar(temp[-1]))
                temp.clear()
                temp.append(c)
        else:
            temp.append(c)
    else:
        if len(temp) < 3:
            ranges.extend(make_unicode_scalar(i) for i in temp)
        else:
            ranges.append(make_unicode_scalar(temp[0]) + ".." + make_unicode_scalar(temp[-1]))
    print(", ".join(ranges))

for codepoint in range(0x1820, 0x1877 + 1):
    row = [
        make_unicode_scalar(codepoint) +
        " " +
        " ".join(
            i.capitalize() for i in
            unicodedata.name(chr(codepoint)).replace("MONGOLIAN LETTER ", "").split()
        )
    ]
    for writing_system_name in WRITING_SYSTEM_NAMES:
        if codepoint in data[writing_system_name]:
            row.append("•")
        else:
            row.append("")
    print("\t".join(row))

# U+1820..U+1842
# U+1820, U+1828, U+182F..U+1831, U+1834, U+1837, U+1838, U+183A, U+183B, U+1840, U+1843..U+185C
# U+1820, U+1823, U+1828, U+182A, U+182E..U+1830, U+1834, U+1836..U+1838, U+183A, U+185D..U+1872
# U+1820, U+1823, U+1828..U+182A, U+182E..U+1830, U+1834..U+1836, U+1838, U+183A, U+185D, U+185F..U+1861, U+1864..U+1869, U+186C..U+1871, U+1873..U+1877
