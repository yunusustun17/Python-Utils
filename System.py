import os
import shutil
from subprocess import Popen, PIPE


class System:
    @staticmethod
    def getOsName():
        return os.name

    @staticmethod
    def getCwd():
        return os.getcwd()

    @staticmethod
    def isFile(path):
        return os.path.isfile(path)

    @staticmethod
    def isFolder(path):
        return os.path.isdir(path)

    @staticmethod
    def isPathExists(path):
        return os.path.exists(path)

    @staticmethod
    def mkdir(path):
        try:
            os.mkdir(path)
        except FileExistsError:
            print("Cannot create an existing file")

    @staticmethod
    def __copyFile(sourcePath, destinationPath):
        try:
            shutil.copy(sourcePath, destinationPath)
        except shutil.SameFileError:
            print("Source and destination represents the same file.")
        except IsADirectoryError:
            print("Destination is a directory.")
        except PermissionError:
            print("Permission denied.")
        except:
            print("Error occurred while copying file.")

    def __copyFolder(self, sourcePath, destinationPath):
        if self.isPathExists(destinationPath):
            shutil.rmtree(destinationPath)
        shutil.copytree(sourcePath, destinationPath)

    def copy(self, sourcePath, destinationPath):
        if self.isFile(sourcePath):
            if not os.path.split(destinationPath)[1]:
                destinationPath = os.path.join(destinationPath, os.path.split(sourcePath)[1])
            self.__copyFile(sourcePath, destinationPath)
        elif self.isFolder(sourcePath):
            self.__copyFolder(sourcePath, destinationPath)
        else:
            raise Exception("This operation not supporting")

    @staticmethod
    def runCommand(command, returnList=None):
        subprocess = Popen(command, shell=True, stdout=PIPE)
        subprocess_return = subprocess.stdout.read().decode("utf-8")
        if returnList:
            return list(filter(None, subprocess_return.split("\n")))
        else:
            return subprocess_return
