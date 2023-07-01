#!C:\Users\antod\Documents\Bastien\3. ETS\E23\MGA802-Python\Cours 3 (1005)\Jeu du pendu\Projet_Finale\projet_aeroport_env\Scripts\python.exe

# $Id: rst2xetex.py 9115 2022-07-28 17:06:24Z milde $
# Author: Guenter Milde
# Copyright: This module has been placed in the public domain.

"""
A minimal front end to the Docutils Publisher, producing Lua/XeLaTeX code.
"""

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except Exception:
    pass

from docutils.core import publish_cmdline

description = ('Generates LaTeX documents from standalone reStructuredText '
               'sources for compilation with the Unicode-aware TeX variants '
               'XeLaTeX or LuaLaTeX. '
               'Reads from <source> (default is stdin) and writes to '
               '<destination> (default is stdout).  See '
               '<https://docutils.sourceforge.io/docs/user/latex.html> for '
               'the full reference.')

publish_cmdline(writer_name='xetex', description=description)
