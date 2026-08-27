
from ..managers.config import Config
from ..utils.command import Executor
from ..utils.printer import prCyan, prYellow


class Tweaker:
    def __init__(self, config: Config):
        self.config: Config = config
        self.execr: Executor = Executor(config)

    def tweak_all(self):
        self.tweak_audio()
        self.tweak_xdg_portal()
        self.tweak_theme_mode()
        self.tweak_rust()
        self.tweak_dm()
        self.tweak_grub()

        if self.config.setup_type == "laptop":
            self.tweak_tlp()

    def tweak_audio(self):
        self.execr.execute("systemctl --user is-enabled pipewire")
        prYellow("Turning on pipewire servers...")
        self.execr.execute("sudo systemctl enable --now pipewire wireplumber")

    def tweak_xdg_portal(self):
        self.execr.execute("systemctl --user is-enabled xdg-desktop-portal")
        
        prYellow("Turninig on xdg-desktop-portal...")
        self.execr.execute("sudo systemctl enable --now xdg-desktop-portal")

    def tweak_dm(self):
        self.execr.execute("systemctl --user is-enabled sddm")

        prYellow("Disabling sddm...")
        self.execr.execute("sudo systemctl disable --now sddm")

    def tweak_rust(self):
        prCyan("Installing rust components...")
        self.execr.execute("rustup update stable")
        self.execr.execute("rustup component add rustfmt rust-analyzer")

    def tweak_grub(self):
        prYellow("Updating grub config...")
        self.execr.execute("sudo grub-mkconfig -o /boot/grub/grub.cfg")

    def tweak_theme_mode(self):
        prCyan("Setting up theme mode...")
        self.execr.execute("gsettings set org.gnome.desktop.interface color-scheme prefer-dark")

    def tweak_tlp(self):
        self.execr.execute("systemctl --user is-enabled tlp")

        prYellow("Enabling tlp...")
        self.execr.execute("sudo systemctl enable --now tlp tlp-pd")



