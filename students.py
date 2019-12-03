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

import pr_csv

#-----------------------------------------------------------------------
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

#-----------------------------------------------------------------------

myfont = "Helvetica 14"

class Student():
    def __init__(self, name, family_name, group):
        self.name = name
        self.family_name = family_name
        self.group = group

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
        return {n : s.name, f : s.family_name, g : s.group}
        
    def setFromList(self, student_list):
        s = self
        s.group = student_list.pop()
        s.family_name = student_list.pop()
        s.name = student_list.pop()
        
    def setFromDict(self, student_dict):
        s = self
        s.name = student_dict["Vorname"]
        s.family_name = student_dict["Nachname"]
        s.group = student_dict["Gruppe"]

class StudentList():
    def __init__(self):
        self.l = list()
        
    def appendStudent(self, student):
        self.l.append(student)
        #print(student)
        #print(student.getDict())
        print("erfolgreich hinzugefügt")
    
    def insertStudentAt(self, index, student):
        try:
            self.l.insert(index, student)
        except:
            return False
        return True
    
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
        
    def getStudentNr(self, name, family_name):
        for student in self.l:
            if student.getName() == name and student.getFamilyName() == family_name:
                position = self.l.index(student)
                return position
            else:
                pass
        return -1
    
    def sortListByName(self):
        sByName = sorted(self.l, key=lambda x: x.name, reverse=False)
        self.l = sorted(sByName, key=lambda x: x.family_name, reverse=False)
        return True
    
    def sortListByGroup(self):
        self.l.sort(key=lambda x: x.group, reverse=False)
        return True

class ReallyDeleteDialog(tk.Toplevel):
    def __init__(self, master, controller, selected_id, title = "Löschen?"):
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

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()
    
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
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
    def __init__(self, master, controller, title = "Neuer Schüler"):
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

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()
    
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
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
        self.con.addStudent(s)
        return True

class EditStudentDialog(tk.Toplevel):
    def __init__(self, master, controller, selected_id, title = "Schüler bearbeiten"):
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
        self.e_name = tk.Entry(box, highlightcolor="blue", background="white", textvariable=nameVar)
        self.initial_focus = self.getFocusElement(self.e_name)
        self.e_name.grid(row=0, column=1)
        
        fnameVar = tk.StringVar()
        fnameVar.set(fname)
        self.l_fname = tk.Label(box, text="Nachname:")
        self.l_fname.grid(row=1, column=0, sticky="w")
        self.e_fname = tk.Entry(box, highlightcolor="blue", background="white", textvariable=fnameVar)
        self.e_fname.grid(row=1, column=1)
        
        groupVar = tk.StringVar()
        groupVar.set(group)
        self.l_group = tk.Label(box, text="Gruppe:")
        self.l_group.grid(row=2, column=0, sticky="w")
        self.e_group = tk.Entry(box, highlightcolor="blue", background="white", textvariable=groupVar)
        self.e_group.grid(row=2, column=1)
        
        box.pack()
    
    def buttonBox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()
    
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
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
        
    def newStudent(self, event=None):
        ns_Dialog = NewStudentDialog(self.app.parent, self)
        
    def addStudent(self, student):
        self.sl.appendStudent(student)
        self.addToStudentlist(student)
    
    def updateStudent(self, student, s_id):
        # Update der Daten
        self.sl.delStudentById(s_id)
        self.sl.insertStudentAt(s_id, student)
        # Update der Anzeige
        values = [student.getFamilyName(), student.getName(), student.getGroup()]
        self.app.studentlist.item(s_id, values=values)

    def addToStudentlist(self, student):
        iid = self.sl.l.index(student)
        values = [student.getFamilyName(), student.getName(), student.getGroup()]
        if iid % 2 == 0:
            tag = "even"
        elif iid % 2 == 1:
            tag = "odd"
        else:
            pass
        self.app.studentlist.insert(parent="", index="end", text=iid, iid=iid, values=values, tags=tag)

    def sortByName(self):
        self.sl.sortListByName()
        self.refillTreeView()
        
    def sortByGroup(self):
        self.sl.sortListByGroup()
        self.refillTreeView()

    def editStudent(self, event=None):
        print("Bearbeiten")
        tree = self.app.studentlist
        selected = tree.selection()
        try:
            selected_id = int(selected[0])
        except:
            tkm.showinfo(title="Hinweis", message="Nichts zum Bearbeiten ausgewählt.")
            return False
        
        self.markEdit(selected_id)
        
        editWin = EditStudentDialog(master=self.app, controller=self, selected_id=selected_id)
        
    def delStudent(self, event=None):
        tree = self.app.studentlist
        selected = tree.selection()
        try:
            selected_id = int(selected[0])
        except:
            tkm.showerror(title="Fehler", message="Nichts zu löschen ausgewählt.")
            return False
        
        self.markDeletion(selected_id)
        
        reallyWin = ReallyDeleteDialog(master=self.app, controller=self, selected_id=selected_id)
    
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
        
    def doDeleteStudent(self, num):
        student = self.sl.getList()[num]
        self.sl.delStudent(student)
        self.app.studentlist.delete(num)
        self.refillTreeView()
    
    def refillTreeView(self):
        slTV = self.app.studentlist
        #print(slTV.get_children())
        for item in slTV.get_children():
            slTV.delete(item)
        #map(slTV.delete, slTV.get_children())
        self.fillTreeView()
    
    def fillTreeView(self):
        sl = self.sl
        for student in sl.getList():
            self.addToStudentlist(student)

    def loadStudent(self, event=None):
        print("Laden")
        
        filename = tkfd.askopenfilename(initialdir = ".", title="Wähle Schülerdatei aus", filetypes = (("CSV-Dateien","*.csv"),("Alle Dateien","*.*")))
                
        c = pr_csv.MyCSV(filename)
        result = c.read()
        #print(result)
        
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
                fn = str(theClass) +" "+ str(theDate)
                filename = fn.strip().replace(" ","_").replace(".","").lower() + ".csv"
        except:
            tkm.showinfo("Fehler bei autom. Dateinamenerzeugung", "Konte den Dateinamen nicht automatisch erzeugen.")
            filename = "out.csv"
        
        try:
            c = pr_csv.MyCSV(filename)
            c.write(self.sl.getList())
            tkm.showinfo("Speichern", "Schülerliste gespeichert unter: {}".format(filename))
        except:
            tkm.showerror("Fehler", "Schülerliste konnte nicht gespeichert werden.")

#
# Main App
#

class Application(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)
        #self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.con = Controller(self)
    
        self.students_title = tk.Label(self, text="Schülererfassung", font=myfont)
        self.students_title.grid(row=0, column=0, sticky = "nws")
        
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
        
        buttonFrame.grid(row=1, column=0, sticky="nswe")
        
        self.studentlistFrame = tk.Frame(self, cursor="hand1")
        self.studentlistFrame.columnconfigure(0, weight=2)
        self.studentlistFrame.rowconfigure(0, weight=1)
        
        self.slBottomFrame = tk.Frame(self.studentlistFrame)
        self.slBottomFrame.grid(row=1,column=0, sticky="we")
        
        self.studentlist = ttk.Treeview(self.studentlistFrame, columns=["ID","Name","Vorname","Gruppe"], padding=2, selectmode="browse")
        self.studentlist.column("#0", width=40)
        self.studentlist.column("#1", width=100)
        self.studentlist.column("#2", width=100)
        self.studentlist.column("#3", width=50)
        self.studentlist.heading("#0", text="ID")
        self.studentlist.heading("#1", text="Name", command=self.con.sortByName)
        self.studentlist.heading("#2", text="Vorname")
        self.studentlist.heading("#3", text="Gruppe", command=self.con.sortByGroup)
        self.studentlist.tag_configure("odd", background="lightgrey")
        self.studentlist.tag_configure("even", background="lightblue")
       # self.studentlist.pack(fill="both")
        self.studentlist.grid(row=0, column=0, sticky="nwse")
        
        self.studentlist.bind("<Double-1>", self.con.editStudent)
        
        self.scrbarStudentlist = tk.Scrollbar(self.studentlistFrame, orient=tk.VERTICAL, command=self.studentlist.yview)
        self.scrbarStudentlist.grid(row=0, column=1, sticky="ns")
        self.studentlist.configure(yscrollcommand=self.scrbarStudentlist.set)
        
        
        self.scrbarHStudentlist = tk.Scrollbar(self.slBottomFrame, orient=tk.HORIZONTAL, command=self.studentlist.xview)
        self.scrbarHStudentlist.pack(fill="x", side=tk.BOTTOM, expand=True)
        self.studentlist.configure(xscrollcommand=self.scrbarHStudentlist.set)
        
        self.studentlistFrame.grid(row=2, column=0, sticky="nwse")
        
        self.analysis_cv = tk.Canvas(master=self, width = self.studentlistFrame.cget("width"), height=20)
        self.analysis_cv.grid(row=3, column=0, sticky="nwse")
        
        self.status = tk.Frame(self)
        self.passwordStatus = tk.Label(self.status, text="\u2610 Passwort", font="Helvetica 8", background="red", foreground="white")
        self.passwordStatus.pack(anchor="e", padx=2)
        self.status.grid(row=4, column=0, sticky="nwse")
        
        self.parent.master.bind("<Control-o>", self.con.loadStudent)
        self.parent.master.bind("<Control-n>", self.con.newStudent)
        self.parent.master.bind("<Control-e>", self.con.editStudent)
        self.parent.master.bind("<Control-d>", self.con.delStudent)
        self.parent.master.bind("<Control-s>", self.con.saveStudent)
        

if __name__ == "__main__":
    root = tk.Tk()
    print(root.tk.call('info', 'patchlevel'))
    style = ttk.Style(root)
    style.map('Treeview', foreground=fixed_map('foreground'),
     background=fixed_map('background'))
    Application(root).pack(fill="both", expand=True)
    root.mainloop()
