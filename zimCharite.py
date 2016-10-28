#!/usr/bin/env python3

import wikiGenerator
import xlsScraper
import sys

# engine to use xls file to extract information and compile these information
# into strDict for automatic generation of wiki database


class Engine:
    def __init__(self, xlspath, wikiname, wikipath="/RAMDisk/"):
        self.scr = xlsScraper.xlsScraper(xlspath)
        self.scr.groupList()
        self.wiki = wikiGenerator.WikiGen(wikipath, wikiname)
        self.wiki.genBase()

        self.writeIndex()
        self.writeWeek()
        self.writeEvents()

    def writeIndex(self):
        indexDict = self.scr.indexDict()
        self.wiki.genRoot(indexDict)

    def writeWeek(self):
        weekList = self.scr.weekDict()
        for w, s in weekList:
            self.wiki.genWeek(w, s)

    def writeEvents(self):
        mList = self.scr.lzdb.getSemester().modules
        for mname,m in mList.items():
            wList = m.weeks
            for wname,w in wList.items():
                f, e = self.scr.eventDict(mname, wname)
                self.wiki.genEvents(f, e)


# interactive texts
helptext = '''Charite Lernziel XLS to ZimWiki Database Converter
Usage:
    --file [-f]     - choose xls file to use (best use absolute paths)
    --wiki [-w]     - choose wiki directory
    --name [-n]     - choose name of wiki database'''

if __name__ == '__main__':
    # default values
    filename = "/home/max/Downloads/export.xls"
    wikipath = "/RAMDisk/"
    wikiname = "test"
    # evaluating starting arguments
    for i, arg in enumerate(sys.argv):
        if arg == ("--help" or "-h"):
            print(helptext)
            sys.exit(0)
        elif arg == ("--file" or "-f"):
            filename = sys.argv[i+1]
        elif arg == ("--wiki" or "-w"):
            wikipath = sys.argv[i+1]
        elif arg == ("--name" or "-n"):
            wikiname = sys.argv[i+1]
    # testing implementation
    print("Lernziele to zim wiki database converter")
    if wikiname == "test":
        wikiname = input("Enter Wiki Name: ")
    eng = Engine(filename, wikiname, wikipath)
