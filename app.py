import sys

from parser import Parser
from config import Config
from installer import Installer

class App:
    def run(self):
        parser = Parser(prog="Jayfaza's dotfiles master.")

        parser.init()
        args = parser.parse_args()
        config = Config()

        config.quiet = args.quiet
        config.update = args.update
        
        if config.update:
            config.setup_type = "desktop"
            Installer(config).update_all()
            exit(0)


        if args.default:
            config.init_default()
        else:
            config.init()


        Installer(config).install()
        exit(0)


