#### Supported tools

:heavy_check_mark: wine  
:heavy_check_mark: winetricks  
:heavy_check_mark: protontricks  
:heavy_check_mark: lutris  
:heavy_check_mark: minigalaxy  
:heavy_check_mark: steamcmd  
:heavy_check_mark: steam-cli  
:heavy_check_mark: mangohud  
:heavy_check_mark: pavucontrol  
:heavy_check_mark: pipewire  
:heavy_check_mark: legendary-gl  
:heavy_check_mark: pulseffects  
:heavy_check_mark: openrgb  
:heavy_check_mark: corectrl  
:heavy_check_mark: truckersmp-cli  
:heavy_check_mark: vibrantLinux  
:heavy_check_mark: dxvk  
:heavy_check_mark: vkd3d  
:white_check_mark: samrewritten  

:heavy_check_mark: Rework TKinter to use <strike>ThemedTk</strike> ttkbootstrap. :tired_face:  
:heavy_check_mark: Switch from setuptools to poetry (done with v1.0.5).
:white_check_mark: Add <a href="https://www.flaticon.com/de/kostenlose-icons/computer" title="computer Icons">Computer Icons erstellt von Freepik - Flaticon</a>

#### Tools

:white_check_mark: Use App's icons in Tools list - tedious with TK.  

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
:white_check_mark: list other Proton installs in SteamLibrary/common
  
#### Proton

:heavy_check_mark: list compatibilitytools.d:
- Proton-GE
- boxtron
- luxtorpeda
- roberta

#### Wine

:heavy_check_mark: list prefixes
:white_check_mark: ... maybe with usage in MB?

#### DOSBox

:heavy_check_mark: show version
:heavy_check_mark: list .conf's

#### Lutris

:white_check_mark: list games in <strike>~/.config/lutris/games/</strike> `~.local/share/lutris/pga.db`

#### GOG

:white_check_mark: list games in `~/.config/minigalaxy/games/` if there are any

#### ScummVM

:heavy_check_mark: list games, if any

#### Other platforms

:white_check_mark: Epic Games, Battle.net, etc - no idea.

#### System requirements

GameInfo is tested to work on the following distributions:

- Arch Linux
- Debian 10 or newer
- Ubuntu 20.04 or newer
- Manjaro 20
- Linux Mint 20 or newer (19.3 lacks support for python3.7, only has 3.6.9)
- MX Linux 19 or newer (19.1 likely needs to run `pip install --upgrade pip setuptools wheel `)
- Fedora 32 Workstation or newer

Tests underway:

- openSUSE Tumbleweed and Leap 15.2 or newer
- Void Linux
- Gentoo Linux (my portage is broken currently)

#### Installation

Steps assume that `python` and `pip` are already installed.

Install dependencies (see sections below)

Then, run:

    $ pip install GameInfo

Install directly from ``github``:


    $ pip install git+https://github.com/amstelchen/GameInfo#egg=GameInfo

When completed, run it with:

    $ GameInfo

#### Dependencies

On Debian-based distributions (Mint, Ubuntu, MX, etc.), installation of the packages `tk` and `python3-tk` may be necessary.

    sudo apt install python3-tk tk
