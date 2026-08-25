from csv import Error
from logging import error
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
        try:
            os.makedirs(path, exist_ok=True)
        except PermissionError:
            self.execr.execute(f"sudo mkdir -p {path}")
        except Error as e:
            prRed(f"Error while creating '{path}':\n{e}")

    def rmdir(self, path: str):
        path = expanduser(path)
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except PermissionError:
                self.execr.execute(f"sudo rm -rf {path}", capture_output=self.config.quiet)

            except Error as e:
                prRed(f"Error while removing dir '{path}':\n{e}")
                exit(1)
        else:
            prRed(f"No directory: {path}") 
            exit(1)
        
    def clear_dir(self, path: str):
        path = expanduser(path)
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                os.mkdir(path)
            except PermissionError:
                self.execr.execute(f"sudo rm -rf {path}", capture_output=self.config.quiet)
                self.execr.execute(f"sudo mkdir {path}", capture_output=self.config.quiet)
            except Error as e:
                prRed(f"Error while clearing dir '{path}':\n{e}")
                exit(1)
        else:
            prRed(f"No directory: {path}")
            exit(1)

    def rmfile(self, path: str):
        path = expanduser(path)
        if os.path.exists(path):
            try:
                os.remove(path)
            except PermissionError:
                self.execr.execute(f"sudo rm -rf {path}", capture_output=self.config.quiet)
            except Error as e:
                prRed(f"Error while removing file '{path}':\n{e}")
        else:
            prRed(f"No file: {path}")
            exit(1)

    def unlink(self, path: str):
        path = expanduser(path)
        if os.path.exists(path):
            try:
                os.unlink(path)
            except PermissionError:
                self.execr.execute(f"sudo unlink {path}", capture_output=self.config.quiet)
            except Error as e:
                prRed(f"Error while unlinking '{path}':\n{e}")
                exit(1)
        else:
            prRed(f"Symlink doesn't exist: {path}") 
            exit(1)


    def symlink(self, src: str, dst: str, force=False):
        try:
            self.execr.execute(f"sudo ln -sf {src} {dst}", capture_output=self.config.quiet)

        except FileExistsError:
            prRed(f"Failed to symlink, file already exists: {dst}.")
            exit(1)

        except Error as e:
            prRed(f"Error while symlinking '{src + " to " + dst}':\n{e}")
            exit(1)

    def cp(self, src: str, dst: str):
        try:
            self.execr.execute(f"sudo cp -r {src} {dst}")
        except Error as e:
            prRed(f"Error while copying '{src}' to '{dst}':\n{e}")
            exit(1)

