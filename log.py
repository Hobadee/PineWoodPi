#!/usr/bin/python3

import time
from enum import Enum, unique

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
    defaultLevel = 'INFO'
    logs = []
    
    def __init__(self):
        # Take a timestamp of when logging was started
        self.timestampStart = time.time()
    

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
    def write(self, log, level=None, output=False):
        if(level == None):
            level = self.defaultLevel

        self.logs.append(logEntry(log, level))

        if(output):
            opLog = self.last()
            self.print(opLog)
    

    ##
    #
    #
    def last(self):
        return self.logs[-1]

    
    def dump(self):
        for log in self.logs:
            self.print(log)


    ##
    # Print all logs
    #
    def print(self, log):
        print("{} [{}]: {}".format(log.getTimestamp(), log.getLevel(), log.getLog()))


log = log()
log.write("asdf")
log.write("Straight ENUM", logLevels.ERROR)
log.write("Integer", 6)
log.write("String", "FATAL")
log.write("Test realtimne OP", output=True)
print("Dumping logs:")
log.dump()
