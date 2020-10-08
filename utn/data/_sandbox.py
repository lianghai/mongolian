from fontTools import unicodedata
import yaml

# with open("phonetic-letters.txt") as f:
#     lines = f.read().splitlines()

# with open("characters.yaml", "w") as f:
#     for line in lines:
#         single_letter_transcription, code_point, ascii_transcription = line.split(", ")
#         character = chr(int(code_point, 16))
#         f.write(f"0x{code_point}: # {character} {unicodedata.name(character)}\n")
#         f.write(f"  ascii_transcription: \"{ascii_transcription}\"\n")
#         if single_letter_transcription != ascii_transcription:
#             f.write(f"  single_letter_transcription: \"{single_letter_transcription}\"\n")

with open("characters.yaml") as f:
    data = yaml.load(f)

for code_point, properties in data.items():
    ascii_transcription = properties["ascii_transcription"]
    # print(f"case {ascii_transcription}(JoiningForm?, [WrittenUnit]?)")
    # print(f"case {ascii_transcription} = \"\\u{{{hex(code_point)[2:].upper()}}}\"")
    # print(f"{ascii_transcription} = 0x{hex(code_point)[2:].upper()}", end=", ")
    print(f"{ascii_transcription}", end=", ")

# with open("written-units.txt") as f:
#     lines = f.read().splitlines()

# with open("-written-units.yaml", "w") as f:
#     for line in lines:
#         single_letter_transcription, *tail = line.split("\t")
#         if tail:
#             ascii_transcription = tail[0]
#         else:
#             ascii_transcription = single_letter_transcription
#         f.write(f"\"{ascii_transcription}\":\n")
#         if ascii_transcription != single_letter_transcription:
#             f.write(f"  single_letter_transcription: \"{single_letter_transcription}\"\n")

# for line in lines:
#     single_letter_transcription, *tail = line.split("\t")
#     if tail:
#         ascii_transcription = tail[0]
#     else:
#         ascii_transcription = single_letter_transcription
#     print(f"{ascii_transcription}, ", end="")
