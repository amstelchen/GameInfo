import os, vdf
from os import listdir
from os.path import isfile, join
from time import perf_counter, perf_counter_ns

from pathlib import Path
import hashlib

from .AppDebug import AppDebug

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096*32), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def mag(fname) -> str:
    with open(fname, "rb") as f:
        magic = f.read(2)

        #return str(magic) #.decode()
        if magic == b"MZ":
            f.seek(0x3c)
            offset = f.read(2)
            #print(int.from_bytes(offset, byteorder="little"))
            f.seek(int.from_bytes(offset, byteorder="little"))
            magic_pe = f.read(2)
            if magic_pe in [b"PE", b"PE"]:
                #return str(magic_pe)
                return "Win(PE)"
            #return str(magic)
            return "DOS(MZ)"

AppList = {
    "b716adaedab07867672624f740076336": ("Dune (1992)", "DUNEPRG.EXE"),
    "8b650651e6c6d5bfd8199da68fccddfa": ("Dune II - The Battle for Arrakis (EU - German French English) v1.07", "DUNE2.EXE"),
    "fa7b8727ae77bdc93dbb98e72aeb5471": ("Dune II - The Building Of A Dynasty (US - English) 1.00", "DUNE2.EXE"),
    "32cc6dc9e5030e9544467f797154c8c5": ("Dune II - The Building Of A Dynasty (US - English) 1.07", "DUNE2.EXE"),
    "29d208b962fa6775e346ec7041aa4feb": ("Dune II - The Building Of A Dynasty (US - English) 1.07 MrFlibble's Fix", "DUNE2.EXE"),
    "9e3dfe97aa04341d599b79f2848903cb": ("Dune II - The Battle for Arrakis (HS - German French English) v1.07", "DUNE2.EXE"),
    "83788ba8c811dfca1466b37ef042fc1b": ("Dune II - DEMO-KY", "DUNE2.EXE"),
    "a0024690f8c3c37c674d6aa21a43f034": ("Dune II - DEMO", "DUNE2.EXE"),
    "da98004761fb9d7994b3b85410c97439": ("Dune II - DuneX v1.29", "DUNEX.EXE", "da98004761fb9d7994b3b85410c97439"),
    "2852b50199881f28d587a444410d0aa4": ("DuneX Setup", "DXSETUP.EXE"),
    "d96391ae20135a7fb259ccb257b036e1": ("Dune 2000", "DUNE2000.orig.EXE"),
    "966bfcdf51573e9c4b2d15d0bf310f3a": ("Dune 2000", "dune2000.exe"),
    "a204548ec3ec34c7787dc12f0527575f": ("Emperor: Battle for Dune - no patch", "EMPEROR.EXE"),
    "31e8ec05a73df18f0b913522a64872fb": ("Emperor: Battle for Dune - v1.09", "EMPEROR.EXE"),
    "1605220":                          ("Dune: Spice Wars", "D4X.exe"),
    "5959bd19fee84a35edbb567f76d7d8d7": ("Super Dune II: Classic Edition", "SUPER.EXE"),
    "bc49be614c9daacba903105082f98ffb": ("Arrakis v1.13 by Stefan Hendriks", "arrakis.exe"),
    "1172710":                          ("Dune: Awakening", "D5X.exe")
}

all_exe_files = []

def DuneFiles(foldersPath):
    returnString = ""
    all_exe_files = [f for f in foldersPath.glob('**/*.[Ee][Xx][Ee]') if f.is_file()]
    #print(all_exe_files)
    for file in all_exe_files:
        for app_num, fields in AppList.items():
            if os.path.basename(file) == fields[1]:
                magic = mag(file)
                timestamp_start = perf_counter_ns()
                md5sum = md5(file)
                timestamp_stop = perf_counter_ns()
                if app_num == md5sum or app_num == "1605220" or app_num == "1172710":
                    #print(file, fields[0], fields[1], md5sum) # os.path.basename(file)
                    returnString += f"{magic} {md5sum} {file.stat().st_size:>9,d} {file.stem + '' + file.suffix:22s}={fields[0]}\n" # {(timestamp_stop - timestamp_start):1.3f} "
                    AppDebug.debug_print(f'{file}: md5sum took {(timestamp_stop - timestamp_start) / 1e6:1.3f}ms')
                    #returnString += "\n"
    return returnString

def DuneInfo():
    returnString = "" 

    foldersPath = Path(os.path.expanduser('~/Spiele'))
    #print(foldersPath)
    returnString += str(foldersPath) + "\n"
    returnString += DuneFiles(foldersPath)

    foldersPath = Path(os.path.expanduser('~/Downloads'))
    #print(foldersPath)
    #DoomWads(foldersPath)

    foldersPath = Path(os.path.expanduser('~/.config/gzdoom'))
    #print(foldersPath)
    #DoomWads(foldersPath)

    libraryfoldersPath = os.path.expanduser('~/.steam/steam/config/libraryfolders.vdf')
        #try:
    d = vdf.parse(open(libraryfoldersPath))
        #returnString += "\nSteam library folders:=\n"
    countApps = int(0)
    sizeApps = 0
    for folder in d['libraryfolders']:
        if folder == "contentstatsid":
            continue
        totalSize = int(d['libraryfolders'][folder]['totalsize'])
        folderPath = d['libraryfolders'][folder]['path']
        dictApps = d['libraryfolders'][folder]['apps']
        for AppID in dictApps:
            if "1605220" in AppID:
                AppPath = os.path.join(folderPath, "steamapps/common")
                AppPathGame = os.path.join(AppPath, "D4X")
                AppDebug.debug_print(AppPathGame)
                returnString += AppPathGame + "\n"
                foldersPath = Path(AppPathGame)
                returnString += DuneFiles(foldersPath)
            if "1172710" in AppID:
                AppPath = os.path.join(folderPath, "steamapps/common")
                AppPathGame = os.path.join(AppPath, "Dune Awakening")
                AppDebug.debug_print(AppPathGame)
                returnString += AppPathGame + "\n"
                foldersPath = Path(AppPathGame)
                returnString += DuneFiles(foldersPath)
    return returnString
