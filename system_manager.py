from csv import Error
from logging import error
import os
from os.path import expanduser
from command import Command
import shutil

from config import Config
from printer import prRed

class SystemManager:
    def __init__(self, config: Config):
        self.quiet: bool = config.quiet

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
            Command(f"sudo mkdir -p {path}").execute()
        except Error as e:
            prRed(f"Error while creating '{path}':\n{e}")

    def rmdir(self, path: str):
        path = expanduser(path)
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except PermissionError:
                Command(f"sudo rm -rf {path}", capture_output=self.quiet).execute()

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
                Command(f"sudo rm -rf {path}", capture_output=self.quiet).execute()
                Command(f"sudo mkdir {path}", capture_output=self.quiet).execute()
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
                Command(f"sudo rm -rf {path}", capture_output=self.quiet).execute()
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
                Command(f"sudo unlink {path}", capture_output=self.quiet).execute()
            except Error as e:
                prRed(f"Error while unlinking '{path}':\n{e}")
                exit(1)
        else:
            prRed(f"Symlink doesn't exist: {path}") 
            exit(1)


    def symlink(self, src: str, dst: str, force=False):
        try:
            Command(f"sudo rm -rf {dst} && sudo ln -s {src} {dst}", capture_output=self.quiet).execute()

        except FileExistsError:
            prRed(f"Failed to symlink, file already exists: {dst}.")
            exit(1)

        except Error as e:
            prRed(f"Error while symlinking '{src + " to " + dst}':\n{e}")
            exit(1)

    def cp(self, src: str, dst: str):
        try:
            Command(f"sudo cp -r {src} {dst}").execute()
        except Error as e:
            prRed(f"Error while copying '{src}' to '{dst}':\n{e}")
            exit(1)

