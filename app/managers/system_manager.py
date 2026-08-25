from csv import Error
from logging import error
from ntpath import exists
import os
from os.path import expanduser
from ..utils.command import Command, Executor
import shutil

from ..managers.config import Config
from ..utils.printer import prRed

class SystemManager:
    def __init__(self, config: Config):
        self.config: Config = config
        self.execr: Executor = Executor(config)

    def cd(self, path: str):
        path = expanduser(path)

        if os.path.exists(path):
            os.chdir(path)
        else:
            error(f"Path doesn't exists: {path}")

    def mkdir(self, path: str):
        path = expanduser(path)
        self.execr.execute(f"sudo mkdir -p {path}")

    def rmdir(self, path: str):
        path = expanduser(path)
        if os.path.exists(path):
            self.execr.execute(f"sudo rm -rf {path}")
        else:
            prRed(f"No directory: {path}") 
            exit(1)
        
    def clear_dir(self, path: str):
        path = expanduser(path)
        if os.path.exists(path):
            self.execr.execute(f"sudo rm -rf {path}")
            self.execr.execute(f"sudo mkdir {path}")
        else:
            prRed(f"No directory: {path}")
            exit(1)

    def rmfile(self, path: str):
        path = expanduser(path)
        if os.path.exists(path):
            self.execr.execute(f"sudo rm -rf {path}")
        else:
            prRed(f"No file: {path}")
            exit(1)

    def unlink(self, path: str):
        path = expanduser(path)
        if os.path.exists(path):
                self.execr.execute(f"sudo unlink {path}")
        else:
            prRed(f"Symlink doesn't exist: {path}") 
            exit(1)


    def symlink(self, src: str, dst: str):
        if not os.path.exists(dst):
            self.execr.execute(f"sudo ln -sf {src} {dst}")
        else:
            prRed(f"Symlink already exists: {dst}")


    def cp(self, src: str, dst: str):
        if not os.path.exists(dst):
            self.execr.execute(f"sudo cp -r {src} {dst}")
        else:
            prRed("Failed to copy, file exists: {dst}")
            exit(1)

