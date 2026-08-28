import argparse

class Parser(argparse.ArgumentParser):
    def init(self) -> None:
        group = self.add_mutually_exclusive_group(required=True)
        self.add_argument('-d', '--default', action='store_true')
        self.add_argument('-q', '--quiet', action='store_true')
        self.add_argument('-s', '--sync', action='store_true')
        group.add_argument('-p', '--push', action='store_true')
        group.add_argument('-u', '--update', action='store_true')
        group.add_argument('-i', '--install', action='store_true')
        

