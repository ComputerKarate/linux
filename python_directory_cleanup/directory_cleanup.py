#!/usr/bin/python3
import os
import sys
import logging as log
import datetime
import glob
from configparser import ConfigParser

VERSION = 'directory_cleanup\nVersion: 1.0.0'
#############################################
# 3 files are required to operate:
#
# 1. directory_cleanup.py   -> This application
# 2. directory_cleanup.cfg  -> Application configuration
# 3. directory_cleanup.data -> List of directories to process
#
# TODO: Wrap all print statements in a test
# TODO: Create a usage() to display the config options
# TODO: Make "cleanup_config_file" a cli argument
# TODO: Find a way to process hidden files when python3 < 3.11
#       Glob cannot process hidden files and directories, at least on Linux, until Python 3.11+
#       On Linux, hidden is defined as a file or directory with a leading "."
#       This is a low priority since "." files are usually small and empty "." directories don't
#       take a lot of space
#
#############################################

#############################################
# Program configuration for this script
cleanup_config_file = 'directory_cleanup.cfg'
config = ConfigParser()
config.read(cleanup_config_file)

#############################################
# The application reads a data file to
# retrieve a list of directories and file types
# to process
#
# The syntax for a config entry is:
#   Required   : Required :  optional
# <root folder>:<num days>:<file pattern>
#
#############################################

#############################################
# Begin processing variables
#############################################
# A new logfile will be created every day
logging_directory = ""
formatted_date = datetime.datetime.now().strftime("%Y-%m-%d")
startup_messages = [] # System messages will be logged later
log_system_online = False

# This is populated from cleanup_config_file
data_values_file = ""

# Top level directories from data file
data_values = []

# List of files to check
file_list = []

# List of directories to check
directory_list = []

# Establish verbosity level
VERBOSE_LOGGING = False

# If running interactively, print as well as log
PRINT_OUTPUT = False


#############################################
##### Establish values for required configuration
#############################################
def initialize_configuration_values():
    global VERBOSE_LOGGING
    global data_values_file 
    global PRINT_OUTPUT  

    # Useful if running interactively instead of as a SystemD service
    if config['DEFAULT']['PRINT_OUTPUT']:
        if 'True' == config['DEFAULT']['PRINT_OUTPUT']:
            PRINT_OUTPUT = True
            startup_messages.append("All output will be printed as well as logged")
            print("All output will be printed as well as logged")

    if config['DEFAULT']['verbose_logging']:
        if PRINT_OUTPUT:
            startup_messages.append("Config value for verbose logging is: %s" % config['DEFAULT']['verbose_logging'])
            print("Config value for verbose logging is: %s" % config['DEFAULT']['verbose_logging'])
        if 'True' == config['DEFAULT']['verbose_logging']:
            VERBOSE_LOGGING = True

    if config['DEFAULT']['verbose_logging_trigger_filename']:
        # Check for file existence
        if os.path.isfile(config['DEFAULT']['verbose_logging_trigger_filename']):
            if PRINT_OUTPUT:
                print("***** %s exists. Turning on verbose logging" % config['DEFAULT']['verbose_logging_trigger_filename'])
                print("***** Delete %s to disable verbose logging" % config['DEFAULT']['verbose_logging_trigger_filename'])
            startup_messages.append("***** %s exists. Turning on verbose logging" % config['DEFAULT']['verbose_logging_trigger_filename'])
            startup_messages.append("***** Delete %s to disable verbose logging" % config['DEFAULT']['verbose_logging_trigger_filename'])
            VERBOSE_LOGGING = True

    if config['DEFAULT']['data_values_file']:
        data_values_file = config['DEFAULT']['data_values_file']
        if PRINT_OUTPUT:
            print("Processing directories found in: %s" % data_values_file)
        if os.path.isfile(data_values_file):
            if PRINT_OUTPUT:
                print("%s exists. Processing will continue..." % data_values_file)
        else:
            print("ERROR: Required file: %s not found. Processing will stop" % data_values_file)
            quit()

#############################################
##### Setup logging environment
#############################################
def initialize_logging(APP_NAME):
    global logging_directory
    global log_system_online

    if config['DEFAULT']['log_directory']:
        logging_directory = config['DEFAULT']['log_directory']
    else:
        logging_directory = '/tmp'
        if PRINT_OUTPUT:
            startup_messages.append("ERROR: Config value missing for log_directory in %s" % cleanup_config_file)
            print("ERROR: Config value missing for log_directory in %s" % cleanup_config_file)
            startup_messages.append("RECOVERY: Setting Logging directory to %s" % logging_directory)
            print("RECOVERY: Setting Logging directory to %s" % logging_directory)

    if not os.path.exists(logging_directory):
        startup_messages.append("ERROR: %s not found creating now" % logging_directory)
        print("ERROR: %s not found creating now" % logging_directory)

        try:
            os.makedirs(logging_directory)
        except OSError:
            print("ERROR: Failed to create directory: %s. Exiting immediately" % (logging_directory))
            quit()

    log.basicConfig(
        # Explicitly control the '/' or '\' appended to the path
        filename=logging_directory.rstrip('/').rstrip('\\') + '/' + APP_NAME + '_' + formatted_date + '.log',
        level='INFO',
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S'
    )
    
    log_system_online = True

    logit("========================================")
    logit("%s logging initialized" % (APP_NAME))
    logit("")
    if len(startup_messages) > 0:
        logit("Startup messages:")
        for message in startup_messages:
            logit(message)
        logit("Startup messages complete")


#############################################
##### Log the message
#############################################
def logit(message):
    if PRINT_OUTPUT:
        print(message)
    if log_system_online:
        log.info(message)


#############################################
##### Read list directories to process
def read_cleanup_list():
    global data_values

    logit("\tReading entries from %s" % (data_values_file))

    filehandle = open(data_values_file, "r")
    tempvalues = filehandle.read()
    tempvalues = tempvalues.splitlines()

    for value in tempvalues:
        # Skip comments and empty lines
        if not value.startswith('#') and len(value) > 1:
            data_values.append(value)

    logit("\t%s entries read from %s" % (len(data_values), data_values_file))



#############################################
##### Process list of candidates
#############################################
def process_cleanup_list():
    global file_list
    global directory_list

    if VERBOSE_LOGGING:
        logit("process_cleanup_list start")

    for entry in data_values:
        entrylist = entry.split('|')
        start_processing(entrylist)

    remove_file(file_list)
    remove_directory(directory_list)
    file_list.clear()
    directory_list.clear()

    if VERBOSE_LOGGING:
        logit("process_cleanup_list complete")



#############################################
##### Delete files flagged as aged out
def remove_file(file_list):
    for file in file_list:
        logit("\tRemoving File: %s" % (file))
        # It will be rare that the delete process
        # throws an error but it could crash the
        # program and processing would stop until
        # manually resolved
        try:
            os.remove(file)
        except:
            logit("ERROR: Unable to delete file: %s" % (file))



#############################################
##### Delete directories flagged as aged out
def remove_directory(directory_list):
    for dir in directory_list:
        logit("\tDeleting Directory: %s" % (dir))
        # This is a try / except because we only
        # want to delete empty directories. We have
        # already pruned the files so any existing files
        # are not aged out yet. Hierarchy of empty
        # directories do not take much space and do
        # not pose a security risk
        try:
            os.rmdir(dir)
        except OSError:
            logit("\tNOTE: %s not empty, skipping" % (dir))



#############################################
##### Primary processing function
# The expected format for 'record'  is:
# ['directory entry', 'file age in days', 'file pattern']
#############################################
def start_processing(record):
    global file_list
    global directory_list
    search_directory_pattern = ""

    # record[1] is a string we convert to an integer
    # representing a number of days. We then subtract the current
    # datetime to compare it against the file/dir datetime
    threshold_date = datetime.datetime.now() - datetime.timedelta(days = int(record[1]))

    # Control formatting by always removing trailing slash from the end of path
    record[0] = record[0].rstrip('/').rstrip('\\')

    # Verify directory exists
    # If a directory does not exist, it will be ignored
    if not os.path.isdir(record[0]):
        logit("ERROR: %s does not exist. Do you need to create it?" % (record[0]))
    else:
        if VERBOSE_LOGGING:
            logit("     record[0]: %s, threshold_date: %s, record[2]: %s" % (record[0], threshold_date, record[2]))

        # If no file pattern was specified recursively grab them all
        if record[2] == '':
            search_directory_pattern = record[0] + '/**/*'
        else:
            search_directory_pattern = record[0] + '/' + record[2]

        if VERBOSE_LOGGING:
            logit("     search_directory_pattern: %s" % (search_directory_pattern))

        if sys.version_info < (3, 11):
            rawlist = glob.glob(search_directory_pattern, recursive=True)
        else:
            rawlist = glob.glob(search_directory_pattern, recursive=True, include_hidden=True)

        for entry in rawlist:
            file_timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(entry))
            if threshold_date > file_timestamp:
                if os.path.isdir(entry):
                    directory_list.append(entry) 
                elif os.path.isfile(entry):
                    file_list.append(entry)



#############################################
##### Processing begins here
#############################################
initialize_configuration_values()
initialize_logging("directory_cleanup")
if sys.version_info < (3, 11):
    if VERBOSE_LOGGING:
        logit("     python version < 3.11, hidden files will not be processed")
else:
    if VERBOSE_LOGGING:
        logit("     python version 3.11 or greater, hidden files will be processed")
read_cleanup_list()
process_cleanup_list()

logit("Cleanup complete")
logit("========================================")
