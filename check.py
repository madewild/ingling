"""Comparing files"""

import os
import sys
from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

SESS = sys.argv[1]

assignments = {}

for sess in range(int(SESS)):
    session = sess + 1
    root = f"data/2023/sess{session}/"
    folders = os.listdir(root)
    print(f"\n{len(folders)} assignments found for session {session}")
    for folder in sorted(folders):
        student = folder.split("_")[0]
        files = os.listdir(f"{root}{folder}")
        json_files = [f for f in files if f.endswith(".json")]
        if len(json_files) == 0:
            print(f"No JSON file found for {student}")
            sys.exit()
        elif len(json_files) > 1:
            print(f"More than one JSON file found for {student}")
            sys.exit()
        else:
            json_file = open(f"{root}{folder}/{json_files[0]}", encoding="utf-8").read()
            assignments[f"{student}-session{session}"] = json_file

for key1, value1 in assignments.items():
    for key2, value2 in assignments.items():
        if key2 != key1:
            if value1 == value2:
                print(f"{key1} is the same as {key2}!")
            else:
                simscore = similarity(value1, value2)
                if simscore > .6:
                    print(f"{key1} is very similar to {key2}")
