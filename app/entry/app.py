import sys

from ..utils.parser import Parser
from ..managers.config import Config
from ..installers.installer import Installer
from ..utils.printer import prRed

class App:
    def run(self):
        parser = Parser(prog="Jayfaza's dotfiles master.")

        parser.init()
        args = parser.parse_args()
        config = Config(args)

        config.init()

        Installer(config).install()
        exit(0)


