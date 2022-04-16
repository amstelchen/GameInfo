#!/usr/bin/env python

#import gi
#gi.require_version("Gtk", "3.0")
#from gi.repository import Gtk
#from gi.repository.GdkPixbuf import Pixbuf

import tkinter as tk
#from tkinter import ttk
import tkinter.ttk as ttk
from ttkthemes import ThemedTk

import os, sys, re
import sysconfig
from subprocess import PIPE, Popen, check_output
import subprocess
import json
from xml.dom import minidom
import string
#from PIL import Image, ImageTk

from os import listdir
from os.path import isfile, join

import gettext

VERSION = "1.0.3"

__appname__ = "GameInfo"
__version__ = VERSION # "1.0.3"
__author__ = "Michael John"
__licence__ = \
'Copyright © 2022 Michael John <michael.john@gmx.at>\n' \
'Lizenz GPLv3: GNU GPL Version 3 oder neuer <https://gnu.org/licenses/gpl.html>\n' \
'Dies ist freie Software; es steht Ihnen frei, sie zu verändern und weiterzugeben.\n' \
'Es gibt KEINE GARANTIE, soweit als vom Gesetz erlaubt.\n' \
'Geschrieben von Michael John.'

#print(f'{__appname__} {__version__}')

gettextobj = gettext.translation('gameinfo', localedir='locales', languages=['de'])
gettextobj.install()
_ = gettextobj.gettext
    
def cmdline(command):
    process = Popen(args=command, stdout=PIPE, shell=True, universal_newlines=True) #text_mode = True
    #process.text_mode = True
    return process.communicate()[0]

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

print(_("Fetching system info, this can take a second..."))
'''outputALLE = cmdline('wine --version ; echo -n "winetricks-" && winetricks --version ; '
    'protontricks --version | sed "s/\ (/-/;s/)//" ; ' #lutris --version ; '
    'echo -n "minigalaxy-" && minigalaxy --version ; echo quit | steamcmd | grep version | '
    'sed "s/\-\ /-/" ; echo -n "steam_cli-" ; steam-cli --version')'''

toolitems = file.getElementsByTagName('toolitem')
outputALLE = str("")
for toolitem in toolitems:
    command = toolitem.attributes["command"].value
    version = toolitem.attributes["version"].value
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

print(outputALLE)

#stringy = outputVAAPI.decode('utf-8')
#print(type(stringy))

class Application(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        #tt = tk.Tk()
        #a = ttk.Frame()

        #theme = ThemedTk.themes('ubuntu')
        #self.master.theme_use('ubuntu')
        #t = thtk.ThemedTk()

        s = ttk.Style(self.master)
        s.theme_use('clam')
        print(s.theme_names())

        #style = ttk.Style()
        #style.theme_use('yaru')
        #self.master.style = style

        myimage_16 = tk.PhotoImage(file="GameInfo.png")  
        #tt.iconbitmap = tk.PhotoImage(file='GameInfo.png')
        #tt.iconbitmap('GameInfo.png')
        #icon = tk.Tk().iconbitmap('GameInfo.png')
        #tk.Tk().call('wm', 'iconphoto', self._root.w, tk.PhotoImage(file='GameInfo.png'))

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
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        #a.master.iconbitmap(myimage_16)
        self.master.iconphoto(False, myimage_16) # finally works now :-)
        #print("debug")
    
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
            returnString= returnString.replace("   ", " ")
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

        if selection in ("Lutris", "GOG", "Epic Games", "Battle.net"):
            returnString = str(selection) + " " + _("not yet implemented, sorry.")

        if selection == "Help":
            returnString = _("Not yet implemented.")
            #splitChar = "---"
        if selection == "About":
            returnString = f'{__appname__} {__version__}:\n\n{__licence__}' #{__author__}
            splitChar = "---"

        if selection in ("System", "Platforms", "GameInfo"):
            returnString = _("Please select a sub-category.")

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

        #if selection == "Distro":
            #returnString+= "$DESKTOP_SESSION:" + self.get_desktop_environment()

    def mycallback(self, event):
 
        _iid = self.treeLeft.identify_row(event.y)
 
        if _iid != self.last_focus:
            if self.last_focus:
                self.tree.item(self.last_focus, tags=[])
            self.tree.item(_iid, tags=['focus'])
            self.last_focus = _iid

    def createWidgets(self, textPane):

        icons = ["edit-cut", "edit-paste", "edit-copy"]

        #path = os.path.abspath(path)
        #i = './icon/Home-icon_16.gif'
        #root_pic1 = Image.open(i)
        #self.root_pic2 = ImageTk.PhotoImage(root_pic1)  

        myimage_16=tk.PhotoImage(file="GameInfo.png")
        #,iconbitmap=myimage_16 # does not work with TV

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Monospace', 10)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

        m1 = tk.PanedWindow(width=100,border=10,borderwidth=0,handlepad=0, background="#000000",handlesize=0) #height=800, width=1024)

        m1.pack(fill=tk.X, expand=1)

        #left = tk.Label(m1, text="left pane")
        treeLeft = ttk.Treeview(style="mystyle.Treeview")

        treeLeft.bind("<<TreeviewSelect>>", self.print_element)
        #treeLeft.bind("<Motion>", self.mycallback)

        #tree["columns"]=("one") #,"two","three")
        treeLeft.column("#0", width=150, minwidth=150, stretch=tk.NO)
        treeLeft.pack(side=tk.LEFT,fill=tk.X)
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
        folder2=treeLeft.insert("", cnt, 100, text="Platforms", open=True) #, values=("23-Jun-17 11:05","File folder",""))
        for entry in menuPlatforms:
            treeLeft.insert(100, cnt + 1, text=entry) #, values=("23-Jun-17 11:25","TXT file","1 KB"))
            cnt += 1

        #x1 = tree.insert("", 1, "1", text="hallo")
        #m1.add(left)
        m1.add(treeLeft)

        folder2=treeLeft.insert("", cnt, 200, text="GameInfo", open=True) #, values=("23-Jun-17 11:05","File folder",""))
        for entry in menuGameInfo:
            treeLeft.insert(200, cnt + 1, text=entry) #, values=("23-Jun-17 11:25","TXT file","1 KB"))
            cnt += 1

        m2 = tk.PanedWindow(m1, orient=tk.VERTICAL, width=1000,height=600)
        m1.add(m2, minsize=100)

        #top = tk.Label(m2, text=textPane, font="Sans 20")
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

        #m2.add(top)
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

def main():
    app = Application()           
    app.master.title(f'{__appname__} {__version__}')
    app.mainloop()        

if __name__ == "__main__":
    main()