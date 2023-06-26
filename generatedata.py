from scripts.source2cfg import getCPGfromSourceFiles
from scripts.cfg2json import getCPG2DotFiles, getJsonFromDotFolder
import subprocess
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('lang', type=str, help="Language")


args = parser.parse_args()
lang = args.lang
code_path = "/home/anonymous/PycharmProjects/thesisPractical/codes/"
cpg = f"{code_path}-cpg"
cpgs2dot = f"{code_path}-dot"
temp = f"{code_path}-temp"
dot2json = f"{code_path}-json"
json2rep = f"{code_path}-graphrepr"
getCPGfromSourceFiles(code_path, cpg,lang=f"{lang}")

getCPG2DotFiles(cpg, cpgs2dot, temp, processes=40, lang=f"{lang}")

getJsonFromDotFolder(cpgs2dot,dot2json)

subprocess.run(["python", f"/home/anonymous/PycharmProjects/thesisPractical/graph2vec/src/graph2vec.py", "--input-path", f"{dot2json}", "--output-path", f"{json2rep}", "--dimensions", "16", "--epochs", "32"])