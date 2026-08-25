import sys

from parser import Parser
from config import Config
from installer import Installer
from printer import prRed

class App:
    def run(self):
        parser = Parser(prog="Jayfaza's dotfiles master.")

        parser.init()
        args = parser.parse_args()
        config = Config(args)

        config.init()

        Installer(config).install()
        exit(0)


