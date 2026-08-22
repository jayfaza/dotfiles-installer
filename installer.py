import os
from logging import error, info, warning
from os.path import expanduser
import shutil
from config import Config 
from command import Command

class Installer:
    def __init__(self, config: Config):
        self.config: Config = config 

    def install(self):
        self.install_deps()
        self.install_dotfiles()
        if self.is_some_aur():
            self.install_aur_deps()
            self.install_aur() 
            self.install_cursor_theme()
        self.empty_config()
        self.stow_configs()
        self.clean_garbage()
        self.optional_tweaks()
        
    def install_dotfiles(self):
        if os.path.exists(expanduser("~/dotfiles")):
            warning("~/dotfiles folder is already exists.")
            return

        self.cd_home_directory()

        info("Cloning dotfiles repository...")

        Command("git clone https://github.com/jayfaza/dotfiles.git").execute()

    def install_cursor_theme(self):
        Command(f"{self.config.aur} -S bibata-cursor-theme-bin").execute()
        info("Cursor theme is set up [OK]")

    def cd_home_directory(self):
        os.chdir(expanduser("~"))

    def create_cache_dir(self):
        try:
            os.mkdir(expanduser("~/.cache"))
        except FileExistsError:
            warning("~/.cache exists. [WARN]") 

    def cd_to_cache_dir(self):
        os.chdir(expanduser("~/.cache"))

    def remove_aur_cache(self):
        shutil.rmtree(expanduser(f"~/.cache/{self.config.aur}"))

    def install_deps(self):
        info("Installing dependencies...")
        deps_cmd = Command("sudo pacman -S").expand_by(self.config.deps)
        if self.config.setup_type == "laptop":
            deps_cmd.expand_by(["tlp", "tlp-pd"])

        try:
            deps_cmd.execute()
            info("Sucsessfuly installed dependencies [OK]")
        except:
            error("FAILED to install deps [ERR]")

    def install_aur(self):
        self.create_cache_dir()
        self.cd_to_cache_dir()
        info(f"Installing {self.config.aur}")
        Command(f"git clone https://aur.archlinux.org/{self.config.aur}.git").execute()
        os.chdir(expanduser(f"~/.cache/{self.config.aur}"))
        Command("makepkg -si").execute()
        info(f"{self.config.aur} was sucsessfuly installed [OK]")

    def install_aur_deps(self):
        info("Installing AUR dependencies...")
        Command("sudo pacman -S --needed base-devel").execute()
        info("AUR dependencies was installed [OK]")

    def is_some_aur(self) -> bool:
        if self.config.aur:
            if self.config.aur == "paru" or self.config.aur == "yay":
                return True
            else:
                return False
        else:
            return False

    def stow_configs(self):
        os.chdir(expanduser("~/dotfiles"))
        self.remove_bash_profile()
        Command("stow .").execute()
        self.stow_grub()
        self.stow_xdg()
        if self.config.setup_type == "laptop":
            self.stow_tlp()

    def clean_garbage(self):
        self.remove_aur_cache() 
        self.remove_archinstall_conf()
        self.remove_install_script()
        
    def remove_archinstall_conf(self):
        conf = expanduser("~/user_configuration.json")
        if os.path.exists(conf):
            os.remove(conf)

    def remove_install_script(self):
        script = expanduser("~/install.sh")
        if os.path.exists(script):
            os.remove(script)

    def install_scripts(self):
        os.symlink(expanduser("~/dotfiles/scripts/commitdots"), "/usr/bin/cs")

    def remove_bash_profile(self):
        bash = expanduser("~/.bash_profile")
        if os.path.exists(bash):
            os.remove(bash)
            warning("Bash profile file, removing... [WARN]")

    def empty_config(self):
        try:
            shutil.rmtree(expanduser("~/.config"))
        except FileNotFoundError:
            os.mkdir(expanduser("~/.config"))
            info("Config was cleaned [OK]")
        except Exception as e:
            error(f"Error while emptying .config: {e} [ERR]")


    def stow_grub(self):
        grub_path = "/etc/default/grub"
        if os.path.exists(grub_path):
            os.chmod(grub_path, 0o777)
            os.remove(grub_path)
        os.symlink(expanduser("~/dotfiles/.config/grub/grub"), grub_path)

    def update_grub_config(self):
        Command("grub-mkconfig -o /boot/grub/grub.cfg").execute()

    def optional_tweaks(self):
        self.tweak_audio()
        self.tweak_xdg_portal()
        self.tweak_dm()
        self.update_grub_config()
        self.set_dark_mode()
        if self.config.setup_type == "laptop":
            self.tweak_tlp()

    def tweak_audio(self):
        if Command("sudo systemctl is-enabled pipewire").execute_output().stdout == "disabled":
            Command("systemctl --user enable --now pipewire").execute()
        if Command("sudo systemctl is-enabled wireplumber").execute_output().stdout == "disabled":
            Command("systemctl --user enable --now wireplumber").execute()

    def tweak_xdg_portal(self):
        if Command("sudo systemctl is-enabled xdg-desktop-portal").execute_output().stdout == "disabled":
            Command("systemctl --user enable --now xdg-desktop-portal").execute()

    def tweak_dm(self):
        if Command("sudo systemctl is-enabled sddm").execute_output().stdout == "enabled":
            Command("sudo systemctl disable sddm").execute()

    def set_dark_mode(self):
        Command("gsettings set org.gnome.desktop.interface color-scheme prefer-dark").execute()

    def tweak_tlp(self):
        if Command("sudo systemctl is-enabled tlp").execute_output().stdout == "disabled":
            Command("sudo systemctl enable --now tlp tlp-pd").execute()

    def stow_xdg(self):
        user_dirs_path = "/etc/xdg/user-dirs.conf"
        if os.path.exists(user_dirs_path):
            os.remove(user_dirs_path)
        os.symlink(expanduser("~/dotfiles/.config/xdg/user-dirs.conf"), user_dirs_path)

    def stow_tlp(self):
        tlp = "/etc/tlp.conf"
        if os.path.exists(tlp):
            os.remove(tlp)
        os.symlink(expanduser("~/dotfiles/.config/tlp/tlp.conf"), tlp)

