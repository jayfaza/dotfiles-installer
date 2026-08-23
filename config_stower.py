from logging import error
from os.path import expanduser
import subprocess

from command import Command
from system_manager import SystemManager
import os

class ConfigStower:
    def __init__(self, setup: str):
        self.sysman: SystemManager = SystemManager()
        self.setup: str = setup
        self.home: str = expanduser("~")
        self.bash_profile: str = f"{self.home}/.bash_profile"
        self.config: str = f"{self.home}/.config/"
        self.grub_default: str = "/etc/default/grub"
        self.grub_config: str = f"{self.home}/dotfiles/.config/grub/grub"
        self.tlp_default: str = "/etc/tlp.conf"
        self.tlp_config: str = f"{self.home}/dotfiles/.config/tlp/tlp.conf"
        self.xdg_default: str = "/etc/xdg/user-dirs.conf"
        self.xdg_config: str = f"{self.home}/dotfiles/.config/xdg/user-dirs.conf"

    def stow(self):
        self.stow_prepare()
        self.stow_grub()
        self.stow_xdg()
        self.stow_all()

        if self.setup == "laptop":
            self.stow_tlp()

    def stow_prepare(self):
        self.sysman.cd(f"{self.home}/dotfiles/")
        
        if os.path.exists(self.config):
            self.sysman.clear_dir(self.config)
        else:
            self.sysman.mkdir(self.config)

        if os.path.exists(self.bash_profile):
            self.sysman.rmfile(self.bash_profile)

        if os.path.exists(self.tlp_default):
            self.sysman.rmfile(self.tlp_default)

        if os.path.exists(self.grub_default):
            self.sysman.rmfile(self.grub_default)

    def stow_grub(self):
        self.sysman.symlink(self.grub_config, self.grub_default)

    def stow_xdg(self):
        self.sysman.symlink(self.xdg_config, self.xdg_default)

    def stow_tlp(self):
        self.sysman.symlink(self.tlp_config, self.tlp_default)

    def stow_all(self):
        Command("stow .").execute()
        


