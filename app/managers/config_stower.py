from os.path import expanduser
import subprocess
import time

from ..utils.command import Command, Executor
from ..managers.config import Config
from ..utils.printer import prCyan, prGreen, prRed, prYellow
from ..managers.system_manager import SystemManager
import os

class ConfigStower:
    def __init__(self, config: Config):
        self.sysman: SystemManager = SystemManager(config)
        self.execr: Executor = Executor(config)
        self.conf: Config = config
        self.home: str = expanduser("~")
        self.bash_profile: str = f"{self.home}/.bash_profile"
        self.config: str = f"{self.home}/.config/"
        self.grub_default: str = "/etc/default/grub"
        self.grub_config: str = f"{self.home}/dotfiles/.config/grub/grub"
        self.tlp_default: str = "/etc/tlp.conf"
        self.tlp_config: str = f"{self.home}/dotfiles/.config/tlp/tlp.conf"
        self.xdg_default: str = "/etc/xdg/user-dirs.conf"
        self.xdg_config: str = f"{self.home}/dotfiles/.config/xdg/user-dirs.conf"
        self.firefox_dotfiles_config: str = f"{self.home}/dotfiles/.config/firefox/prefs.js"
        self.firefox_dotfiles_extensions_dir: str = f"{self.home}/dotfiles/.config/firefox/extensions/"
        self.firefox_dotfiles_extensions_config: str = f"{self.home}/dotfiles/.config/firefox/extensions.json"
        self.firefox_default_config: str

    def stow_all(self):
        self.stow_prepare()
        self.stow_grub()
        self.stow_xdg()
        self.stow_firefox_settings()
        self.stow_configs()

        if self.conf.setup_type == "laptop":
            self.stow_tlp()

    def stow_prepare(self):
        self.sysman.cd(f"{self.home}/dotfiles/")
        
        self.execr.execute("systemctl --user stop --now xdg-desktop-portal")

        if not os.path.exists(self.config):
            self.sysman.mkdir(self.config)


        self.define_firefox_profile()

        if os.path.exists(self.bash_profile):
            self.sysman.rmfile(self.bash_profile)

        if os.path.exists(self.tlp_default):
            self.sysman.rmfile(self.tlp_default)

        if os.path.exists(self.grub_default):
            self.sysman.rmfile(self.grub_default)

        if os.path.exists(self.xdg_default):
            self.sysman.rmfile(self.xdg_default)

        if os.path.exists(f"{self.firefox_default_config}/prefs.js"):
            self.sysman.rmfile(f"{self.firefox_default_config}/prefs.js")

        if os.path.exists(f"{self.firefox_default_config}/extensions/"):
            self.sysman.rmdir(f"{self.firefox_default_config}/extensions/")

        if os.path.exists(f"{self.firefox_default_config}/extensions.json"):
            self.sysman.rmfile(f"{self.firefox_default_config}/extensions.json")
            

    def stow_grub(self):
        prYellow("Stowing grub config")
        self.sysman.symlink(self.grub_config, self.grub_default)
        self.execr.execute("sudo cp -r ~/dotfiles/.config/grub/themes/sayonara /boot/grub/themes/")

    def stow_xdg(self):
        prCyan("Stowing xdg config...")
        
        self.sysman.symlink(self.xdg_config, self.xdg_default)

    def stow_tlp(self):
        prYellow("Stowing tlp config...")

        self.sysman.cp(self.tlp_config, self.tlp_default)

    def stow_configs(self):
        prCyan("Stowing .config configs...")
        self.execr.execute("stow . --ignore=user_configuration.json --ignore=install.sh --ignore=README.md --ignore dotfiles_configs", self.conf.quiet)


    def stow_firefox_settings(self):
        prCyan(f"Stowing firefox...")
        self.sysman.symlink(self.firefox_dotfiles_config, f"{self.firefox_default_config}/prefs.js")

        
    def define_firefox_profile(self):
        self.generate_firefox_config()

        firefox_dir = expanduser("~/.config/mozilla/firefox")
        firefox_dir_entry = os.listdir(firefox_dir)

        firefox_profile_dir= None 

        for entry in firefox_dir_entry:
            if entry.endswith("release"):
                firefox_profile_dir = f"{firefox_dir}/{entry}"
                # firefox_settings= f"{firefox_profile_dir}/prefs.js"

                if os.path.exists(firefox_profile_dir):
                    self.firefox_default_config = firefox_profile_dir
        
        if firefox_profile_dir:
            prGreen(f"Found firefox profile: {firefox_profile_dir}")
        else:
            prRed(f"Firefox config not found!")
            exit(1)

    def generate_firefox_config(self):
        process = subprocess.Popen(["firefox", "--headless"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)
        process.kill()




