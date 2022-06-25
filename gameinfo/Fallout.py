import os, vdf
from os import listdir
from os.path import isfile, join
from BitsBytes import bytes2human
#import pefile
from pefile import PE
from subprocess import PIPE, Popen, check_output
#from DllVersionInfo import *
import hashlib

hasDLCs = True
hasNoDLCs = False

Official, Unofficial, MainDatafile = 0, 1, 2

AppList = { "38400": ("Fallout", "FALLOUTW.EXE", "FalloutLauncher.exe", hasNoDLCs), 
            "38410": ("Fallout 2", "fallout2HR.exe", "Fallout2Launcher.exe", hasNoDLCs), 
            "38420": ("Fallout Tactics", "BOS_HR.exe", "TacticsLauncher.exe", hasNoDLCs), 
            "22300": ("Fallout 3", "Fallout3.exe", "FalloutLauncherSteam.exe", hasDLCs),
            "22370": ("Fallout 3 - Game of the Year Edition", "Fallout3.exe", "FalloutLauncherSteam.exe", hasDLCs),
            "22380": ("Fallout: New Vegas", "FalloutNV.exe", "FalloutNVLauncher.exe", hasDLCs,
                ["Dead Money", "Honest Hearts", "Old World Blues", "Lonesome Road", "Courier's Stash", "Gun Runners' Arsenal"]),
            "377160": ("Fallout 4", "Fallout4.exe", "TBD", hasDLCs),
            "1151340": ("Fallout 76", "Fallout76.exe", "TBD", hasDLCs),
            "588430": ("Fallout Shelter", "FalloutShelter.exe", "FalloutShelter.exe", hasNoDLCs)
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

    if DatafileKind == 0:
        onlyfiles = [f for f in listdir(AppPath) if isfile(join(AppPath, f)) and "esm" in f and " " not in f and "Fallout" not in f and "SeventySix" not in f]
    if DatafileKind == 1:
        onlyfiles = [f for f in listdir(AppPath) if isfile(join(AppPath, f)) and ("esm" in f and " " in f or "Patch" in f) or "esp" in f]
    if DatafileKind == 2:
        onlyfiles = [f for f in listdir(AppPath) if isfile(join(AppPath, f)) and "esm" in f and ("Fallout" in f or "SeventySix" in f) and "Patch" not in f]
    if len(onlyfiles) == 0:
        return ["(none)"]
    return onlyfiles

def FalloutInfo():

    returnString = "" # f'Fallout {"version"}:={steamCtime} - {lineVersion}\n'
    libraryfoldersPath = os.path.expanduser('~/.steam/steam/config/libraryfolders.vdf')
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
                if AppID == "22380":
                    if AppVersion == "1.4.0.525":
                        AppVersion += " ✓"
                if AppID == "377160":
                    if AppVersion == "1.7.15":
                        AppVersion += " ✓"
                    else:
                        AppVersion += " !"
                if AppID == "1151340":
                    if AppVersion == "1.6.4.60":
                        AppVersion += " ✓"
                    else:
                        AppVersion += " !"
                returnString += f"{AppList[AppID][0]:<18s} AppID {AppID:>7s}, {' ':9s}total size {sizeApp:>5s}," \
                                f"\n{' ':19s}{(StrVersion + ' ' + AppVersion):<23s} found in {AppList[AppID][1]} " \
                                f"\n{' ':19s}md5:  {md5(AppPathExe)}" \
                                f"\n{' ':19s}sha1: {sha1(AppPathExe)}"  # {AppPathExe}")
                countApps += 1
                sizeApps += int(dictApps[AppID])
                # was filtered by AppID.startswith("22") or AppID == "377160" or AppID == "1151340" and  
                if AppList[AppID][3] == hasDLCs and len(AppPathData) > 0:
                    #print(AppPathData, len(AppPathData))
                    returnString += "\nMain data file:    " + "\n                   ".join(FalloutDLCs(AppPathData, DatafileKind=MainDatafile))
                    returnString += "\nOfficial DLCs:     " + "\n                   ".join(FalloutDLCs(AppPathData, DatafileKind=Official))
                    returnString += "\nUnofficial DLCs:   " + "\n                   ".join(FalloutDLCs(AppPathData, DatafileKind=Unofficial))
                returnString += "\n\n"
    #returnString += "_________________________________________\n"
    returnString += f"{str(countApps):>2s} games or apps {bytes2human(sizeApps):>24s}"
    return returnString

def main():
    print(FalloutInfo())

if __name__ == '__main__':
    main()
