#### TODO

:heavy_check_mark: Rework TKinter to use <strike>ThemedTk</strike> ttkbootstrap. :tired_face:  
:heavy_check_mark: Switch from setuptools to poetry (done with v1.0.5).  
:heavy_check_mark: Add <a href="https://www.flaticon.com/de/kostenlose-icons/computer" title="computer Icons">Computer Icons erstellt von Freepik - Flaticon</a>

#### Tools

:white_check_mark: Use App's icons in Tools list - tedious with TK. Unfortunately, even after further attempts to get this working, it doesn't.  

:white_check_mark: Provide a hook whether there is an update available for each tool.

:heavy_check_mark: Support various package manager hooks, i.e.
- `pacman/yay`,
- `apt/dpkg`, 
- `yum/dnf`,
- or even `xbps`.

(mostly done)

:white_check_mark: Provide a button to start each tool.

:white_check_mark: dosbox (dosbox-staging) on openSUSE has a differntly formatted version-string.

:heavy_check_mark: Up to `lutris-0.5.9`, a progressbar was shown when GameInfo was running `lutris --version`. This has been changed with `lutris-0.5.10` onwards.  

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

:heavy_check_mark: show version and/or update availability

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

#### Other platforms

:white_check_mark: Epic Games, Battle.net, etc - no idea.

#### System requirements

GameInfo is tested to work on the following distributions:

(see README.md)

Tests underway:

- Gentoo Linux (my portage is broken currently)

#### Supported tools

(see README.md)

#### Planned tools

(see README.md)
