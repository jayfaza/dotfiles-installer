from argparse import Namespace

from ..utils.printer import bcolors, prCyan, prPurple, prRed, prYellow


class Config:
    def __init__(self, args: Namespace) -> None:   
        self.deps_list: list[str]
        self.deps_str: str
        self.setup_type: str
        self.aur: str
        self.quiet: bool = args.quiet
        self.update: bool = args.update
        self.default: bool = args.default
        self.install: bool = args.install
        self.caelestia: bool
    
    def init(self) -> None:
        if self.default or self.update:
            self.get_setup_type()
            self.init_default()
            return

        self.get_setup_type()
        self.set_default_deps()
        self.add_deps()
        self.choose_aur_man()

    def init_default(self) -> None:
        self.caelestia = False
        self.set_default_deps()
        self.aur = "yay"

    def get_setup_type(self) -> None:
        while True:
            prPurple("Desktop - D, Laptop - l.")
            setup_type = input(f"{bcolors.BOLD}Your setup type? [D/l]: {bcolors.ENDC}").lower()
            if setup_type != "d" and setup_type != "l":
                continue
            else:
                break

        self.set_setup_type(setup_type)

    def set_setup_type(self, setup_type: str) -> None:
        match setup_type:
            case "d":
                self.setup_type = "desktop"
            case "l":
                self.setup_type = "laptop"
            case _:
                pass


    def input_new_deps(self) -> None:
        try:
            new_deps_list = input("Enter".format(bcolors.OKCYAN) + "deps".format(bcolors.WARNING) + "between spaces: ".format(bcolors.OKCYAN)).split()
            new_deps_str = ''.join(new_deps_list)
        except:
            prRed("Error whith dependencies adding.")
            exit(1)

        
        self.deps_list.extend(new_deps_list)
        self.deps_str += new_deps_str

    def print_current_deps(self) -> None:
        prCyan("Your current deps:\n")
        prYellow(f"{self.deps_list}\n")

    def is_deps_addition(self) -> bool:
        self.print_current_deps()
        while True:

            option = input(f"{bcolors.OKCYAN}Would you like to add some extra deps? [Y/n]: {bcolors.ENDC}").lower()
            if option == "y":
                return True
            if option == "n":
                return False
            else:
                continue

    def add_deps(self) -> None:
        if self.is_deps_addition():
            self.input_new_deps()

    def set_default_deps(self) -> None:
        self.deps_list = ["uwsm", "unzip", "which", "adw-gtk-theme", "swaybg", "nvim", "nvim", "nwg-look", "fuzzel", "lsd", "stow", "npm", "pipewire", "wireplumber", "rustup", "niri", "kitty", "nautilus", "firefox", "waybar", "mako", "fish", "xdg-desktop-portal", "xdg-desktop-portal-gnome", "xdg-desktop-portal-gtk", "gnome-keyring", "git"]
        self.deps_str = " ".join(self.deps_list)

    def choose_aur_man(self) -> None:
        if self.is_aur():
            while True:

                self.aur = input(f"{bcolors.OKCYAN}Paru or yay? [P/y]: {bcolors.ENDC}").lower()

                match self.aur:
                    case "y":
                        self.aur = "yay"
                        break
                    case "p":
                        self.aur = "paru"
                        break
                    case _:
                        continue 
        else:
            self.aur = "none"

    def is_aur(self) -> bool:
        while True:
            aur = input(f"{bcolors.OKCYAN} Would you like to setup AUR manager? [Y/n]: {bcolors.ENDC}").lower() 
            if aur == "y":
                return True
            elif aur == "n":
                print("Skipping AUR installation.")
                return False
            else:
                continue

    def is_caelestia(self):
        while True:
            caelestia = input(f"{bcolors.OKCYAN} Would you like to install caelestia-shell? [Y/n]: {bcolors.ENDC}").lower()
            match caelestia:
                case "y":
                    self.caelestia = True
                    break
                case "n":
                    self.caelestia = False
                    break
                case _:
                    continue


