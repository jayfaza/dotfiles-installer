from os.path import expanduser
import os

from config import Config
from printer import prYellow 
from system_manager import SystemManager

class GarbageCleaner:
    def __init__(self, config: Config):
        self.sysman: SystemManager = SystemManager(config)
        self.config: Config = config 
        home = expanduser("~")
        self.aur_cache_dir: str = f"{home}/.cache/"
        self.archinstall_conf: str = f"{home}/user_configuration.json"
        self.installscript_file: str = f"{home}/install.sh"

    def clear_garbage(self):
        self.remove_aur_cache()
        self.remove_archinstall_conf()
        self.remove_install_script()

    def remove_aur_cache(self):
        prYellow("Clearing AUR installation cache...")
        if os.path.exists(self.aur_cache_dir):
            self.sysman.rmdir(self.aur_cache_dir)

    def remove_archinstall_conf(self):
        prYellow("Clearing userless archinstall config...")
        if os.path.exists(self.archinstall_conf):
            self.sysman.unlink(self.archinstall_conf)

    def remove_install_script(self):
        prYellow("Clearing bash installation script...")
        if os.path.exists(self.installscript_file):
            self.sysman.unlink(self.installscript_file)
 

