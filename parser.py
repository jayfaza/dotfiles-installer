import argparse

class Parser(argparse.ArgumentParser):
    def init(self) -> None:
        self.add_argument('-d', '--default', action='store_true')

