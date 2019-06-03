import sys

from mmd import mmdutils

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    mmdutils.main()


if __name__ == "__main__":
    main()
