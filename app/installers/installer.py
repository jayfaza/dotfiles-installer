import os

from os.path import expanduser
from ..utils.printer import prCyan, prGreen, prYellow
from ..managers.system_manager import SystemManager
from ..managers.config import Config 
from ..utils.command import Command, Executor
from ..managers.config_stower import ConfigStower
from ..managers.tweaker import Tweaker
from ..managers.garbage_cleaner import GarbageCleaner

class Installer:
    def __init__(self, config: Config):
        self.config: Config = config 
        self.sysman: SystemManager = SystemManager(config)
        self.execr: Executor = Executor(config)
        self.config_stower: ConfigStower = ConfigStower(config)
        self.tweaker: Tweaker = Tweaker(config)
        self.garbage_cleaner: GarbageCleaner = GarbageCleaner(config)

    def update_everything(self):
        self.update_packages()
        self.install_dotfiles()
        self.config_stower.stow_all()
        self.garbage_cleaner.clear_garbage()

        prGreen(f"\nEverything has been updated!")

    def install(self):
        if self.config.update:
            self.update_everything()
            return

        self.install_deps()
        if self.is_some_aur():
            self.install_aur_deps()
            self.install_aur() 
            self.install_cursor_theme()
            if self.config.caelestia:
                self.install_caelestia()

        self.install_dotfiles()
        self.config_stower.stow_all()
        self.garbage_cleaner.clear_garbage()
        self.tweaker.tweak_all()

        prGreen(f"\nEverything has been prepared and installed.\n Welcome back!")
        
    def install_dotfiles(self):
        prCyan("Downloading jayfaza's dotfiles...")
        if os.path.exists(expanduser("~/dotfiles")):

            prYellow("~/dotfiles repository already exists!")
            prYellow("Updating dotfiles repository...")
            self.update_dotfiles()
            self.sysman.cd("~/dotfiles")
            return


        self.sysman.cd("~")

        self.execr.execute("git clone https://github.com/jayfaza/dotfiles.git")

    def install_cursor_theme(self):
        prCyan("Installing cursor theme...")
        if self.config.quiet:
            self.execr.execute(f"{self.config.aur} -S bibata-cursor-theme-bin --noconfirm")
        else: 
            self.execr.execute(f"{self.config.aur} -S bibata-cursor-theme-bin")

    def install_deps(self):
        prCyan(f"Installing dotfiles dependencies:\n\n{self.config.deps_list}\n")

        if self.config.quiet:
            self.execr.execute(f"sudo pacman -S {self.config.deps_str} --noconfirm")
            if self.config.setup_type == "laptop":
                self.execr.execute("sudo pacman -S tlp tlp-pd --noconfirm")
        else:
            self.execr.execute(f"sudo pacman -S {self.config.deps_str}")

            if self.config.setup_type == "laptop":
                self.execr.execute("sudo pacman -S tlp tlp-pd")


    def install_aur(self):
        prYellow(f"Installing AUR: {self.config.aur}")
        
        cache = expanduser("~/.cache")
        self.sysman.mkdir(cache)
        self.sysman.cd(cache)
        aur = f"{cache}/{self.config.aur}"

        if os.path.exists(aur):
            self.sysman.rmdir(aur)

        self.execr.execute(f"git clone https://aur.archlinux.org/{self.config.aur}.git", capture_output=self.config.quiet)

        self.sysman.cd(f"~/.cache/{self.config.aur}")

        if self.config.quiet:
            self.execr.execute("makepkg -si --noconfirm")
        else:
            self.execr.execute("makepkg -si")


    def install_aur_deps(self):
        prCyan("Installing AUR dependencies...")
        self.execr.execute(f"sudo pacman -S --needed base-devel", capture_output=self.config.quiet)

        if self.config.quiet:
            self.execr.execute(f"sudo pacman -S --needed base-devel --noconfirm")
        else:
            self.execr.execute(f"sudo pacman -S --needed base-devel")

    def is_some_aur(self) -> bool:
        
        if self.config.aur:
            if self.config.aur == "paru" or self.config.aur == "yay":
                return True
            elif self.config.aur == "none":
                return False
            else:
                return False
        else:
            return False

    def update_packages(self):
        prCyan("Updating packages...") 
        if self.config.quiet:
            self.execr.execute("sudo pacman -Syu --noconfirm")
        else:
            self.execr.execute("sudo pacman -Syu")


    def update_dotfiles(self):
        self.sysman.cd("~")
        self.sysman.clear_dir("~/dotfiles")
        self.execr.execute("git clone https://github.com/jayfaza/dotfiles.git")

    def install_caelestia(self):
        prCyan(f"Installing caelestia...")
        if not self.config.quiet:
            self.execr.execute(f"{self.config.aur} -S midnight-shell-git")
        if self.config.quiet:
            self.execr.execute(f"{self.config.aur} -S midnight-shell-git --noconfirm")
        

