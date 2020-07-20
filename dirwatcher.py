__author__ = "Jordan Haagenson"

import argparse
import logging
import os
# import re
import signal
import sys
import time
# import glob

# import log_calls

model_directory = {}
global model_directory


def setup_logger():
    '''
    Create handlers and formatters, then connect them to a logger
    :return: logger
    :rtype: logging.Logger
    '''
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)8s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


logger = setup_logger()


def new_timestamp():
    return time.time()


# @log_calls.log_calls
def startup_banner(t):
    """
    Create start-up banner
    :param t: timestamp
    :type t: float
    :return: startup banner
    """
    return logger.info(r'''
        -------------------------------------------------------------------------------------------
         _______   __   _______ ___                    ___  __   ____________   _______   __    __                  
        |   _   \ |  | |   __  \\  \        /\        /  / /  \ |____    ____| |  _____| |  |  |  |   
        |  | |  | |  | |  |_/  / \  \      /  \      /  / /    \     |  |      | |       |  |__|  |
        |  | |  | |  | |   _  \   \  \    / /\ \    /  / /  /\  \    |  |      | |       |   __   |
        |  | |  | |  | |  | \  \   \  \  / /  \ \  /  / /  ____  \   |  |      | |       |  |  |  |
        |  |_|  | |  | |  |  \  \   \  \/ /    \ \/  / /  /    \  \  |  |      | |_____  |  |  |  |
        |______/  |__| |__|   \__\   \___/      \___/ /__/      \__\ |__|      |_______| |__|  |__|
        -------------------------------------------------------------------------------------------
        ''' + f'{t}'
    )


# @log_calls.log_calls
def shutdown_banner(t):
    """
    Creates shutdown banner
    :param t: time since startup
    :type t: float
    :return: shutdown banner
    """
    return logger.info(r"""
        -------------------------------------------------------------------------------------------
         _______   __   _______ ___                    ___  __   ____________   _______   __    __ 
        |   _   \ |  | |   __  \\  \        /\        /  / /  \ |____    ____| |  _____| |  |  |  |
        |  | |  | |  | |  |_/  / \  \      /  \      /  / /    \     |  |      | |       |  |__|  |
        |  | |  | |  | |   _  \   \  \    / /\ \    /  / /  /\  \    |  |      | |       |   __   |
        |  | |  | |  | |  | \  \   \  \  / /  \ \  /  / /  ____  \   |  |      | |       |  |  |  |
        |  |_|  | |  | |  |  \  \   \  \/ /    \ \/  / /  /    \  \  |  |      | |_____  |  |  |  |
        |______/  |__| |__|   \__\   \___/      \___/ /__/      \__\ |__|      |_______| |__|  |__|
        -------------------------------------------------------------------------------------------
        """ + f'total uptime: {t}'
    )


# @log_calls.log_calls
def scan_single_file(file, magic):
    """
    Scans a single file for magic string and returns first
    line containing magic string or last read line
    :param file: filename
    :type file: str
    :param magic: magic string
    :type magic: str
    :return: index of last read line
    :rtype: int
    """
    try:
        with open(file) as f:
            last_read = model_directory[file] if model_directory[file] is type(int) else 0
            for line in f:
                index = line.find(magic, last_read)
                if index == -1:
                    logger.info("No magic text found")
            # string = f.read()
            # index = string.find(magic)
            # f.seek(index, 1)
                else:
                    logger.info("Found magic string at %(index)s")
        return index
    except Exception as e:
        logger.error(e)
    return model_directory


# @log_calls.log_calls
def detect_added_files(files, magic):
    """
    Check list of files against model_directory,
    if there is a file not already in model_directory,
    it's added to the directory, and scanned for magic string
    :param files: list of files matching parameters in directory
    :type files: list
    :param magic: magic string to pass into scanning a new file
    :type magic: str
    :return: model_directory with any new added files
    :rtype: dict
    """
    try:
        for file in files:
            if file not in model_directory.keys():
                model_directory[file] = scan_single_file(file, magic)
                logger.info('New file added to dictionary - %(file)s')
        return model_directory
    except Exception as e:
        logger.error(e)
    return model_directory


# @log_calls.log_calls
def detect_removed_files(files):
    """
    Check list of files against model_directory,
    if there is a file in model_directory that isn't in files list,
    remove from dictionary
    :param files: list of files matching parameters in directory
    :type files: list
    :return: model_directory updated
    :rtype: dict
    """
    try:
        for key in model_directory.keys():
            if key not in files:
                model_directory.pop(key)
                logger.info('File removed from directory: %(key)s')
        return model_directory
    except Exception as e:
        logger.error(e)
    return model_directory


# @log_calls.log_calls
def watch_directory(directory, ext, magic_text):
    """
    syncs the model_directory to the changing conditions in the actual directory
    :param directory: directory the program is watching
    :type directory: str
    :param ext: extension of files to look for inside of directory (example: .txt)
    :type ext: str
    :param magic_text: magic string to pass into added files function
    :type magic_text: str
    :return: model_directory
    :rtype: dict
    """
    try:
        if os.path.isdir(directory):
            files = [name for name in os.listdir(directory)
                     if name.endswith(ext)]
            detect_added_files(files, magic_text)
            detect_removed_files(files)
        return model_directory
    except Exception as e:
        logger.error(e)
        os.mkdir(directory)
    return model_directory


# @log_calls.log_calls
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
    logger.warning('Received %(signal.Signals(sig_num).name)s at %(new_timestamp())s')
    exit_flag = True



def create_parser():
    """
    Create the parser to be used by dirwatcher
    :return: parser
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(prog="Dirwatcher")
    parser.add_argument('--poll', '-p', default=5, type=float,
                        help="controls polling interval")
    parser.add_argument('--magic', default='magic', type=str,
                        help="specifies magic text to search for")
    parser.add_argument('--ext', default='.txt', type=str,
                        help="what kind of file extension to search within")
    parser.add_argument('--dir', default='test_dir', type=str,
                        help="directory to watch")
    return parser


# @log_calls.log_calls(record_history=True)
def main():
    """
    The main loop that houses all the calls to various functions,
    and runs the program from start to finish
    """
    logger = setup_logger()
    startup_time = new_timestamp()
    startup_banner(startup_time)
    exit_flag = False
    parser = create_parser()
    args = parser.parse_args()
    polling_interval = args.poll
    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process

    while not exit_flag:
        try:
            watch_directory(args.dir, args.ext, args.magic)
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            logger.error(e, "There was an error when trying to run watch_directory")
        # put a sleep inside my while loop so I don't peg the cpu usage to 100%
        time.sleep(polling_interval)

    # final exit point happens here
    shutdown_time = new_timestamp()
    # Log a message that we are shutting down
    # Include the overall uptime since program start
    shutdown_banner(shutdown_time-startup_time)
    sys.exit()


if __name__ == "__main__":
    main()