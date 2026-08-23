class Config:
    def __init__(self) -> None:   
        self.deps: list[str]
        self.setup_type: str
        self.aur: str
    
    def init(self) -> None:
        self.get_setup_type()
        self.set_default_deps()
        self.add_deps()
        self.choose_aur_man()

    def init_default(self) -> None:
        self.setup_type = "desktop"
        self.set_default_deps()
        self.aur = "yay"

    def get_setup_type(self) -> None:
        print("Desktop - D, Laptop - l")
        setup_type = input("Your setup type? [D/l]: ").lower()
        self.match_setup_type(setup_type)

    def match_setup_type(self, setup_type: str) -> None:
        match setup_type:
            case "d":
                self.setup_type = "desktop"
            case "l":
                self.setup_type = "laptop"
            case _:
                pass


    def input_new_deps(self) -> None:
        try:
            new_deps = input("Enter deps between spaces: ").split()
        except:
            print("Skipping adding extra deps")
            return

        
        self.deps.extend(new_deps)

    def print_current_deps(self) -> None:
        print("Your current deps:\n")
        print(f"{self.deps}\n")

    def is_deps_addition(self) -> bool:
        self.print_current_deps()
        option = input("Would you like to add some extra deps? [Y/n]: ").lower()
        if option == "y":
            return True
        else:
            return False

    def add_deps(self) -> None:
        if self.is_deps_addition():
            self.input_new_deps()

    def set_default_deps(self) -> None:
        self.deps = ["which", "adw-gtk-theme", "swaybg", "nvim", "nvim", "nwg-look", "fuzzel", "lsd", "stow", "npm", "pipewire", "wireplumber", "rustup", "niri", "kitty", "nautilus", "firefox", "waybar", "mako", "fish", "xdg-desktop-portal", "xdg-desktop-portal-gnome", "xdg-desktop-portal-gtk", "gnome-keyring", "git"]

    def choose_aur_man(self) -> None:
        if self.is_aur():
            self.aur = input("Paru or yay? [P/y]: ").lower()

            match self.aur:
                case "y":
                    self.aur = "yay"
                case "p":
                    self.aur = "paru"
                case _:
                    pass
        else:
            self.aur = "none"

    def is_aur(self) -> bool:
        if input("Would you like to setup AUR manager? [Y/n]: ").lower() == "y":
            return True
        else:
            print("Skipping AUR installation.")
            return False

