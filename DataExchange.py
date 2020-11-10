#region About
"""
pyVersion = IronPython 2.7xx and Python 3.7xx

These classes are compatible with both Rhino and Revit
and are meant to assist in exchanging data between
these platforms, or between any program and the OS.

Each data tool is an object with accessible
methods therein which can be linked together. There is
no main function and nothing will run without being
explicitly instantiated

Because this is meant to be used in both Python3 and
ironPython precautions must be taken in the code!
"""
#endregion

# UNIVERSAL MODULES
import boto3 # aws S3 storage api
import collections
import json
import platform
import sys
import traceback
import ujson

from collections import Sequence
from itertools import chain, count

import csv
import os

sys.path.append(r"C:/python38/lib/site-packages")


# ====================== #
# FILE WRITING UTILITIES #
# ====================== #
def CreateFullFilePath(extension="json", dirPath=None, fileName=None):
    # file path operations or something
    if not fileName:
        fileName = "rando{0}".format(extension.upper())
    if dirPath == None:
        dirPath = self.pathObj.CurrentUserDesktopPath()
    elif dirPath == 'current':
        dirPath = self.pathObj.CurrentFileDirectory()
    elif dirPath == 'Lib':
        self.dirPath = None
    
    # concatenate full file path differently depending on the os
    if platform.system() == "Windows":
        completeFilePath = r"{0}\{1}.{2}".format(dirPath, fileName, extension)
    # mac os directories
    if platform.system() == "Darwin":
        completeFilePath = r"{0}/{1}.{2}".format(dirPath, fileName, extension)
    
    return(completeFilePath)

def CreateDataRowStr(dataRowStrList):
    newLine = "\n"
    dataRowsStr = newLine.join(dataRowStrList)
    return(dataRowsStr)

# data prep for JSON AND CSV modules
class DataPrep:
    def __init__(self):
        pass

    def GroupNthItemList(self, data, groupSize):
        dataOut = []
        for building in data:
            count = 0
            for facadeIndex in range(len(building)):
                anotherNest = []
                facadesTempList = []

                # group facades in sub lists by looping through groupSize
                for groupIndex in range(groupSize):
                    masterIndex = (facadeIndex + groupIndex + count)
                    if masterIndex <= (len(building) - 1):
                        facadesTempList.append(building[masterIndex])
                if len(facadesTempList) > 0:
                    count += (groupSize - 1)

                    # still dont understand why this i needed...group the groups?
                    anotherNest.append(facadesTempList)
                    dataOut.append(anotherNest)
        return(dataOut)

class ListTools:
    def __init__(self):
        pass

        # def ListDepth(self, dataList):
        #dataList = iter(dataList)
        # try:
        # for level in count():
        #dataList = chain([next(dataList)], dataList)
        #dataList = chain.from_iterable(s for s in dataList if isinstance(s, Sequence))

        # do not recognize the formatting after except
        # except StopIteration:
        # return(level)
        # yield from is not ironpython safe???
        # def MissingNumbersInSequence(numList, start, end):
        # very advanced formatting, is this recursion?
        # if end - start <= 1:
        # if numList[end] - numList[start] > 1:
        # yield from range(numList[start] + 1, numList[end])
        # return

        #index = start + (end - start) // 2

        # is the lower half consecutive?
        #consecutive_low =  numList[index] == numList[start] + (index - start)
        # if not consecutive_low:
        # yield from MissingNumbersInSequence(numList, start, index)

        # is the upper part consecutive?
        #consecutive_high =  numList[index] == numList[end] - (end - index)
        # if not consecutive_high:
        # yield from MissingNumbersInSequence(numList, index, end)

        return(False)

class RangeDict(dict):
    def __getitem__(self, item):
        if type(item) != range:  # or xrange in Python 2
            for key in self:
                if item in key:
                    return(self[key])
        else:
            return(super().__getitem__(item))


# ============================ #
# DATA READING/WRITING CLASSES #
# ============================ #
def frange(start, stop=None, step=None):
    # use float number in range() function

    # if stop and step argument is null set start=0.0 and step=1.0
    if stop == None:
        stop = start + 0.0
        start = 0.0

    if step == None:
        step = 1.0

    while True:
        if step > 0 and start >= stop:
            break
        elif step < 0 and start <= stop:
            break
        yield("{0}".format(start))
        start = start + step

def frange2(x, y, jump):
    while x < y:
        yield x
        x += jump

class FilePathTools:
    def __init__(self):
        self.targetDirectory = None

    def CurrentFilePath(self):
        return(os.path.abspath(__file__))

    def CurrentFileDirectory(self):
        return(os.path.dirname(self.CurrentFilePath()))

    def CurrentUserDesktopPath(self):
        return(os.path.expanduser("~\Desktop"))

    def CurrentUser(self):
        return(os.path.expanduser("~"))

    def ShiftFilePath(self, path, branchesBack=1, append=None):
        pathReverse = path[::-1]
        newPathReverse = pathReverse.split('\\', branchesBack)[-1]
        newPath = newPathReverse[::-1]

        # always write append string as r"" - set as variable
        if type(append) is str:
            return(r"{0}\{1}".format(newPath, append))

class JSONTools:
    """
    This class works for both Python2,3 and IronPython

    fileName and dirPath are separated to simply the assignment
    of creating files in specific, but common locations by allowing
    keywords that the code recognizes to create a long path string.
    This to prevent the manual copying and pasting process.
    """

    def __init__(self):
        # instantiate FilePathTools Class
        self.pathObj = FilePathTools()

    def WriteJSON(self, data, dirPath=None, fileName=None):
        # concatenate full file path
        completeFilePath = CreateFullFilePath(extension="json", dirPath=dirPath, fileName=fileName)
        
        # write json
        with open(completeFilePath, 'w') as writePath:
            JSONdump = json.dump(data, writePath)

        return(JSONdump)

    def WriteUJSON(self, data, dirPath=None, fileName=None):
        # concatenate full file path
        completeFilePath = CreateFullFilePath(extension="json", dirPath=dirPath, fileName=fileName)
        
        print(completeFilePath)

        # write ujson
        with open(completeFilePath, 'w') as writePath:
            UJSONdump = ujson.dump(data, writePath)
        
        return(UJSONdump)

    def Write_MSGPACK(self, data, filePath=None, fileName=None):
        if fileName == None:
            fileName = "randoMSGPACK"

        if filePath == None:
            filePath = self.pathObj.CurrentUserDesktopPath()
        elif filePath == 'current':
            filePath = self.pathObj.CurrentFileDirectory()
        elif filePath == 'Lib':
            self.filePath = None

        completeFilePath = r"{0}\{1}.msgpack".format(filePath, fileName)

        # Write msgpack file
        with open(completeFilePath, 'w') as writePath:
            msgpack.pack(data, writePath)
        
    def ReadJSON(self, filePath=None):
        if filePath == None:
            raise Exception("Complete path must be used!")

        with open(filePath, 'r') as read:
            dataOut = json.load(read)
        return(dataOut)

    def ReadUJSON(self, filePath=None):
        if filePath == None:
            raise Exception("Complete path must be provided.")

        with open(filePath, 'r') as read:
            dataOut = ujson.load(read)
        return(dataOut)

    def ReadMSGPACK(self, filePath=None):
        if filePath == None:
            raise Exception("Complete path must be used!")

        with open(filePath, 'r') as read:
            dataOut = msgpack.unpack(read)
        return(dataOut)

class CSVTools:
    """
    data assumes data is single column, if more than one column then you can make iterable
    """

    def __init__(self, fileName=None, filePath=None):
        # instantiate FilePathTools Class
        self.pathObj = FilePathTools()

        self.fileName = fileName
        self.filePath = filePath

        # default file write locations and keyword options
        if self.fileName == None:
            self.fileName = "randoCSV"

        if self.filePath == None:
            self.filePath = FilePathTools().CurrentUserDesktopPath()
        elif self.filePath == 'current':
            self.filePath == FilePathTools().CurrentFileDirectory()
        elif self.filePath == 'Lib':
            self.filePath = None

    def ReadCSV(self, row=True, cellStart=None, cellEnd=None):
        # cellStart = (row#, column#)

        # assume fileName contiains full path, unless files are saved in same location
        with open(self.fileName, mode='r') as csvFile:
            # read rows
            if row == True:
                csvReader = csv.reader(csvFile, delimiter=',')
                csvData = [i for i in csvReader]

            # read columns
            elif row == False:
                csvReader = csv.reader(csvFile, delimiter=',')
                csvData = [i for i in zip(*csvReader)]

        return(csvData)

    def WriteCSV(self, data, row=True, cellStart=None, cellEnd=None):
        # cellStart = (row#, column#)

        completeFilePath = "{0}/{1}.csv".format(self.filePath, self.fileName)

        with open(completeFilePath, mode='w') as csvFile:
            writerObj = csv.writer(
                csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # write row
            if row == True:
                for i in data:
                    writerObj.writerow(i)

            # write column
            elif row == False:
                data2 = zip(data)
                for i in data2:
                    writerObj.writerow([i])
        return(None)

    def WriteCSV2(self, data, cellStart=None, cellEnd=None):
        # cellStart = (row#, column#)
        print('hello world')
        inPath = "{0}/{1}.csv".format(self.filePath, 'in')
        outPath = "{0}/{1}.csv".format(self.filePath, 'out')

        in_file = open(inPath, mode='r')
        reader = csv.reader(in_file)

        myList = list(reader)
        in_file.close()

        print(myList)

        #myList[2][0] = 'cat'
        #myNewList = open(outPath, mode='w', newline='')
        #writer = csv.writer(myNewList)
        # writer.writerows(myList)
        # myNewList.close()

class SQLTools:
    """
    This class only works in Python 2 & 3. Not implimented for ironPython.
    Please call subprocess to use within Rhino or Revit. 
    """

    def __init__(self):
        import sqlite3
        pass

    def WriteDB(self):
        pass

    def UpdateDB(self):
        pass

    def ReadDB(self):
        pass

class PLYTools:
    def __init__(self):
        # instantiate FilePathTools Class
        self.pathObj = FilePathTools()

    def ReadPLY(self, filePath):
        if filePath == None:
            raise Exception("Complete path must be provided.")

        plyDataComplete = open(filePath,'rt').read().split('\n')

        return(plyDataComplete)

    def WritePLY(self, dataRowStrList, dirPath=None, fileName=None):
        # concatenate full file path
        completeFilePath = CreateFullFilePath(extension="ply", dirPath=dirPath, fileName=fileName)

        # convert data list of strings into one continuous string input with "\n" added at each return
        dataRowsStr = CreateDataRowStr(dataRowStrList)

        # write to JSON
        plyNewFile = open(completeFilePath,'wt')
        plyNewFile.write(dataRowsStr)

        return(plyNewFile)

class S3Tools:
    def __init__(self):
        # instantiate FilePathTools Class
        self.pathObj = FilePathTools()

    def GetBuckets(self):
        from botocore.config import Config

        my_config = Config(
            region_name = 'us-west-1',
            signature_version = 'v4',
            retries = {
                'max_attempts': 10,
                'mode': 'standard'
            }
        )

        client = boto3.client('kinesis', config=my_config)

    def DownloadModel(self):
        pass

    def UploadModel(self):
        pass


# =========== #
# GRASSHOPPER #
# =========== #
class GRASSHOPPERTools:
    def __init__(self):
        pass

    def DEPRECATED(self, raggedList):
        # Grasshopper imports
        import clr
        clr.AddReference("Grasshopper")
        from Grasshopper import DataTree
        from Grasshopper.Kernel.Data import GH_Path

        from System import Array
        from System import Object

        rl = raggedList
        result = DataTree[object]()
        for i in range(len(rl)):
            temp = []
            for j in range(len(rl[i])):
                temp.append(rl[i][j])
            # print i, " - ",temp
            path = GH_Path(i)
            result.AddRange(temp, path)
        return(result)

    def NestedListToDataTree(self, input, none_and_holes=True, source=[0]):
        # Grasshopper imports
        import clr
        clr.AddReference("Grasshopper")
        from Grasshopper import DataTree
        from Grasshopper.Kernel.Data import GH_Path

        from System import Array
        from System import Object

        def proc(input, tree, track):
            path = GH_Path(Array[int](track))
            if len(input) == 0 and none_and_holes:
                tree.EnsurePath(path)
                return
            for i, item in enumerate(input):
                if hasattr(item, '__iter__'):  # if list or tuple
                    track.append(i)
                    proc(item, tree, track)
                    track.pop()
                else:
                    if none_and_holes:
                        tree.Insert(item, path, i)
                    elif item is not None:
                        tree.Add(item, path)
        if input is not None:
            t = DataTree[object]()
            proc(input, t, source[:])
            return t

    def DataTreeToNestedList(self, aTree):
        # Grasshopper imports
        import clr
        clr.AddReference("Grasshopper")
        from Grasshopper import DataTree
        from Grasshopper.Kernel.Data import GH_Path

        from System import Array
        from System import Object

        theList = []
        for i in range(aTree.BranchCount):
            thisListPart = []
            thisBranch = aTree.Branch(i)
            for j in range(len(thisBranch)):
                thisListPart.append(thisBranch[j])
            theList.append(thisListPart)
        return(theList)


# ============== #
# TEST FUNCTIONS #
# ============== #
def TestS3():
    # Let's use Amazon S3
    s3 = boto3.resource('s3')
    print(s3)
    
    # Print out bucket names
    for bucket in s3.buckets.all():
        print(bucket.name)

if __name__ == "__main__":
    TestS3()