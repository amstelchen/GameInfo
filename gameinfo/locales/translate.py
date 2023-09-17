#!/usr/bin/env python3

import os, re, sys
import subprocess

if len(sys.argv) < 3:
    print("Argument(s) missing.\nUsage: " + os.path.basename(__file__) + " [language] [domain]")
    exit()
lang = sys.argv[1]
domain = sys.argv[2]
file = os.path.join(os.path.dirname(__file__), lang, "LC_MESSAGES", domain + ".po")
# i.e. "quickconvert.desktop"

os.system("clear")

with open(file, "r") as f:
    print(file)
    for line in f.readlines():
        if line.startswith("msgid"):
            orig = line.strip().replace("msgid ", "")
            if orig == "":
                continue
            print("msgid " + orig + "")
            result = subprocess.run(["trans", "-b", ":" + lang, "\"" + orig.strip() + "\""],
                stdout=subprocess.PIPE, text=True, check=True)
            print("msgstr \"" + result.stdout.strip().replace("\"\"", "") + "\"") #.decode("utf-8"))
