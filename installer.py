import os
from logging import error, info, warning
from os.path import expanduser
from system_manager import SystemManager
from config import Config 
from command import Command
from config_stower import ConfigStower
from tweaker import Tweaker
from garbage_cleaner import GarbageCleaner

class Installer:
    def __init__(self, config: Config):
        self.config: Config = config 
        self.sysman: SystemManager = SystemManager()
        self.config_stower: ConfigStower = ConfigStower(config.setup_type)
        self.tweaker: Tweaker = Tweaker(config.setup_type)
        self.garbage_cleaner: GarbageCleaner = GarbageCleaner(config)

    def install(self):
        self.install_deps()
        self.install_dotfiles()
        if self.is_some_aur():
            self.install_aur_deps()
            self.install_aur() 
            self.install_cursor_theme()
        self.config_stower.stow()
        self.garbage_cleaner.clear_garbage()
        self.tweaker.tweak_all()

        warning("Everything has been prepared and installed, Welcome back!")
        
    def install_dotfiles(self):
        if os.path.exists(expanduser("~/dotfiles")):
            warning("~/dotfiles folder is already exists.")
            return

        self.sysman.cd("~")

        Command("git clone https://github.com/jayfaza/dotfiles.git").execute()

    def install_cursor_theme(self):
        Command(f"{self.config.aur} -S bibata-cursor-theme-bin").execute()

    def install_deps(self):
        deps_cmd = Command("sudo pacman -S").expand_by(self.config.deps)
        if self.config.setup_type == "laptop":
            deps_cmd = deps_cmd.expand_by(["tlp", "tlp-pd"])
        deps_cmd.execute()

    def install_aur(self):
        self.sysman.mkdir("~/.cache")
        self.sysman.cd("~/.cache")

        info(f"Installing {self.config.aur}")

        Command(f"git clone https://aur.archlinux.org/{self.config.aur}.git").execute()

        self.sysman.cd(f"~/.cache/{self.config.aur}")

        Command("makepkg -si").execute()

    def install_aur_deps(self):
        Command("sudo pacman -S --needed base-devel").execute()

    def is_some_aur(self) -> bool:
        if self.config.aur:
            if self.config.aur == "paru" or self.config.aur == "yay":
                return True
            else:
                return False
        else:
            return False

