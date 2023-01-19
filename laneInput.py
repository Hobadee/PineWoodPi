import lane

##
# Class to init/store lane info
#
# Right now we are definitely violating the principle of single-responsibility
#
class lane(threading.Thread):

    laneNo = None
    laneInput = None
    log = None

    timeStart = 0
    timeStop = 0
    timeTotal = 0
    dnf = False

    run = False

    laneOutput = None

    ##
    # Constructor
    #
    def __init__(self, laneNo, laneInput, laneOutput, log, *args, **kwargs):
        super(lane,self).__init__(*args, **kwargs)
        self.laneNo = laneNo
        self.laneInput = laneInput
        self.DID = DigitalInputDevice(self.laneInput, True)
        self.log = log
        self.laneOutput = laneOutput
    
    ##
    # Return the status of the lane sensor
    # False - beam broken
    # True - beam active
    #
    def broken(self):
        if self.DID.value == 1:
            return False
        else:
            return True
    
    ##
    #
    #
    def run(self):
        # Flip "run" flag True
        self.run = True
        self.log.debug("Running lane {}".format(self.laneNo))
        while(self.getSensor() and self.run):
            # Poll the sensor super-fast
            pass
        # As soon as the sensor trips, log the time and return
        if(self.run == True):
            self.timeStop = time.time()
            self.log.debug("Lane {} finished at {}".format(self.laneNo, self.timeStop))
    

    ##
    # Mechanism to stop the thread
    #
    def stop(self):
        self.run = False
    

    ##
    # Return the lane number
    #
    def getLaneNo(self):
        return self.laneNo
    

    ##
    # Returns if a car is sensed by the sensor or not
    #
    # True if a car is there, False otherwise
    #
    def getSensor(self):
        if(self.DID.value == 0):
            return True
        return False


    ##
    #
    #
    def setTimeStart(self, time):
        self.timeStart = time
    

    ##
    #
    #
    def totalTime(self):
        if (self.dnf):
            return 999
        if self.timeStart == 0 or self.timeStop == 0:
            # Start or Stop haven't been set yet - puke
            return 0
        return self.timeStop - self.timeStart


    ##
    # 
    #
    def setDNF(self, dnf):
        self.dnf = dnf


    ##
    #
    #
    def getDNF(self):
        return self.dnf