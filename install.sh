#!/bin/bash

sudo cp -v GameInfo.png /usr/share/pixmaps/GameInfo.png
sudo cp -v GameInfo.desktop /usr/share/applications/
sudo cp ~/.local/bin/GameInfo /usr/bin/GameInfo
cp -v GameInfo.desktop ~/Desktop/GameInfo.desktop

xgettext -d gameinfo -o gameinfo/locales/gameinfo.pot gameinfo/*.py
#L="nl"; LC="LC_MESSAGES"; mkdir -p $L/$LC ; msginit -l $L -o $L/$LC/gameinfo.po && msgfmt -o $L/$LC/gameinfo.mo $L/$LC/gameinfo.po
poedit 2>/dev/null
sudo cp -v gameinfo/locales/de/LC_MESSAGES/*.mo /usr/share/locale/de/LC_MESSAGES/

poetry build

poetry export --only main -f requirements.txt -o requirements.txt --without-hashes
poetry export --with dev -f requirements.txt -o requirements-dev.txt --without-hashes

#python setup.py sdist
#python -m build --wheel --no-isolation
#updpkgsums
#makepkg -fci

#xdg-open ~/Desktop/GameInfo.desktop
#python -m GameInfo
GameInfo
