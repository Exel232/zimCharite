import os
import time

def parseEventFileName(eventStr, replSpace=0):
    # return a hashed event file string from a raw event string
    
    titleList = eventStr.split(":", 1)
    if len(titleList) > 1:
        nameHash = "".join([ h[:1] for h in titleList[1].replace("/","").split() ])
        shortTitle = titleList[0] + " " + nameHash
    else:
        shortTitle = titleList[0]
    if replSpace:
        return shortTitle.replace(" ", "_")
    else:
        return shortTitle


class WikiGen:
    def __init__(self, wikipath='/RAMDisk/', name='test'):
        # path to generate wiki on if not available generate new
        self.wd = wikipath + name
        self.name = name
        self.makeDir(self.wd)

        self.end = ".txt"

    def genBase(self):
        # generate notebook.zim
        index = '''[Notebook]
version=0.4
name={0}
interwiki=
home=Home
icon=
document_root=
shared=True
endofline=unix
disable_trash=False
profile='''.format(self.name)

        with open(self.wd + os.sep + 'notebook.zim', 'w') as indFile:
            indFile.write(index)

    def genRoot(self, strDict):
        # generate root text pointing to Lernziel Modules and Weeks
        name = strDict["title"].replace(" ", "_")
        path = self.wd + os.sep + name
        self.root = path
        self.makeDir(self.root)
        # generate txt file with title and index pointing to subsequent
        # hierarchy
        text = ZimText().compileIndex(strDict)
        with open(self.wd + os.sep + name + self.end, "w") as rfile:
            rfile.write(text)

    def genWeek(self, week, strDict):
        # rewrite this function to accept lzclasses
        root = self.root + os.sep + week.replace("/", "").replace(" ", "_")
        print(root)
        self.makeDir(root)
        wtext = ZimText().compileWeek(strDict)
        with open(root + ".txt", "w") as wfile:
            wfile.write(wtext)

    def genEvents(self, folder, eventlist):
        week = self.root + os.sep + folder.replace("/", "").replace(" ", "_")
        # eventlist structure is a dict of vorlesungen seminare and
        # ukurs_prak, these in turn contain a list of strDicts for
        # eventd
        # first generate vorlesungen
        # vl = week + os.sep + "Vorlesungen"
        # self.makeDir(vl)
        for v in eventlist["Events"]:
            vtext = ZimText().compileEvent(v)
            titleList = v["title"].split(":", 1)
            nameHash = "".join([ h[:1] for h in titleList[1].replace("/","").split() ])
            shortTitle = (titleList[0] + " " + nameHash).replace(" ", "_")
            # shortTitle = v["title"].replace("/", "").replace(" ", "_")
            filepath = week + os.sep + shortTitle + self.end
            if os.path.exists(filepath):
                continue
            with open(filepath, "w") as vfile:
                vfile.write(vtext)

    def makeDir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)


class ZimText:
    # rewrite this class to use lzclasses

    def __init__(self):
        # generate usable text structure from dict with single strings to be
        # added
        # structure
        # [title] - single title
        # [subtitles] - multiple subtitles

        offset = time.strftime("%z", time.localtime()).split("00", 1)[0]
        ztime = time.strftime(
            "%Y-%m-%dT%H:%M:%S+{}:00".format(offset), time.localtime())
        self.header = '''Content-Type: text/x-zim-wiki
Wiki-Format: zim 0.4
Creation-Date: 2015-05-15T15:03:00+02:00

'''.format(ztime)
        # self.header = ""

    def compileIndex(self, strDict):
        # put all the parts together
        title = strDict["title"]
        text = self.header + self.Title(title)
        sub = strDict["subtitles"]
        text += self.subTitle(sub[0])
        for s in sub[1:]:
            if len(s) == 1:
                return " "
            text += self.indexPoint(s)
        return text

    def compileWeek(self, strDict):
        # put all the parts together
        title = strDict["title"]
        text = self.header + self.Title(title)
        eventTypes = {}
        for sub in strDict["subtitles"]:
            subList = sub.split(":", 1)
            evType = subList[0]
            hashedName = parseEventFileName(sub)
            eventTypes.setdefault(evType, []).append((hashedName,subList[1]))
            # add the hashed filename and the cleartext to be displayed
        for title, event in eventTypes.items():
            text += self.subTitle(title)
            for s in event:
                text += self.indexPoint(s)
        return text

    def compileEvent(self, strDict):
        # expected difference with only one subtitle containing lernziele
        title = strDict["title"]
        text = self.header + self.Title(title)
        text += self.subTitle("Lernziele")
        
        reali = 1
        spliti = []
        subway = {}
        for i, sub in enumerate(strDict["subtitles"]):
            text += self.Lernziel(sub, reali)
            reali += 1
        text += "\n\n"
        for i in range(1, reali):
            if i in spliti:
                text += self.subTitle(subway[i])
            text += self.sectionTitle("Lernziel {}".format(i))

        text += "\n\n"
        text += self.subTitle("weitere Notizen")

        return text

    def Title(self, header):
        return "====== {0} ======\n\n".format(header)

    def subTitle(self, subtitle):
        return "===== {0} =====\n".format(subtitle)

    def sectionTitle(self, subtitle, pwa=0):
        if pwa:
            return "==== {} ====\n".format(subtitle)
        return "==== {} ====\n\n\n".format(subtitle)

    def indexPoint(self, pathname):
        # 0 is our real link filename, but 1 is the displayed name
        return "* [[+{0}|{1}]]\n".format(pathname[0], pathname[1])

    def Lernziel(self, lz, index):
        return "{0}. {1}\n".format(index, lz)


if __name__ == '__main__':
    wiki = WikiGen()
