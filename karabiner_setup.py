import json
import os

CONFIG_FILE = "~/.config/karabiner/karabiner.json"
TEMPLATE_FILE = "template.json"
PROFILE_NAME = "Windows Japanese"

KEYCONFIG_FILE = "keyconfig.txt"

MODIFIER_MAP = {
    "shift": "left_shift",
    "command": "left_command",
    "cotrol": "left_control",
    "option": "left_option",
    "s": "left_shift",
    "c": "left_command",
    "C": "left_ctrl",
    "o": "left_option",
}


def convert_key(k):
    a = k.split("+")
    if len(a) == 1:
        key_code = a[0]
        modifier = ""
    else:
        key_code = a[1]
        modifier = MODIFIER_MAP[a[0]]
    ret = {"key_code": key_code}
    if modifier:
        ret["modifiers"] = [modifier]
    return ret


def convert_rule(s):
    a = s.split()
    element = {
        "description": s,
        "manipulators": [
            {"from": convert_key(a[0]), "to": [convert_key(a[1])], "type": "basic"}
        ],
    }
    return element


def main():
    with open(os.path.expanduser(CONFIG_FILE)) as fp:
        config = json.load(fp)
    index_modified = None
    for i, prof in enumerate(config["profiles"]):
        if prof["name"] == PROFILE_NAME:
            index_modified = i
    if index_modified is None:
        index_modified = len(config["profiles"])
        with open(TEMPLATE_FILE) as fp:
            template = json.load(fp)
            config["profiles"].append(template)
    rules = []
    with open(KEYCONFIG_FILE) as fp:
        for line in fp:
            line = line.rstrip()
            if line != "":
                rules.append(convert_rule(line))
    config["rules"] = rules
    print(json.dumps(config, indent=4))


if __name__ == "__main__":
    main()
