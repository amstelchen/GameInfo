import os, vdf
from os import listdir
from os.path import isfile, join
from .BitsBytes import bytes2human
#import pefile
from pefile import PE
from subprocess import PIPE, Popen, check_output
#from DllVersionInfo import *
import hashlib
import requests
try:
    import py7zr
except ModuleNotFoundError:
    pass
#import libarchive.public

hasDLCs = True
hasNoDLCs = False

Official, Unofficial, MainDatafile = 0, 1, 2

AppList = {
    "38400": ("Fallout", "FALLOUTW.EXE", "FalloutLauncher.exe", hasNoDLCs), 
    "38410": ("Fallout 2", "fallout2HR.exe", "Fallout2Launcher.exe", hasNoDLCs), 
    "38420": ("Fallout Tactics", "BOS_HR.exe", "TacticsLauncher.exe", hasNoDLCs), 
    "22300": ("Fallout 3", "Fallout3.exe", "FalloutLauncherSteam.exe", hasDLCs),
    "22370": ("Fallout 3 - Game of the Year Edition", "Fallout3.exe", "FalloutLauncherSteam.exe", hasDLCs),
    "22380": ("Fallout: New Vegas", "FalloutNV.exe", "FalloutNVLauncher.exe", hasDLCs,
        ["Dead Money", "Honest Hearts", "Old World Blues", "Lonesome Road", "Courier's Stash", "Gun Runners' Arsenal"]),
    "377160": ("Fallout 4", "Fallout4.exe", "TBD", hasDLCs),
    "1151340": ("Fallout 76", "Fallout76.exe", "TBD", hasDLCs),
    "588430": ("Fallout Shelter", "FalloutShelter.exe", "FalloutShelter.exe", hasNoDLCs),
    "489830": ("Skyrim Special Edition", "SkyrimSE.exe", "SkyrimSELauncher.exe", hasDLCs),  # includes Anniversary Edition
    "22330": ("The Elder Scrolls IV - Oblivion", "Oblivion.exe", "OblivionLauncher.exe", hasDLCs),
    "1716740": ("Starfield", "Starfield.exe", "Starfield.exe", hasDLCs)
}

ScriptExtenders = {
    "FOSE": ["Fallout Script Extender", "1.2b2", "https://fose.silverlock.org/download/fose_v1_2_beta2.7z", "fose_loader.exe"],
    "NVSE": ["New Vegas Script Extender", "5.1b4", "http://nvse.silverlock.org/download/nvse_5_1_beta4.7z", "nvse_loader.exe"],
    "F4SE": ["Fallout 4 Script Extender", "0.6.23", "https://f4se.silverlock.org/beta/f4se_0_06_23.7z", "f4se_loader.exe"],
    "SKSE": ["Skyrim Script Extender", "2.2.3", "https://skse.silverlock.org/beta/skse64_2_02_03.7z", "skse64_loader.exe"],
    "OBSE": ["Oblivion Script Extender", "0.2.1", "http://obse.silverlock.org/download/obse_0021.zip", "obse_loader.exe"],
    "SFSE": ["Starfield Script Extender", "0.1.0", "https://sfse.silverlock.org/download/sfse_dummy.7z", "sfse_loader.exe"]
    # https://www.nexusmods.com/starfield/mods/106?tab=files&file_id=996
}

def du(path):
    """disk usage in human readable format (e.g. '2,1GB')"""
    return check_output(['du','-sh', path]).split()[0].decode('utf-8').replace("G", " G").replace("M", " M")

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sha1(fname):
    hash_sha1 = hashlib.sha1()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()

def cmdline(command):
    process = Popen(args=command, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True) #text_mode = True
    #process.text_mode = True
    return process.communicate()[0]

def FalloutDLCs(AppPath, DatafileKind=Official):

    if DatafileKind == Official:
        onlyfiles = [f for f in listdir(AppPath) if isfile(join(AppPath, f)) and 
            "esm" in f and " " not in f and "Fallout" not in f and "SeventySix" not in f and "Skyrim" not in f and "Oblivion" not in f and "Starfield" not in f]
    if DatafileKind == Unofficial:
        onlyfiles = [f for f in listdir(AppPath) if isfile(join(AppPath, f)) and 
            ("esm" in f and " " in f or "Patch" in f and "Patch.ba2" not in f) or "esp" in f]
    if DatafileKind == MainDatafile:
        onlyfiles = [f for f in listdir(AppPath) if isfile(join(AppPath, f)) 
            and "esm" in f and ("Fallout" in f or "SeventySix" in f or "Skyrim" in f or "Oblivion" in f or "Starfield" in f) and "Patch" not in f]
    if len(onlyfiles) == 0:
        return ["(none)"]
    return onlyfiles

def FalloutSE(AppPath, ScriptExtenderKey): # -> list():
    SE = ScriptExtenders[ScriptExtenderKey]
    if os.path.exists(os.path.join(AppPath, SE[3])):
        #print(ScriptExtenders[ScriptExtenderKey][1])
        return SE
    else:
        returnText = ["(Not found locally. Will be installed shortly.)"]
        url = SE[2]
        returnText.append(f"\n=Getting {url} and saving as {SE[3]}.")
        returnText.append("\n=Please unpack the archive into the game folder.")
        request = requests.get(url)
        if request.status_code != 200:
            returnText.pop()
            returnText.append(f"\n=(Not found ({request.status_code}). Check the website.)")
            return returnText
        # print(AppPath)
        # print(SE)
        with open(os.path.join(AppPath, SE[2].split('/')[4]), 'wb') as f:
            f.write(request.content)
        #try:
        #    archive = py7zr.SevenZipFile(os.path.join(AppPath, SE[2].split('/')[4]), mode='r')
        #    archive.extractall(path=AppPath)
        #    archive.close()
        #except py7zr.exceptions.UnsupportedCompressionMethodError:
        #    pass

        #with libarchive.public.file_reader(os.path.join(AppPath, SE[2].split('/')[4])) as e:
        #    for entry in e:
        #        with open(os.path.join(AppPath, SE[2].split('/')[4], str(entry)), 'wb') as f:
        #            for block in entry.get_blocks():
        #                f.write(block)
        #        print(str(entry))
        #        returnText.append(str(entry))

        return returnText

def FalloutInfo():

    returnString = "" # f'Fallout {"version"}:={steamCtime} - {lineVersion}\n'
    libraryfoldersPath = os.path.expanduser('~/.steam/steam/config/libraryfolders.vdf')  # -test
    #try:
    d = vdf.parse(open(libraryfoldersPath))
    #returnString += "\nSteam library folders:=\n"
    countApps = int(0)
    sizeApps = 0
    for folder in d['libraryfolders']:
        #workaround for Steam on Debian default installations
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
            #if AppID in ["22300", "22370", "22380", "377160"]:
            if AppID in AppList:
                AppPath = os.path.join(folderPath, "steamapps/common")
                AppPathGame = os.path.join(AppPath, AppList[AppID][0].replace(":", "").replace("t 76", "t76"))
                AppPathData = ""
                try:
                    AppPathData = os.path.join(AppPathGame, "Data")
                except FileNotFoundError:
                    AppPathData = ""
                AppPathExe = os.path.join(AppPathGame, AppList[AppID][1])
                sizeApp = bytes2human(int(dictApps[AppID]), format="%(value)3.1f %(symbol)s")
                if sizeApp == "0.0 B":
                    sizeApp = du(AppPathGame)
                #pe = PE(AppPathExe)
                #if not 'VS_FIXEDFILEINFO' in pe.__dict__:
                    #print("ERROR: Oops, %s has no version info. Can't continue." % (pename))
                #    return
                #if not pe.VS_FIXEDFILEINFO:
                    #print("ERROR: VS_FIXEDFILEINFO field not set for %s. Can't continue." % (pename))
                #    return
                #verinfo = pe.VS_FIXEDFILEINFO
                #prodver = (verinfo[0].ProductVersionMS >> 16, verinfo[0].ProductVersionMS & 0xFFFF, verinfo[0].ProductVersionLS >> 16, verinfo[0].ProductVersionLS & 0xFFFF)
                #print("Product version: %d.%d.%d.%d" % prodver)
                #AppVersion = "%d.%d.%d.%d" % prodver
                StrVersion = "Version"
                AppVersion = cmdline("peres -v '" + AppPathExe + "' | grep 'Product' | sed 's/ //g' | cut -d ':' -f2").strip()
                if len(AppVersion) == 0:
                    StrVersion = "[Version info missing]"
                if AppID == "38400":
                    StrVersion = "Patchlevel v1.1"
                    AppVersion += " ✓"
                if AppID == "38410":
                    if md5(AppPathExe) == "3347f6d10bb3d7c02d3614bcf406a912":
                        StrVersion = "Version 1.02, High-Res"
                    if md5(AppPathExe) == "cb9fff3abd57b01848f69d2617d68cbf":
                        StrVersion = "Patchlevel v1.02 (US)"
                if AppID == "38420":
                    if md5(AppPathExe) == "0582a73e30c224be580af8a734e0935c":
                        StrVersion = "Version 1.27, Low-Res"
                    if md5(AppPathExe) == "9bfb9cae9474b12db3c06accc29a5b24":
                        StrVersion = "Version 1.27, High-Res"
                if AppID == "22300":
                    if AppVersion == "1.7.0.4":
                        AppVersion += " ✓"
                if AppID == "22380":  # Fallout NV
                    if AppVersion == "1.4.0.525":
                        AppVersion += " ✓"
                if AppID == "377160":
                    if AppVersion == "1.10.163.0": # latest patch, not listed in https://fallout.fandom.com/wiki/Fallout_4_patches
                        AppVersion += " ✓"
                    else:
                        AppVersion += " !"
                if AppID == "1151340":
                    if AppVersion == "1.7.6.7": # patch data taken from https://fallout.fandom.com/wiki/Fallout_76_patches
                        AppVersion += " ✓"
                    else:
                        AppVersion += " !"
                if AppID == "489830":  # Skyrim SE
                    if AppVersion == "1.6.640.0":
                        AppVersion += " ✓"
                if AppID == "22330":  # Oblivion
                    if AppVersion == "1.2.0.416":
                        AppVersion += " ✓"
                if AppID == "1716740":  # Starfield
                    if AppVersion == "1.7.23.0":
                        AppVersion += " ✓"
                #returnString += f"{AppList[AppID][0]:<18s} AppID {AppID:>7s}, {' ':9s}total size {sizeApp:>5s}," \
                #                f"\n{' ':19s}{(StrVersion + ' ' + AppVersion):<23s} found in {AppList[AppID][1]} " \
                #                f"\n{' ':19s}md5:  {md5(AppPathExe)}" \
                #                f"\n{' ':19s}sha1: {sha1(AppPathExe)}"
                returnString += f"{AppList[AppID][0]}=AppID {AppID:>7s}, {' ':9s}total size {sizeApp:>5s}," \
                                f"\n={(StrVersion + ' ' + AppVersion):<23s} found in {AppList[AppID][1]} " \
                                f"\n=md5:  {md5(AppPathExe)}" \
                                f"\n=sha1: {sha1(AppPathExe)}"
                countApps += 1
                sizeApps += int(dictApps[AppID])
                # was filtered by AppID.startswith("22") or AppID == "377160" or AppID == "1151340" and  
                if AppList[AppID][3] == hasDLCs and len(AppPathData) > 0:
                    # print(AppPathData, len(AppPathData))
                    returnString += "\n  Main data file:=" + "\n=".join(FalloutDLCs(AppPathData, DatafileKind=MainDatafile))
                    returnString += "\n  Official DLCs:=" + "\n=".join(FalloutDLCs(AppPathData, DatafileKind=Official))
                    returnString += "\n  Unofficial DLCs:=" + "\n=".join(FalloutDLCs(AppPathData, DatafileKind=Unofficial))
                ScriptExtenderKey = ""
                if AppID in ["22300", "22370"]: # FO3
                    ScriptExtenderKey = "FOSE"
                if AppID == "22380": # FNV
                    ScriptExtenderKey = "NVSE"
                if AppID == "377160": # FO4
                    ScriptExtenderKey = "F4SE"
                if AppID == "489830": # SKYRIM
                    ScriptExtenderKey = "SKSE"
                if AppID == "22330": # OBLIVION
                    ScriptExtenderKey = "OBSE"
                if AppID == "1716740": # STARFIELD
                    ScriptExtenderKey = "SFSE"
                if ScriptExtenderKey:
                    SE = FalloutSE(AppPathGame, ScriptExtenderKey)
                    if len(SE) >= 3: # is not None:
                        # print(SE)
                        returnString += "\n  ScriptExtender:=" + SE[0] + " " + SE[1] + "\n=" + SE[2] # ".join([se for se for SE])
                    else:
                        returnString += "\n  ScriptExtender:=" + SE[0]
                returnString += "\n\n"
    #returnString += "_________________________________________\n"
    returnString += f"{str(countApps):>1s} games=total size {bytes2human(sizeApps):>6s}"
    return returnString

def main():
    print(FalloutInfo())

if __name__ == '__main__':
    main()
