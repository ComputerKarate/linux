#!/usr/bin/python3
import os
import logging as log
import datetime
import glob
from configparser import ConfigParser

VERSION = 'DirectoryCleanup\nVersion: 1.0.0'
#############################################
# 3 files are required to operate:
#
# 1. DirectoryCleanup.py   -> This application
# 2. DirectoryCleanup.cfg  -> Application configuration
# 3. DirectoryCleanup.data -> List of directories to process
#
#############################################

#############################################
# Program configuration for this script
CleanupConfigFile = 'DirectoryCleanup.cfg'
config = ConfigParser()
config.read(CleanupConfigFile)


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
DataValuesFile = "DirectoryCleanup.data"


#############################################
# Begin processing variables
#############################################
# A new logfile will be created every day
loggingDirectory = config['DEFAULT']['LogDirectory']
formattedDate = datetime.datetime.now().strftime("%Y-%m-%d")

# Top level directories from data file
datavalues = []

# List of files to check
fileList = []

# List of directories to check
dirList = []

#############################################
##### Setup logging environment
#############################################
def initializeLogging(APP_NAME):
    # Explicitly control the '/' or '\' appended to the path
    logFileName = loggingDirectory.rstrip('/').rstrip('\\') + '/' + APP_NAME + '_' + formattedDate + '.log'

    if not os.path.exists(loggingDirectory):
        logit(loggingDirectory + " not found creating now")
        try:
            os.makedirs(loggingDirectory)
        except OSError:
            logit("\tERROR: Attempting to create directory: %s" % (loggingDirectory))

    # The logging module will setup several important defaults
    log.basicConfig(
        filename=logFileName,
        level='DEBUG',
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S'
    )

    logit("========================================")
    logit("%s Logging initialized" % (APP_NAME))
    logit("")


#############################################
##### Log the message
#############################################
def logit(message):
    if config.getboolean("DEFAULT", "DEBUG"):
        print(message)
    log.info(message)



#############################################
##### Read list directories to process
def ReadCleanupList():
    global datavalues

    logit("\tReading entries from %s" % (DataValuesFile))

    filehandle = open(DataValuesFile, "r")
    tempvalues = filehandle.read()
    tempvalues = tempvalues.splitlines()

    # Try to only accept clean entries
    for value in tempvalues:
        # Skip comments and empty lines
        if not value.startswith('#') and len(value) > 1:
            datavalues.append(value)

    logit("\t%s entries read from %s" % (len(datavalues), DataValuesFile))



#############################################
##### Process list of candidates
def ProcessCleanupList():
    global fileList
    global dirList

    logit("ProcessCleanupList start")

    for entry in datavalues:
        entrylist = entry.split('|')
        startProcessing(entrylist)

    removeFile(fileList)
    removeDirectory(dirList)
    fileList.clear()
    dirList.clear()

    logit("ProcessCleanupList complete")



#############################################
##### Delete files flagged as aged out
def removeFile(file_list):

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
def removeDirectory(dir_list):

    for dir in dir_list:
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
def startProcessing(record):
    global fileList
    global dirList
    searchDirectoryPattern = ""

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

    # If no file pattern was specified recursively grab them all
    if record[2] == '':
        searchDirectoryPattern = record[0] + '/**/*'
    else:
        searchDirectoryPattern = record[0] + '/' + record[2]

    rawlist = glob.glob(searchDirectoryPattern, recursive=True)

    for entry in rawlist:
        file_timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(entry))
        if threshold_date > file_timestamp:
            logit("\t\tProcessing: %s" % entry)
            if os.path.isdir(entry):
                dirList.append(entry) 
            elif os.path.isfile(entry):
                fileList.append(entry)



#############################################
##### Processing begins here
#############################################
initializeLogging("DiskCleanup")
ReadCleanupList()
ProcessCleanupList()

logit("Cleanup complete")
logit("========================================")
