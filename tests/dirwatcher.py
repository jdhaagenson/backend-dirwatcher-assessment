__author__ = "Jordan Haagenson"

import argparse
import os
import logging
import log_calls
import log_utils
import sys
import io
import re
import time
import signal

logger =

model_directory = {}


def scan_single_file():
    pass


def detect_added_files():
    pass


def detect_removed_files():
    pass


def watch_directory():
    pass




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
    logger.warn('Received ' + signal.Signals(sig_num).name)
    exit_flag = True




def sync_directory(model, directory):
    """
    Sync directory contents to model
    :param model: Model for tracking directory contents
    :type model: dict
    :param directory: Directory to watch
    :type directory: str
    :return:
    :rtype:
    """


def create_parser():
    parser = argparse.ArgumentParser(prog="Dirwatcher")
    parser.add_argument('poll', '-p', default=1.0,
                        help="controls polling interval")
    parser.add_argument('magic', '-m',
                        help="specifies magic text to search for")
    parser.add_argument('ext', '-e', default='.txt',
                        help="what kind of file extension to search within")
    parser.add_argument('dir', '-d',
                        help="directory to watch")
    return parser


def main():
    exit_flag = False
    # Hook into these two signals from the OS
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
# Now my signal_handler will get called if OS sends
# either of these to my process

while not exit_flag:
    try:
        # call my directory watching function
        pass
    except Exception as e:
        # This is an UNHANDLED exception
        # Log an ERROR level message here
        pass
    # put a sleep inside my while loop so I don't peg the cpu usage to 100%
    time.sleep(polling_interval)

    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start



