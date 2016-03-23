#! D:/owendir/programs/Python275/pythonw.exe
# digest demo
from Tkinter import Tk
import hashlib
import getpass
import sys
import subprocess
import time

r = Tk()
r.withdraw()  # disable pop-up window

key = r.clipboard_get()
print "got key: " + key

r.clipboard_clear()
r.destroy()

time.sleep(2)
exit(0)

subprocess.call(["D:/owendir/apps/KeePass-2.30/KeePass.exe",
                 "D:/userdata/owu/My Documents/OwenNewDatabase-160318.kdbx",
                 "-pw:" + key])
