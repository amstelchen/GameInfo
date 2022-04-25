#!/bin/bash

sudo cp -v GameInfo.png /usr/share/pixmaps/GameInfo.png
sudo cp -v GameInfo.desktop /usr/share/applications/
sudo cp ~/.local/bin/GameInfo /usr/bin/GameInfo
cp -v GameInfo.desktop ~/Desktop/GameInfo.desktop

xgettext -d gameinfo -o gameinfo/locales/gameinfo.pot gameinfo/*.py
poedit 2>/dev/null
sudo cp -v gameinfo/locales/de/LC_MESSAGES/*.mo /usr/share/locale/de/LC_MESSAGES/

#python setup.py sdist
#python -m build --wheel --no-isolation
#updpkgsums
#makepkg -fci

#xdg-open ~/Desktop/GameInfo.desktop
python -m GameInfo
#GoalFM.py