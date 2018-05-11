import sys
from cx_Freeze import setup, Executable

sys.modules['FixTk'] = None


pkgs = [u"future_fstrings",  u'transactions',
        u'portConstruct', u'styler', u'xlFuncs']

build_exe_options = {
    'packages': pkgs,
    'excludes': ['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter', 'PyQt4'],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="AIF-JR",
      version="1.0",
      description="A replacement for Jake Schurch!!",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base=base)])
