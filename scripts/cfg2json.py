import itertools
import json
import random
import shutil
JOERN_PATH = f"/home/anonymous/PycharmProjects/thesisPractical/joern/joern-cli/"
import pygraphviz
import subprocess
import os
from collections import deque
from scripts.source2cfg import recurseFolders
cpgs = "/home/anonymous/PycharmProjects/thesisPractical/codes/tuke-codes-cpg"
cpgs2dot = "/home/anonymous/PycharmProjects/thesisPractical/codes/tuke-codes-dot"
dot2json = "/home/anonymous/PycharmProjects/thesisPractical/codes/tuke-codes-json"
temp = "/home/anonymous/PycharmProjects/thesisPractical/codes/java-codes-temp"
def getCPG2DotFiles(ip, op, temp, lang="c", start=0, processes=20):
    pathlist = deque()
    recurseFolders(ip, pathlist)
    print(f"Total File Paths: {len(pathlist)}")
    print(pathlist[0])
    if not os.path.exists(temp):
        os.makedirs(temp)
    dot_file = "1-cpg.dot"
    if lang != "c":
        dot_file = "0-cpg.dot"
    queue = [x for x in range(processes)]
    plist = deque()
    count = 0

    file = None
    if not os.path.exists(op):
        os.makedirs(op)
    folder = None
    while len(pathlist):
        if len(plist) < processes:
            curr = pathlist.popleft()
            file = curr.split("/")[-1]
            folder = file.split(".")[0]
            id = queue.pop()
            if os.path.exists(f"{temp}/{id}"):
                shutil.rmtree(f"{temp}/{id}")
            plist.append([
                subprocess.Popen(
                    [f"{JOERN_PATH}/joern-export", f"{curr}", "--format=dot", "-o", f"{temp}/{id}/"]),id])
            count += 1
            if len(plist) == processes:
                print(f"Files processed {count}", "\n")
        else:
            plist[0][0].wait()
            if os.path.exists(f"{temp}/{plist[0][1]}/{dot_file}"):
                    shutil.copy(f"{temp}/{plist[0][1]}/{dot_file}", f"{op}/{folder}.{count}{dot_file}")
            queue.append(plist[0][1])
            plist.popleft()

def getJsonfromDot(fileName, inP, outP):
    if not os.path.exists(outP):
        os.makedirs(outP)
    try:
        G = pygraphviz.AGraph(inP)
    except:
        return
    print(G.name)
    if G.number_of_nodes() <= 2 or G.number_of_edges() <= 2:
        return
    toJson = {
        "edges": [],
        "features": {}
    }
    cur = 0
    node2index = {}
    index2degree = {}
    indSet = set()
    for i in G.nodes():
        node2index[i] = cur
        cur += 1

    for j in G.edges():
        inE = node2index.get(j[0])
        outE = node2index.get(j[1])
        indSet.add(inE)
        indSet.add(outE)
        toJson["edges"].append([inE, outE])
        index2degree[inE] = index2degree.get(inE, 0) + 1
        index2degree[outE] = index2degree.get(outE, 0) + 1

    for y in indSet:
        toJson["features"][str(y)] = str(index2degree.get(y, 0))
    open(f"{outP}/{fileName}.{G.name}.{str(random.randint(100000,999900))}.json","w").write(json.dumps(toJson))
# def getJsonfromCFG(inP, outP):
#     cfgList = deque()
#     recurseFolders(inP, cfgList)
#     if not os.path.exists(outP):
#         os.makedirs(outP)
#     for e in cfgList:
#         G = pygraphviz.AGraph(f"{e[0]}")
#         if G.number_of_nodes() <= 2 or G.number_of_edges() <= 2:
#             continue
#         toJson = {
#             "edges": [],
#             "features": {}
#         }
#         cur = 0
#         node2index = {}
#         index2degree = {}
#         objJson = json.loads(json.dumps(toJson))
#         indSet = set()
#         for i in G.nodes():
#             node2index[i] = cur
#             cur += 1

#         for j in G.edges():
#             inE = node2index.get(j[0])
#             outE = node2index.get(j[1])
#             indSet.add(inE)
#             indSet.add(outE)
#             objJson["edges"].append([inE, outE])
#             index2degree[inE] = index2degree.get(inE, 0) + 1
#             index2degree[outE] = index2degree.get(outE, 0) + 1

#         for y in indSet:
#             objJson["features"][str(y)] = str(index2degree.get(y, 0))
#         objJson = str(objJson).replace("'", '"')
#         open(f"{outP}/{str(random.randint(1000,9999))}.json","w").write(objJson)
def getJsonFromDotFolder(path, output):
    pathlist = deque()
    recurseFolders(path, pathlist)
    print(f"Total File Paths: {len(pathlist)}")
    for i in pathlist:
        getJsonfromDot(i.split("/")[-1],f"{i}",output)
