from .GameInfo import *

class AppDebug():
    def debug_print(message):
        try:
            if os.environ['GAMEINFO_DEBUG'] == "1":
                print("DEBUG: " + message)
        except:
            pass
