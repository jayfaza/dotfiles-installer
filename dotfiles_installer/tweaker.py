from os.path import expanduser

from command import Command
from config import Config
from printer import prCyan, prGreen, prRed, prYellow

class Tweaker:
    def __init__(self, config: Config):
        self.config: Config = config

    def tweak_all(self):
        self.tweak_audio()
        self.tweak_xdg_portal()
        self.tweak_theme_mode()
        self.tweak_rust()
        self.tweak_dm()
        self.tweak_grub()
        self.tweak_shell_configs()

        if self.config.setup_type == "laptop":
            self.tweak_tlp()

    def tweak_audio(self):
        output = Command("systemctl --user is-enabled pipewire", capture_output=True).execute_output().stdout.decode()
        if output == "disabled":
            prYellow("Turning on pipewire servers...")
            Command("sudo systemctl enable --now pipewire wireplumber", capture_output=self.config.quiet).execute()
        else:
            prGreen("Pipewire is enabled, skip...")
            pass

    def tweak_xdg_portal(self):
        output = Command("systemctl --user is-enabled xdg-desktop-portal", capture_output=True).execute_output().stdout.decode()
        
        if output == "disabled":
            prYellow("Turninig on xdg-desktop-portal...")
            Command("sudo systemctl enable --now xdg-desktop-portal", capture_output=self.config.quiet).execute()
        else:
            prGreen("xdg-desktop-portal is enabled, skip...")
            pass

    def tweak_dm(self):
        output = Command("systemctl --user is-enabled sddm", capture_output=True).execute_output().stdout.decode()

        if output == "enabled":
            prYellow("Disabling sddm...")
            Command("sudo systemctl disable --now sddm", capture_output=self.config.quiet).execute()
        else:
            prGreen("Sddm is disabled, skip...")
            pass

    def tweak_rust(self):
        prCyan("Installing rust components...")
        Command("rustup update stable", capture_output=self.config.quiet).execute()
        Command("rustup component add rustfmt rust-analyzer", capture_output=self.config.quiet).execute()

    def tweak_grub(self):
        prYellow("Updating grub config...")
        Command("sudo grub-mkconfig -o /boot/grub/grub.cfg", capture_output=self.config.quiet).execute()

    def tweak_theme_mode(self):
        prCyan("Setting up theme mode...")
        Command("gsettings set org.gnome.desktop.interface color-scheme prefer-dark", capture_output=self.config.quiet).execute()

    def tweak_tlp(self):
        output = Command("systemctl --user is-enabled tlp", capture_output=True).execute_output().stdout.decode()

        if output == "disabled":
            prYellow("Enabling tlp...")
            Command("sudo systemctl enable --now tlp tlp-pd").execute()
        else:
            prGreen("Tlp is enabled, skip...")
            pass

    def tweak_shell_configs(self):
        home = expanduser("~")
        configs = f"{home}/dotfiles/dotfiles_configs"
        setup = f"{configs}/setup"
        vm = f"{configs}/vm"
        try:
            with open(setup, "w") as f:
                f.write(self.config.setup_type)
                f.close()
            with open(vm, "w") as f:
                if self.config.setup_type == "desktop":
                    f.write("start-hyprland")
                if self.config.setup_type == "laptop":
                    f.write("niri-session")
                f.close()
        except:
            prRed("Failed to create dotfiles-configs.")
            exit(1)
