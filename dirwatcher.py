##
__author__ = "Jordan Haagenson"

import argparse
import logging
import os
# import re
import signal
import sys
import time

##
global model_directory
model_directory = {}

##
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

##
global logger
logger = setup_logger()

##
def new_timestamp():
    return time.time()

##
def startup_banner(t):
    """
    Create start-up banner
    :param t: timestamp
    :type t: float
    :return: startup banner
    """
    return logger.info(
        r''' STARTING UP...
        -------------------------------------------------------------------------------------------
         Starting Up at {} ({})
         _______   __   _______ ___                    ___  __   ____________   _______   __    __              
        |   _   \ |  | |   __  \\  \        /\        /  / /  \ |____    ____| |  _____| |  |  |  |   
        |  | |  | |  | |  |_/  / \  \      /  \      /  / /    \     |  |      | |       |  |__|  |
        |  | |  | |  | |   _  \   \  \    / /\ \    /  / /  /\  \    |  |      | |       |   __   |
        |  | |  | |  | |  | \  \   \  \  / /  \ \  /  / /  ____  \   |  |      | |       |  |  |  |
        |  |_|  | |  | |  |  \  \   \  \/ /    \ \/  / /  /    \  \  |  |      | |_____  |  |  |  |
        |______/  |__| |__|   \__\   \___/      \___/ /__/      \__\ |__|      |_______| |__|  |__|
        -------------------------------------------------------------------------------------------
        '''.format(t, time.ctime(t))
    )

##
def shutdown_banner(t, elapsed):
    """
    Creates shutdown banner
    :param t: time since startup
    :type t: float
    :return: shutdown banner
    """
    return logger.info(
        r""" SHUTTING DOWN....
        ---------------------------------------------------------------------
        Shutting down at {} ({})
        Total uptime was {} ~ about {} seconds
         ____________  __    __   _______     _______   ___    __   _______
        |____    ____||  |  |  | |   ____|   |   ____| |   \  |  | |   _   \
             |  |     |  |__|  | |  |____    |  |____  |    \ |  | |  | \   |
             |  |     |   __   | |   ____|   |   ____| |  |\ \|  | |  |  |  |
             |  |     |  |  |  | |  |        |  |      |  | \    | |  |  |  |
             |  |     |  |  |  | |  |____    |  |____  |  |  \   | |  |_/   |
             |__|     |__|  |__| |_______|   |_______| |__|   \__| |_______/ 
        ---------------------------------------------------------------------
        """
            .format(t, time.ctime(t), elapsed, round(elapsed))
    )

##
def scan_single_file(key, value, magic):
    """
    Scans a single file for a magic string, only reads up to first instance of magic string
    then assigns position of magic string to value of model_directory, this is the same value
    that will be used to start reading from next time the file is scanned.
    If no magic string is found, assigns value to -1 so that the contents aren't read again next time
    the function is called.
    :param key: file name
    :type key: str
    :param value: index of magic string or 0 for new files
    :type value: int
    :param magic: magic string to search for
    :type magic: str
    :return: model_directory
    :rtype: dict
    """
    global model_directory
    try:
        if value >= 0:
            with open(key) as f:
                f.seek(value + 1, 1) if value > 0 else f.seek(value, 1)
                index = f.read().find(magic)
                model_directory[key] = index
                if index == -1:
                    logger.info("No magic text found in file: {}".format(key))
                else:
                    logger.info("Found magic string at index {} inside file: {}".format(index, key))
        return model_directory
    except Exception as e:
        logger.error("There was a {} error trying to scan file {}".format(e.args, key))

##
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
    global model_directory
    try:
        for file in files:
            if file not in model_directory.keys():
                model_directory[file] = 0
                logger.info('New file added to dictionary: {}'.format(file))
                scan_single_file(file, 0, magic)
        return model_directory
    except Exception as e:
        logger.error("There was a {} error while trying to detect added files".format(e.args))
        return model_directory

##
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
    global model_directory
    try:
        for key in model_directory.keys():
            if key not in files:
                model_directory.pop(key)
                logger.info('File removed from directory: {}'.format(key))
        return model_directory
    except Exception as e:
        logger.error("There was a {} error while trying to detect removed files".format(e.args))
        return model_directory

##
def watch_directory(directory, ext, magic_text):
    """
    Syncs the model_directory to the changing conditions
    in the actual directory
    :param directory: directory the program is watching
    :type directory: str
    :param ext: extension of files to look for inside of directory (example: .txt)
    :type ext: str
    :param magic_text: magic string to pass into added files function
    :type magic_text: str
    :return: model_directory
    :rtype: dict
    """
    global model_directory
    try:
        if os.path.isdir(directory):
            # files = [name for name in os.listdir(directory)
            #          if name.endswith(ext)]
            files = get_list_files(directory, ext)
            detect_added_files(files, magic_text)
            detect_removed_files(files)
            sync_directory(magic_text)
            return model_directory
    except Exception as e:
        logger.error("Directory {} does not exist".format(directory))
        return model_directory

def get_list_files(directory, ext):
    """
    Gets a list of all files in the target directory
    :param directory: directory to target
    :type directory: str
    :param ext: extension of files to look for
    :type ext: str
    :return: list of files with ext in the directory
    :rtype: list
    """
    try:
        if os.path.isdir(directory):
            files = [f'{directory}/{name}' for name in os.listdir(directory)
                     if name.endswith(ext)]
            return files
    except Exception as e:
        logger.error('There was a[n] {} error when trying to open directory'.format(e.args))

##
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
    global exit_flag
    signames = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                    if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warning('Received signal: ' + signames[sig_num])
    if sig_num == signal.SIGINT or signal.SIGTERM:
        exit_flag = True

##
def sync_directory(magic):
    """
    Opens each file already in model_directory and searches for magic string inside
    and assigns the value of the corresponding file in the dictionary to be the
    first instance it finds of magic string. It does not go line by line however, it goes
    by character. So if there are multiple instances of magic string in the same line, the
    first instance will be logged, and then the next time the function runs, it will capture
    the next and so on
    :param magic: magic string
    :type magic: str
    :return: model_directory with positions of magic string, if found
    :rtype: dict
    """
    global model_directory
    try:
        for k, v in model_directory.items():
            if v != -1:
                with open(k) as f:
                    contents = f.read()
                    f.seek(v + 1) if v > 0 else f.seek(v)
                    match = contents.find(magic, v + 1)
                    model_directory[k] = match
                    if match == -1:
                        logger.info("Magic string not found in {}".format(k))
                    else:
                        logger.info("Magic string found at position {} in file {}".format(match, k))
        return model_directory
    except Exception as e:
        logger.error("There was a[n] {} error while trying to sync directory".format(e.args))
        return model_directory

##
def create_parser():
    """
    Create the parser to be used by dirwatcher
    :return: parser
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(prog="dirwatcher")
    parser.add_argument('--poll', '-p', default=5, type=float,
                        help="controls polling interval")
    parser.add_argument('--magic', default='magic', type=str,
                        help="specifies magic text to search for")
    parser.add_argument('--ext', default='.txt', type=str,
                        help="what kind of file extension to search within")
    parser.add_argument('--dir', default='test_dir', type=str,
                        help="directory to watch")
    return parser

##
def main():
    """
    The main loop that houses all the calls to various functions,
    and runs the program from start to finish
    """
    global exit_flag
    global model_directory

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
            # files = get_list_files(args.dir, args.ext)
            # detect_added_files(args.dir, files, args.magic)
            # detect_removed_files(files)
            sync_directory(args.magic)
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            logger.error("There was a[n] {} error when trying to run watch_directory".format(e.args))
        # put a sleep inside my while loop so I don't peg the cpu usage to 100%
        time.sleep(polling_interval)

    # final exit point happens here
    shutdown_time = new_timestamp()
    # Log a message that we are shutting down
    # Include the overall uptime since program start
    shutdown_banner(shutdown_time, shutdown_time - startup_time)
    sys.exit()


if __name__ == "__main__":
    main()
