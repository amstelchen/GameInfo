from .__init__ import *

from .Version import __appname__, __version__, __author__, __copyright__, __licence__
from .AppDebug import AppDebug, WaitMessage

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

def MachineInfo() -> str:
    SystemPath = "/sys/devices/virtual/dmi/id"
    if os.path.exists(SystemPath):
        onlyfiles = [f for f in listdir(SystemPath)]
        for file in onlyfiles:
            with open(os.path.join(SystemPath, file), 'r') as infoFile:
                lineInfo = infoFile.read()
                returnString += "=" + str(lineInfo) + "\n"
    else:
        returnString += "\n" + _("Machine info sysfs directory not found.")
    return returnString

def ParseMachineTags(Tags: str) -> str:
    lineMod = ""
    for line in Tags.splitlines():
        if "_Unavailable_" in line:
            continue
        if "To be filled by O.E.M." in line:
            continue
        if "dmi" in line:
            continue
        line = line.split(':')
        if "sys_vendor" in line[0]:
            line[0] = line[0].replace('sys', 'System')
        if "bios" in line[0]:
            line[0] = line[0].replace('bios', 'BIOS')
        else:
            line[0] = line[0].capitalize()
        lineMod += ':'.join([line[0].replace('_', ' '), line[1] + "\n"])
        if "version" in line[0]:
            lineMod += ":\n"
    # return Tag.replace('bios', 'BIOS').capitalize().replace('_', ' ')
    return lineMod

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
    if DistributionId in ["debian", "ubuntu", "linuxmint", "mint", "pop", "kali", "raspbian", "zorin"]:
        return "debian"
    if DistributionId in "arch manjaro garuda endeavouros arcolinux artix".split():
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

def GetDistributionLogoName():
    with open("/etc/os-release", mode="r", encoding = 'utf-8') as f:
        for line in f.readlines():
            #print(line)
            if "LOGO=" in line:
                result = str(line.split("=")[1].strip().strip('\"'))
                AppDebug.debug_print("DistributionLogo: " + result)
                return result
        if GetDistributionId() == "debian":
            return "debian-logo"
        if GetDistributionId() == "ubuntu":
            return "ubuntu-logo-icon"
        if GetDistributionId() == "zorin":
            return "zorin-os-logo-icon"
        if GetDistributionId() == "linuxmint":
            return "linuxmint-logo"
        if GetDistributionId() == "distributor-logo-Tumbleweed": # opensuse-tumbleweed
            return "xfce4-button-opensuse"
    
def GetDistributionLogoImage(Logo):
    #if "logo" not in Logo:
    #    Logo += "-logo"
    try:
        icon_file = Gtk.IconTheme.get_default().lookup_icon(Logo, 32, 0).get_filename()
        if os.path.isfile(icon_file):
            if "svg" in icon_file:
                image_data = cairosvg.svg2png(url=icon_file)
                image = (Image.open(io.BytesIO(image_data)))
                photo = image.resize((64, 64), Image.Resampling.LANCZOS) #, Image.ANTIALIAS)
            if "png" in icon_file:
                image = Image.open(icon_file)
                photo = image.resize((64, 64), Image.Resampling.LANCZOS) #, Image.ANTIALIAS)
        return ImageTk.PhotoImage(photo)
    except:
        #print(distro_logo)
        distro_logo = os.path.join("/usr/share/pixmaps/", Logo + ".svg")
        if os.path.isfile(distro_logo):
            image_data = cairosvg.svg2png(url=distro_logo)
            image = (Image.open(io.BytesIO(image_data)))
            photo = image.resize((64, 64), Image.Resampling.LANCZOS) #, Image.ANTIALIAS)
        else:
            distro_logo = os.path.join("/usr/share/pixmaps/", Logo + ".png")
            if os.path.isfile(distro_logo):
                image = Image.open(distro_logo)
                photo = image.resize((64, 64), Image.Resampling.LANCZOS) #, Image.ANTIALIAS)
            else:
                distro_logo = os.path.join("/usr/share/pixmaps/", Logo + "-logo.png")
                if os.path.isfile(distro_logo):
                    image = Image.open(distro_logo)
                    photo = image.resize((64, 64), Image.Resampling.LANCZOS) #, Image.ANTIALIAS)
        return ImageTk.PhotoImage(photo)

def GetDesktopLogoImage(Logo):
    if Logo == "gnome":
        Logo = "org.gnome.Software"
    if Logo == "xfce" or Logo == "xfce4":
        Logo = "xfce4-logo"
    try:
        icon_file = Gtk.IconTheme.get_default().lookup_icon(Logo, 32, 0).get_filename()
        #print(icon_file)
        if "svg" in icon_file:
            image_data = cairosvg.svg2png(url=icon_file)
            image = (Image.open(io.BytesIO(image_data)))
            photo = image.resize((64, 64), Image.Resampling.LANCZOS) #, Image.ANTIALIAS)
        if "png" in icon_file:
            image = Image.open(icon_file)
            photo = image.resize((64, 64), Image.Resampling.LANCZOS) #, Image.ANTIALIAS)
        return ImageTk.PhotoImage(photo)
    except AttributeError:
        return None

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
        return "OpenRGB"
    if icon_name == "minigalaxy":
        return "io.github.sharkwouter.Minigalaxy"
    if icon_name == "vibrantLinux":
        return "io.github.libvibrant.vibrantLinux"
    if icon_name == "wine":
        return "application-x-wine-extension-icl"
    if icon_name == "protontricks":
        return "winetricks"
    if icon_name == "steamcmd":
        return "steam_tray_mono"
    if icon_name == "pavucontrol":
        return "multimedia"
    if icon_name == "OBS":
        return "com.obsproject.Studio"
    if icon_name == "cpupower-gui":
        return "org.rnd2.cpupower_gui"
    return icon_name

def ListTools() -> str:
    AppDebug.debug_print(WaitMessage)
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
    if Distribution == "slackware": PackageManager = "slackpkg info"; CutString=" | grep Package | cut -d ':' -f 2"

    for toolitem in toolitems:
        StartTimeTool = time.time()
        toolitem_command = toolitem.attributes["command"].value
        toolitem_version = toolitem.attributes["version"].value
        AppDebug.debug_print(f'{_("Checking for")} {toolitem_command}...', end="")
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
            #AppDebug.debug_print(f"{PackageManager} {toolitem_command}")
            cmdlineResult = cmdline(PackageManager + " " + toolitem_version + CutString).strip(' ')
            toolResult = cmdlineResult # split(' ')[0] 
        if len(toolResult) == 0:
            toolResult += "\n"
        else:
            toolResult = toolResult.replace('-','–')
        outputALLE += toolitem_command + "|" + toolResult
        FinishTimeTool = time.time()
        AppDebug.debug_print(show_time=False, message=f"Time elapsed: {(FinishTimeTool - StartTimeTool) * 1000:2.2f}ms", prefix="")

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

    prefixes = ["~/.wine", "~/.wine32", "~/.config/wine/prefixes", "~/.local/share/wineprefixes"]
    for prefix in prefixes:
        returnString += str(prefix) + ":="
        if os.path.isdir(os.path.expanduser(str(prefix))):
            pathToPrefix = Path(os.path.expanduser(prefix))
            sumBytesPrefix = sum(f.stat().st_size for f in pathToPrefix.glob('**/*') if f.is_file())
            returnString += _("Yes") + " (" + bytes2human(sumBytesPrefix,format="%(value)3.1f %(symbol)s", symbols="iec") + "B)\n"
        else:
            returnString += _("No") + "\n"

    returnString += "\n"

    caches = ["~/.cache/wine", "~/.cache/winetricks"]
    for cache in caches:
        returnString += str(cache) + ":="
        if os.path.isdir(os.path.expanduser(str(cache))):
            pathToCache = Path(os.path.expanduser(cache))
            sumBytesCache = sum(f.stat().st_size for f in pathToCache.glob('**/*') if f.is_file())
            returnString += _("Yes") + " (" + bytes2human(sumBytesCache,format="%(value)3.1f %(symbol)s", symbols="iec") + "B)\n"
        else:
            returnString += _("No") + "\n"

    return returnString

def PlayOnLinuxInfo() -> str:
    returnString = f'PlayOnLinux {_("version")}:={cmdline("playonlinux --version || playonlinux4 --version")}\n'
    prefixes = ["~/.PlayOnLinux/wineprefix"]
    for prefix in prefixes:
        returnString += str(prefix) + ":="
        if os.path.isdir(os.path.expanduser(str(prefix))):
            pathToPrefix = Path(os.path.expanduser(prefix))
            sumBytesPrefix = sum(f.stat().st_size for f in pathToPrefix.glob('**/*') if f.is_file())
            returnString += _("Yes") + " (" + bytes2human(sumBytesPrefix,format="%(value)3.1f %(symbol)s", symbols="iec") + "B)\n"
        else:
            returnString += _("No") + "\n"
    returnString += "\n"

    mypath = os.path.expanduser("~/.PlayOnLinux/shortcuts")
    if os.path.exists(mypath):
        returnString += _("games or apps")
        #try:
        #onlydirs = [f for f in listdir(mypath) if isdir(join(mypath, f))]
        #for dir in onlydirs:
            #returnString += "=" + dir + "\n"
        #except FileNotFoundError as err:
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for file in onlyfiles:
            returnString += "=" + str(file) + "\n"
    else:
        returnString += "\n" + _("PlayOnLinux install directory not found.")
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
    returnString = "System-wide Proton install:=\n\n"
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
            returnString += "=" + str(file).ljust(23)
            if os.path.exists(join(mypath, str(file), "compatibilitytool.vdf")):
                #print(join(mypath, str(file), "compatibilitytool.vdf"))
                vdf_content = vdf.parse(open(join(mypath, file, "compatibilitytool.vdf")))
                if str(file) == "proton-ge-custom":
                    file = "Proton-GE"
                display_name = vdf_content['compatibilitytools']['compat_tools'][file]['display_name']
                returnString += display_name + "\n"
            else:
                vdf_content = vdf.parse(open(join(mypath, file)))
                display_name = vdf_content['compatibilitytools']['compat_tools'][Path(file).stem]['display_name']
                returnString += display_name + "\n"
    else:
        returnString += "\n" + _("Steam compatibilitytools install directory not found.")
    libraryfoldersPath = os.path.expanduser('~/.steam/steam/config/libraryfolders.vdf')
    try:
        vdf_content = vdf.parse(open(libraryfoldersPath))
        returnString += "\nSteam Proton installs:=\n\n"
        for folder in vdf_content['libraryfolders']:
            #workaround for Steam on Debian default installations
            if folder == "contentstatsid":
                continue
            folderPath = vdf_content['libraryfolders'][folder]['path']
            folderPathCommon = os.path.join(folderPath, 'steamapps/common/')
            AppDebug.debug_print(folderPathCommon)
            proton_installs = [d for d in listdir(folderPathCommon) if str(d).lower().startswith('proton')]
            if len(proton_installs) > 0:
                returnString += folderPath #+ ":="
                for proton in proton_installs:
                    returnString += "=" + proton.ljust(23)
                    if os.path.exists(join(folderPathCommon, proton, "version")):
                        with open(join(folderPathCommon, proton, "version"), "r", newline=None) as versionfile:
                            returnString += f" {versionfile.readline()}"
                    else:
                        returnString += "\n"
            AppDebug.debug_print(proton_installs)
    except FileNotFoundError:
        returnString += "\n" + libraryfoldersPath + " " + _("not found")
    return returnString

def DOSBoxInfo() -> str:
    returnString = f'DOSBox {_("version")}:={cmdline("dosbox --version | head -n 2 | tail -n 1 | sed s/DOSBox[[:space:]]version[[:space:]]//;")}\n'
    mypath = os.path.expanduser("~/.dosbox/")
    #returnString += cmdline("dosbox --version | head -n 2 | tail -n 1 | sed 's/version//'; echo")
    if os.path.exists(mypath):
        returnString += _("Config files")
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for file in onlyfiles:
            returnString += "=" + file.ljust(20) + " "
            with open(join(mypath, file), "r") as configfile:
                filelines = configfile.read()
                if "[autoexec]" in filelines:
                    returnString += f'(has [autoexec] section: {_("Yes")})\n'
                else:
                    returnString += f'(has [autoexec] section: {_("No")})\n'
    else:
        returnString += "\n" + _("DOSBox install directory not found.")
    return returnString

def LutrisInfo() -> str:
    sql_others = "SELECT id, runner, name FROM games WHERE runner IS NOT 'steam' AND runner IS NOT '' GROUP BY name ORDER BY runner ASC;"
    sql_steam  = "SELECT id, runner, name FROM games WHERE runner IS 'steam' ORDER BY name;"

    returnString = f'Lutris {_("version")}:={cmdline("lutris --version | sed s/lutris-//;")}\n'
    #returnString += "Lutris " + cmdline("lutris --version | sed 's/lutris-//'; echo")
    #mypath = os.path.expanduser("~/.config/lutris/games/")
    #returnString += _("Games")
    #onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    #for file in onlyfiles:
    #    returnString += ": " + os.path.splitext(file)[0] + "\n"
    #splitChar = ": "
    mypath = os.path.expanduser("~/.local/share/lutris/")
    try:
        conn = sqlite3.connect(os.path.join(mypath, 'pga.db'))
        cursor = conn.execute(sql_others)
        returnString += _("Games (others)")
        for row in cursor:
            returnString += f"={(row[2]):<40}\t\t{ row[1] }\n"
        cursor = conn.execute(sql_steam)
        returnString += "\n" + _("Games (Steam)")
        for row in cursor:
            returnString += f"={(row[2]):<40}\n"
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
    returnString = f'ScummVM {_("version")}:={cmdline("scummvm --version | head -n 1")}\n'
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

def EpicGamesInfo() -> str:
    #returnString = "legendary " + _('version') + ":(" + cmdline("legendary --version | cut -d ' ' -f 3-") # + "\n"
    returnString = ""
    mypath = os.path.expanduser("~/.config/legendary/config.ini")
    if os.path.exists(mypath):
        #returnString += _("Games")
        listStatus = cmdline("legendary status 2>/dev/null")
        returnString += listStatus.replace(':', '=')
        listGamesAvailable = cmdline("legendary list 2>/dev/null") # | sed '/^$/d'")
        #for line in listGames:
        returnString += listGamesAvailable.replace(' (', '=(')
        listGamesInstalled = cmdline("legendary list-installed 2>/dev/null") # | sed '/^$/d'")
        #for line in listGames:
        returnString += listGamesInstalled.replace(' (', '=(').replace('Platform: Windows | ', '').replace('->', '=->')
    else:
        returnString += "\n" + _("legendary install directory not found.")
    return returnString

def ItchInfo() -> str:
    try:
        mypath = os.path.expanduser("~/.config/itch/")
        with open("/usr/share/itch/package.json", "r") as json_file:
            json_data = json.load(json_file)
            #print(json_data['version'])

        butler_path = os.path.join(mypath, "broth/butler/versions/")
        butler_version = [d for d in listdir(butler_path) if isdir(join(butler_path, d))][0]
        setup_path = os.path.join(mypath, "broth/itch-setup/versions/")
        setup_version = [d for d in listdir(setup_path) if isdir(join(setup_path, d))][0]

        returnString = f'itch {_("version")}:={json_data["description"]} {json_data["version"]}\n'
        returnString += f'=butler {str(butler_version)}\n'
        returnString += f'=itch-setup {str(setup_version)}\n\n'

        conn = sqlite3.connect(os.path.join(mypath, 'db/butler.db'))
        cursor = conn.execute("SELECT g.id, g.title FROM games g, caves c WHERE g.id = c.game_id AND g.classification='game'")
        returnString += _("Games")
        rownum = 0
        for row in cursor:
            rownum += 1
            returnString += "=" + row[1] + "\n"
        if rownum == 0:
            returnString += "=" + "(none)" + "\n"

        cursor = conn.execute("SELECT g.id, g.title FROM games g, caves c WHERE g.id = c.game_id AND g.classification='tool'")
        returnString += "\n" + _("Tools")
        #print(cursor.rowcount)
        rownum = 0
        for row in cursor:
            rownum += 1
            returnString += "=" + row[1] + "\n"
        if rownum == 0:
            returnString += "=" + "(none)" + "\n"

        conn.close()
    except (sqlite3.OperationalError, FileNotFoundError):
        returnString += "\n" + _("Itch install directory not found.")
    return returnString

def FlatpakInfo() -> str:
    output = cmdline("flatpak --version | cut -d ' ' -f2")
    returnString = f'Flatpak {_("version")}:\t\t\t{output}\n'

    folders = ["~/.local/share/flatpak", "~/.var/app", "/var/lib/flatpak", "/etc/flatpak/installations.d"]
    for folder in folders:
        returnString += str(folder) + ":="
        if os.path.isdir(os.path.expanduser(str(folder))):
            pathToPrefix = Path(os.path.expanduser(folder))
            sumBytesPrefix = sum(f.stat().st_size for f in pathToPrefix.glob('**/*') if f.is_file() and not f.is_symlink())
            returnString += _("Yes") + " (" + bytes2human(sumBytesPrefix,format="%(value)3.1f %(symbol)s", symbols="iec") + "B)\n"
            # returnString += _("Yes") + "\n"
        else:
            returnString += _("No") + "\n"

    mypath = os.path.expanduser(folders[0])  # = ~/.local/share/flatpak
    if os.path.exists(mypath):
        #returnString += _("Games")
        #listStatus = cmdline("flatpak list 2>/dev/null")
        #returnString += listStatus.replace(':', '=')
        listAppsAvailable = cmdline("flatpak list 2>/dev/null").split('\n') # | sed '/^$/d'")
        listAppsAvailable = [l.split('\t') for l in listAppsAvailable]
        returnString += "\n" + tabulate.tabulate(listAppsAvailable, tablefmt="tsv") # .replace('	', '=')
    else:
        returnString += "\n" + _("flatpak install directory not found.")
    return returnString
