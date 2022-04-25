from .GameInfo import Application
#from .AppDebug import AppDebug

def main():
    app = Application()           
    #app.title(f'{__appname__} {__version__}')
    app.mainloop() 

if __name__ == '__main__':
    main()
