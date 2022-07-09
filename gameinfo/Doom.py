import os, vdf
from os import listdir
from os.path import isfile, join
from time import perf_counter

from pathlib import Path
import hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096*32), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


AppList = {
    "2280": ("Ultimate Doom", "Doom.exe"),
    "2300": ("Doom 2", "Doom2.exe"),
    "9050": ("Doom 3", "Doom3.exe"),
    "9160": ("Master Levels of Doom", "Doom3.exe")
}

DoomFiles = {
    "f0cefca49926d00903cf57551d901abe": [ "Doom", "1.9", "Shareware", "February 2, 1995"],
    "1cd63c5ddff1bf8ce844237f580e9cf3": [ "Doom", "1.9", "Registered", "February 2, 1995"],
    "c4fe9fd920207691a9f493668e0a2083": [ "The Ultimate Doom", "1.9", "Retail", "May 25, 1995"],
    "573f3f178c76709f512089ed15484391": [ "John Romero's SIGIL (compat)", "1.21"],
    "743d6323cb2b9be24c258ff0fc350883": [ "John Romero's SIGIL", "1.21"],
    "8517c4e8f0eef90b82852667d345eb86": [ "Doom: Unity Edition", "", "", "September 3, 2019"],
    "8ab6d0527a29efdc1ef200e5687b5cae": [ "Doom: Unity Edition", "", "", "September 3, 2019"],
    "0c7caf25ad1584721ff5ecc38dec97a0": [ "Doom: Unity Edition extras.wad", "", "", "September 3, 2019"],
    "30e3c2d0350b67bfbf47271970b74b2f": [ "Doom II", "1.666", "August 29, 1994"],
    "d9153ced9fd5b898b36cc5844e35b520": [ "Doom II", "1.666", "(German)"],
    "ea74a47a791fdef2e9f2ea8b8a9da13b": [ "Doom II", "1.72", "September 21, 1994"],
    "d7a07e5d3f4625074312bc299d7ed33f": [ "Doom II", "1.7a", "October 18, 1994"],
    "c236745bb01d89bbb866c8fed81b6f8c": [ "Doom II", "1.8", "January 23, 1995"],
    "25e1459ca71d321525f84628f45ca8cd": [ "Doom II", "1.9", "February 2, 1995"],
    "75c8cf89566741fa9d22447604053bd7": [ "Final Doom (The Plutonia Experiment)", "1.9", "June 10, 1995"],
    "4e158d9953c79ccf97bd0663244cc6b6": [ "Final Doom (TNT: Evilution)", "1.9", "June 10, 1995"],
    "cb03fd0cd84b10579c2b2b313199d4c1": ("Master Levels for Doom II", "Attack"),
    "a421ca18cea00a2696162f8d2a2beeca": ("Master Levels for Doom II", "Black Tower", ""),
    "18eb4ffb3094ddb690e62211dc6169a1": ("Master Levels for Doom II", "Bloodsea Keep"),
    "33493942592d764e7787fb0ad7d03044": ("Master Levels for Doom II", "Canyon"),
    "e7c273033376824edf95e1328261e7de": ("Master Levels for Doom II", "The Catwalk"),
    "77c179948df47a7a613bd1181c959892": ("Master Levels for Doom II", "The Combine"),
    "cbf714b499ebdef2682990eaf93fdb5f": ("Master Levels for Doom II", "The Fistula"),
    "f000701a3ed1f49249ee08550c03dfa5": ("Master Levels for Doom II", "The Garrison"),
    "a1efff02df6d873762ebac6b12358bbc": ("Master Levels for Doom II", "Geryon: 6th Canto of Inferno", "John Anderson (Dr. Sleep)"),
    "787fa80fe9665c322f853b74838e77cc": ("Master Levels for Doom II", "Titan Manor"),
    "b4eaf844b135cc2a0058c6e0149b4408": ("Master Levels for Doom II", "Mephisto's Maosoleum"),
    "aea597159dee96bcc58f3f9e3e586182": ("Master Levels for Doom II", "Minos' Judgement: 4th Canto of Inferno", "John Anderson (Dr. Sleep)"),
    "46f58580e7792f486c747cf1117c4ca1": ("Master Levels for Doom II", "Nessus: 5th Canto of Inferno", "John Anderson (Dr. Sleep)"),
    "d560abb6d5719d46ebb47b27d7813a4b": ("Master Levels for Doom II", "Paradox"),
    "b572d518d564c7d7b6b259a726538cbb": ("Master Levels for Doom II", "Subspace"),
    "bb417f07804373415a6ed8e533242c3c": ("Master Levels for Doom II", "Subterra"),
    "65b4abcb74e7a386d5c024cf250d6336": ("Master Levels for Doom II", "The Express Elevator To Hell / Bad Dream"),
    "8474f6d663f04630de05ecac36b574d1": ("Master Levels for Doom II", "Trapped On Titan"),
    "a49dccebb5f32307246b7f32da121cf7": ("Master Levels for Doom II", "Vesperas: 7th Canto of Inferno", "John Anderson (Dr. Sleep)"),
    "3c0874f2df3c06a002ee2a18aba0f0e8": ("Master Levels for Doom II", "Virgil's Lead: 3rd Canto of Inferno", "John Anderson (Dr. Sleep)"),
    "8f857cd9272ac60d7a3a3579ca771ef5": [ "Brutal Doom v21"],
    "69093105f1eda4f2b1ed9718c14e0f7b": [ "Brutal Doom v21 RC7"],
    "5a07f72f8eb325c18a4887120753fc04": [ "Brutal Doom v5"],
    "bbbfd3924a333a665abb3e130bf0913c": [ "Brutal Doom v18"],   
    "5280c3ac2354aea753e9be94e628a291": [ "Brutal Doom v19"],
    "063dccb838f5de359c27d2e294cf4181": [ "Extermintion Day"],
    "fe27485f01019edc29619f826f1c2ea5": [ "Brutal Doom: Hell on Earth Starter Pack"],
    "19bca4ee9a03b7578cbb9f4062631e52": [ "No End in Sight (NEiS)", "", "", "November 20th, 2016"],
    "4146b6c8743fa4ddcdab678c0ab09986": ["Doom 3", "game00.pk4"],
    "660964d29a4351b388b3b7492e2d069a": ["Doom 3", "game01.pk4"],
    "e8ccd6db6e200fac417f19f6cea677f3": ["Doom 3", "game02.pk4"],
    "cf84eae12beecb61f913acbb800b2d8e": ["Doom 3", "game03.pk4"],
    "71b8d37b2444d3d86a36fd61783844fe": ["Doom 3", "pak000.pk4", 353159257],
    "4bc4f3ba04ec2b4f4837be40e840a3c1": ["Doom 3", "pak001.pk4", 229649726],
    "fa84069e9642ad9aa4b49624150cc345": ["Doom 3", "pak002.pk4", 416937674],
    "f22d8464997924e4913e467e7d62d5fe": ["Doom 3", "pak003.pk4", 317590154],
    "38561a3c73f93f2e6fd31abf1d4e9102": ["Doom 3", "pak004.pk4", 237752384],
    "2afd4ece27d36393b7538d55a345b90d": ["Doom 3", "pak005.pk4"],
    "a6e7003fa9dcc75073dc02b56399b370": ["Doom 3", "pak006.pk4"],
    "6319f086f930ec1618ab09b4c20c268c": ["Doom 3", "pak007.pk4"],
    "28750b7841de9453eb335bad6841a2a5": ["Doom 3", "pak008.pk4"],
    "5983f399d825882e4add6008e18f3e69": ["Doom 3: Resurrection of Evil", "game01.pk4"],
    "b37c3ef9f88b2fa692bf8438d0897c98": ["Doom 3: Resurrection of Evil", "game02.pk4"],
    "4f3088e5d279b2bf8583d55e01588a79": ["Doom 3: Resurrection of Evil", "game03.pk4"],
    "06fc9be965e345587064056bf22236d2": ["Doom 3: Resurrection of Evil", "pak001.pk4"]
}

allwads = []

def DoomWads(foldersPath):
    allwads = [f for f in foldersPath.glob('**/*.[Wwpp][Aakk][Dd34]') if f.is_file()] #and str(f).lower() in ['wad', 'pk3', 'pk4']]

    for file in allwads:    
        if file.stat().st_size < 1024*1024*196:
            timestamp_start = perf_counter()
            md5sum = md5(file)
            timestamp_stop = perf_counter()
            print(f"{md5sum} {file.stat().st_size:>9d} {file.stem + '' + file.suffix:22s} {(timestamp_stop - timestamp_start):1.3f} ", end="")
            for checksum, vals in DoomFiles.items():
                if checksum == md5sum:
                    print(f"{' '.join(vals)}", end="")
        else:
            for checksum, vals in DoomFiles.items():
                try:
                    if vals[2] == file.stat().st_size:
                        print(f"{'(skipped, matching by filesize)':32s} {file.stat().st_size:>9d} {file.stem + '' + file.suffix:22s} {'':6s}", end="")
                        print(f"{vals[0]} {vals[1]}", end="")
                except IndexError:
                    pass
        print("")


foldersPath = Path(os.path.expanduser('~/Spiele'))
print(foldersPath)
DoomWads(foldersPath)

foldersPath = Path(os.path.expanduser('~/Downloads'))
print(foldersPath)
DoomWads(foldersPath)

foldersPath = Path(os.path.expanduser('~/.config/gzdoom'))
print(foldersPath)
DoomWads(foldersPath)

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
    #print(type(d['libraryfolders'][folder]['apps']))
    #print(folderPath) #, end="")
    #d['libraryfolders'][folder]['apps'][377160] = "Fallout 4"
    dictApps = d['libraryfolders'][folder]['apps']
    #dictApps[377160] = "Fallout 4"
    for AppID in dictApps:
        #if AppID in ["9050"]:
        if AppID in AppList:
            AppPath = os.path.join(folderPath, "steamapps/common")
            AppPathGame = os.path.join(AppPath, AppList[AppID][0])
            #AppPathData = ""
            print(AppPathGame)
            foldersPath = Path(AppPathGame)
            DoomWads(foldersPath)
