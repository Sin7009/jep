from cx_Freeze import setup, Executable
import sys

build_exe_options = {
    'zip_include_packages': ['PyQt5.QtWidgets', 'PyQt5.QtCore', 'PyQt5.QtGui', 'dataclasses','keyboard','pyperclip'],
    'excludes': ['Qt5WebEngineCore_conda', 'Qt5WebKit'],
    'include_files': [('resources', 'resources')],
    'optimize': 2,
}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('jep.py', base=base, target_name='Своя Игра', icon='jep.ico', shortcut_name='Своя Игра', shortcut_dir='DesktopFolder')
]

setup(
    name='Своя Игра',
    version='0.0.3',
    description='Урок-викторина Своя Игра для младших школьников по предмету Мир начинается с меня. 4 класс.',
    options={'build_exe': build_exe_options},
    executables=executables
)
