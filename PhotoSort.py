from os import walk
from os import makedirs
from os.path import exists

from shutil import copyfile

from time import time
from datetime import datetime

from exifpy import exifread


def printTime(label, time):
    ms = time * 1000
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    print(label + '%d:%02d:%02d:%04d' % (h, m, s, ms))


def printTimeStats(timeDiff, numberOfFiles):
    if (numberOfFiles > 0):
        timePerFile = timeDiff / numberOfFiles

        printTime('total time   : ', timeDiff)
        print('total files  : %d' % (numberOfFiles))
        printTime('time per file: ', timePerFile)


def main():
    #importDir = '/some/input/dir'
    #outputDir = '/some/export/dir'

    timeStart = time()
    numberOfFiles = 0

    for root, dirs, files in walk(importDir):

        numberOfFiles += len(files)

        for file in files:
            oldFile = root + '/' + file

            # Open image file for reading (binary mode)
            f = open(oldFile, 'rb')

            # Return Exif tags
            tags = exifread.process_file(f, stop_tag='EXIF DateTimeOriginal', details=False)
            for tag in tags:
                if 'DateTime' in tag:
                    dt = datetime.strptime(str(tags[tag]), '%Y:%m:%d %H:%M:%S')

                    iso = dt.isocalendar()
                    dir = outputDir + '/' + dt.strftime('%Y/%m/%d/')
                    newFile = dir + '/' + file

                    if not exists(dir):
                        makedirs(dir)

                    copyfile(oldFile, newFile)

    timeEnd = time() - timeStart
    printTimeStats(timeEnd, numberOfFiles)


main()