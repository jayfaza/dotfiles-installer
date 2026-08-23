from parser import Parser
from config import Config
from installer import Installer

class App:
    def run(self):
        parser = Parser(prog="Jayfaza's dotfiles master.")

        parser.init()
        args = parser.parse_args()
        config = Config()

        if args.default:
            config.init_default()
        else:
            config.init()

        Installer(config).install()


