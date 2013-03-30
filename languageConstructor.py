import json
import re
import player
import time
from StringIO import StringIO

class Language:
    def __init__(self, fp, debug=False):
        self.fp = fp
        self.debug = debug

    def constructMethodStandard(self, chunkSize):
        chunks = []
        n = 0
        currentChunk = []
        for line in self.fp:
            if self.debug:
                print line
            if n < chunkSize:
                try: 
                    currentCall = self.isCall(line)
                    if currentCall:
                        currentChunk.append(currentCall)
                    n+=1
                except ValueError:
                    print "Something Bizarre just happened!"
            elif n == chunkSize:
                chunks.append(currentChunk)
                n = 0
                currentChunk = []
                try: 
                    currentCall = self.isCall(line)
                    if currentCall:
                        currentChunk.append(currentCall)
                        n+=1
                except ValueError:
                    print "Something Bizarre just happened!"
        chunks.append(currentChunk)
        return chunks 	

    def isCall(self, line):
        if re.search(r"\[method\=[A-Z]+\]", line):
            data = Call()
            data.castString(line)
            return data
        return None

class Call:
    def __init__(self):
        self.data = {}

    def castString(self, string):
        params = string.split("][")
        for param in params:
            if "method=" in param:
                self.data["method"] = re.sub(r'^(.*?)(method\=)([A-Z]+)(.*?)$', r'\3', param)
            elif "status=" in param:
                self.data["status"] = int(re.sub(r'^(.*?)(status\=)([0-9]+)(.*?)$', r'\3', param))
            elif "resp_msecs=" in param:
                self.data["responseTime"] = int(re.sub(r'^(.*?)(resp_msecs\=)([0-9]+)(.*?)$', r'\3', param))
            elif "resp_bytes=" in param:
                self.data["responseBytes"] = int(re.sub(r'^(.*?)(resp_bytes\=)([0-9]+)(.*?)$', r'\3', param))
            elif "req_bytes=" in param:
                self.data["requestBytes"] = int(re.sub(r'^(.*?)(req_bytes\=)([0-9]+)(.*?)$',r'\3',param))

class RequestStandard:
    def __init__(self):
        self.methods = {}
        self.status = {}
        self.responseBytes = {}
        self.responseTime = {}
        self.requestBytes = {}

    def construct(self, calls):
        for call in calls:
            self.incrementHistogram(self.methods, call.data["method"])
            self.incrementHistogram(self.status, call.data["status"])
            self.incrementHistogram(self.responseBytes, call.data["responseBytes"])
            self.incrementHistogram(self.responseTime, call.data["responseTime"])
            self.incrementHistogram(self.requestBytes, call.data["requestBytes"])

    def incrementHistogram(self, dictionary, value):
        if value in dictionary:
            dictionary[value] += 1
        else:
            dictionary[value] = 1

def histogramAverage(histogram):
    total = 0.0
    totalLength = 0
    for key in histogram:
        total += (key*histogram[key])
        totalLength += histogram[key]
    return total/totalLength if totalLength != 0 else 0

def distanceBetweenStandards(standard1, standard2):
    requestBytes = (histogramAverage(standard1.requestBytes) - histogramAverage(standard2.requestBytes))
    responseTime = (histogramAverage(standard1.responseTime) - histogramAverage(standard2.responseTime))
    responseBytes = (histogramAverage(standard1.responseBytes) - histogramAverage(standard2.responseBytes))
    status = dictionaryDistance(standard1.status, standard2.status)
    method = dictionaryDistance(standard1.methods, standard2.methods)
    return (requestBytes, responseTime, responseBytes, status, method)

def dictionaryDistance(firstVector, secondVector):
    distance = 0
    firstScale = float(sum(firstVector.values()))
    secondScale = float(sum(secondVector.values()))
    for key in firstVector:
        if key in secondVector:
            distance += ((firstVector[key]/firstScale)-(secondVector[key]/secondScale))
        else:
            distance += firstVector[key]
    return distance


print "Initializing"
test = Language(open("../filepicker.io.log", "rb"))
standard = test.constructMethodStandard(200000)
averaging = RequestStandard()
averaging.construct(standard[0])

print "Listening to logs"
fp = open("/tmp/logs.log", "r")
lines = []
N = 10
fp.read()
while True:
    where = fp.tell()
    line = fp.readline()
    if not line:
        time.sleep(.5)
        fp.seek(where)
    else:
        lines.append(line)

    if len(lines) == N:
        check = Language(StringIO("".join(lines)), debug=False)
        overTime = check.constructMethodStandard(N)
        allDifferences = []
        for value in overTime:
            currentStandard = RequestStandard()
            currentStandard.construct(value)
            difference = distanceBetweenStandards(averaging, currentStandard)
            player.play_data(difference)
            time.sleep(.5)
        lines = []
