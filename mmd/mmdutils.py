import argparse
import logging
import os
import sys
from configparser import ConfigParser
from os import path
from mmd.version import PROGRAM_VERSION
from mmd.mmdlib import Analyser

# constants
PROGRAM_NAME = "mmdutils"
STD_OUT_LOG_FORMATTER = "* %(message)s"
LOG_FORMATTER = "%(asctime)s %(module)s %(funcName)s %(lineno)d %(message)s"
LOG_FILE = PROGRAM_NAME + ".log"
CONFIG_FILE_NAME = PROGRAM_NAME + ".conf"
MENU_MAIN_DESC = "MMD Utils Program."
LOGGING_LEVEL = logging.DEBUG
EXIT_CODE_OK = 0
EXIT_CODE_ERROR = 2
ENV_CONFIG_PATH = "CONFIG_PATH"


def main():
    """ MMD utils program. """

    # build main menu parser
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME, description=MENU_MAIN_DESC)
    parser.add_argument('-V', '-v', '--version', action='version', version='%(prog)s (version {})'.format(PROGRAM_VERSION))
    parser.add_argument("-c", "-config", dest="config", default=None, required=False, help="Optional config path.")

    # create a new logger
    logger = logging.getLogger("mmdutils")

    # build the sub program parsers
    subparsers = parser.add_subparsers(title="mmd commands")
    create_commands(logger, subparsers)
    add_common_args(subparsers)

    # parse the user's args
    args = parser.parse_args()

    # get config path and load config object
    config_path = get_config_path(args)
    config = load_config(config_path)

    # configure the logger
    configure_logger(logger, config)

    # if no args are given then output basic info and exit
    if len(sys.argv) == 1:
        print_usage(parser)
        return EXIT_CODE_OK

    # determine if -verbose option specified and if so add a log handler to stdout
    if args.verbose:
        configure_verbose_option(logger)

    # log config path and user commands
    logger.info("command: " + " ".join(sys.argv))

    # invoke the correct handler based on the user's sub command and args
    try:
        args.func(args)
    except KeyboardInterrupt:
        logger.info("program execution interrupted by user")
        return EXIT_CODE_OK
    except ValueError as ve:
        logger.error(ve)
        sys.stderr.write("Error: " + str(ve) + "\n")
        return EXIT_CODE_ERROR
    except Exception as e:
        logger.error(e)
        sys.stderr.write(repr(e) + "\n")
        return EXIT_CODE_ERROR

    return EXIT_CODE_OK


def load_config(config_path):
    # configure the config parser
    config = ConfigParser()
    if config_path is not None:
        config.read(config_path)
    return config


def add_common_args(subparsers):
    # iterate the subparsers internal dict and add a verbose option to each one
    for sub_name, sub in subparsers.__dict__['choices'].items():
        sub.add_argument("-verbose", dest="verbose", action="store_true", help="Output more info to console.")


def create_commands(logger, subparsers):
    # order matters in the help dialog
    Analyser(logger, subparsers)


def configure_verbose_option(logger):
    log_handler_std_out = logging.StreamHandler(sys.stdout)
    log_handler_std_out.setLevel(logging.DEBUG)
    log_handler_std_out.setFormatter(logging.Formatter(STD_OUT_LOG_FORMATTER))
    logger.addHandler(log_handler_std_out)
    logger.info("verbose option enabled")


def get_config_path(args):
    # if the config file is provided via command line arg then always use that
    if args.config is not None:
        return args.config

    # otherwise look for a config file path
    config_file = None
    config_home = path.join(path.expanduser("~/.config/mmdutils"), CONFIG_FILE_NAME)
    config_etc = path.join("/etc", CONFIG_FILE_NAME)

    # conf file search order:
    #   0. see if an env variable is set
    #   1. search the executable directory
    #   2. search the user's home directory
    #   3. search /etc
    if ENV_CONFIG_PATH in os.environ:
        config_file = os.environ[ENV_CONFIG_PATH]
    if path.isfile(CONFIG_FILE_NAME):
        config_file = path.join(".", CONFIG_FILE_NAME)
    elif path.isfile(config_home):
        config_file = config_home
    elif path.isfile(config_etc):
        config_file = config_etc
    return config_file


def configure_logger(logger, config):
    log_file = None
    log_disabled = None

    if config is not None:
        if "defaults" in config and "log_file" in config["defaults"]:
            log_file = config["defaults"]["log_file"]
        if "defaults" in config and "log_disabled" in config["defaults"]:
            log_disabled = config["defaults"]["log_disabled"]

    # configure a logger
    logger.setLevel(LOGGING_LEVEL)
    if log_disabled is not None:
        logger.disabled = log_disabled in ['true', '1', 'True', 'TRUE', 'yes']
        if logger.disabled:
            print("logging disabled by config file!")
    # configure default logger file writer
    if log_file is not None:
        log_handler_file = logging.FileHandler(log_file)
    else:
        log_handler_file = logging.FileHandler(LOG_FILE)
    log_handler_file.setFormatter(logging.Formatter(LOG_FORMATTER))
    log_handler_file.setLevel(LOGGING_LEVEL)
    logger.addHandler(log_handler_file)


def print_usage(parser):
    print("usage: mmdutils [-h] [-V] <command>")
    print("\ncommands:\n")

    # retrieve subparsers from parser
    subparsers_actions = [
        action for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)]

    # loop the actions
    for subparsers_action in subparsers_actions:
        # get all subparsers and print top description line
        for choice, subparser in subparsers_action.choices.items():
            print("{}{} {}".format(choice,
                                   " " * (23 - len(choice)),
                                   subparser.description.split('\n')[0]))
    print("")


def str_to_bool(s):
    if s == 'True':
        return True
    else:
        return False


if __name__ == "__main__":
    sys.exit(main())
