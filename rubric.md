# Rubric
####Cmd Line arguments - 5 pts
Program should accept cmd line arguments for directory to watch (dir), file extension to filter on (ext), polling interval (int) and magic text (magic). Polling interval defaults to 1.0 seconds. If the target watch directory does not exist, program should log an appropriate event message for each interval, e.g. "directory XXXXX does not exist"
####Magic Text Detection - 5 pts
The program must actually run, instead of failing instantly due to cmd line argument problems. Magic text sequences are detected within files. Detection events are logged to STDOUT, with file name and line numbers. If a line contains multiple magic strings, only one message is logged. Any previously detected magic text should not be logged again.
####OS Signal Handler - 10 pts
Program should respond to SIGINT and SIGTERM signals from the OS. signal events should be logged so that a human can determine what the signal was. Program should terminate upon either signal.
####Exception Handling - 5pts
The program should have one or more exception (try/except) handlers. Program should stay running even if the entire watched directory is suddenly deleted. Also Stay running if a watched file is deleted. Log an appropriate event message in these cases.
####Logging - 10 pts
- Use the python built-in logging module, not print statements. - All log messages should contain timestamps. - Events to log are startup banner, shutdown banner, exceptions, magic text found events, files added or removed from watched dir, and OS signal events. - Log messages to STDOUT, not to a file. - ONLY ONE termination (exit) point for the program. That is, no `sys.exit(1)` embedded in a function somewhere.
#### Repo - 5 pts
Use previously cloned repos as examples: Your Repo must have a .gitignore file. Repo shall not contain any log files, test directories/files, .vscode folder, or stray .pyc or .DS_Store files. Note however: Unittest directories and files are allowed but not required. Repo shall not contain a virtual environment. Source code should have docstrings, __author__ header, and pass all PEP8 (flake8) tests. Any meaningless commit messages such as "Done", "Finished", "Completed", "Debugged Code", "fixed bug", "asdf", "blah", and the like shall be awarded negative points.
