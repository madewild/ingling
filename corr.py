"""Automated testing of patterns"""

import json
import os
import sys

import spacy
from spacy.matcher import Matcher

SESS = sys.argv[1]

def match_pattern(spacy_model, pattern):
    """Take a pattern as input and return matches (with longest match)"""
    res = set()
    nlp = spacy.load(spacy_model)
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)
    matcher.add("", pattern)
    matches = matcher(doc)
    spans = [doc[start:end] for _, start, end in matches]
    for span in spacy.util.filter_spans(spans):
        match_string = str(span).lower()
        res.add(match_string)
    return res

text = open("data/test.txt", encoding="utf-8").read()
models = ["fr_core_news_sm", "fr_core_news_md", "fr_core_news_lg", "fr_dep_news_trf"]
models = models[-1:]

root = f"data/2023/sess{SESS}/"
folders = os.listdir(root)
print(f"\n{len(folders)} assignments found\n")
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
        try:
            patterns = json.loads(json_file)
        except json.decoder.JSONDecodeError:
            print(f"No valid JSON file for {student}, skipping")
            continue
        scores = []
        for model in models:
            results = match_pattern(model, patterns)
            expected = [l.strip() for l in open("data/gold.txt", encoding="utf-8").readlines()]
            score = 0
            for phrase in expected:
                if phrase in results:
                    score += 1
            scores.append(score)
        #print(scores)
        max_score = max(scores)
        print(f"{student}: {max_score}/20")
            #print(results)
