import os
import shutil
from multiprocessing.pool import ThreadPool
import subprocess
import itertools
from collections import deque
JOERN_PATH = f"/home/anonymous/PycharmProjects/thesisPractical/joern/joern-cli/"


def recurseFolders(inPath, pathList):
    if inPath[-1] == '/':
        inPath = inPath[:-1]
    dirContent = os.listdir(inPath)
    if not dirContent:
        return
    for i in dirContent:
        newPath = inPath + f"/{i}"
        if os.path.isdir(newPath):
            recurseFolders(newPath, pathList)
        else:
            pathList.append(newPath)


def getCPGfromSourceFiles(inP, outP, start=0, processes=20, lang="c"):
    pathlist = deque()
    recurseFolders(inP, pathlist)
    if start:
        pathlist = deque(itertools.islice(pathlist, start))
    print(f"Total File Paths: {len(pathlist)}")
    if not os.path.exists(outP):
        os.makedirs(outP)
    plist = deque()
    count = start
    exe = "c2cpg.sh"
    if lang != "c":
        exe = "javasrc2cpg"
    while pathlist:
        if len(plist) < processes:
            curr = pathlist.popleft()
            file = curr.split("/")[-1]
            plist.append(
                subprocess.Popen([f"{JOERN_PATH}{exe}", "-J-Xmx80m", f"{curr}", "-o", f"{outP}/{file}.{count}.bin"]))
            count += 1
            if len(plist) == processes:
                print(f"Files processed {count}", "\n")
        else:
            plist[0].wait()
            if plist[0].returncode == 0:
                plist.popleft()
