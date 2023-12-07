from setuptools import setup

APP_NAME = 'Work Simulator'
APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
