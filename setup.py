
import sys
from cx_Freeze import setup, Executable



base = None
targetName = 'Spritemator.exe'


if sys.platform == 'win32':
    base = 'Win32GUI'


exe = Executable(
    script='src/application.py',
    base=base,
    targetName = targetName
)

options = {
    'build_exe' : {
        'excludes' : ['curses', 'email', 'tcl', 'ttk', 'tkinter'],
        'compressed' : True,
    }
}



setup(
    name="Spritemator",
    version="0.6",
    description="A Sprite editor and animator",
    executables=[exe],
    options=options, requires=['PyQt5']
)