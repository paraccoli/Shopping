import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os", "subprocess"],
    "includes": ["run"],
}

setup(
    name="Shopping",
    version="1.0",
    description="Shopping Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("setup.py", base=None, icon="icon.ico")],
)