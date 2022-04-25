#!/usr/bin/env python

from pprint import pprint

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
#from gi.repository.GdkPixbuf import Pixbuf

import tkinter as tk
#from tkinter import ttk
#import tkinter.ttk as ttk
#from ttkthemes import ThemedTk
from PIL import Image, ImageTk

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import os, sys, re, io
import sysconfig
from subprocess import PIPE, Popen, check_output
import subprocess
import json
from xml.dom import minidom
import string

from os import listdir
from os.path import isfile, join

import gettext
import cairosvg

import sqlite3

from .AppDebug import AppDebug
#import AppDebug
#from AboutDialog import AboutDialog

VERSION = "1.0.5"

__appname__ = "GameInfo"
__version__ = VERSION
__author__ = "Michael John"
__licence__ = \
'Copyright © 2022 Michael John <michael.john@gmx.at>\n' \
'Lizenz GPLv3: GNU GPL Version 3 oder neuer <https://gnu.org/licenses/gpl.html>\n' \
'Dies ist freie Software; es steht Ihnen frei, sie zu verändern und weiterzugeben.\n' \
'Es gibt KEINE GARANTIE, soweit als vom Gesetz erlaubt.\n' \
'Geschrieben von Michael John.'

AppDebug.debug_print(f'{__appname__} {__version__}')

try:
    # localedir=os.path.dirname(__file__) + '/locales'
    #gettext = gettext.translation('gameinfo', localedir='/usr/share/locale', languages=['de'])
    gettext = gettext.translation('gameinfo', languages=['de'])
    gettext.install("gameinfo")
    _ = gettext.gettext
except FileNotFoundError as e:
    debug_print(e)
    
def cmdline(command):
    process = Popen(args=command, stdout=PIPE, shell=True, universal_newlines=True) #text_mode = True
    #process.text_mode = True
    return process.communicate()[0]

def open_info():
    #tk.messagebox.showinfo("hi")
    #msg = tk.messagebox.Dialog("hi")

    #dialog_Option = AboutDialog()
    #self.SetTopWindow(self.dialog_Event)
    #dialog_Option.ShowModal()
    #dialog_Option.Destroy()
    return True

def refresh():
    #Application.createWidgets(textPane="Distro")
    pass

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

menuitems = file.getElementsByTagName('menuitem')
for menuitem in menuitems:
    #print(menu.firstChild.data)
    #print(menuitem.attributes['value'].value)
    #print(menuitem.attributes['command'].value)
    #print(menuitem.attributes['splitChar'].value)
    #menuReturn.append(menuitem.attributes['value'].value)
    #menuReturn.append(cmdline(menuitem.attributes['command'].value))
    menuitem.attributes['command'].value = cmdline(menuitem.attributes['command'].value)
    pass

menuPlatforms = ["Tools", "Steam", "Proton", "Wine", "DOSBox", "Lutris", "GOG", "ScummVM", "Epic Games", "Battle.net"]

menuGameInfo = [_("Help"), _("About")]

#print(sysconfig.get_python_version())
#print(sys.version)

AppDebug.debug_print(_("Fetching system info, this can take a second..."))
toolitems = file.getElementsByTagName('toolitem')
outputALLE = str("")
for toolitem in toolitems:
    command = toolitem.attributes["command"].value
    version = toolitem.attributes["version"].value
    AppDebug.debug_print(_("Checking for") + " " + command)
    if command.find("!") == -1:
        toolResult = cmdline(str(command + " " + version))
    else:
        toolResult = cmdline(str(version))
    #toolResult = toolResult.decode('utf-8')
    #splitChar = item.attributes["splitChar"].value
    #outputALLE += command + "-" + toolResult + "\n"
    if toolResult.find(command.replace('!','')) == -1:
        outputALLE += command.replace('!','') + "-" + toolResult
    else:
        outputALLE += toolResult

#AppDebug.debug_print(outputALLE)

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
            
    def __init__(self, master=None):

        winSize = (1024, 768)
        ttk.Window.__init__(self, master, size=winSize, minsize=winSize, iconphoto = os.path.join(os.path.dirname(__file__), "GameInfo.png"))

        self.title(f'{__appname__} {__version__}')

        #self.themename = "flatly"
        #self.iconphoto = "GameInfo.png"

        self.size = winSize

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

        #tt = tk.Tk()
        #master = ttk.Frame(size=winSize)

        #theme = ThemedTk.themes('ubuntu')
        #self.master.theme_use('ubuntu')
        #t = thtk.ThemedTk()

        #s = ttk.Style(self.master)
        #s.theme_use('clam')
        #print(s.theme_names())

        #style = ttk.Style()
        #style.theme_use('yaru')
        #self.master.style = style

        #myimage_16 = tk.PhotoImage(file="GameInfo.png")  
        #tt.iconbitmap = tk.PhotoImage(file='GameInfo.png')
        #tt.iconbitmap('GameInfo.png')
        #icon = tk.Tk().iconbitmap('GameInfo.png')
        #tk.Tk().call('wm', 'iconphoto', self._root.w, tk.PhotoImage(file='GameInfo.png'))

        #self.grid()
        
        w = 1024 # width for the Tk root
        h = 568 # height for the Tk root

        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        #self.size = (ws, hs)

        self.position_center()

        # set the dimensions of the screen 
        # and where it is placed
        #self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        #a.master.iconbitmap(myimage_16)
        #self.master.iconphoto(False, myimage_16) # finally works now :-)
        #print("debug")

        self.createWidgets(textPane="Distro")

    def print_element(self, event):
        tree = event.widget
        selection = [tree.item(item)["text"] for item in tree.selection()]
        AppDebug.debug_print(_("Selected entry") + ": " + str(selection))

        #m2.add(tree)       
        #app.master.m2.add(tree)
        #self.updateWidgets(self.master.treeRight, selection)

        #self.fillTreeview(self.master.treeRight, selection)

        self.createWidgets(textPane=selection)

    def updateWidgets(self, treeView, selection):
        #for label in filter(lambda w:isinstance(w,Label), frame.children.itervalues()):
        idx = 0
        #for tv in filter(lambda w:isinstance(w,ttk.Treeview), self.master.winfo_children()):
        #for child in self.master.winfo_children():
            #print(tv, str(tv.index))
            #print(type(tv))
            #if idx == 1:
                #tv.destroy()
                #tv.delete(*tv.get_children())
            #idx += 1
            #if tv._index == 0:
            #    print("bla")
        #for elem in self.m:
        #    print(elem)
        #self.createWidgets()
        self.fillTreeview(treeView, selection)

        #self.master.top.text = "bla"
        
        #for la in filter(lambda w:isinstance(w,tk.Label), self.master.winfo_children()):
            #la.destroy()
            #la.text = selection

        #self.pack_slaves(0).text = selection

        #top = tk.Label(self.m2, text="top pane", font="Times 20 italic bold")
        #top.pack()

    def fillTreeview(self, treeView, selection="Distro"):

        #selectedSet = outputDISTRO

        returnString = ""
        splitChar = ":"
        linesIgnore = 0

        #print(type(selection))
        if isinstance(selection, list):
            selection = str(selection[0])

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

        if selection == "Kernel": #"Linux Kernel"
            splitChar = "="
            linesIgnore = 2
        if selection == "Distro": #"Linux Distro"
            returnString+= "$DESKTOP_SESSION=" + self.get_desktop_environment()
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
        #if selection == "PCI":
        #    splitChar = ": "
        #if selection == "USB":
        #    splitChar = ":"

        if selection == "Vulkan":
            returnString= returnString.replace('\t', "  ")
        if selection == "VA-API":
            #returnString = returnString.replace("       ", " ")
            #returnString = " ".join(returnString).splitlines()
            #for line in returnString:
            #    returnString += " ".join(line).split()
            #returnString= " ".join(returnString).split() #.trim(" ") #.replace("   ", " ")
            splitChar = ":\t"
            linesIgnore = 0
        if selection == "VDPAU":
            splitChar = "\t"
            #linesIgnore = 1000
        if selection == "OpenGL":
            splitChar = ": "
        if selection == "OpenCL":
            #returnString.replace("     ", " ")
            pass
        if selection == "Tools":
            returnString = outputALLE
            splitChar = "-"
            linesIgnore = 0

        if selection == "Wine":
            returnString = "WINE version:" + cmdline("wine --version ; echo")
            #prefixes = ["$HOME/.wine", "$HOME/.wine32", "$HOME/.config/wine/prefixes"]
            prefixes = ["~/.wine", "~/.wine32", "~/.config/wine/prefixes"]
            for prefix in prefixes:
                returnString += str(prefix) + ":"
                if os.path.isdir(os.path.expanduser(str(prefix))):
                    returnString += _("Yes") + "\n"
                else:
                    returnString += _("No") + "\n"
                #returnString += str(prefix) + ":" + print("Yes") if os.path.isdir(str(prefix)) == True else print("No") + "\n"

        if selection == "Proton":
            proton_dir = (cmdline("grep _proton= `which proton`")).replace('\n','')
            proton_bin = (cmdline("which proton")).replace('\n','')
            proton_ver = cmdline("grep CURRENT_PREFIX_VERSION= " + proton_dir.replace("_proton=",""))

            returnString = proton_dir + "\n(set in " + proton_bin + ")\n"
            returnString += proton_ver

            #mypath = os.path.dirname(proton_dir.replace("_proton=","").replace("\n",""))
            mypath = "compatibilitytools.d"
            returnString += "\nOther tools in " + mypath
            mypath = "/usr/share/steam/compatibilitytools.d"
            onlyfiles = [f for f in listdir(mypath)]
            for file in onlyfiles:
                returnString += "=" + str(file) + "\n"
            splitChar = "="

        if selection == "DOSBox":
            returnString += cmdline("dosbox --version | head -n 2 | tail -n 1 | sed 's/ox/ox:/'; echo")
            mypath = os.path.expanduser("~/.dosbox/")
            returnString += _("Config files")
            onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
            for file in onlyfiles:
                returnString += ": " + str(file) + "\n"
            splitChar = ": "

        if selection == "Lutris":
            returnString += "Lutris " + cmdline("lutris --version | sed 's/lutris-//'; echo")
            #mypath = os.path.expanduser("~/.config/lutris/games/")
            returnString += _("Games")
            #onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
            #for file in onlyfiles:
            #    returnString += ": " + os.path.splitext(file)[0] + "\n"
            #splitChar = ": "
            conn = sqlite3.connect('/home/mic/.local/share/lutris/pga.db')
            cursor = conn.execute("SELECT id, name from games")
            for row in cursor:
                returnString += ": " + row[1] + "\n"
            conn.close()

        if selection == "GOG":
            returnString += "Minigalaxy " + cmdline("minigalaxy --version; echo")
            mypath = os.path.expanduser("~/.config/minigalaxy/games/")
            returnString += _("Games")
            onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
            for file in onlyfiles:
                returnString += ": " + os.path.splitext(file)[0] + "\n"
            splitChar = ": "

        if selection == "ScummVM":
            returnString += cmdline("scummvm --version | head -n 1; echo")
            mypath = os.path.expanduser("~/.config/scummvm/scummvm.ini")
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
            splitChar = "="

        if selection in ("Epic Games", "Battle.net", "Steam"):
            returnString = str(selection) + " " + _("not yet implemented, sorry.")

        if selection == _("Help"):
            returnString = _("Not yet implemented.")
            #splitChar = "---"
        if selection == _("About"):
            returnString = f'{__appname__} {__version__}:\n\n{__licence__}' #{__author__}
            splitChar = "---"
            #treeRight["columns"]=("#0") #,"two", "three")
            treeView.column("#0", width=900, minwidth=350, stretch=ttk.NO)

        if selection in (_("System"), _("Platforms"), "GameInfo"):
            returnString = _("Please select a sub-category.") + ":"

        treeView.tag_configure("evenrow",background='white smoke',foreground='black')
        treeView.tag_configure("oddrow",background='white',foreground='black')

        zeile = 1
        photo = None
        #for line in selectedSet.splitlines():
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
                    if selection == "OpenGL":
                        part2 = "-"
                    else:
                        part2 = ""
                if selection == "Tools":
                    icon_name = part1
                    if part1 == "openrgb":
                        icon_name = "OpenRGB"
                    if part1 == "minigalaxy":
                        icon_name = "io.github.sharkwouter.Minigalaxy"
                    if part1 == "pavucontrol":
                        icon_name = "multimedia-volume-control"
                    if part1 == "vibrantLinux":
                        icon_name = "io.github.libvibrant.vibrantLinux"
                    if part1 == "protontricks":
                        icon_name = "wine"
                    if part1 == "steamcmd":
                        icon_name = "steam_tray_mono"
                    try:
                        #icon_theme = Gtk.IconTheme()
                        #ico = icon_theme.get_default()
                        #icon_theme = Gtk.Settings.get_default()
                        #print(Gtk.Settings.get_default().get_property("gtk-icon-theme-name"))
                        icon_theme = Gtk.IconTheme.get_default()
                        icon_info = icon_theme.lookup_icon(icon_name, 32, 0)
                    except:
                        #AppDebug.debug_print("")
                        pass
                    try:
                        #print(icon_info.get_filename())
                        image = None
                        if icon_info != None:
                            image_filename = icon_info.get_filename()
                        else:
                            AppDebug.debug_print("No file for " + icon_name + " :-(")
                    except:
                        #AppDebug.debug_print("")
                        image_filename = None
                        itemx = treeView.insert("", index=zeile, text=part1, values=(part2, ""), tags=(tag,))
                        zeile += 1
                        continue
                    if "svg" in image_filename:
                        image_data = cairosvg.svg2png(url=image_filename)
                        image = (Image.open(io.BytesIO(image_data)))
                        photo = image.resize((32, 32), Image.Resampling.LANCZOS) #, Image.ANTIALIAS)
                        photo = ImageTk.PhotoImage(photo)
                    if "png" in image_filename:
                        image = Image.open(image_filename)
                        photo = image.resize((32, 32), Image.Resampling.LANCZOS) #, Image.ANTIALIAS)
                        photo = ImageTk.PhotoImage(photo)
                try:
                    AppDebug.debug_print("  Füge " + icon_name + " in den Baum zu Index " + str(zeile) + " hinzu...")
                    AppDebug.debug_print(pprint(photo))
                    itemx = treeView.insert("", index=zeile, text=part1, values=(part2, ""), tags=(tag,), image=photo)
                    AppDebug.debug_print("  ok! " + str(type(photo)))
                except:
                    photo = None
                    #AppDebug.debug_print(icon_name + " fehlgeschlagen")
                    itemx = treeView.insert("", index=zeile, text=part1, values=(part2, ""), tags=(tag,))
                else:
                    #treeView.insert("", index=zeile, text=line, tags=(tag,))
                    pass
            zeile += 1

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
      
    def createWidgets(self, textPane):

        #self.children.clear()

        self.clear_frame()

        '''toolbar = ttk.Frame(self)
        toolbar.pack(side=TOP, fill=X)

        photo = ttk.PhotoImage(file="GameInfo.png")
        ttk.icons.Icon()
        
        b1 = ttk.Button(
            toolbar,
            #relief=FLAT,
            compound = LEFT,
            text="new",
            command=self.callback,
            image=photo)
        b1.photo = photo
        b1.pack(side=LEFT, padx=0, pady=0)
        
        b2 = ttk.Button(
            toolbar,
            text="open",
            compound = LEFT,
            command=self.callback)
            #relief=FLAT,
            #image=ttk.Image.open("GameInfo.png")) # .PhotoImage("GameInfo.png"))
        b2.pack(side=LEFT, padx=0, pady=0)

        menubar = ttk.Menu(self)

        salutations = ttk.Menu(menubar)
        salutations.add_command(label="Say Hello", command=lambda: print("Hello"))
        salutations.add_command(label="Say Goodbye", command=lambda: print("Goodbye"))

        menubar.add_cascade(label="Salutations", menu=salutations)

        self.config(menu=menubar) '''
    
        icons = ["edit-cut", "edit-paste", "edit-copy"]

        #path = os.path.abspath(path)
        #i = './icon/Home-icon_16.gif'
        #root_pic1 = Image.open(i)
        #self.root_pic2 = ImageTk.PhotoImage(root_pic1)  

        #myimage_16=tk.PhotoImage(file="GameInfo.png")
        #,iconbitmap=myimage_16 # does not work with TV

        f = ttk.Frame()
        f.pack(side=BOTTOM)

        #b1 = ttk.Button(self, text="Submit", bootstyle="success")
        #b1.pack(side=LEFT, padx=5, pady=10)

        b2 = ttk.Button(f, text=_("Refresh"), bootstyle="warning", width=10, command=refresh) #self.createWidgets("Distro"))
        b2.pack(side=RIGHT, padx=5, pady=10, anchor=ttk.SE)

        b3 = ttk.Button(f, text=_("About"), bootstyle="info", width=10, command=open_info)
        b3.pack(side=RIGHT, padx=5, pady=10, anchor=ttk.SE)

        b4 = ttk.Button(f, text=_("Quit"), bootstyle="danger", width=10, command=self.quit)
        b4.pack(side=RIGHT, padx=5, pady=10, anchor=ttk.SE)

        #self.quitButton = ttk.Button(self, text='Quit', command=self.quit)
        #self.quitButton.pack(side=LEFT)
        #self.quitButton.grid()            

        #m0 = ttk.PanedWindow(self, orient="vertical")
        #m0.pack(fill=ttk.Y, expand=150)

        #m1 = tk.PanedWindow(width=100,border=10,borderwidth=0,handlepad=0, background="#000000",handlesize=0) #height=800, width=1024)
        m1 = ttk.PanedWindow(self, orient="horizontal",width=250)
        m1.pack(fill=ttk.BOTH, expand=250, side=TOP)

        #left = tk.Label(m1, text="left pane")
        treeLeft = ttk.Treeview(style="mystyle.Treeview.Left")
        treeLeft.pack(fill=X, side=LEFT)

        treeLeft.bind("<<TreeviewSelect>>", self.print_element)
        #treeLeft.bind("<Motion>", self.mycallback)

        #tree["columns"]=("one") #,"two","three")
        treeLeft.column("#0", width=150, minwidth=150, stretch=ttk.NO)
        treeLeft.pack(side=ttk.LEFT,fill=ttk.X)
        # Level 1
        folder1=treeLeft.insert("", 0, 0, text="System", open=True) #, values=("23-Jun-17 11:05","File folder",""))
        cnt = 0
        #for entry in menuSystem:
            #treeLeft.insert(0, cnt + 1, text=entry) #, values=("23-Jun-17 11:25","TXT file","1 KB"))
            #cnt += 1
        #    pass
        menuitems = file.getElementsByTagName('menuitem')
        for menuitem in sorted(menuitems, key=lambda menuitem: menuitem.attributes['id'].value):
        #for menuitem in menuitems:
        #print(menu.firstChild.data)
            #print(menuitem.attributes['value'].value)
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

        #m1.add(b1)
        #m1.add(b2)

        #x1 = tree.insert("", 1, "1", text="hallo")
        #m1.add(left)

        folder2=treeLeft.insert("", cnt, 200, text="GameInfo", open=True) #, values=("23-Jun-17 11:05","File folder",""))
        for entry in menuGameInfo:
            treeLeft.insert(200, cnt + 1, text=entry) #, values=("23-Jun-17 11:25","TXT file","1 KB"))
            cnt += 1

        m2 = ttk.PanedWindow(m1, orient=ttk.VERTICAL, width=1000,height=self.winfo_height())
        m2.pack(side=TOP)
        #m1.add(m2, minsize=100)
        m1.add(m2)

        #top = tk.Label(m2, text=textPane, font="Sans 20")
        treeRight = ttk.Treeview(m2, style="mystyle.Treeview.Right",name="right_tree")
        
        treeRight["columns"]=("#0", "#1")
        treeRight.column("#0", width=400, minwidth=400, stretch=ttk.NO)
        treeRight.column("#1", width=470, minwidth=470, stretch=ttk.NO)
        #treeRight.heading("#0",text="dfgsdfghsdfkjgsdhfjklsdfh",anchor=ttk.W) #text="Name"
        #if True: #selection == "Alle":
        #    treeRight.heading("#0", text="Name",anchor=ttk.W) #text="Wert"
        #else:
        #    treeRight.heading("one", text="",anchor=ttk.W)
        #tree.heading("two", text="Type",anchor=tk.W)
        #tree.heading("three", text="Size",anchor=tk.W)
        #tree.pack(side=ttk.TOP,fill=ttk.BOTH)
        treeRight.pack(side=TOP)

        #logo = ttk.Image.open(os.path.dirname(__file__) + "/GameInfo.png")
        #logo2 = logo.resize((100, 100), Image.Resampling.LANCZOS) #, Image.ANTIALIAS)
        #logo3 = ImageTk.PhotoImage(logo2)
        #f = ttk.Frame(iconbitmap=logo3)
        #f.pack()

        if textPane == "":

            #frame = ttk.Frame(self, width=512, height=512)
            #frame.pack()
            #frame.place(anchor='center', relx=0.5, rely=0.5)

            # Create an object of tkinter ImageTk
            #img = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(__file__),"..","GameInfo.png")))
            
            #label = ttk.Label(frame, image = img)
            #label.pack()

            #m2.add(frame)
            pass
        else:
            m2.add(treeRight)

        self.fillTreeview(treeRight, selection=textPane)

        #m2.add(top)
        #m2.add(tree, minsize=100)

        #bottom = tk.Label(m2, text="bottom pane", font="Times 20 italic bold")
        #text1 = tk.Label(m2,text="fdgsdkflgjsdkfgjsdfklgjsdlkfögjsdfkg",height=300,background="#ffffff",width=400)
        #text1.pack(side=tk.TOP,fill=tk.Y)
        '''tree = ttk.Treeview()
        tree["columns"]=("one","two","three")
        tree.heading("#0",text="Name",anchor=tk.W)
        tree.heading("one", text="Date modified",anchor=tk.W)
        tree.heading("two", text="Type",anchor=tk.W)
        tree.heading("three", text="Size",anchor=tk.W)
        tree.pack(side=tk.TOP,fill=tk.X)
        m2.add(text1)
        m2.add(tree)'''
        #m2.add(bottom)

    def get_desktop_environment(self):
        #From http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
        # and http://ubuntuforums.org/showthread.php?t=652320
        # and http://ubuntuforums.org/showthread.php?t=652320
        # and http://ubuntuforums.org/showthread.php?t=1139057
        if sys.platform in ["win32", "cygwin"]:
            return "windows"
        elif sys.platform == "darwin":
            return "mac"
        else: #Most likely either a POSIX system or something not much common
            desktop_session = os.environ.get("DESKTOP_SESSION")
            if desktop_session is not None: #easier to match if we doesn't have  to deal with caracter cases
                desktop_session = desktop_session.lower()
                if desktop_session in ["gnome","unity", "cinnamon", "mate", "xfce4", "lxde", "fluxbox", 
                                        "blackbox", "openbox", "icewm", "jwm", "afterstep","trinity", "kde"]:
                    return desktop_session
                ## Special cases ##
                # Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if using LXDE.
                # There is no guarantee that they will not do the same with the other desktop environments.
                elif "xfce" in desktop_session or desktop_session.startswith("xubuntu"):
                    return "xfce4"
                elif desktop_session.startswith("ubuntu"):
                    return "unity"       
                elif desktop_session.startswith("lubuntu"):
                    return "lxde" 
                elif desktop_session.startswith("kubuntu"): 
                    return "kde" 
                elif desktop_session.startswith("razor"): # e.g. razorkwin
                    return "razor-qt"
                elif desktop_session.startswith("wmaker"): # e.g. wmaker-common
                    return "windowmaker"
            if os.environ.get('KDE_FULL_SESSION') == 'true':
                return "kde"
            elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                if not "deprecated" in os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                    return "gnome2"
            #From http://ubuntuforums.org/showthread.php?t=652320
            #elif self.is_running("xfce-mcs-manage"):
                #return "xfce4"
            #elif self.is_running("ksmserver"):
                #return "kde"
        return "unknown"

    def is_running(self, process):
        #From http://www.bloggerpolis.com/2011/05/how-to-check-if-a-process-is-running-using-python/
        # and http://richarddingwall.name/2009/06/18/windows-equivalents-of-ps-and-kill-commands/
        try: #Linux/Unix
            s = subprocess.Popen(["ps", "axw"],stdout=subprocess.PIPE)
        except: #Windows
            s = subprocess.Popen(["tasklist", "/v"],stdout=subprocess.PIPE)
        #for x in s.stdout:
        #    if re.search(process, x):
        #        return True
        return False
