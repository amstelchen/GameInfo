#!/usr/bin/env python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf

import tkinter as tk
from tkinter import ttk
import os, sys
import sysconfig
from subprocess import PIPE, Popen, check_output
import json
from xml.dom import minidom
import string
from PIL import Image, ImageTk

from os import listdir
from os.path import isfile, join

__appname__ = "GameInfo"
__version__ = "1.0.2"
__author__ = "Michael John"
__licence__ = \
'Copyright © 2022 Michael John <michael.john@gmx.at>\n' \
'Lizenz GPLv3: GNU GPL Version 3 oder neuer <https://gnu.org/licenses/gpl.html>\n' \
'Dies ist freie Software; es steht Ihnen frei, sie zu verändern und weiterzugeben.\n' \
'Es gibt KEINE GARANTIE, soweit als vom Gesetz erlaubt.\n' \
'Geschrieben von Michael John.'

#print(f'{__appname__} {__version__}')

def cmdline(command):
    process = Popen(args=command, stdout=PIPE, shell=True, universal_newlines=True) #text_mode = True
    #process.text_mode = True
    return process.communicate()[0]

#menuSystem = ["Linux Kernel", "Linux Distro", "CPU", "GPU", "Vulkan", "OpenGL", "VDPAU", "VA-API"]

#menuReturn = []

#with open('GameInfo.json') as json_file:
#    data = json.load(json_file)
#    print(data)

file = minidom.parse("GameInfo.xml")
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

menuPlatforms = ["Alle", "Steam", "Proton", "Wine", "DOSBox", "Lutris", "GOG", "Epic Games", "Battle.net"]

menuGameInfo = ["Help", "About"]

#print(sysconfig.get_python_version())
#print(sys.version)

#proc = subprocess.Popen(["cat", "/etc/services"], stdout=subprocess.PIPE, shell=True)
#(out, err) = proc.communicate()
#print("program output:", out)

#import subprocess
#output = check_output("cat /etc/services", shell=True)

#print(cmdline("cat /etc/services"))

print("Fetching system info, this can take a second...")
outputALLE = cmdline('wine --version ; echo -n "winetricks-" && winetricks --version ; '
    'protontricks --version | sed "s/\ (/-/;s/)//" ; ' #lutris --version ; '
    'echo -n "minigalaxy-" && minigalaxy --version ; echo quit | steamcmd | grep version | '
    'sed "s/\-\ /-/" ; echo -n "steam_cli-" ; steam-cli --version')
#print(type(outputVAAPI))

#stringy = outputVAAPI.decode('utf-8')
#print(type(stringy))

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        a = tk.Frame()

        #self.grid()               
        self.createWidgets(textPane="System")

        w = 1024 # width for the Tk root
        h = 568 # height for the Tk root

        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        a.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    def print_element(self, event):
        tree = event.widget
        selection = [tree.item(item)["text"] for item in tree.selection()]
        print("Selected item:", str(selection))

        #m2.add(tree)       
        #app.master.m2.add(tree)
        self.updateWidgets(selection)

        #self.createWidgets()

    def updateWidgets(self, selection):
        #for label in filter(lambda w:isinstance(w,Label), frame.children.itervalues()):
        idx = 0
        for tv in filter(lambda w:isinstance(w,ttk.Treeview), self.master.winfo_children()):
        #for child in self.master.winfo_children():
            #print(tv, str(tv.index))
            #print(type(tv))
            if idx == 1:
                #tv.destroy()
                tv.delete(*tv.get_children())
            idx += 1
            #if tv._index == 0:
            #    print("bla")
        #for elem in self.m:
        #    print(elem)
        #self.createWidgets()
        self.fillTreeview(tv, selection)

        #self.master.top.text = "bla"
        
        for la in filter(lambda w:isinstance(w,tk.Label), self.master.winfo_children()):
            #la.destroy()
            la.text = selection

        #self.pack_slaves(0).text = selection

        #top = tk.Label(self.m2, text="top pane", font="Times 20 italic bold")
        #top.pack()

    def fillTreeview(self, tree, selection):

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
            splitChar = "="
            #linesIgnore = 1000
        if selection == "CPU":
            splitChar = ":"
            #linesIgnore = 1000
        if selection == "GPU":
            splitChar = ": "
            #linesIgnore = 1000
        #if selection == "PCI":
        #    splitChar = ": "
        #if selection == "USB":
        #    splitChar = ":"

        if selection == "Vulkan":
            returnString= returnString.replace('\t', "  ")
        if selection == "VA-API":
            linesIgnore = 3
        if selection == "VDPAU":
            splitChar = "\t"
            linesIgnore = 1000
        if selection == "OpenGL":
            splitChar = ": "
        if selection == "OpenCL":
            #returnString.replace("     ", " ")
            pass
        if selection == "Alle":
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
                    returnString += "Yes\n"
                else:
                    returnString += "No\n"
                #returnString += str(prefix) + ":" + print("Yes") if os.path.isdir(str(prefix)) == True else print("No") + "\n"

        if selection == "Proton":
            proton_dir = cmdline("grep _proton= `which proton`")
            returnString = proton_dir
            proton_ver = cmdline("grep CURRENT_PREFIX_VERSION= " + proton_dir.replace("_proton=",""))
            returnString += proton_ver
            splitChar = "="

        if selection == "DOSBox":
            returnString += cmdline("dosbox --version | head -n 2 | tail -n 1 | sed 's/ox/ox:/'; echo")
            mypath = os.path.expanduser("~/.dosbox/")
            returnString += "Config files"
            onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
            for file in onlyfiles:
                returnString += ": " + str(file) + "\n"
            splitChar = ": "

        if selection in ("Lutris", "GOG", "Epic Games", "Battle.net"):
            returnString = str(selection) + " not yet implemented, sorry."

        if selection == "Help":
            returnString = "Not yet implemented"
            #splitChar = "---"
        if selection == "About":
            returnString = f'{__appname__} {__version__}:\n\n{__licence__}' #{__author__}
            splitChar = "---"

        if selection in ("System", "Platforms", "GameInfo"):
            returnString = "Please select a sub-category."

        l = 1
        #for line in selectedSet.splitlines():
        for line in returnString.splitlines():
            try:
                if l > linesIgnore:
                    part1 = line.split(splitChar, 1)[0]
                    try:
                        part2 = line.split(splitChar, 1)[1]
                    except:
                        if selection == "OpenGL":
                            part2 = "-"
                        else:
                            part2 = ""
                    tree.insert("", l, text=part1, values=(part2, ""))
                    pass
                else:
                    tree.insert("", l, text=line)
            except:
                tree.insert("", l, text=line)
            l += 1

    def createWidgets(self, textPane):

        icons = ["edit-cut", "edit-paste", "edit-copy"]

        #path = os.path.abspath(path)
        #i = './icon/Home-icon_16.gif'
        #root_pic1 = Image.open(i)
        #self.root_pic2 = ImageTk.PhotoImage(root_pic1)  

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Monospace', 10)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

        m1 = tk.PanedWindow(width=100,border=10,borderwidth=0,handlepad=0, background="#000000",handlesize=0) #height=800, width=1024)

        m1.pack(fill=tk.X, expand=1)

        #left = tk.Label(m1, text="left pane")
        tree = ttk.Treeview(style="mystyle.Treeview")

        tree.bind("<<TreeviewSelect>>", self.print_element)

        #tree["columns"]=("one") #,"two","three")
        tree.column("#0", width=150, minwidth=150, stretch=tk.NO)
        tree.pack(side=tk.LEFT,fill=tk.X)
        # Level 1
        folder1=tree.insert("", 0, 0, text="System", open=True) #, values=("23-Jun-17 11:05","File folder",""))
        cnt = 0
        #for entry in menuSystem:
            #tree.insert(0, cnt + 1, text=entry) #, values=("23-Jun-17 11:25","TXT file","1 KB"))
            #cnt += 1
        #    pass
        menuitems = file.getElementsByTagName('menuitem')
        for menuitem in sorted(menuitems, key=lambda menuitem: menuitem.attributes['id'].value):
        #for menuitem in menuitems:
        #print(menu.firstChild.data)
            #print(menuitem.attributes['value'].value)
            pixbuf = Gtk.IconTheme.get_default().load_icon(icons[0], 64, 0) 

            item = tree.insert(0, cnt + 1, text=menuitem.attributes['value'].value) #,image=ImageTk.PhotoImage(pixbuf))
            #image_show_2.set_from_pixbuf(pixbuf)
            cnt += 1
        cnt = 100
        folder2=tree.insert("", cnt, 100, text="Platforms", open=True) #, values=("23-Jun-17 11:05","File folder",""))
        for entry in menuPlatforms:
            tree.insert(100, cnt + 1, text=entry) #, values=("23-Jun-17 11:25","TXT file","1 KB"))
            cnt += 1

        #x1 = tree.insert("", 1, "1", text="hallo")
        #m1.add(left)
        m1.add(tree)

        folder2=tree.insert("", cnt, 200, text="GameInfo", open=True) #, values=("23-Jun-17 11:05","File folder",""))
        for entry in menuGameInfo:
            tree.insert(200, cnt + 1, text=entry) #, values=("23-Jun-17 11:25","TXT file","1 KB"))
            cnt += 1

        m2 = tk.PanedWindow(m1, orient=tk.VERTICAL, width=1000,height=600)
        m1.add(m2, minsize=100)

        top = tk.Label(m2, text=textPane, font="Times 20 italic bold")
        tree = ttk.Treeview(style="mystyle.Treeview")
        
        tree["columns"]=("one") #,"two", "three")
        tree.column("#0", width=400, minwidth=200, stretch=tk.NO)
        tree.heading("#0",text="",anchor=tk.W) #text="Name"
        if True: #selection == "Alle":
            tree.heading("one", text="",anchor=tk.W) #text="Wert"
        else:
            tree.heading("one", text="",anchor=tk.W)
        #tree.heading("two", text="Type",anchor=tk.W)
        #tree.heading("three", text="Size",anchor=tk.W)
        tree.pack(side=tk.TOP,fill=tk.BOTH)

        self.fillTreeview(tree, "Distro")

        m2.add(top)
        m2.add(tree, minsize=100)

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

        self.quitButton = tk.Button(self, text='Quit',
            command=self.quit)            
        #self.quitButton.grid()            

app = Application()           
app.master.title(f'{__appname__} {__version__}')
app.mainloop()        