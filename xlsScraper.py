import xlrd
from collections import defaultdict
import LzClasses


class xlsScraper:
    def __init__(self, path):
        book = xlrd.open_workbook(path)
        self.sheet = book.sheets()[0]
        hValues = self.validate(self.sheet.row_values(0)) # these are our title values
    
    def validate(self, header):
        print(header)
        if len(header) == 7:
            return header
        else:
            return 0

    def getTypes(self, plist):
        # print(plist)
        combinations = []
        for p in plist:
            if p not in combinations:
                combinations.append(p)
        return combinations


    def groupList(self):
        # dictionary containing module week
        
        self.lzdb = LzClasses.LzDatabase("Test")
        prevIndex = ""
        for r in range(1, self.sheet.nrows):
            row = self.sheet.row_values(r)[:7]
            # 0 - modul 1 - period 2 - week 3 - event 4 - dim 5 - cog 6 - lz
            self.lzdb.addLz(*row)

    def indexDict(self, name="Ausarbeitungen"):
        # we now compile the information from the modules into the main index.
        # this file shows us an overview of the different module weeks and
        # links to the subsequent index files
        strDict = dict()
        strDict["title"] = name
        stitle = ["Index"]
        for mname,m in self.lzdb.getSemester().modules.items():
            modname = mname
            weeks = m.getWeeknames()
            for w in weeks:
                stitle.append(["{0} {1}".format(modname, w),
                               "{}".format(w)])
            # we iterate over the modules to add subtitles -
            # subtitles contain list with first item title name and second item
            # list of index points to point to further references, these are
            # here the module weeks
        strDict["subtitles"] = stitle
        return strDict

    def weekDict(self):
        # usage of wikiGen event creator. we need to forward the folder and
        # week we are going to use and the strDict containing specific event
        # type keys
        # first create a list of week, strDict pairs
        all_list = []
        modules = self.lzdb.getSemester().modules
        for mname,m in modules.items():
            weeks = m.weeks
            for wname,w in weeks.items():
                event_keys = w.getEvents()
                
                week_dict = {}
                week_dict["title"] = "{0} {1}".format(m.name, w.name)
                week_dict["subtitles"] = event_keys
                # fix problems later
                ev_item = ["{0} {1}".format(m.name, w.name), week_dict]
                all_list.append(ev_item)

        return all_list

    def eventDict(self, module, week):
        events = self.lzdb.getSemester().modules[module].weeks[week].events
        event_list = {"Events": []}
        for e,elz in events.items():
            eDict = {}
            lz_list = []
            for lz in elz:
                # now lz is an object
                lz_list.append(lz.name + " " + lz.dimens)

            eDict["title"] = "{0}".\
                    format(e)
            eDict["subtitles"] = lz_list
            event_list["Events"].append(eDict)
        folder = "{0} {1}".format(module, week)
        return folder, event_list

    # sqalchemy compatibility functions
    def getHeaders(self):
        return self.sheet.row_values(0)

    def getRows(self):
 #       print(self.sheet.nrows)
        for i in range(1, self.sheet.nrows):
            # print(i)
            # prin(self.sheet.row_values(i))
            yield self.sheet.row_values(i)

if __name__ == '__main__':
    scr = xlsScraper("/home/max/Downloads/export.xls")
    scr.groupList()
    print(scr.indexDict())
    scr.eventDict(21, 1)
