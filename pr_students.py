#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:47:45 2019

@author: mputzlocher
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as tkm
from tkinter import filedialog as tkfd
#import locale
import pr_points as poi

import pr_csv

# -----------------------------------------------------------------------
# Fix for tk 8.6.9


def fixed_map(style, option):
    # Fix for setting text colour for Tkinter 8.6.9
    # From: https://core.tcl.tk/tk/info/509cafafae
    #
    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out.

    # style.map() returns an empty list for missing options, so this
    # should be future-safe.
    return [elm for elm in style.map('Treeview', query_opt=option) if
            elm[:2] != ('!disabled', '!selected')]

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
# Fix for wrong Sorting - Sorting like DIN 5007
    
def din5007(instring):
	""" This function implements sort keys for the german language according to 
	DIN 5007."""
	
	# key1: compare words lowercase and replace umlauts according to DIN 5007
	key1=instring.lower()
	key1=key1.replace(u"ä", u"a")
	key1=key1.replace(u"ö", u"o")
	key1=key1.replace(u"ü", u"u")
	key1=key1.replace(u"ß", u"ss")
	
	# key2: sort the lowercase word before the uppercase word and sort
	# the word with umlaut after the word without umlaut
	key2=instring.swapcase()
	
	# in case two words are the same according to key1, sort the words
	# according to key2. 
	return (key1, key2)

# -----------------------------------------------------------------------

myfont = "Helvetica 14"


# Model

class Student():
    def __init__(self, name, family_name, group):
        self.name = name
        self.family_name = family_name
        self.group = group
        self.hash = self.calcHash()
        
    def calcHash(self):
        myhash = hex(hash(self.name + self.family_name))
        return myhash
    
    def getHash(self):
        return self.hash

    def getName(self):
        return self.name

    def getFamilyName(self):
        return self.family_name

    def getGroup(self):
        return self.group

    def getList(self):
        s = self
        return [s.name, s.family_name, s.group]

    def getDict(self):
        s = self
        n = "Vorname"
        f = "Nachname"
        g = "Gruppe"
        return {n: s.name, f: s.family_name, g: s.group}

    def setFromList(self, student_list):
        s = self
        s.group = student_list.pop()
        s.family_name = student_list.pop()
        s.name = student_list.pop()
        s.hash = s.calcHash()

    def setFromDict(self, student_dict):
        s = self
        s.name = student_dict["Vorname"]
        s.family_name = student_dict["Nachname"]
        s.group = student_dict["Gruppe"]
        s.hash = s.calcHash()

class StudentList():
    def __init__(self):
        self.l = list()
        
    def checkNoDoubleEntry(self, student):
        hashlist = [s.getHash() for s in self.l]
        if student.getHash() in hashlist:
            print("student already in table.")
            return False
        else:
            print("new entry for student")
            return True
    
    def checkGroupChange(self, student, s_id):
        hashlist = [s.getHash() for s in self.l]
        sHash = student.getHash()
        if sHash in hashlist:
            existingStudent = self.getStudentByHash(sHash)
            groupcond = student.getGroup() != existingStudent.getGroup()
            ID = self.getStudentIDByHash(sHash)
            #print("ID {} for Hash {}".format(ID, sHash))
            IDcond = ID == s_id 
            if groupcond and IDcond:
                print("Group changed.")
                return True
            elif groupcond and not IDcond:
                print("Group changed but wrong ID:")
                print("got {}, but should be {}".format(s_id, self.getStudentIDByHash(sHash)))
            else:
                print("Group not changed.")
                return False
        else:
            print("student not in list")
            return False
    
    def appendStudent(self, student):
        print("Studentlist append")
        if self.checkNoDoubleEntry(student):        
            self.l.append(student)
            print("erfolgreich hinzugefügt")
            return True
        else:
            tkm.showerror(title="Fehler",
                          message="Eintrag existiert bereits.")
            print("nichts hinzugefügt.")
            #print(student)
            #print(student.getDict())
            return False

    def insertStudentAt(self, index, student):
        success = False
        try:
            self.l.insert(index, student)
            success = True
        except:
            success = False
        return success

    def delStudent(self, student):
        s = student
        try:
            self.l.remove(s)
            print(s.name + " entfernt.")
        except:
            print("Nichts gelöscht.")
            return False
        return True

    def delStudentById(self, sid):
        try:
            del self.l[sid]
            print("Nummer " + str(sid) + " entfernt.")
        except:
            print("Nichts gelöscht.")
            return False
        return True

    def delAllStudents(self):
        for sid in range(len(self.l)):
            self.delStudentById(0)
        if len(self.l) == 0:
            print("Alle Schüler gelöscht.")

    def getList(self):
        return self.l

    def getStudentIDByName(self, name, family_name):
        for student in self.l:
            if student.getName() == name and student.getFamilyName() == family_name:
                position = self.l.index(student)
                res = position
            else:
                res = -1
        return res
    
    def getStudentIDByHash(self, sHash):
        print("searching for {}".format(sHash))
        mystudent = self.getStudentByHash(sHash)
        if mystudent != None:
            print("found student: {}".format(mystudent.getName()))
            position = self.l.index(mystudent)
            res = position
            print("has ID: {}".format(res))
        else:
            res = -1
        return res                

    def getStudentByHash(self, sHash):
        student = next((s for s in self.l if s.getHash() == sHash), None)
        return student
        
    def sortListByName(self):
        sByName = sorted(self.l, key=lambda x: din5007(x.name), reverse=False)
        self.l = sorted(sByName, key=lambda x: din5007(x.family_name), reverse=False)
        return True

    def sortListByGroup(self):
        self.l.sort(key=lambda x: din5007(x.group), reverse=False)
        return True


class PointList():
    def __init__(self, studentList, exercisesDict):
        self.sL = studentList
        self.exD = exercisesDict
        print(self.exD)

        self.exNames = self.exD.keys()
        self.exPoints = self.exD.values()

        sL = self.sL
        exNames = self.exNames

        self.pL = list()

        for student in sL:
            sHash = student.getHash()
            inner_pL = list()
            for exercise in exNames:
                p = " "
                inner_pL.append(p)
            self.pL.append((sHash, inner_pL))

        print(self.pL)

    def getList(self):
        return self.pL

    def getEntry(self, sHash):
        entry = next((entry for entry in self.pL if entry[0]==sHash), None)
        return entry
    
    def get_points(self, sHash, exNum):
        print("Getting points of ex. {} of student {}.".format(exNum, sHash))
        
        inner_pL = self.get_pointsList(sHash)
        
        points = inner_pL[exNum]
        print(points)
        return points

    def get_pointsList(self, sHash):
        inner_pL = next((entry[1] for entry in self.pL if entry[0]==sHash), None)
        return inner_pL
    
    def get_sum(self, sHash):
        inner_pointslist = self.get_pointsList(sHash)
        result = 0
        try:
            pointslist = [float(entry) for entry in inner_pointslist]
            result = sum(pointslist)
        except:
            result = "x"
        print("Summe ist {}".format(str(result)))
        return result

    def set_points(self, sHash, exNum, value):
        print("Setting points of ex. {} of student {} to {}.".format(exNum, sHash, value))
        
        inner_pL = self.get_pointsList(sHash)
        inner_pL[exNum] = value
        
        return True

    def delEntry(self, sHash):
        entry = self.getEntry(sHash)
        print("removing {}".format(entry))
        self.pL.remove(entry)
        return True

# Dialog

class ReallyDeleteDialog(tk.Toplevel):
    def __init__(self, master, controller, selected_id, title="Löschen?"):
        super().__init__(master)
        self.title(title)
        self.transient(master)
        self.master = master
        self.con = controller
        self.sel_id = selected_id

        print("Löschen-Dialog")

        body = tk.Frame(self)
        self.initial_focus = self.getFocusElement(body)
        body.pack(padx=5, pady=5)

        self.infoBox()
        self.buttonBox()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (master.winfo_rootx()+50,
                                  master.winfo_rooty()+50))
        self.initial_focus.focus_set()

        self.wait_window(self)

    def getFocusElement(self, body):
        element = body
        return element

    def infoBox(self):
        box = tk.Frame(self)

        studentlist = self.con.sl.getList()
        student = studentlist[self.sel_id]
        name = student.getName()
        fname = student.getFamilyName()

        ltext = " ".join([name, fname]) + " wirklich löschen?"

        self.l_name = tk.Label(box, text=ltext)
        self.l_name.grid(row=0, column=0, sticky="w")

        box.pack()

    def buttonBox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10,
                      command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return -1
        else:
            pass

        self.withdraw()
        self.update_idletasks()
        self.apply()

        self.backToMaster()

    def cancel(self, event=None):
        self.con.unmarkDeletion(self.sel_id)
        self.backToMaster()

    def backToMaster(self):
        # put focus back to the parent window
        self.master.focus_set()
        self.destroy()

    def validate(self):
        return True

    def apply(self):
        self.con.doDeleteStudent(self.sel_id)
        return True


class NewStudentDialog(tk.Toplevel):
    def __init__(self, master, controller, title="Neuer Schüler"):
        super().__init__(master)
        self.transient(master)
        self.master = master
        self.con = controller

        print("Dialog")

        body = tk.Frame(self)
        self.initial_focus = self.getFocusElement(body)
        body.pack(padx=5, pady=5)

        self.entryBox()
        self.buttonBox()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (master.winfo_rootx()+50,
                                  master.winfo_rooty()+50))
        self.initial_focus.focus_set()

        self.wait_window(self)

    def getFocusElement(self, body):
        element = body
        return element

    def entryBox(self):
        box = tk.Frame(self)

        self.l_name = tk.Label(box, text="Vorname:")
        self.l_name.grid(row=0, column=0, sticky="w")
        self.e_name = tk.Entry(box, highlightcolor="blue", background="white")
        self.initial_focus = self.getFocusElement(self.e_name)
        self.e_name.grid(row=0, column=1)

        self.l_fname = tk.Label(box, text="Nachname:")
        self.l_fname.grid(row=1, column=0, sticky="w")
        self.e_fname = tk.Entry(box, highlightcolor="blue", background="white")
        self.e_fname.grid(row=1, column=1)

        self.l_group = tk.Label(box, text="Gruppe:")
        self.l_group.grid(row=2, column=0, sticky="w")
        self.e_group = tk.Entry(box, highlightcolor="blue", background="white")
        self.e_group.grid(row=2, column=1)

        box.pack()

    def buttonBox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10,
                      command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return -1
        else:
            pass

        self.withdraw()
        self.update_idletasks()
        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.master.focus_set()
        self.destroy()

    def validate(self):
        return True

    def apply(self):
        n = self.e_name.get()
        fn = self.e_fname.get()
        g = self.e_group.get()
        s = Student(name=n, family_name=fn, group=g)
        print(s.getDict())
        self.con.addStudent(s)
        return True


class EditStudentDialog(tk.Toplevel):
    def __init__(self, master, controller, selected_id, title="Schüler bearbeiten"):
        super().__init__(master)
        self.transient(master)
        self.master = master
        self.con = controller
        self.sel_id = selected_id

        body = tk.Frame(self)
        self.initial_focus = self.getFocusElement(body)
        body.pack(padx=5, pady=5)

        self.entryBox()
        self.buttonBox()

        self.wait_visibility()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self.getFocusElement(body)

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (master.winfo_rootx()+50,
                                  master.winfo_rooty()+50))
        self.initial_focus.focus_set()

        self.wait_window(self)

    def getFocusElement(self, body):
        element = body
        return element

    def entryBox(self):
        box = tk.Frame(self)

        studentlist = self.con.sl.getList()
        student = studentlist[self.sel_id]
        name = student.getName()
        fname = student.getFamilyName()
        group = student.getGroup()

        nameVar = tk.StringVar()
        nameVar.set(name)
        self.l_name = tk.Label(box, text="Vorname:")
        self.l_name.grid(row=0, column=0, sticky="w")
        self.e_name = tk.Entry(box, highlightcolor="blue",
                               background="white", textvariable=nameVar)
        self.initial_focus = self.getFocusElement(self.e_name)
        self.e_name.grid(row=0, column=1)

        fnameVar = tk.StringVar()
        fnameVar.set(fname)
        self.l_fname = tk.Label(box, text="Nachname:")
        self.l_fname.grid(row=1, column=0, sticky="w")
        self.e_fname = tk.Entry(
            box, highlightcolor="blue", background="white", textvariable=fnameVar)
        self.e_fname.grid(row=1, column=1)

        groupVar = tk.StringVar()
        groupVar.set(group)
        self.l_group = tk.Label(box, text="Gruppe:")
        self.l_group.grid(row=2, column=0, sticky="w")
        self.e_group = tk.Entry(
            box, highlightcolor="blue", background="white", textvariable=groupVar)
        self.e_group.grid(row=2, column=1)

        box.pack()

    def buttonBox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10,
                      command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return -1
        else:
            pass

        self.withdraw()
        self.update_idletasks()
        self.apply()

        self.con.unmarkEdit(self.sel_id)
        self.backToMaster()

    def cancel(self, event=None):
        self.con.unmarkEditNoChange(self.sel_id)
        self.backToMaster()

    def backToMaster(self):
        # put focus back to the parent window
        self.master.focus_set()
        self.destroy()

    def validate(self):
        return True

    def apply(self):
        n = self.e_name.get()
        fn = self.e_fname.get()
        g = self.e_group.get()
        s = Student(name=n, family_name=fn, group=g)
        self.con.updateStudent(s, self.sel_id)
        return True

#
# Controller
#


class Controller():
    def __init__(self, app):
        self.app = app
        self.sl = StudentList()
        
        self.flag_pointsEntry = False
    
    def activatePointsList(self):    
        self.exD = self.app.parent.controller.exercises.get_dict()
        self.pl = PointList(self.sl.getList(), self.exD)

    def newStudent(self, event=None):
        ns_Dialog = NewStudentDialog(self.app.parent, self)

    def addStudent(self, student):
        succ = self.sl.appendStudent(student)
        if succ:
            self.addToStudentlist(student)
        else:
            print("not able to add")
            

    def determineValuesTreeView(self, student):
        if not self.flag_pointsEntry:
            values = [None, student.getHash(), student.getFamilyName(), student.getName(),
                      student.getGroup()]
        else:
            sHash = student.getHash()
            pointValues = self.pl.get_pointsList(sHash)
            numberForFilling = 20-len(pointValues)
            emptyValuesListForFilling = ["" for _ in range(numberForFilling)]
            sumValue = self.pl.get_sum(sHash)
            values = [None, student.getHash(), student.getFamilyName(), student.getName(),
                      student.getGroup()] + pointValues + emptyValuesListForFilling + [sumValue]
        return values

    def doUpdate(self, student, s_id):
        # Update der Daten
        self.sl.delStudentById(s_id)
        self.sl.insertStudentAt(s_id, student)
        # Update der Anzeige
        values = self.determineValuesTreeView(student)
        self.app.studentlist.item(s_id, values=values)
            

    def updateStudent(self, student, s_id):
        # If no collision
        if self.sl.checkNoDoubleEntry(student):
            self.doUpdate(student, s_id)    
        # collision!
        elif self.sl.checkGroupChange(student, s_id):
            tkm.showinfo(title="Hinweis",
                          message="Eintrag existiert bereits.\n Nur Gruppe geändert.")
            self.doUpdate(student, s_id)
        else:
            tkm.showerror(title="Fehler",
                          message="Eintrag existiert bereits.")
            # do nothing
            pass
        

    def addToStudentlist(self, student):
        try:
            iid = self.sl.l.index(student)
        except:
            iid = 0
            print("{} not found".format(student.getDict()))
            raise
        
        if iid % 2 == 0:
            tag = "even"
        elif iid % 2 == 1:
            tag = "odd"
        else:
            pass
        values = self.determineValuesTreeView(student)
        print("values: {}".format(values))
        
        self.app.studentlist.insert(
            parent="", index="end", text=iid, iid=iid, values=values, tags=tag)

    def sortByName(self):
        self.sl.sortListByName()
        self.refillTreeView()

    def sortByGroup(self):
        self.sl.sortListByGroup()
        self.refillTreeView()
        
    def selectStudent(self, event=None):
        print("select")
        pass

    def editStudent(self, event=None):
        print("Bearbeiten")
        tree = self.app.studentlist
        selected = tree.selection()
        try:
            selected_id = int(selected[0])
        except:
            tkm.showinfo(title="Hinweis",
                         message="Nichts zum Bearbeiten ausgewählt.")
            return False

        self.markEdit(selected_id)

        editWin = EditStudentDialog(
            master=self.app, controller=self, selected_id=selected_id)

    def delStudent(self, event=None):
        tree = self.app.studentlist
        selected = tree.selection()
        try:
            selected_id = int(selected[0])
        except:
            tkm.showerror(title="Fehler",
                          message="Nichts zu löschen ausgewählt.")
            return False

        self.markDeletion(selected_id)

        reallyWin = ReallyDeleteDialog(
            master=self.app, controller=self, selected_id=selected_id)

    def markEdit(self, selected_id):
        tree = self.app.studentlist
        # Mark for deletion
        tree.item(selected_id, tags=("edit"))
        tree.selection_toggle(selected_id)
        tree.tag_configure("edit", background="lightgreen")

    def unmarkEdit(self, selected_id):
        tree = self.app.studentlist
        # Un-Mark from deletion
        tree.selection_toggle(selected_id)
        tree.tag_configure("edit", background="lightgrey")
        if selected_id % 2 == 0:
            tree.item(selected_id, tags=("even"))
        elif selected_id % 2 == 1:
            tree.item(selected_id, tags=("odd"))
        else:
            tree.item(selected_id, tags=(""))

    def unmarkEditNoChange(self, selected_id):
        tree = self.app.studentlist
        # Un-Mark from deletion
        tree.selection_toggle(selected_id)
        tree.tag_configure("edit", background="white")
        if selected_id % 2 == 0:
            tree.item(selected_id, tags=("even"))
        elif selected_id % 2 == 1:
            tree.item(selected_id, tags=("odd"))
        else:
            tree.item(selected_id, tags=(""))

    def markDeletion(self, selected_id):
        tree = self.app.studentlist
        # Mark for deletion
        tree.item(selected_id, tags=("del"))
        tree.selection_toggle(selected_id)
        tree.tag_configure("del", background="yellow")

    def unmarkDeletion(self, selected_id):
        tree = self.app.studentlist
        # Un-Mark from deletion
        tree.selection_toggle(selected_id)
        tree.tag_configure("del", background="white")
        if selected_id % 2 == 0:
            tree.item(selected_id, tags=("even"))
        elif selected_id % 2 == 1:
            tree.item(selected_id, tags=("odd"))
        else:
            tree.item(selected_id, tags=(""))

    def doDeleteStudent(self, ID):
        student = self.sl.getList()[ID]
        if self.flag_pointsEntry:
            self.pl.delEntry(student.getHash())
        else:
            pass
        self.sl.delStudent(student)
        self.app.studentlist.delete(ID)
        self.refillTreeView()

    def refillTreeView(self):
        print("Student: refilling")
        slTV = self.app.studentlist
        # print(slTV.get_children())
        for item in slTV.get_children():
            slTV.delete(item)
        #map(slTV.delete, slTV.get_children())
        self.fillTreeView()

    def fillTreeView(self):
        print("Student: filling")
        sl = self.sl
        for student in sl.getList():
            self.addToStudentlist(student)

    def loadStudent(self, event=None):
        print("Laden")

        filename = tkfd.askopenfilename(initialdir=".", title="Wähle Schülerdatei aus", filetypes=(
            ("CSV-Dateien", "*.csv"), ("Alle Dateien", "*.*")))

        c = pr_csv.MyCSV(filename)
        result = c.read()
        # print(result)

        self.sl.delAllStudents()
        self.refillTreeView()

        for entry in result:
            s = Student(name=entry["Vorname"],
                        family_name=entry["Nachname"],
                        group=entry["Gruppe"])
            self.sl.appendStudent(s)

        self.refillTreeView()

    def saveStudent(self, event=None):
        print("Speichern")
        filename = ""

        try:
            mainapp = self.app.parent.exam
            theClass = mainapp.e_class.get()
            if theClass == "":
                raise Exception("Keine Klasse angegeben.")
            else:
                theDate = mainapp.e_date.get()
                fn = str(theClass) + " " + str(theDate)
                filename = fn.strip().replace(" ", "_").replace(".", "").lower() + ".csv"
        except:
            tkm.showinfo("Fehler bei autom. Dateinamenerzeugung",
                         "Konte den Dateinamen nicht automatisch erzeugen.")
            filename = "out.csv"

        try:
            c = pr_csv.MyCSV(filename)
            c.write(self.sl.getList())
            tkm.showinfo(
                "Speichern", "Schülerliste gespeichert unter: {}".format(filename))
        except:
            tkm.showerror(
                "Fehler", "Schülerliste konnte nicht gespeichert werden.")

    def editPoints(self, event=None):
        if self.flag_pointsEntry == False:
            self.activatePointsList() # makes self.pl and self.exD available
            self.app.updateTVExColDisplay(self.exD)    
        
            self.flag_pointsEntry = True
            self.app.updatePointsEntryStatus(self.flag_pointsEntry)
        else:
            pass
        
        tree = self.app.studentlist
        selected = tree.selection()
        
        try:
            selected_id = int(selected[0])
        except:
            tkm.showinfo(title="Hinweis",
                         message="Nichts zum Bearbeiten ausgewählt.")
            return False

        self.markEdit(selected_id)

        editWin = poi.EditPointsDialog(
            master=self.app, controller=self, selected_id=selected_id)
        return True
    
    def updatePoints(self, sHash, pointslist):
        print("StudCon: Update Points called")
        
        for counter, entry in enumerate(pointslist):    
            self.pl.set_points(sHash, exNum=counter, value=entry)
        
        self.app.updateTVExColDisplay(self.exD)
        self.refillTreeView()
        
    def nextEditPoints(self, event=None, selected_id = 0):
        self.app.updateTVExColDisplay(self.exD)
        #tree = self.app.studentlist
        
        #tree.selection_set(selected_id)
        
        self.unmarkEditNoChange(selected_id)

        selected_id += 1
        try:
            self.markEdit(selected_id)
        except:
            tkm.showinfo("Letzter Eintrag", "Letzter Schüler erreicht.")
            return False
            #raise
            
        editWin = poi.EditPointsDialog(
            master=self.app, controller=self, selected_id=selected_id)
        return True     
    
#
# Main App
#


class Application(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)
        #self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)

        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)

        self.con = Controller(self)

        self.students_title = tk.Label(
            self, text="Schülererfassung", font=myfont)
        self.students_title.grid(row=0, column=0, sticky="nws")

        buttonFrame = tk.Frame(self)
        #buttonFrame.columnconfigure(0, weight=1)

        self.loadStudentButton = tk.Button(buttonFrame, text="Laden")
        self.loadStudentButton["command"] = self.con.loadStudent
        self.loadStudentButton.grid(row=0, column=0)

        self.newStudentButton = tk.Button(buttonFrame, text="Neuer Schüler")
        self.newStudentButton["command"] = self.con.newStudent
        self.newStudentButton.grid(row=0, column=1)

        self.editStudentButton = tk.Button(buttonFrame, text="Bearbeiten")
        self.editStudentButton["command"] = self.con.editStudent
        self.editStudentButton.grid(row=0, column=2)

        self.delStudentButton = tk.Button(buttonFrame, text="Löschen")
        self.delStudentButton["command"] = self.con.delStudent
        self.delStudentButton.grid(row=0, column=3)

        self.writeStudentButton = tk.Button(buttonFrame, text="Speichern")
        self.writeStudentButton["command"] = self.con.saveStudent
        self.writeStudentButton.grid(row=0, column=4)

        self.editPointsButton = tk.Button(buttonFrame, text="Punkte eingeben")
        self.editPointsButton["command"] = self.con.editPoints
        self.editPointsButton.grid(row=0, column=5)

        buttonFrame.grid(row=1, column=0, sticky="nswe")

        self.studentlistFrame = tk.Frame(self, cursor="hand1")
        self.studentlistFrame.columnconfigure(0, weight=2)
        self.studentlistFrame.rowconfigure(0, weight=1)

        self.slBottomFrame = tk.Frame(self.studentlistFrame)
        self.slBottomFrame.grid(row=1, column=0, sticky="we")

        self.studentlist = ttk.Treeview(self.studentlistFrame, columns=[
                                        "ID", "hash", "Name", "Vorname", "Gruppe"
                                        ] + ["ex"+str(i+1) for i in range(20)] + ["Summe"],
                                        displaycolumns="#all",
                                        padding=2, selectmode="browse")
        self.studentlist.column("#0", width=10)
        self.studentlist.column(0, width=20)
        self.studentlist.column(1, width=40)
        self.studentlist.column(2, width=100)
        self.studentlist.column(3, width=100)
        self.studentlist.column(4, width=10)
        
        for i in range(20):
            nr = i+5
            self.studentlist.column(nr, width=30)
            self.studentlist.heading(nr, text=str(i+1))
            
        self.studentlist.column(25, width=30)
        self.studentlist.heading(25, text="Summe")
        
        self.studentlist.configure(displaycolumns=[2, 3, 4])
            
        self.studentlist.heading("#0", text="ID")
        self.studentlist.heading(
            2, text="Name", command=self.con.sortByName)
        self.studentlist.heading(3, text="Vorname")
        self.studentlist.heading(
            4, text="Gruppe", command=self.con.sortByGroup)
        
        
        self.studentlist.tag_configure("odd", background="light grey")
        self.studentlist.tag_configure("even", background="light blue")
        self.studentlist.grid(row=0, column=0, sticky="nwse")
        
        self.TVstyle = ttk.Style()
        print("TVstate: {}".format(self.studentlist.state()))

        self.studentlist.bind("<Double-1>", self.con.editStudent)
        self.studentlist.bind("<<TreeViewSelect>>", self.con.selectStudent)

        self.scrbarStudentlist = tk.Scrollbar(
            self.studentlistFrame, orient=tk.VERTICAL, command=self.studentlist.yview)
        self.scrbarStudentlist.grid(row=0, column=1, sticky="ns")
        self.studentlist.configure(yscrollcommand=self.scrbarStudentlist.set)

        self.scrbarHStudentlist = tk.Scrollbar(
            self.slBottomFrame, orient=tk.HORIZONTAL, command=self.studentlist.xview)
        self.scrbarHStudentlist.pack(fill="x", side=tk.BOTTOM, expand=True)
        self.studentlist.configure(xscrollcommand=self.scrbarHStudentlist.set)

        self.studentlistFrame.grid(row=2, column=0, sticky="nwse")

        self.analysis_cv = tk.Canvas(
            master=self, width=self.studentlistFrame.cget("width"), height=20)
        self.analysis_cv.grid(row=3, column=0, sticky="nwse")

        self.status = tk.Frame(self)
        self.status.grid(row=4, column=0, sticky="nwse")
        self.status.columnconfigure(0, weight=1)
        self.status.columnconfigure(1, weight=1)
        self.pointsEntryStatus = tk.Label(
            self.status, text="Keine Punkte", font="Helvetica 8", background="red", foreground="white")
        self.pointsEntryStatus.grid(row=0, column=0, sticky="e", padx=2)
        
        self.passwordStatus = tk.Label(
            self.status, text="\u2610 Passwort", font="Helvetica 8", background="red", foreground="white")
        self.passwordStatus.grid(row=0, column=1, sticky="e", padx=2)

        self.parent.master.bind("<Control-o>", self.con.loadStudent)
        self.parent.master.bind("<Control-n>", self.con.newStudent)
        self.parent.master.bind("<Control-e>", self.con.editStudent)
        self.parent.master.bind("<Control-d>", self.con.delStudent)
        self.parent.master.bind("<Control-s>", self.con.saveStudent)

    def updatePointsEntryStatus(self, flag):
        if flag:
            self.pointsEntryStatus.config(text="Punkte", background="yellow", fg="black")
        else:
            self.pointsEntryStatus.config(text="Keine Punkte", background="red", fg="white")
        pass
    
    def updateTVColWidths(self):
        self.studentlist.column("#0", width=10)
        self.studentlist.column(0, width=20)
        self.studentlist.column(1, width=40)
        self.studentlist.column(2, width=100)
        self.studentlist.column(3, width=100)
        self.studentlist.column(4, width=10)
        
        for i in range(20):
            nr = i+5
            self.studentlist.column(nr, width=30)
            
        self.studentlist.column(25, width=30)
       
    
    def updateTVExColDisplay(self, exD):
        nr_ex = len(exD)
        exDisplayList = [i + 5 for i in range(nr_ex)]
        columnsToDisplay = [2, 3, 4] + exDisplayList + [25]
        self.studentlist.configure(displaycolumns=columnsToDisplay)
        for counter, (exName, exPoints) in enumerate(exD.items()):
            colnum = counter + 5
            self.studentlist.heading(colnum, text=exName)
        
        self.updateTVColWidths()
            

if __name__ == "__main__":
    root = tk.Tk()
    print(root.tk.call('info', 'patchlevel'))
#    style = ttk.Style(root)
#    style.map('Treeview', foreground=fixed_map('foreground'),
#              background=fixed_map('background'))
    Application(root).pack(fill="both", expand=True)
    root.mainloop()
