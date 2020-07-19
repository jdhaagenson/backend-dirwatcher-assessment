__author__ = "Jordan Haagenson"

import argparse
import logging
import os
import re
import signal
import sys
import time

import log_calls

model_directory = {}

logging.basicConfig(
    format='%(asctime)s %(levelname)8s %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def make_magic_text_pattern(magic_text):
    """
    :param magic_text: magic_text passed in through parser
    :type magic_text: str
    :return: re.Pattern object
    :rtype: re.Pattern
    """
    magic = re.compile(magic_text)



def new_timestamp():
    return time.time()


@log_calls.log_calls
def startup_banner():
    """
    Creates startup banner to be print to console at start of program
    :return: startup banner
    :rtype: str
    """
    logger.info(r'''
        -------------------------------------------------------------------------------------------
         _______   __   _______ ___                    ___  __   ____________   _______   __    __                  
        |   _   \ |  | |   __  \\  \        /\        /  / /  \ |____    ____| |  _____| |  |  |  |   
        |  | |  | |  | |  |_/  / \  \      /  \      /  / /    \     |  |      | |       |  |__|  |
        |  | |  | |  | |   _  \   \  \    / /\ \    /  / /  /\  \    |  |      | |       |   __   |
        |  | |  | |  | |  | \  \   \  \  / /  \ \  /  / /  ____  \   |  |      | |       |  |  |  |
        |  |_|  | |  | |  |  \  \   \  \/ /    \ \/  / /  /    \  \  |  |      | |_____  |  |  |  |
        |______/  |__| |__|   \__\   \___/      \___/ /__/      \__\ |__|      |_______| |__|  |__|
        -------------------------------------------------------------------------------------------
        ''' + '%(asctime)s'

    )

@log_calls.log_calls
def shutdown_banner():
    pass
@log_calls.log_calls
def scan_single_file(file, magic):
    with open(file) as f:
        f

@log_calls.log_calls
def detect_added_files():
    pass

@log_calls.log_calls
def detect_removed_files():
    pass

@log_calls.log_calls
def watch_directory(directory, ext, magic_text):
    if os.path.isdir(directory):
        files = [name for name in os.listdir(directory)
                 if name.endswith(ext)]
        # pyfiles = glob.glob(f'{directory}/*.{ext}')
        for file in files:
            model_directory[file] = scan_single_file(file, magic_text)
        detect_added_files()
        detect_removed_files()
    return model_directory


@log_calls.log_calls
def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM AND SIGINT. Other signals can be mapped here
    as well (SIGHUP?)
    Basically, it just sets a global flag, and main() will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS
    :type sig_num: int
    :param frame: Not used
    :return: None
    """
    # log the associated signal name
    logging.warning('Received ' + signal.Signals(sig_num).name)
    exit_flag = True
    if signal.Signals(sig_num).name == 'SIGINT':
        raise KeyboardInterrupt


def create_parser():
    parser = argparse.ArgumentParser(prog="Dirwatcher")
    parser.add_argument('polling_interval', '-p', default=1.0,
                        help="controls polling interval")
    parser.add_argument('magic', '-m',
                        help="specifies magic text to search for")
    parser.add_argument('ext', '-e', default='.txt',
                        help="what kind of file extension to search within")
    parser.add_argument('dir', '-d',
                        help="directory to watch")
    return parser

@log_calls.log_calls(record_history=True)
def main():
    startup_banner()
    exit_flag = False
    parser = create_parser()
    args = parser.parse_args()
    polling_interval = args.polling_interval
    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process

    while not exit_flag:
        try:
            watch_directory(args)
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            logging.error(e, "There was an error when trying to run watch_directory")
        # put a sleep inside my while loop so I don't peg the cpu usage to 100%
        time.sleep(polling_interval)

    # final exit point happens here

    shutdown_banner()
    # Log a message that we are shutting down
    # Include the overall uptime since program start
    sys.exit()


if __name__ == "__main__":
    main()