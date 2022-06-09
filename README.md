[![Documentation Status](https://readthedocs.org/projects/gameinfo/badge/?version=latest)](https://gameinfo.readthedocs.io/en/latest/?badge=latest) [![Python package](https://github.com/amstelchen/GameInfo/actions/workflows/python-package-no-pytest.yml/badge.svg)](https://github.com/amstelchen/GameInfo/actions/workflows/python-package-no-pytest.yml)

<h1>GameInfo</h1>

A system info tool for gamers.

#### Supported tools

|__Emulators/Runners__|__CLI tools__|__Streaming/Video__|__Audio__|
|-|-|-|-|
|:heavy_check_mark: Wine  |:heavy_check_mark: steamcmd  |:heavy_check_mark: discord |:heavy_check_mark: pavucontrol
|:heavy_check_mark: DOSBox  |:heavy_check_mark: steam-cli  |:heavy_check_mark: twitch |:heavy_check_mark: pipewire
|:heavy_check_mark: ScummVM  |:heavy_check_mark: legendary-gl |:heavy_check_mark: obs-studio |:heavy_check_mark: pulseffects
|:heavy_check_mark: Lutris  |:heavy_check_mark: truckersmp-cli  |:heavy_check_mark: kdenlive |:heavy_check_mark: easyeffects*
|:heavy_check_mark: Minigalaxy  |:heavy_check_mark: samrewritten  |  |
|:heavy_check_mark: PlayOnLinux  |  |
|:heavy_check_mark: Heroic Launcher  |  |
|__Graphics__|__Perf tuning__|__Modding__|__Helpers__
|:heavy_check_mark: dxvk  |:heavy_check_mark: mangohud  |:heavy_check_mark: openrgb  |:heavy_check_mark: winetricks
|:heavy_check_mark: vkd3d  |:heavy_check_mark: corectrl  |:heavy_check_mark:  vibrantLinux |:heavy_check_mark: protontricks
| |:heavy_check_mark: cpupower-gui | |

<sub>(*) might replace pulseeffects</sub>

Planned:

- Redshift / Blueshift
- GameHub


#### Installation

Steps assume that `python` (>= 3.7) and `pip` are already installed.

Install dependencies (see sections below)

Then, run:

    $ pip install GameInfo

Install directly from ``github``:


    $ pip install git+https://github.com/amstelchen/GameInfo#egg=GameInfo

When completed, run it with:

    $ GameInfo

#### Dependencies

On Debian-based distributions (Mint, Ubuntu, MX, etc.), installation of the packages `tk` and `python3-tk` may be necessary.

    $ sudo apt install python3-tk tk

On Arch based distributions, only tk needs to be installed.

    $ sudo pacman -S tk

On Void Linux, installation of the packages `python3-tkinter` and `python3-gobject` is necessary instead.

    $ sudo xbps-install python3-tkinter python3-gobject

Anyways, it often helps to keep your python installation updated:

    $ python -m pip install --upgrade pip wheel setuptools

#### System requirements

*GameInfo* is tested to work on the following distributions:

- Arch Linux (or any Arch based distribution like Manjaro, ArcoLinux, ... <sup>(1.0.12)</sup>
- Debian 10 or newer (10.1, 11.3) <sup>(1.0.12)</sup>
- Ubuntu, Kubuntu, Xubuntu 20.04 or newer, Pop!_OS 20.04 or newer <sup>(1.0.12)</sup>
- Manjaro 20 <sup>(1.0.12)</sup>
- Linux Mint 20 or newer <sup>(1.0.12)</sup> (19.3 lacks support for python3.7, only has 3.6.9)
- MX Linux 19 or newer <sup>(1.0.10)</sup> (19.1 likely needs to run `pip install --upgrade pip setuptools wheel `)
- Zorin OS 16.1 <sup>(1.0.12-git)</sup> (15.3 lacks support for python3.7, only has 3.6.9, plus misses a lot of libraries)
- Fedora 32 Workstation or newer <sup>(1.0.12)</sup>
- Void Linux <sup>(1.0.12)</sup>
- Garuda Linux <sup>(1.0.12)</sup>
- openSUSE Tumbleweed and Leap 15.2 or newer <sup>(1.0.12)</sup>
- Slackware 64 14.2 and 15.0 <sup>(1.0.12)</sup>
- EndeavourOS <sup>(1.0.12)</sup>
  
If you encounter any bugs or incompatibilities, __please report them [here](https://github.com/amstelchen/GameInfo/issues/new)__.

Tests underway:

- Gentoo Linux (my portage is broken currently)
- Artix Linux (a bug prevents proper display of list entries)
- Haiku (just for fun, you probably won't play games on Haiku)
- NixOS 22.05 (probably never going to work)

#### Debugging

```
$ GAMEINFO_DEBUG=1 GameInfo
2022-06-09 01:42:43.612974 DEBUG: GameInfo 1.0.12
2022-06-09 01:42:43.613849 DEBUG: DistributionId: arch
2022-06-09 01:42:43.613883 DEBUG: DistributionKind: arch
2022-06-09 01:42:43.677696 DEBUG: Themes loaded: cosmo flatly litera minty lumen sandstone yeti pulse united morph journal darkly superhero solar cyborg vapor simplex cerculean 
2022-06-09 01:42:44.184135 DEBUG: Fetching system info, this can take a second...
2022-06-09 01:42:44.185443 DEBUG: Checking for wine... Time elapsed: 4.60ms

```

#### Troubleshooting

:heavy_check_mark: No distribution logo in Slackware:

```
echo "LOGO=slackware-logo" | sudo tee -a /etc/os-release
wget -O slackware-logo.svg https://upload.wikimedia.org/wikipedia/commons/3/34/Slackware_logo.svg
sudo mv slackware-logo.svg /usr/share/pixmaps
```
:heavy_check_mark: Similar to Xubuntu:
```
echo LOGO=xubuntu | sudo tee -a /etc/os-release
```

:heavy_check_mark: *GameInfo* is not on the user's PATH.

```
$ echo "# Add ~/.local/ to PATH
export PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc
```
Set accordingly when using another shell.

:heavy_check_mark: Up to `lutris-0.5.9`, a progressbar was shown even when *GameInfo* was running `lutris --version`: This has been changed with `lutris-0.5.10` onwards. 

:heavy_check_mark: dosbox (dosbox-staging) on openSUSE has a differntly formatted version-string. This has been fixed in *GameInfo*.

#### Screenshots

(always outdated)

[![https://imgur.com/JgTRGmp.png](https://imgur.com/JgTRGmp.png)](https://imgur.com/JgTRGmp.png)

#### Licences

*GameInfo* is licensed under the [GPLv2](LICENSE) license.

<a href="https://www.flaticon.com/de/kostenlose-icons/computer" title="computer Icons">Computer Icons created by Freepik - Flaticon</a>
