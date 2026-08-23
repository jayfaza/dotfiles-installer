from command import Command

class Tweaker:
    def __init__(self, setup: str):
        self.setup: str = setup

    def tweak_all(self):
        self.tweak_audio()
        self.tweak_xdg_portal()
        self.tweak_theme_mode()
        self.tweak_rust()
        self.tweak_dm()
        self.tweak_grub()

        if self.setup == "laptop":
            self.tweak_tlp()

    def tweak_audio(self):
        output = Command("systemctl --user is-enabled pipewire").execute_output().stdout.decode()
        if output == "disabled":
            Command("sudo systemctl enable --now pipewire wireplumber").execute()
        else:
            pass

    def tweak_xdg_portal(self):
        output = Command("systemctl --user is-enabled xdg-desktop-portal").execute_output().stdout.decode()
        
        if output == "disabled":
            Command("sudo systemctl enable --now xdg-desktop-portal").execute()
        else:
            pass

    def tweak_dm(self):
        output = Command("systemctl --user is-enabled sddm").execute_output().stdout.decode()

        if output == "enabled":
            Command("sudo systemctl disable --now sddm").execute()
        else:
            pass

    def tweak_rust(self):
        Command("rustup update stable").execute()
        Command("rustup component add rustfmt rust-analyzer").execute()

    def tweak_grub(self):
        Command("sudo grub-mkconfig -o /boot/grub/grub.cfg").execute()

    def tweak_theme_mode(self):
        Command("gsettings set org.gnome.desktop.interface color-scheme prefer-dark").execute()

    def tweak_tlp(self):
        output = Command("systemctl --user is-enabled tlp").execute_output().stdout.decode()

        if output == "disabled":
            Command("sudo systemctl enable --now tlp tlp-pd").execute()
        else:
            pass

