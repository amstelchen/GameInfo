from .__init__ import *

from .Version import __appname__, __version__, __author__, __copyright__, __licence__
from .AppDebug import AppDebug

def PrintAbout() -> str:
    returnString = (f'{__appname__} Version: {__version__}\n\n'
        f'Python Version: {".".join([str(value) for value in sys.version_info[0:3]])}\n'
        f'ttkbootstrap Version: {version("ttkbootstrap"):s}\n'
        f'TK Version: {tk.TkVersion:.1f}\n'
        f'PIL Version: {PIL.__version__:s}\n'
        f'\n{__copyright__}\n'
        f'\n{__licence__}\n')
    return returnString

def cmdline(command):
    process = Popen(args=command, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True) #text_mode = True
    #process.text_mode = True
    return process.communicate()[0]

def GetDistributionId() -> str:
    with open("/etc/os-release", mode="r", encoding = 'utf-8') as f:
        for line in f.readlines():
            #print(line)
            if "VERSION_ID=" in line:
                continue
            if "ID=" in line:
                result = str(line.split("=")[1].strip().strip('\"'))
                AppDebug.debug_print("DistributionId: " + result)
                return result

def GetDistributionKind() -> str:
    DistributionId = GetDistributionId()
    if DistributionId in ["debian", "ubuntu", "linuxmint", "mint", "kali", "raspbian"]:
        return "debian"
    if DistributionId in "arch manjaro garuda".split():
        return "arch"
    if DistributionId in "fedora centos rhel mageia mandriva".split():
        return "fedora"
    if DistributionId in "opensuse-tumbleweed opensuse-leap opensuse sles".split():
        return "suse"
    if DistributionId in ["void"]:
        return "void"
    if DistributionId in ["slackware"]:
        return "slackware"
    if DistributionId in "ol amzn".split():
        return ""

#def PrintInfo(Section: Section, Separator: char):
#    AppDebug.debug_print(f'{Section} {Separator}')

def PopulateMenuitems():
    file = minidom.parse(os.path.join(os.path.dirname(__file__), "GameInfo.xml"))
    menuitems = file.getElementsByTagName('menuitem')
    for menuitem in menuitems:
        section = menuitem.attributes['value'].value
        command = menuitem.attributes['command'].value
        result = cmdline(command)
        #AppDebug.debug_print(command)
        if len(result) > 0:
            menuitem.attributes['command'].value = result
        else:
            menuitem.attributes['command'].value = section + " info could not be retrieved."
    return menuitems

def ReplaceIconname(icon_name) -> str:
    if icon_name == "openrgb":
        icon_name = "OpenRGB"
    if icon_name == "minigalaxy":
        icon_name = "io.github.sharkwouter.Minigalaxy"
    if icon_name == "pavucontrol":
        icon_name = "multimedia-volume-control"
    if icon_name == "vibrantLinux":
        icon_name = "io.github.libvibrant.vibrantLinux"
    if icon_name == "protontricks":
        icon_name = "wine"
    if icon_name == "steamcmd":
        icon_name = "steam_tray_mono"
    if icon_name == "pavucontrol":
        icon_name = "multimedia"
    return icon_name

def ListTools() -> str:
    AppDebug.debug_print(_("Fetching system info, this can take a second..."))
    StartTime = time.time()

    file = minidom.parse(os.path.join(os.path.dirname(__file__), "GameInfo.xml"))
    toolitems = file.getElementsByTagName('toolitem')
    outputALLE = str("")

    Distribution = GetDistributionKind()
    PackageManager = ""; CutString=""
    if Distribution == "arch": PackageManager = "pacman -Q"; CutString = " | cut -d ' ' -f 2"
    if Distribution == "debian": PackageManager = "apt-cache policy"; CutString=" | head -n 2 | tail -n 1 | cut -d ':' -f 2"
    if Distribution == "fedora": PackageManager = "rpm -q" # "dnf info -C -q python3 | grep Version | uniq"
    if Distribution == "suse": PackageManager = "rpm -q" # "zypper"
    if Distribution == "void": PackageManager = "xbps-query -S"; CutString=" | grep pkgver | cut -d ':' -f 2 | cut -d '-' -f 2"
    if Distribution == "slackware": PackageManager = "slackpkg"

    for toolitem in toolitems:
        toolitem_command = toolitem.attributes["command"].value
        toolitem_version = toolitem.attributes["version"].value
        AppDebug.debug_print(_("Checking for") + " " + toolitem_command)
        # contains no ! or ?, just the filename
        if toolitem_command.find("!") == -1 and toolitem_command.find("?") == -1:
            toolResult = cmdline(str(toolitem_command + " " + toolitem_version))
        # contains a ! -> execute the version string
        if toolitem_command.find("!") == 0:
            toolitem_command = toolitem_command.strip('!')
            toolResult = cmdline(str(toolitem_version))
        # contains a ? -> ask the package manager
        if toolitem_command.find("?") == 0:
            toolitem_command = toolitem_command.strip('?')
            AppDebug.debug_print(f"{PackageManager} {toolitem_command}")
            cmdlineResult = cmdline(PackageManager + " " + toolitem_version + CutString).strip(' ')
            toolResult = cmdlineResult # split(' ')[0] 
        if len(toolResult) == 0:
            toolResult += "\n"
        else:
            toolResult = toolResult.replace('-','–')
        outputALLE += toolitem_command + "|" + toolResult

    #AppDebug.debug_print(outputALLE)
    FinishTime = time.time()
    AppDebug.debug_print(f"Time elapsed: {(FinishTime - StartTime):.2f}s")
    return outputALLE

def DisplayInfoUnused() -> str:
    # using "cat /sys/class/drm/*/edid | edid-decode -s" instead
    #returnString= returnString.replace('\t', "  ")
    cs = randr.connected_screens()
    returnString = ""
    for s in cs:
        #print(s.__str__())
        returnString += s.__str__() + "|\n"
        for m in s.supported_modes:
            #print(m.__str__())
            returnString += m.__str__() + "\n"
    splitChar = "|"
    return returnString

def WineInfo() -> str:
    returnString = f'Wine {_("version")}:={cmdline("wine --version")}\n'
    prefixes = ["~/.wine", "~/.wine32", "~/.config/wine/prefixes"]
    for prefix in prefixes:
        returnString += str(prefix) + ":="
        if os.path.isdir(os.path.expanduser(str(prefix))):
            pathToPrefix = Path(os.path.expanduser(prefix))
            sumBytesPrefix = sum(f.stat().st_size for f in pathToPrefix.glob('**/*') if f.is_file())
            returnString += _("Yes") + " (" + bytes2human(sumBytesPrefix,format="%(value)3.1f %(symbol)s", symbols="iec") + "B)\n"
        else:
            returnString += _("No") + "\n"
        #returnString += str(prefix) + ":" + print("Yes") if os.path.isdir(str(prefix)) == True else print("No") + "\n"
    return returnString

def SteamInfo() -> str:
    lineVersion = _("unknown")
    steamCtime = ""

    # only on Arch
    steamBinary = os.path.expanduser("~/.local/share/Steam/ubuntu12_32/steam")
    # on Debian and Arch
    steamBinary = os.path.expanduser("~/.steam/steam/ubuntu12_32/steam")
    if os.path.isfile(steamBinary):
        steamCtime = time.ctime(os.path.getmtime(steamBinary))

    # only on Arch
    steamRuntime = os.path.expanduser("~/.local/share/Steam/ubuntu12_32/steam-runtime/version.txt")
    # on Debian and Arch
    steamRuntime = os.path.expanduser("~/.steam/steam/ubuntu12_32/steam-runtime/version.txt")
    if os.path.isfile(steamRuntime):
        with open(steamRuntime, 'r') as versionFile:
            lineVersion = versionFile.readline()
        #if len(lineVersion) == 0:

    returnString = f'Steam {_("version")}:={steamCtime} - {lineVersion}\n'
    #prefixes = ["$HOME/.wine", "$HOME/.wine32", "$HOME/.config/wine/prefixes"]
    prefixes = ["~/.local/share/Steam", "~/.steam/steam/", "~/.steampath", "~/.steam/bin32/"]
    returnString += "Steam install folders:=\n\n"
    for prefix in prefixes:
        returnString += str(prefix) + ":="
        if os.path.isdir(os.path.expanduser(str(prefix))):
            returnString += _("Yes") + "\n"
        else:
            returnString += _("No") + "\n"
        #returnString += str(prefix) + ":" + print("Yes") if os.path.isdir(str(prefix)) == True else print("No") + "\n"
    libraryfoldersPath = os.path.expanduser('~/.steam/steam/config/libraryfolders.vdf')
    try:
        d = vdf.parse(open(libraryfoldersPath))
        returnString += "\nSteam library folders:=\n"
        for folder in d['libraryfolders']:
            #workaround for Steam on Debian default installations
            if folder == "contentstatsid":
                continue
            totalSize = int(d['libraryfolders'][folder]['totalsize'])
            folderPath = d['libraryfolders'][folder]['path']
            sizeApps = 0
            countApps = 0
            #print(type(d['libraryfolders'][folder]['apps']))
            dictApps = d['libraryfolders'][folder]['apps']
            for app in dictApps:
                countApps += 1
                sizeApps += int(dictApps[app])
            #workaround for Steam for the default library reported 0 size
            if totalSize == 0:
                total, used, free = shutil.disk_usage(folderPath)
                totalSize = total
                freeSize = free
            else:
                freeSize = totalSize - sizeApps
            #if freeSize < 0: freeSize = 0
            returnString += "\n" + folderPath + ":="
            returnString += str(countApps).rjust(3,' ') + " " + _("games or apps") + "  "
            returnString += bytes2human(totalSize,format="%(value)3.1f %(symbol)s") + " " + _("total")
            returnString += " (" + bytes2human(sizeApps,format="%(value)3.1f %(symbol)s") + " " + _("used")
            returnString += ", " + bytes2human(freeSize,format="%(value)3.1f %(symbol)s") + " " + _("free") + ")"
    except FileNotFoundError:
        returnString += "\n" + libraryfoldersPath + " " + _("not found")
    return returnString

def ProtonInfo() -> str:
    returnString = ""
    #proton_bin = (cmdline("which proton")).replace('\n','')
    proton_bin = (cmdline("command -v proton")).replace('\n','')
    #print(proton_bin)
    if len(proton_bin) == 0:
        returnString += "Proton executable not found." + "\n"
    else:
        #proton_dir = (cmdline("grep _proton= `which proton`")).replace('\n','')
        proton_dir = (cmdline("cat `command -v proton` | grep _proton=")).replace('\n','').replace("_proton=","")
        if len(proton_dir) == 0:
            returnString += "Proton variable _proton not found."
        #returnString += proton_dir
        #print(proton_dir)
    if len(proton_bin) > 0 and len(proton_dir) > 0:
        proton_ver = cmdline("cat " + proton_dir + " | grep CURRENT_PREFIX_VERSION=")
        if len(proton_ver) == 0:
            returnString += "Proton custom executable not found." + "\n"
        else:
            returnString += "proton_bin:=" + proton_bin + "\n"
            returnString += "proton_dir (set in " + proton_bin + "):=" + proton_dir +"\n\n"
            returnString += proton_ver
            #print(proton_ver)

    #mypath = os.path.dirname(proton_dir.replace("_proton=","").replace("\n",""))
    mypath = "compatibilitytools.d"
    returnString += "\nOther tools in " + mypath
    mypath = "/usr/share/steam/compatibilitytools.d"
    if os.path.exists(mypath):
        onlyfiles = [f for f in listdir(mypath)]
        for file in onlyfiles:
            returnString += "=" + str(file) + "\n"
    else:
        returnString += "\n" + _("Steam compatibilitytools install directory not found.")
    return returnString

def DOSBoxInfo() -> str:
    returnString = f'DOSBox {_("version")}:={cmdline("dosbox --version | head -n 2 | tail -n 1 | sed s/DOSBox[[:space:]]version[[:space:]]//;")}\n'
    mypath = os.path.expanduser("~/.dosbox/")
    #returnString += cmdline("dosbox --version | head -n 2 | tail -n 1 | sed 's/version//'; echo")
    if os.path.exists(mypath):
        returnString += _("Config files")
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for file in onlyfiles:
            returnString += "=" + str(file) + "\n"
    else:
        returnString += "\n" + _("DOSBox install directory not found.")
    return returnString

def LutrisInfo() -> str:
    returnString = f'Lutris {_("version")}:={cmdline("lutris --version | sed s/lutris-//;")}\n'
    #returnString += "Lutris " + cmdline("lutris --version | sed 's/lutris-//'; echo")
    #mypath = os.path.expanduser("~/.config/lutris/games/")
    #returnString += _("Games")
    #onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    #for file in onlyfiles:
    #    returnString += ": " + os.path.splitext(file)[0] + "\n"
    #splitChar = ": "
    try:
        conn = sqlite3.connect('/home/mic/.local/share/lutris/pga.db')
        cursor = conn.execute("SELECT id, name from games")
        returnString += _("Games")
        for row in cursor:
            returnString += "=" + row[1] + "\n"
        conn.close()
    except sqlite3.OperationalError:
        returnString += "\n" + _("Lutris install directory not found.")
    return returnString

def GOGInfo() -> str:
    selection = "Minigalaxy"
    returnString = f'{selection} {_("version")}:={cmdline("minigalaxy --version")}\n'
    mypath = os.path.expanduser("~/.config/minigalaxy/games/")
    #returnString += "Minigalaxy " + cmdline("minigalaxy --version; echo")
    if os.path.exists(mypath):
        returnString += _("Games")
        #try:
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for file in onlyfiles:
            returnString += "=" + os.path.splitext(file)[0] + "\n"
        #except FileNotFoundError as err:
    else:
        returnString += "\n" + _("Minigalaxy/GOG install directory not found.")
    return returnString

def ScummVMInfo() -> str:
    returnString = f'ScummVM {_("version")}:={cmdline("scummvm --version | head -n 1 | sed s/ScummVM[[:space:]]//;")}\n'
    #returnString += cmdline("scummvm --version | head -n 1; echo")
    mypath = os.path.expanduser("~/.config/scummvm/scummvm.ini")
    if os.path.exists(mypath):
        returnString += _("Games")
        INIfile = open(mypath, 'r')
        lines = INIfile.readlines()
        count = 0
        for line in lines:
            count += 1
            if "description" in line:
                #print("Line{}: {}".format(count, line.strip())
                returnString += line.strip("description") # + "\n"
        cutString = cmdline("scummvm --version | tail -n 1")
        #print(cutString)
        returnString += '\n' + cutString.split(':')[0].rstrip('\n')
        wordCount = 0
        #returnString += "="
        for word in cutString.split(':')[1].split(' '):
            returnString += word + ' '
            #if wordCount == 3:
                #returnString += "\n"
            if wordCount % 8 == 0:
                returnString += "\n="
            wordCount += 1
        #print(returnString)
    else:
        returnString += "\n" + _("ScummVM install directory not found.")
    return returnString
