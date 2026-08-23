import os
from os.path import expanduser
from printer import prCyan, prGreen, prYellow
from system_manager import SystemManager
from config import Config 
from command import Command
from config_stower import ConfigStower
from tweaker import Tweaker
from garbage_cleaner import GarbageCleaner

class Installer:
    def __init__(self, config: Config):
        self.config: Config = config 
        self.sysman: SystemManager = SystemManager(config)
        self.config_stower: ConfigStower = ConfigStower(config)
        self.tweaker: Tweaker = Tweaker(config)
        self.garbage_cleaner: GarbageCleaner = GarbageCleaner(config)
        self.quiet: bool = config.quiet 

    def update_all(self):
        self.update_packages()
        self.install_dotfiles()
        self.config_stower.stow_all()
        self.garbage_cleaner.clear_garbage()

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

        prGreen(f"\nEverything has been prepared and installed.\n Welcome back!")
        
    def install_dotfiles(self):
        prCyan("Downloading jayfaza's dotfiles...")
        if os.path.exists(expanduser("~/dotfiles")):

            prYellow("~/dotfiles folder is already exists!")
            prYellow("Updating dotfiles repository...")
            self.sysman.cd("~/dotfiles/")
            Command("git pull --force", capture_output=self.quiet).execute()
            return


        self.sysman.cd("~")

        Command("git clone https://github.com/jayfaza/dotfiles.git", capture_output=self.quiet).execute()

    def install_cursor_theme(self):
        prCyan("Installing cursor theme...")
        Command(f"{self.config.aur} -S bibata-cursor-theme-bin", capture_output=self.quiet).execute()

    def install_deps(self):
        prCyan(f"Installing dotfiles dependencies\n\n{self.config.deps}")
        deps_cmd = Command("sudo pacman -S", capture_output=self.quiet).expand_by(self.config.deps)
        if self.config.setup_type == "laptop":
            prYellow(f"Installing 'tlp' 'tlp-pd' packages for laptop setup...")
            deps_cmd = deps_cmd.expand_by(["tlp", "tlp-pd"])
        deps_cmd.execute()

    def install_aur(self):
        prYellow(f"Installing AUR: {self.config.aur}")

        self.sysman.mkdir("~/.cache")
        self.sysman.cd("~/.cache")

        Command(f"git clone https://aur.archlinux.org/{self.config.aur}.git", capture_output=self.quiet).execute()

        self.sysman.cd(f"~/.cache/{self.config.aur}")

        Command("makepkg -si", capture_output=self.quiet).execute()

    def install_aur_deps(self):
        prCyan("Installing AUR dependencies...")
        Command("sudo pacman -S --needed base-devel", capture_output=self.quiet).execute()

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
        Command("sudo pacman -Syu", capture_output=self.quiet).execute()

