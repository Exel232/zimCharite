#!/usr/bin/env python3

# we should implement a class framework for simpler lernziel management
class LzDatabase:
    def __init__(self, identifier):
        self.name = identifier
        self.semesters = {}

    def addSemester(self, semester):
        if semester not in self.semesters:
            self.semesters[semester] = Semester(semester)
            self.s = semester

    def getSemester(self):
        return self.semesters[self.s]

    def addLz(self, modul, semester, week, event, dim, cog, lz):
        self.addSemester(semester)
        self.semesters[semester].addLz(modul, semester, week, event, dim, cog, lz)


class Semester:
    def __init__(self, semester):
        self.name = semester
        self.modules = {}

    def addModule(self, name, semester):
        if name not in self.modules:
            self.modules[name] = Modul(name, semester)

    def getModules(self):
        return self.modules.keys()

    def getModule(self, name):
        return self.modules[name]

    def addLz(self, modul, semester, week, event, dim, cog, lz):
        if semester != self.name:
            return 1
        self.addModule(modul, semester)
        self.modules[modul].addLz(week, event, dim, cog, lz)



class Modul:
    def __init__(self, name, semester):
        self.name = name
        self.semester = semester
        self.weeks = {}

    def addWeek(self, weekname):
        if weekname not in self.weeks:
            self.weeks[weekname] = Week(weekname)

    def getWeeknames(self):
        return self.weeks.keys()

    def getWeek(self, name):
        return self.weeks[name]

    def addLz(self, week, event, dim, cog, lz):
        self.addWeek(week)
        self.weeks[week].addLz(lz, dim, cog, event)


class Week:
    def __init__(self, name):
        self.name = name
        self.events = {}

    def addEvent(self, name):
        if name not in self.events:
            self.events[name] = []

    def linkLzEvent(self, name, lzObj):
        self.events[name].append(lzObj)

    def addLz(self, name, dim, cog, event):
        self.addEvent(event)
        self.linkLzEvent(event, Lernziel(name, dim, cog, event))

    def getEvents(self):
        return self.events.keys()

    def getLzList(self):
        outList = []
        for l in self.events.items():
            outList += l
        return outList
        


class Lernziel:
    def __init__(self, desc, dimension, cognition, event):
        self.name = desc
        self.dimens = dimension
        self.cogn = cognition
        self.event = event
