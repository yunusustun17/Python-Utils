import os
import time

import paramiko


class Sftp:
    transport = None
    sftp = None

    def __init__(self, host, username, password=None, ssh_port=22, private_key=None, passphrase=None):
        # For paramiko log
        # paramiko.util.log_to_file("paramiko.log")

        self.transport = paramiko.Transport((host, ssh_port))
        if password:
            self.transport.connect(None, username=username, password=password)
        elif private_key:
            k = paramiko.RSAKey.from_private_key_file(private_key, passphrase)
            self.transport.connect(None, username=username, pkey=k)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def removeRemoteFiles(self, remoteFolderPath):
        # Remove remote files and folder
        channel = self.transport.open_channel(kind="session")
        channel.exec_command(f"rm -rf {remoteFolderPath}/*")
        while not channel.exit_status_ready():
            print("command processing..")
            time.sleep(1)

    def copyFile(self, localPath, remotePath):
        # Upload
        self.sftp.put(localPath, remotePath)

    def copyFolder(self, localPath, remotePath):
        # Upload Folder
        folders = []
        files = []
        newFiles = []

        for dirPath, dirNames, fileNames in os.walk(localPath):
            for fileName in fileNames:
                fileFullPath = os.path.join(dirPath, fileName)
                newFileFullPath = remotePath + fileFullPath.replace(localPath, "")
                folders.append(os.path.split(newFileFullPath)[0])
                files.append(fileFullPath)
                newFiles.append(newFileFullPath)

        folders = sorted(list(set(folders)))

        for folder in folders:
            channel = self.transport.open_channel(kind="session")
            channel.exec_command(f"mkdir -p {folder}")
            while not channel.exit_status_ready():
                print("command processing..")
                time.sleep(1)

        for key, value in enumerate(files):
            self.sftp.put(files[key], newFiles[key])

    def runCommand(self, command):
        # Run command
        channel = self.transport.open_channel(kind="session")
        channel.exec_command(command)
        while not channel.exit_status_ready():
            print("command processing..")
            time.sleep(2)

    def __del__(self):
        # Close
        if self.sftp: self.sftp.close()
        if self.transport: self.transport.close()
