from .__init__ import *
from .GameInfo import *

gettext = gettext.translation('gameinfo', localedir=os.path.join(os.path.dirname(__file__), 'locales'), languages=['de'])
gettext.install("gameinfo")
_ = gettext.gettext

WaitMessage = _("Fetching system info, this can take a second...")

class AppDebug():
    def debug_print(message):
        try:
            if os.environ['GAMEINFO_DEBUG'] == "1":
                print("DEBUG: " + message)
        except:
            pass
