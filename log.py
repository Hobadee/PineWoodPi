#!/usr/bin/python3

import time
import threading                    # To make logs thread-safe
from enum import Enum, unique

#import os                                               # Used for OS interaction (os.system('clear'))

@unique
class logLevels(Enum):
    NONE = 0
    FATAL = 1
    ERROR = 2
    WARNING = 3
    INFO = 4
    DEBUG = 5
    TRACE = 6
    

##
# Class for a log entry
# 
class logEntry:

    timestamp = None
    log = None
    level = None

    def __init__(self, log, level):
        self.timestamp = time.time()
        self.log = log

        try:
            # Try mapping to an ENUM
            if(isinstance(level, int)):
                level = logLevels(level)
            if(isinstance(level, str)):
                level = logLevels[level]
            #if(isinstance(level, logLevels)):
                # We are all good 
        except:
            # We can't map to an ENUM.
            # Default to INFO level for this entry
            # It would be nice to log this as a WARNING, but we don't have a pointer to our parent
            level = logLevels['INFO']

        self.level = level
    
    def getLog(self):
        return self.log
    
    def getLevel(self):
        return self.level.name
    
    def getTimestamp(self):
        return self.timestamp

    def isLevel(self, level):
        return self.level == level
    
    ##
    # Returns if this logs timestamp is before a given timestamp
    #
    def isBefore(self, timestamp):
        return self.timestamp < timestamp
    
    ##
    # Returns if this logs timestamp is after a given timestamp
    #
    def isAfter(self, timestamp):
        return self.timestamp > timestamp


##
# Class to log data
# Should have different output options.  (Serial, web, etc...)
#
class log:

    timestampStart = None
    defaultLevel = None
    displayLevel = None
    logs = []
    # TODO: Implement list of outputs
    # Each output should have it's own displayLevel
    # Possible outputs: print, serial, web, etc...
    outputs = []
    
    def __init__(self, defaultLevel=None, displayLevel=None):
        # Take a timestamp of when logging was started
        self.timestampStart = time.time()
        # Enable this to be thread-safe
        self._lock = threading.Lock()

        self.defaultLevel = self.mapENUM('INFO')
        self.displayLevel = self.mapENUM('INFO')

        if(defaultLevel):
            self.defaultLevel = defaultLevel
        if(displayLevel):
            self.displayLevel = displayLevel
    
    
    ##
    # TODO: Take ENUMs into account
    #
    def setDisplayLevel(self, displayLevel):
        displayLevel = self.mapENUM(displayLevel)
        self.displayLevel = displayLevel
    

    ##
    # TODO: Take ENUMs into account
    #
    def setDefaultLevel(self, defaultLevel):
        defaultLevel = self.mapENUM(defaultLevel)
        self.defaultLevel = defaultLevel

    
    ##
    # Map a level to an ENUM
    # TODO: Finish implementation!
    #
    def mapENUM(self, level):
        try:
            # Try mapping to an ENUM
            if(isinstance(level, int)):
                level = logLevels(level)
            if(isinstance(level, str)):
                level = logLevels[level]
            #if(isinstance(level, logLevels)):
                # We are all good 
        except:
            # We can't map to an ENUM.
            self.write("Cannot map \"{}\" to a logLevels ENUM!  Will be logged as {}".format(level, self.defaultLevel), level="WARNING")
            level = self.defaultLevel
        finally:
            return level
    

    ##
    # Write a message to the log
    #
    # Valid log levels may be passed as strings, ints, or logLevels ENUM
    # 0 - NONE
    # 1 - FATAL
    # 2 - ERROR
    # 3 - WARNING
    # 4 - INFO
    # 5 - DEBUG
    # 6 - TRACE
    #
    # forceOP will force the log to be output, even if that message would normally be hidden
    #
    def write(self, log, level=None, forceOP=False):

        # If level hasn't been set, default it
        if(level == None):
            level = self.defaultLevel

        # Map level to an ENUM
        level = self.mapENUM(level)

        # Make the write operation thread-safe
        with self._lock:
            self.logs.append(logEntry(log, level))

            if(self.displayLevel.value >= level.value or forceOP):
                opLog = self.getLast()
                self.output(opLog)
    

    ##
    # Log a FATAL message
    #
    def fatal(self, log):
        self.write(log, level='FATAL')
    

    ##
    # Log an ERROR message
    #
    def error(self, log):
        self.write(log, level='ERROR')
    

    ##
    # Log a WARNING message
    #
    def warning(self, log):
        self.write(log, level='WARNING')
    

    ##
    # Log an INFO message
    #
    def info(self, log):
        self.write(log, level='INFO')


    ##
    # Log a DEBUG message
    #
    def debug(self, log):
        self.write(log, level='DEBUG')
    

    ##
    # Log a TRACE message
    #
    def trace(self, log):
        self.write(log, level='TRACE')


    ##
    # Returns the last log
    #
    def getLast(self):
        return self.logs[-1]

    
    ##
    # Print ALL logs to the terminal
    #
    def dump(self):
        for log in self.logs:
            self.output(log)


    ##
    # Print a log
    #
    def output(self, log, facility=None):
        pass
        print("{} [{}]: {}".format(log.getTimestamp(), log.getLevel(), log.getLog()))

