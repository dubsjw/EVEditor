import sys
from cx_Freeze import setup, Executable

build_exe_options = {}

exe = Executable(
    script = "EVEditor/EVEditor.py",
    base="Win32GUI",
    targetName="Product.exe"
)
    
setup(  name = "EVEditor",
        version = "1.0.0",
        author = "Jacob Dubs",
        description = "A simple environment variable editor.",
        options = {"build_exe": build_exe_options},
        executables = [exe])