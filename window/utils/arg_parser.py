import argparse
import sys


class NyangaArgParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(
            2,
            f"\n\033[1m\033[31m{self.prog}: error: {message}, please refer to -h / --help \033[0m\n\n",
        )
