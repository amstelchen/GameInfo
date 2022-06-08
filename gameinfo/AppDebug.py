from .__init__ import *
from .GameInfo import *
from datetime import datetime

gettext = gettext.translation('gameinfo', localedir=os.path.join(os.path.dirname(__file__), 'locales'))
gettext.install("gameinfo")
_ = gettext.gettext

WaitMessage = _("Fetching system info, this can take a second...")

class AppDebug():
    def debug_print(message: str, prefix="DEBUG: ", end="\n", show_time = True):
        try:
            if os.environ['GAMEINFO_DEBUG'] == "1":
                if show_time:
                    date_str = str(datetime.now())
                    timedate = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
                else:
                    timedate = ""
                print(f"{timedate} {prefix}{message}", end=end, flush=True)
        except KeyError:
            pass
