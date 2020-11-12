import json

import yaml

for filename in ["written-units", "characters"]:
    with open(filename + ".yaml") as f:
        data = yaml.safe_load(f)
    with open(filename + ".json", "w") as f:
        json.dump(data, f, ensure_ascii=False)
