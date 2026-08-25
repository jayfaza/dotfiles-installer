import argparse

class Parser(argparse.ArgumentParser):
    def init(self) -> None:
        self.add_argument('-d', '--default', action='store_true')
        self.add_argument('-q', '--quiet', action='store_true')
        self.add_argument('-u', '--update', action='store_true')

