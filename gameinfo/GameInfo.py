#!/usr/bin/env python

from .__init__ import *

from .Version import __appname__, __version__, __author__, __licence__
from .AppDebug import AppDebug, WaitMessage
from .Functions import cmdline, PrintAbout, PopulateMenuitems, ReplaceIconname, ListTools
from .Functions import ParseMachineTags, GetDistributionKind, GetDistributionId, GetDistributionLogoName, GetDistributionLogoImage, GetDesktopLogoImage
from .Functions import WineInfo, PlayOnLinuxInfo, SteamInfo, ProtonInfo, DOSBoxInfo, LutrisInfo, GOGInfo, ScummVMInfo, EpicGamesInfo, ItchInfo, FlatpakInfo
from .Desktop import get_desktop_environment, is_running
from .Fallout import FalloutInfo
from .Doom import DoomInfo
from .Dune import DuneInfo
from .SteamLogs import SteamLogs

AppDebug.debug_print(f'{__appname__} {__version__}')
AppDebug.debug_print(f"DistributionKind: {GetDistributionKind()}")

try:
    # localedir=os.path.dirname(__file__) + '/locales'
    #gettext = gettext.translation('gameinfo', localedir='/usr/share/locale', languages=['de'])
    gettext = gettext.translation('gameinfo', localedir=os.path.join(os.path.dirname(__file__), 'locales'))
    gettext.install("gameinfo")
    _ = gettext.gettext
except FileNotFoundError as e:
    debug_print(e)
    
file = minidom.parse(os.path.join(os.path.dirname(__file__), "GameInfo.xml"))
menus = file.getElementsByTagName('menu')
for menu in menus:
    pass

menuPlatforms = ["Tools", "Steam", "Proton", "Wine", "PlayOnLinux", "DOSBox", "Lutris", "GOG", "ScummVM", "Epic Games", "itch.io", "Flatpak"]
menuPlugins = ["Fallout", "Doom", "Dune", "SteamLogs"]
menuGameInfo = [_("Help"), _("About")]
WaitMessage = _("Fetching system info, this can take a second...")

class Application(ttk.Window):
    def dic_imgs(self):
        imgs = {}
        for i in glob.glob("icons/*.png"):
            pathfile = i
            i = os.path.basename(i)
            name = i.split(".")[0]
            imgs[name] = PhotoImage(file=pathfile)
        return imgs
    
    def callback(self):
        AppDebug.debug_print("called the callback!")
            
    def open_info(self):
        #self.createWidgets(textPane=_("About"))
        self.fillTreeview(selection=_("About"))

    def refresh(self):
        #self.createWidgets(textPane="Distro")
        self.fillTreeview(selection="Tools") # was "Machine"

    def __init__(self, master=None):

        winSize = (1280, 870)
        ttk.Window.__init__(self, master, size=winSize, minsize=winSize, iconphoto = os.path.join(os.path.dirname(__file__), "images", "GameInfo.png"))

        self.title(f'{__appname__} {__version__}')

        #self.themename = "flatly"
        #self.iconphoto = "GameInfo.png"

        style = ttk.Style()
        style.configure("mystyle.Treeview.Left", highlightthickness=0, bd=0, font=('Sans Regular', 12)) # Modify the font of the body
        style.configure("mystyle.Treeview.Right", highlightthickness=0, bd=0, font=('Monospace', 10)) # Modify the font of the body
        style.configure("mystyle.Treeview.Right", highlightthickness=0, bd=0, font=('Monospace', 10)) # Modify the font of the body
        style.layout("mystyle.Treeview.Left", [('mystyle.Treeview.Left.treearea', {'sticky': 'nswe'})]) # Remove the borders
        style.layout("mystyle.Treeview.Right", [('mystyle.Treeview.Right.treearea', {'sticky': 'nswe'})]) # Remove the borders

        #style = ttk.Style(theme='united')

        themes = ""
        for theme in style.theme_names():
            themes += str(theme) + " "
        AppDebug.debug_print(_("Themes loaded") + ": " + themes)

        w = 1024 # width for the Tk root
        h = 768 # height for the Tk root

        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        #self.size = (ws, hs)
        #self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.size = winSize
        self.position_center()

        self.createWidgets()
        # self.updateWidgets(textPane="Tools") # was "Machine"

    def TreeElementClicked(self, event):
        selectedTreeWidget = event.widget
        selection = [selectedTreeWidget.item(item)["text"] for item in selectedTreeWidget.selection()]
        AppDebug.debug_print(_("Selected entry") + ": " + str(selection))

        self.updateWidgets(textPane=selection)

    def updateWidgets(self, textPane):
        self.fillTreeview(textPane)

    def fillTreeview(self, selection="Tools"): # was "Machine"

        returnString = ""
        splitChar = ":"
        linesIgnore = 0
        firstColumnWidth = 400
        secondColumnWidth = 900
        rowHeight = 20

        sl = self.winfo_children()[3].place_slaves()
        for s in sl: s.destroy()

        treeRight = self.winfo_children()[3]
        treeRight.delete(*treeRight.get_children())
        treeRight.column("#0", width=firstColumnWidth, minwidth=firstColumnWidth, stretch=ttk.NO)

        if isinstance(selection, list):
            selection = str(selection[0])

        menuitems = PopulateMenuitems()

        for item in menuitems:
            name = item.attributes["value"].value
            if name == selection:
                returnString = item.attributes["command"].value
                splitChar = item.attributes["splitChar"].value
                try:
                    linesIgnore = int(item.attributes["linesIgnore"].value)
                except:
                    linesIgnore = 0
                break

        selectedSet = returnString
        #selectedSet = menuitems["Distro"]
        #selectedSet = menuitems.attributes["value"].value

        if selection == "Machine":
            splitChar = ":"
            returnString = ParseMachineTags(returnString)

        if selection == "Distro": #"Linux Distro"
            strDesktopEnvironment = get_desktop_environment(self)
            self.temp_imgs_logos = []
            returnString = returnString.replace('\"','')
            returnString+= "$DESKTOP_SESSION=" + get_desktop_environment(self)
            splitChar = "="
            rowHeight=20
            #linesIgnore = 1000
            self.temp_imgs_logos.append(GetDistributionLogoImage(GetDistributionLogoName()))
            panel1 = ttk.Label(self.winfo_children()[3], image = self.temp_imgs_logos[0], border=0)
            panel1.place(x = 10, y = 300, width=64, height=64)
            self.temp_imgs_logos.append(GetDesktopLogoImage(strDesktopEnvironment))
            panel2 = ttk.Label(self.winfo_children()[3], image = self.temp_imgs_logos[1], border=0)
            panel2.place(x = 100, y = 300, width=64, height=64)
            
            #treeRight.insert("", 0, text="", values=("", ""), image=self._photo)
            #print(self.temp_imgs)

        if selection == "Kernel":
            splitChar = "="
            #linesIgnore = 2

        if selection == "CPU":
            splitChar = ":"
            #linesIgnore = 1000

        if selection == "GPU":
            returnString = returnString.replace(': ','|')
            returnString = returnString.replace(' at','|at')
            splitChar = "|"
            #linesIgnore = 1000

        if selection == "PCI":
            #splitChar = ": "
            pass

        if selection == "USB":
            #splitChar = ":"
            pass

        if selection == "Display":
            splitChar = ":"

        if selection == "Vulkan":
            returnString= returnString.replace('\t', "  ")
            returnString= returnString.replace('Vulkan version', ":\nVulkan version")
            returnString= returnString.replace('lay) V', "lay):\nV")
            firstColumnWidth = 600

        if selection == "VA-API":
            splitChar = ":\t"
            linesIgnore = 0

        if selection == "VDPAU":
            splitChar = "\t"
            #linesIgnore = 1000
            firstColumnWidth = 900

        if selection == "OpenGL":
            splitChar = ": "

        if selection == "OpenCL":
            #returnString.replace("     ", " ")
            pass

        if selection == "Sensors":
            splitChar = "\t"
            #linesIgnore = 1000
            firstColumnWidth = 900
            secondColumnWidth = 0

        if selection == "Input":
            splitChar = "="
            endString = ""
            try:
                for line in returnString.split("\n"):
                    if len(line) == 0:
                        break
                    #print(line,flush=True)
                    splitString = line.split(':', maxsplit=1)[1]
                    if "=" in splitString:
                        endString += splitString.replace('\"', '') + "\n"
                    #if "UNIQ" in splitString:
                        #splitString = splitString.replace("UNIQ", "\n")
                    if "MODALIAS" in splitString:
                        endString += "=\n"
                returnString = endString
            except IndexError:
                pass

        if selection == "Steam":
            returnString = SteamInfo()
            splitChar = "="
            firstColumnWidth = 300

        if selection == "Wine":
            returnString = WineInfo()
            splitChar = "="
            firstColumnWidth = 300

        if selection == "PlayOnLinux":
            returnString = PlayOnLinuxInfo()
            splitChar = "="
            firstColumnWidth = 300

        if selection == "Proton":
            returnString = ProtonInfo()
            splitChar = "="
            firstColumnWidth = 350

        if selection == "DOSBox":
            returnString = DOSBoxInfo()
            splitChar = "="
            firstColumnWidth = 300

        if selection == "Lutris":
            returnString = LutrisInfo()
            splitChar = "="
            firstColumnWidth = 300

        if selection == "GOG":
            returnString = GOGInfo()
            splitChar = "="
            firstColumnWidth = 300

        if selection == "ScummVM":
            returnString = ScummVMInfo()
            splitChar = "="
            firstColumnWidth = 300

        if selection == "Epic Games":
            returnString = EpicGamesInfo()
            splitChar = "="
            firstColumnWidth = 250
            secondColumnWidth = 700

        if selection == "itch.io":
            returnString = ItchInfo()
            splitChar = "="
            firstColumnWidth = 300

        if selection == "Flatpak":
            returnString = FlatpakInfo()
            splitChar = "="
            firstColumnWidth = 1000

        if selection in ("Battle.net"):
            returnString = str(selection) + " " + _("not yet implemented, sorry.")

        if selection in (_("System"), _("Platforms"), _("Plugins"), "GameInfo"):
            returnString = _("Please select a sub-category.") + ":"

        if selection == _("Fallout"):
            returnString = FalloutInfo()
            splitChar = "="
            firstColumnWidth = 300

        if selection == _("Doom"):
            returnString = DoomInfo()
            splitChar = "="
            firstColumnWidth = 500

        if selection == _("Dune"):
            returnString = DuneInfo()
            splitChar = "="
            firstColumnWidth = 500

        if selection == _("SteamLogs"):
            returnString = SteamLogs()
            splitChar = "="
            firstColumnWidth = 500

        if selection == _("Help"):
            returnString = _("Not yet implemented.")
            firstColumnWidth = 900

        if selection == _("About"):
            returnString = PrintAbout()
            splitChar = "---"
            firstColumnWidth = 900

        if selection == "Tools":
            treeRight.insert("", 0, text=WaitMessage, values=(""), tags=("evenrow"))
            self.update()
            returnString = ListTools()
            treeRight.delete(*treeRight.get_children())
            splitChar = "|"
            linesIgnore = 0
            rowHeight = 32

        zeile = 1
        self.temp_imgs = []

        self.style.configure("mystyle.Treeview.Right", highlightthickness=0, bd=0, font=('Monospace', 10), rowheight=rowHeight)
        self.style.layout("mystyle.Treeview.Right", [('mystyle.Treeview.Right.treearea', {'sticky': 'nswe'})])
        for line in returnString.splitlines():

            if zeile % 2 == 0:
                tag = "evenrow"
            else:
                tag = "oddrow"

            if zeile > linesIgnore:
                part1 = line.split(splitChar, 1)[0]
                try:
                    part2 = line.split(splitChar, 1)[1]
                except:
                    part2 = ""

            if selection == "Tools":
                firstColumnWidth = 300
                secondColumnWidth = 900

                icon_name = part1
                part1 = "  " + part1
                icon_name = ReplaceIconname(icon_name)

                icon_theme = Gtk.IconTheme.get_default()
                icon_info = icon_theme.lookup_icon(icon_name, 32, 0)
                AppDebug.debug_print("icon_name: " + icon_name)

                if icon_info != None:
                    image_filename = icon_info.get_filename()
                    AppDebug.debug_print("image_filename: " + image_filename)
                else:
                    AppDebug.debug_print("No file for " + icon_name + " :-(")
                    image_filename = os.path.join(os.path.dirname(__file__), "images", "GameInfo.png")
                    photo = None
                    
                #if image_filename.find("/org/gtk") == 0:
                #    image_filename = os.path.join(os.path.dirname(__file__), "images", "GameInfo.png")
                #    photo = None
                #    AppDebug.debug_print(image_filename + " ist leer")

                if "svg" in image_filename:
                    image_data = cairosvg.svg2png(url=image_filename)
                    image = (Image.open(io.BytesIO(image_data)))
                    photo = image.resize((32, 32), Image.Resampling.LANCZOS) #, Image.ANTIALIAS)
                    self._photo = ImageTk.PhotoImage(photo)
                    self.temp_imgs.append(self._photo)
                if "png" in image_filename:
                    image = Image.open(image_filename)
                    photo = image.resize((32, 32), Image.Resampling.LANCZOS) #, Image.ANTIALIAS)
                    self._photo = ImageTk.PhotoImage(photo)
                    self.temp_imgs.append(self._photo)

                #AppDebug.debug_print("len: " + str(len(temp_imgs)))
                treeRight.insert("", index=zeile, text=part1, values=(part2, ""), tags=(tag,), image=self.temp_imgs[zeile - 1])
            else:
                treeRight.insert("", index=zeile, text=part1, values=(part2, ""), tags=(tag,))
            zeile += 1

        #for line in selectedSet.splitlines():
            #icon_theme = Gtk.IconTheme()
            #ico = icon_theme.get_default()
            #icon_theme = Gtk.Settings.get_default()
            #print(Gtk.Settings.get_default().get_property("gtk-icon-theme-name"))
            #AppDebug.debug_print("")
            #print(icon_info.get_filename())
            #AppDebug.debug_print("")
            #itemx = treeView.insert("", index=zeile, text=part1, values=(part2, ""), tags=(tag,))
            #zeile += 1
            #continue
            #AppDebug.debug_print("  Füge " + icon_name + " in den Baum zu Index " + str(zeile) + " hinzu...")
            #AppDebug.debug_print(pprint(photo))
            #itemx = treeRight.insert("", index=zeile, text=part1, values=(part2, ""), tags=(tag,), image=photo)
            #AppDebug.debug_print("  ok! " + str(type(photo)))
            #AppDebug.debug_print("...fehlgeschlagen")
            #itemx = treeRight.insert("", index=zeile, text=part1, values=(part2, ""), tags=(tag,))
            #
            #print(zeile)'''
        treeRight.column("#0", width=firstColumnWidth, minwidth=firstColumnWidth, stretch=ttk.NO)
        treeRight.column("#1", width=secondColumnWidth, minwidth=secondColumnWidth, stretch=ttk.NO)

    def mycallback(self, event):
 
        _iid = self.treeLeft.identify_row(event.y)
 
        if _iid != self.last_focus:
            if self.last_focus:
                self.tree.item(self.last_focus, tags=[])
            self.tree.item(_iid, tags=['focus'])
            self.last_focus = _iid

    def clear_frame(self):
        for widgets in self.winfo_children():
            #if widgets.widgetName == "ttk:treeview":
            widgets.destroy()
      
    def createWidgets(self):

        #self.clear_frame()

        f = ttk.Frame(master=self)
        f.pack(side=BOTTOM)

        b2 = ttk.Button(f, text=_("Refresh"), bootstyle="warning", width=10, command=self.refresh) #self.createWidgets("Distro"))
        b2.pack(side=RIGHT, padx=5, pady=10, anchor=ttk.SE)

        b3 = ttk.Button(f, text=_("About"), bootstyle="info", width=10, command=self.open_info)
        b3.pack(side=RIGHT, padx=5, pady=10, anchor=ttk.SE)

        b4 = ttk.Button(f, text=_("Quit"), bootstyle="danger", width=10, command=self.quit)
        b4.pack(side=RIGHT, padx=5, pady=10, anchor=ttk.SE)

        m1 = ttk.PanedWindow(self, orient="horizontal",width=250)
        m1.pack(fill=ttk.BOTH, expand=250, side=TOP)

        treeLeft = ttk.Treeview(style="mystyle.Treeview.Left")
        treeLeft.pack(fill=X, side=LEFT)

        treeLeft.bind("<<TreeviewSelect>>", self.TreeElementClicked)

        treeLeft.column("#0", width=150, minwidth=150, stretch=ttk.NO)
        treeLeft.pack(side=ttk.LEFT,fill=ttk.X)

        # Level 1
        folder1=treeLeft.insert("", 0, 0, text="System", open=True) #, values=("23-Jun-17 11:05","File folder",""))
        cnt = 0
        menuitems = file.getElementsByTagName('menuitem')
        for menuitem in sorted(menuitems, key=lambda menuitem: int(menuitem.attributes['id'].value)):
            #pixbuf = Gtk.IconTheme.get_default().load_icon(icons[0], 64, 0) 
            item = treeLeft.insert(0, cnt + 1, text=menuitem.attributes['value'].value) #,image=ImageTk.PhotoImage(pixbuf))
            #image_show_2.set_from_pixbuf(pixbuf)
            cnt += 1
        cnt = 100
        folder2=treeLeft.insert("", cnt, 100, text=_("Platforms"), open=True) #, values=("23-Jun-17 11:05","File folder",""))
        for entry in menuPlatforms:
            treeLeft.insert(100, cnt + 1, text=entry) #, values=("23-Jun-17 11:25","TXT file","1 KB"))
            cnt += 1

        m1.add(treeLeft)

        folderPlugins=treeLeft.insert("", cnt, 200, text="Plugins", open=True) #, values=("23-Jun-17 11:05","File folder",""))
        for entry in menuPlugins:
            treeLeft.insert(200, cnt + 1, text=entry) #, values=("23-Jun-17 11:25","TXT file","1 KB"))
            cnt += 1

        folder2=treeLeft.insert("", cnt, 300, text="GameInfo", open=True) #, values=("23-Jun-17 11:05","File folder",""))
        for entry in menuGameInfo:
            treeLeft.insert(300, cnt + 1, text=entry) #, values=("23-Jun-17 11:25","TXT file","1 KB"))
            cnt += 1

        m2 = ttk.PanedWindow(m1, orient=ttk.VERTICAL, width=1000,height=self.winfo_height())
        m2.pack(side=TOP)
        #m1.add(m2, minsize=100)
        m1.add(m2)

        #top = tk.Label(m2, text=textPane, font="Sans 20")
        treeRight = ttk.Treeview(style="mystyle.Treeview.Right", name="right_tree")
        
        treeRight["columns"]=("#0", "#1")
        #treeRight.column("pic", width=400, minwidth=400, stretch=ttk.NO)
        treeRight.column("#0", width=400, minwidth=400, stretch=ttk.NO)
        treeRight.column("#1", width=500, minwidth=500, stretch=ttk.NO)
        treeRight.pack(side=TOP)

        treeRight.tag_configure("evenrow",background='white smoke',foreground='black')
        treeRight.tag_configure("oddrow",background='white',foreground='black')

        m2.add(treeRight)

        #main_logo = Image.open(os.path.join(os.path.dirname(__file__), "images", "GameInfo.png"))
        main_logo = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "images", "GameInfo.png"))
        panel_logo = ttk.Label(treeRight, image = main_logo, border=0, padding=0,
            text=f'{__appname__} {__version__}', compound='top', 
            background='white', font='Calibri 16') #, style="mystyle.LogoLabel")
        panel_logo.image = main_logo
        panel_logo.text = "TODO"
        x_logo = treeRight.winfo_width() // 2 + 256
        y_logo = self.winfo_height() // 2 - 256 - 100
        panel_logo.place(x = x_logo, y = y_logo)

