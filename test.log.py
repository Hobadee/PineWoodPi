#!/usr/bin/python3

from log import *

log = log()
#log.setDisplayLevel(1)
log.write("No level set")
log.write("Straight ENUM level set", logLevels.ERROR)
log.write("Integer level set", 2)
log.write("String level set", "ERROR")
log.write("Forcing output", forceOP=True)
log.write("Level 1", 1)
log.write("Level 2", 2)
log.write("Level 3", 3)
log.write("Level 4", 4)
log.write("Level 5", 5)
log.write("Level 6", 6)
log.write("Invalid Level set", 7)
#print("Dumping logs:")
#log.dump()
