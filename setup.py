import sys
from cx_Freeze import setup, Executable

# Dependencias adicionales si las tienes
# dependencies = ['mysql.connector']

build_exe_options = {
    'packages': [],
    'excludes': [],
    'includes': [],
    'include_files': []
}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'  # Si deseas una interfaz gráfica en Windows

executables = [Executable('ejecutablemenu.py', base=base)]

setup(
    name='VirtualMenu',
    version='1.0',
    description='Virtual Menu Application',
    options={'build_exe': build_exe_options},
    executables=executables
)
