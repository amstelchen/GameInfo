import os
from os.path import isfile, join
from pathlib import Path
from datetime import datetime, timezone

from .AppDebug import AppDebug
from .BitsBytes import bytes2human

import gettext

gettext = gettext.translation('gameinfo', localedir=os.path.join(os.path.dirname(__file__), 'locales'))
gettext.install("gameinfo")
_ = gettext.gettext

def SteamLogs() -> str:
    prefixes = ["~/.local/share/Steam", "~/.steam/steam/", "~/.steampath", "~/.steam/bin32/"]
    returnString = "Steam install folders:=\n\n"

    for prefix in prefixes:
        returnString += str(prefix) + ":="
        if os.path.isdir(os.path.expanduser(str(prefix))):
            returnString += _("Yes") + "\n"
        else:
            returnString += _("No") + "\n"
        #returnString += str(prefix) + ":" + print("Yes") if os.path.isdir(str(prefix)) == True else print("No") + "\n"
    logFoldersPath = Path(os.path.expanduser('~/.steam/steam/logs/'))

    sum_current_log_files, sum_previous_log_files = 0, 0

    returnString += "\nCurrent log files:\n\n"
    all_current_log_files = [f for f in sorted(logFoldersPath.glob('**/*.txt')) if f.is_file() and "previous" not in f.stem and "log_" not in f.stem]
    for file in all_current_log_files:
        modified = datetime.fromtimestamp(file.stat().st_mtime, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')
        sum_current_log_files += file.stat().st_size
        returnString += f"{file.stem + '' + file.suffix:22s}={file.stat().st_size:>9,d} Bytes{'':>3} {modified}\n" # {(timestamp_stop - timestamp_start):1.3f} "
    returnString += f"={sum_current_log_files:>9,d} Bytes ({bytes2human(sum_current_log_files)}B) total"

    returnString += "\nPrevious log files:\n\n"
    all_previous_log_files = [f for f in sorted(logFoldersPath.glob('**/*.txt')) if f.is_file() and ("previous" in f.stem or "log_" in f.stem)]
    for file in all_previous_log_files:
        modified = datetime.fromtimestamp(file.stat().st_mtime, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')
        sum_previous_log_files += file.stat().st_size
        returnString += f"{file.stem + '' + file.suffix:22s}={file.stat().st_size:>9,d} Bytes{'':>3} {modified}\n" # {(timestamp_stop - timestamp_start):1.3f} "
    if sum_previous_log_files == 0:
        returnString += "(none found)"
    else:
        returnString += f"={sum_previous_log_files:>9,d} Bytes ({bytes2human(sum_previous_log_files)}B) total"

    return returnString
