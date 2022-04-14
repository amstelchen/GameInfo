#!/bin/bash

sudo cp -v GameInfo.png /usr/share/pixmaps/GameInfo.png
sudo cp -v GameInfo.desktop /usr/share/applications/
cp -v GameInfo.desktop ~/Desktop/GameInfo.desktop

xgettext -d gameinfo -o locales/gameinfo.pot *.py
#poedit 2>/dev/null

#python setup.py sdist
#python -m build --wheel --no-isolation
#updpkgsums
#makepkg -fci

#xdg-open ~/Desktop/GameInfo.desktop
python -m GameInfo
#GoalFM.py