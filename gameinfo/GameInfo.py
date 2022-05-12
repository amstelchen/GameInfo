#!/usr/bin/env python

from .__init__ import *

from .Version import __appname__, __version__, __author__, __licence__
from .AppDebug import AppDebug
from .PrintInfo import cmdline, PrintAbout, PopulateMenuitems, ReplaceIconname, ListTools
from .PrintInfo import GetDistributionKind, GetDistributionId
from .PrintInfo import WineInfo, SteamInfo, ProtonInfo, DOSBoxInfo, LutrisInfo, GOGInfo, ScummVMInfo
from .Desktop import get_desktop_environment, is_running

AppDebug.debug_print(f'{__appname__} {__version__}')
AppDebug.debug_print(f"DistributionKind: {GetDistributionKind()}")

try:
    # localedir=os.path.dirname(__file__) + '/locales'
    #gettext = gettext.translation('gameinfo', localedir='/usr/share/locale', languages=['de'])
    gettext = gettext.translation('gameinfo', languages=['de'])
    gettext.install("gameinfo")
    _ = gettext.gettext
except FileNotFoundError as e:
    debug_print(e)
    
#menuSystem = ["Linux Kernel", "Linux Distro", "CPU", "GPU", "Vulkan", "OpenGL", "VDPAU", "VA-API"]

#menuReturn = []

#with open('GameInfo.json') as json_file:
#    data = json.load(json_file)
#    print(data)

file = minidom.parse(os.path.join(os.path.dirname(__file__), "GameInfo.xml"))
menus = file.getElementsByTagName('menu')
for menu in menus:
    pass
    #print(menu.firstChild.data)
    #print(menu.attributes['value'].value)
    #if menu.getAttribute('menuitem') == 'Levels':
    #    llist = menu.getElementsByTagName('l')
    #    l = llist.item(level)

menuPlatforms = ["Tools", "Steam", "Proton", "Wine", "DOSBox", "Lutris", "GOG", "ScummVM", "Epic Games", "Battle.net"]

menuGameInfo = [_("Help"), _("About")]

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
        self.fillTreeview(selection="Distro")

    def __init__(self, master=None):

        winSize = (1024, 768)
        ttk.Window.__init__(self, master, size=winSize, minsize=winSize, iconphoto = os.path.join(os.path.dirname(__file__), "images", "GameInfo.png"))

        self.title(f'{__appname__} {__version__}')

        #self.themename = "flatly"
        #self.iconphoto = "GameInfo.png"

        style = ttk.Style()
        style.configure("mystyle.Treeview.Left", highlightthickness=0, bd=0, font=('Sans Regular', 12)) # Modify the font of the body
        style.configure("mystyle.Treeview.Right", highlightthickness=0, bd=0, font=('Monospace', 10)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
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
        self.updateWidgets(textPane="Distro")

    def TreeElementClicked(self, event):
        selectedTreeWidget = event.widget
        selection = [selectedTreeWidget.item(item)["text"] for item in selectedTreeWidget.selection()]
        AppDebug.debug_print(_("Selected entry") + ": " + str(selection))

        self.updateWidgets(textPane=selection)

    def updateWidgets(self, textPane):
        self.fillTreeview(textPane)

    def fillTreeview(self, selection="Distro"):

        returnString = ""
        splitChar = ":"
        linesIgnore = 0
        columnWidth = 400

        treeRight = self.winfo_children()[3]
        treeRight.delete(*treeRight.get_children())
        treeRight.column("#0", width=columnWidth, minwidth=columnWidth, stretch=ttk.NO)

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

        if selection == "Kernel":
            splitChar = "="
            #linesIgnore = 2

        if selection == "Distro": #"Linux Distro"
            returnString = returnString.replace('\"','')
            returnString+= "$DESKTOP_SESSION=" + get_desktop_environment(self)
            splitChar = "="
            #linesIgnore = 1000

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
            columnWidth = 600

        if selection == "VA-API":
            splitChar = ":\t"
            linesIgnore = 0

        if selection == "VDPAU":
            splitChar = "\t"
            #linesIgnore = 1000
            columnWidth = 900

        if selection == "OpenGL":
            splitChar = ": "

        if selection == "OpenCL":
            #returnString.replace("     ", " ")
            pass

        if selection == "Steam":
            returnString = SteamInfo()
            splitChar = "="
            columnWidth = 350

        if selection == "Wine":
            returnString = WineInfo()
            splitChar = "="
            columnWidth = 300

        if selection == "Proton":
            returnString = ProtonInfo()
            splitChar = "="
            columnWidth = 350

        if selection == "DOSBox":
            returnString = DOSBoxInfo()
            splitChar = "="
            columnWidth = 300

        if selection == "Lutris":
            returnString = LutrisInfo()
            splitChar = "="
            columnWidth = 300

        if selection == "GOG":
            returnString = GOGInfo()
            splitChar = "="
            columnWidth = 300

        if selection == "ScummVM":
            returnString = ScummVMInfo()
            splitChar = "="
            columnWidth = 300

        if selection in ("Epic Games", "Battle.net"): #, "Steam"):
            returnString = str(selection) + " " + _("not yet implemented, sorry.")

        if selection in (_("System"), _("Platforms"), "GameInfo"):
            returnString = _("Please select a sub-category.") + ":"

        if selection == _("Help"):
            returnString = _("Not yet implemented.")
            columnWidth = 900

        if selection == _("About"):
            returnString = PrintAbout()
            splitChar = "---"
            columnWidth = 900

        if selection == "Tools":
            returnString = ListTools()
            splitChar = "|"
            linesIgnore = 0

        zeile = 1
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
                columnWidth = 300

                icon_name = part1
                icon_name = ReplaceIconname(icon_name)

                icon_theme = Gtk.IconTheme.get_default()
                icon_info = icon_theme.lookup_icon(icon_name, 32, 0)

                if icon_info != None:
                    image_filename = icon_info.get_filename()
                else:
                    AppDebug.debug_print("No file for " + icon_name + " :-(")
                    image_filename = os.path.join(os.path.dirname(__file__), "images", "GameInfo.png")

                    photo = None
                    
                    if "svg" in image_filename:
                        image_data = cairosvg.svg2png(url=image_filename)
                        image = (Image.open(io.BytesIO(image_data)))
                        photo = image.resize((32, 32), Image.Resampling.LANCZOS) #, Image.ANTIALIAS)
                        photo = ImageTk.PhotoImage(photo)
                    if "png" in image_filename:
                        image = Image.open(image_filename)
                        photo = image.resize((32, 32), Image.Resampling.LANCZOS) #, Image.ANTIALIAS)
                        photo = ImageTk.PhotoImage(photo)

            treeRight.insert("", index=zeile, text=part1, values=(part2, ""), tags=(tag,))
            zeile += 1
        pass

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
        treeRight.column("#0", width=columnWidth, minwidth=350, stretch=ttk.NO)

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

        f = ttk.Frame()
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

        folder2=treeLeft.insert("", cnt, 200, text="GameInfo", open=True) #, values=("23-Jun-17 11:05","File folder",""))
        for entry in menuGameInfo:
            treeLeft.insert(200, cnt + 1, text=entry) #, values=("23-Jun-17 11:25","TXT file","1 KB"))
            cnt += 1

        m2 = ttk.PanedWindow(m1, orient=ttk.VERTICAL, width=1000,height=self.winfo_height())
        m2.pack(side=TOP)
        #m1.add(m2, minsize=100)
        m1.add(m2)

        #top = tk.Label(m2, text=textPane, font="Sans 20")
        treeRight = ttk.Treeview(style="mystyle.Treeview.Right", name="right_tree")
        
        treeRight["columns"]=("pic", "#0", "#1")
        treeRight.column("pic", width=400, minwidth=400, stretch=ttk.NO)
        treeRight.column("#0", width=400, minwidth=400, stretch=ttk.NO)
        treeRight.column("#1", width=500, minwidth=500, stretch=ttk.NO)
        treeRight.pack(side=TOP)

        treeRight.tag_configure("evenrow",background='white smoke',foreground='black')
        treeRight.tag_configure("oddrow",background='white',foreground='black')

        m2.add(treeRight)
