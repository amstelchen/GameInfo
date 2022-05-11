[![Documentation Status](https://readthedocs.org/projects/gameinfo/badge/?version=latest)](https://gameinfo.readthedocs.io/en/latest/?badge=latest) [![Python package](https://github.com/amstelchen/GameInfo/actions/workflows/python-package-no-pytest.yml/badge.svg)](https://github.com/amstelchen/GameInfo/actions/workflows/python-package-no-pytest.yml)

<h1>GameInfo</h1>

A system info tool for gamers.

#### Supported tools

|__Emulators/Runners__|__CLI tools__|__Audio__|
|-|-|-|
|:heavy_check_mark: wine  |:heavy_check_mark: steamcmd  |:heavy_check_mark: pavucontrol
|:heavy_check_mark: winetricks  |:heavy_check_mark: steam-cli  |:heavy_check_mark: pipewire
|:heavy_check_mark: protontricks  |:heavy_check_mark: legendary-gl |:heavy_check_mark: pulseffects
|:heavy_check_mark: lutris  |:heavy_check_mark: truckersmp-cli  |
|:heavy_check_mark: minigalaxy  |:heavy_check_mark: samrewritten  |
|:heavy_check_mark: playonlinux  ||
|__Graphics__|__Perf tuning__|__Modding__|
|:heavy_check_mark: dxvk  |:heavy_check_mark: mangohud  |:heavy_check_mark: openrgb
|:heavy_check_mark: vkd3d  |:heavy_check_mark: corectrl  |:heavy_check_mark: vibrantLinux 

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

On Void Linux, installation of the packages `python3-tkinter` and `python3-gobject` is necessary instead.

    sudo xbps-install python3-tkinter python3-gobject


#### System requirements

GameInfo is tested to work on the following distributions:

- Arch Linux <sup>(1.0.7)</sup>
- Debian 10 or newer <sup>(1.0.7)</sup>
- Ubuntu 20.04 or newer <sup>(1.0.7)</sup>
- Manjaro 20 <sup>(1.0.7)</sup>
- Linux Mint 20 or newer <sup>(1.0.7)</sup> (19.3 lacks support for python3.7, only has 3.6.9)
- MX Linux 19 or newer <sup>(1.0.7)</sup> (19.1 likely needs to run `pip install --upgrade pip setuptools wheel `)
- Fedora 32 Workstation or newer <sup>(1.0.7)</sup>
- Void Linux <sup>(1.0.8)</sup>
- Garuda Linux <sup>(1.0.7)</sup>

#### Debugging

```
$ GAMEINFO_DEBUG=1 GameInfo
DEBUG: GameInfo 1.0.5
DEBUG: Hole Systeminfo, dies kann einen Moment dauern...
DEBUG: Prüfe auf wine
DEBUG: Prüfe auf winetricks
...
DEBUG: Themen geladen: cosmo flatly litera minty lumen
```
#### Screenshots

[![https://imgur.com/QfApzDu.png](https://imgur.com/QfApzDu.png)](https://imgur.com/QfApzDu.png)

#### Licences

*GameInfo* is licensed under the [GPLv2](LICENSE) license.

<a href="https://www.flaticon.com/de/kostenlose-icons/computer" title="computer Icons">Computer Icons created by Freepik - Flaticon</a>
