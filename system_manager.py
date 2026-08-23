from logging import error
import os
from os.path import expanduser
from command import Command
import shutil

class SystemManager:
    def cd(self, path: str):
        path = expanduser(path)

        if os.path.exists(path):
            os.chdir(path)
        else:
            error(f"Path doesn't exists: {path}")

    def mkdir(self, path: str):
        path = expanduser(path)
        os.makedirs(path, exist_ok=True)

    def rmdir(self, path: str):
        path = expanduser(path)
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except PermissionError:
                Command(f"sudo rm -rf {path}").execute()
        else:
            error(f"No directory: {path}") 
        
    def clear_dir(self, path: str):
        path = expanduser(path)
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                os.mkdir(path)
            except PermissionError:
                Command(f"sudo rm -rf {path}").execute()
                Command(f"sudo mkdir {path}").execute()
        else:
            error(f"No directory: {path}")

    def rmfile(self, path: str):
        path = expanduser(path)
        if os.path.exists(path):
            try:
                os.remove(path)
            except:
                Command(f"sudo rm -rf {path}").execute()
        else:
            error(f"No file: {path}")

    def symlink(self, src: str, dst: str):
        try:
            os.symlink(src, dst)
        except: 
            Command(f"sudo ln -sf {src} {dst}").execute()


