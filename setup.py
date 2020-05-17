from cx_Freeze import setup, Executable
import sys

base = None
if (sys.platform == "win32"):
    base = "Win32GUI" 

executables = [Executable("program.py", base=base, icon='fav.ico')]

packages = ["tkinter", "essentials"]
options = {
    'build_exe': {    
        'packages':packages
    },    
}

setup(
    name = "MkNxGn BR Proxy",
    options = options,
    version = "1.0.0",
    description = 'MkNxGn BR Proxy for Minecraft BedRock Server - Created By Mark.',
    executables = executables
)