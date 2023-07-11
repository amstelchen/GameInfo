#### TODO

:heavy_check_mark: Rework TKinter to use <strike>ThemedTk</strike> ttkbootstrap. :tired_face:  
:heavy_check_mark: Switch from setuptools to poetry (done with v1.0.5).  
:heavy_check_mark: Add <a href="https://www.flaticon.com/de/kostenlose-icons/computer" title="computer Icons">Computer Icons erstellt von Freepik - Flaticon</a>  
:heavy_check_mark: Pop_OS logo is ugly; there are logos in good quality in /usr/share/icons/256x256/
:white_check_mark: Fedora and Elementary logos are misplaced  
:white_check_mark: Add new fixes to Troubleshooting section  

#### Tools

:white_check_mark: Use App's icons in Tools list - this was very tedious to implement with TK.  
:white_check_mark: Provide a hook whether there is an update available for each tool.  
:white_check_mark: Provide a button to start each tool.  
:white_check_mark: State whether a specific tools is `GUI` or `CLI`.  

#### Distro

:white_check_mark: Use [python-distro](https://github.com/python-distro/distro) instead of parsing all files individually.

#### System

:white_check_mark: Catch error in section __Vulkan__ when *vulkaninfo* but no driver is installed:
```
Cannot create Vulkan instance.
/build/vulkan-tools-6bmpQy/vulkan-tools-1.1.97+dfsg1/vulkaninfo/vulkaninfo.c:918: failed with VK_ERROR_INCOMPATIBLE_DRIVER
```
:white_check_mark: Catch error in section __VDPAU__ when *vdpauinfo* but no driver is installed:
```
display: :0.0   screen: 0
Failed to open VDPAU backend libvdpau_nvidia.so: cannot open shared object file: No such file or directory
Error creating VDPAU device: 1
```
:white_check_mark: Catch error in section __VA-API__ when *vainfo* but no driver is installed:
```
libva info: VA-API version 1.4.0
libva info: va_getDriverName() returns -1
libva error: va_getDriverName() failed with unknown libva error,driver_name=(null)
vaInitialize failed with error code -1 (unknown libva error),exit
```
<hr>

Move these into README.md when tested:

#### Steam

:heavy_check_mark: list libraries and their space usage, based on *libraryfolders.vdf*  
:white_check_mark: list games  
:white_check_mark: list other Proton installs in *SteamLibrary/steamapps/common*  
  
#### Proton

:heavy_check_mark: list compatibilitytools.d:
- Proton-GE
- boxtron
- luxtorpeda
- roberta

:white_check_mark: show version and/or update availability

#### Wine

:heavy_check_mark: list prefixes  
:heavy_check_mark: ... with usage in MB/GB  

#### DOSBox

:heavy_check_mark: show version  
:heavy_check_mark: list .conf's  

#### Lutris

:heavy_check_mark: list games in <strike>~/.config/lutris/games/</strike> `~.local/share/lutris/pga.db`

#### GOG

:heavy_check_mark: list games in `~/.config/minigalaxy/games/` if there are any

#### ScummVM

:heavy_check_mark: list games, if any

#### Epic Games

:heavy_check_mark: makes use of [legendary-gl](https://github.com/derrod/legendary) to list games
:white_check_mark: and eventually launch them

#### Other platforms

:white_check_mark: itch.io - coming soon.
:white_check_mark: Battle.net - removed.

#### System requirements

GameInfo is tested to work on the following distributions:

(see README.md)

#### Supported tools

(see README.md)

#### Planned tools

(see README.md)
