import sys, os
import json, zipfile, struct, hashlib
import tempfile

def mergeBinProccess(files, fileSaveName):
    files.sort(key=lambda file:file[1])
    bin = b''
    aesFlag = b'\x00'
    startAddrLast = files[0][1]
    fileSizeLast  = 0
    if files[0][2]: # firmware
        name = files[0][0]
        size = os.path.getsize(name)
        f = open(name, "rb")
        firmware = f.read()
        f.close()

        bin += aesFlag                # add aes key flag
        bin += struct.pack('I', size) # add firmware length
        bin += firmware               # add firmware content
        sha256Hash = hashlib.sha256(bin).digest()
        bin += sha256Hash             # add parity

        startAddrLast = 0
        fileSizeLast = len(bin)
        files.remove(files[0])

    for file, addr, firmware, enable in files:
        if not enable:
            continue
        fillLen = addr - (startAddrLast + fileSizeLast)
        if fillLen > 0:               # fill 0xFF
            fill = bytearray([0xFF for i in range(fillLen)])
            bin += fill
        with open(file, "rb") as f:   # add bin file content
            bin += f.read()
        startAddrLast = addr
        fileSizeLast = os.path.getsize(file)
    with open(fileSaveName, "wb") as f:
        f.write(bin)
    print("Save merged bin file success")

def getBurnFilesInfoFromKfpkg(kfpkg):
    tempDir = tempfile.gettempdir()
    listFileName = "flash-list.json"
    try:
        zip = zipfile.ZipFile(kfpkg, mode="r")
        zip.extract(listFileName, tempDir)
        with open(tempDir+"/"+listFileName) as f:
            info = json.load(f)
        filesInfo = {}
        for fileInfo in info["files"]:
            filesInfo[fileInfo["bin"]] = [fileInfo["address"], fileInfo["sha256Prefix"]]
        print(filesInfo, zip.namelist())
        binFiles = zip.namelist()
        binFiles.remove(listFileName)
        zipTempFiles = []
        for file in binFiles:
            zip.extract(file, tempDir)
            zipTempFiles.append( (tempDir + "/" + file, filesInfo[file][0], filesInfo[file][1], True ) )
        zip.close()
    except Exception as e:
        return (None, str(e))
    return (zipTempFiles,"get file info ok")

def checkFilesAddrValid(fileType, files):
    if fileType == "bin":
        files.sort(key=lambda file:file[1])
        startAddr = -1
        fileSize  = 0
        fileShortLast = ""
        count = 0
        for file, addr, firmware, enable in files:
            if not enable:
                continue
            fileShort = ".../"+"/".join(file.split("/")[-2:])
            if startAddr + fileSize > addr:
                return (False, ("File address error")+": {} {} 0x{:X}, {} {} {} [0x{:X},0x{:X}]".format(fileShort, ("start from"), addr, ("but file"), fileShortLast, ("address range is"), startAddr, startAddr+fileSize) )
            fileSize = os.path.getsize(file)
            startAddr = addr
            fileShortLast = fileShort
            count += 1
        if count == 0:
            return (False, ("No file selected"))
    return (True, "FilesAddrValid")

def mergeBin(file):
    tablename = os.path.splitext(file)[0]
    fileType = "bin"

    files, msg = getBurnFilesInfoFromKfpkg(file)
    print(msg)
    if not files:
        print("error at get kfpkg file info")
        return

    ok, msg = checkFilesAddrValid(fileType, files)
    print(msg)
    if not ok:
        print("file addr error")
        return

    # pack and save
    mergeBinProccess(files, tablename +".bin")

mergeBin(sys.argv[1])
