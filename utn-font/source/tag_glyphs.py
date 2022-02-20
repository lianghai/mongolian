from pathlib import Path

from data import script

scripting_dir = Path(__file__).parent

for line in (scripting_dir / "glyph-names.txt").read_text().splitlines():

    # body, _, tail = line.partition(".")
    # cp_notation = body[3:]
    # cp_ints = [int(cp_notation[i:i+4], 16) for i in range(0, len(cp_notation), 4)]
    # phonetic_letters = "_".join(
    #     next(character for character in mongolian.characters.values() if character.cp == cp_int).id
    #     for cp_int in cp_ints
    # )
    # _, _, tail = tail.partition("_")
    # joining_form = ""
    # if tail:
    #     joining_form = {"0": "isol", "1": "init", "2": "medi", "3": "fina"}[tail[0]]
    # written_forms = ""
    # print(line, phonetic_letters, written_forms, joining_form, sep=";")

    eac_name, *parts = line.split("\t")

    print(f""""{eac_name}": "{".".join(parts)}",""")
