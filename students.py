#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:47:45 2019

@author: mputzlocher
"""

import tkinter as tk 
import tkinter.ttk as ttk
from tkinter import messagebox as tkm

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
        s.group = student_list.pop()
        s.family_name = student_list.pop()
        s.name = student_list.pop()
        
    def setFromDict(self, student_dict):
        s.name = student_dict["Vorname"]
        s.family_name = student_dict["Nachname"]
        s.group = student_dict["Gruppe"]

class StudentList():
    def __init__(self):
        self.l = list()
        
    def appendStudent(self, student):
        self.l.append(student)
        print(student)
        print(student.getDict())
        print("erfolgreich hinzugefügt")
    
    def delStudent(self, student):
        s = student
        self.l.remove(s)
        print(s.name + " entfernt.")
    
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

class ReallyDeleteDialog(tk.Toplevel):
    def __init__(self, master, controller, selected, title = "Löschen?"):
        super().__init__(master)
        self.transient(master)
        self.master = master
        self.con = controller
        self.sel = selected
        
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
        student = studentlist[self.sel]
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
        
        self.cancel()
        
    def cancel(self, event=None):
        # self.con.app.studentlist.item(selected_id, tags="")
        # put focus back to the parent window
        self.master.focus_set()
        self.destroy()
    
    def validate(self):
        return True
        
    def apply(self):
        self.con.doDeleteStudent(self.sel)
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

    def addToStudentlist(self, student):
        iid = self.sl.l.index(student)
        values = [student.getFamilyName(), student.getName(), student.getGroup()]
        self.app.studentlist.insert(parent="", index="end", text=iid, iid=iid, values=values)

    def editStudent(self, event=None):
        print("Bearbeiten")
        pass
        
    def delStudent(self, event=None):
        selected = self.app.studentlist.selection()
        try:
            selected_id = int(selected[0])
        except:
            tkm.showerror(title="Fehler", message="Nichts zu löschen ausgewählt.")
            return False
            
        self.app.studentlist.item(selected_id, tags=("del"))
        print(self.app.studentlist.tag_has("del"))
        #self.app.studentlist.tag_configure("del", selectbackground="red")
        self.app.studentlist.tag_configure("del", background="yellow")
        self.app.studentlist.configure()
        #itemClicked = self.app.studentlist.focus()
        #self.app.studentlist.tag_bind('del', '<1>', itemClicked)
        print(self.app.studentlist.tag_configure("del"))
        print(selected_id)
        print("Löschen")
        really = ReallyDeleteDialog(master=self.app, controller=self, selected=selected_id)
    
    def doDeleteStudent(self, num):
        student = self.sl.getList()[num]
        self.sl.delStudent(student)
        self.app.studentlist.delete(num)
        self.refillTreeView()
    
    def refillTreeView(self):
        slTV = self.app.studentlist
        print(slTV.get_children())
        for item in slTV.get_children():
            slTV.delete(item)
        #map(slTV.delete, slTV.get_children())
        self.fillTreeView()
    
    def fillTreeView(self):
        sl = self.sl
        for student in sl.getList():
            self.addToStudentlist(student)
    
    def saveStudent(self, event=None):
        print("Speichern")
        pass

#
# Main App
#

class Example(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        self.con = Controller(self)
        
        buttonFrame = tk.Frame(self)
        
        self.newStudentButton = tk.Button(buttonFrame, text="Neuer Schüler")
        self.newStudentButton["command"] = self.con.newStudent
        self.newStudentButton.grid(row=0, column=0)
        
        self.editStudentButton = tk.Button(buttonFrame, text="Bearbeiten")
        self.editStudentButton["command"] = self.con.editStudent
        self.editStudentButton.grid(row=0, column=1)
        
        self.delStudentButton = tk.Button(buttonFrame, text="Löschen")
        self.delStudentButton["command"] = self.con.delStudent
        self.delStudentButton.grid(row=0, column=2)
        
        self.writeStudentButton = tk.Button(buttonFrame, text="Speichern")
        self.writeStudentButton["command"] = self.con.saveStudent
        self.writeStudentButton.grid(row=0, column=3)
        
        buttonFrame.grid(row=0, column=0, sticky="we")
        
        self.studentlist = ttk.Treeview(self, columns=["ID","Name","Vorname","Gruppe"], padding=2, selectmode="browse")
        self.studentlist.heading("#0", text="ID")
        self.studentlist.heading("#1", text="Name")
        self.studentlist.heading("#2", text="Vorname")
        self.studentlist.heading("#3", text="Gruppe")
        self.studentlist.grid(row=1, column=0)
        
        self.parent.bind("n", self.con.newStudent)
        self.parent.bind("e", self.con.editStudent)
        self.parent.bind("<Delete>", self.con.delStudent)
        self.parent.bind("<Control-s>", self.con.saveStudent)
        

if __name__ == "__main__":
    root = tk.Tk()
    print(root.tk.call('info', 'patchlevel'))
    Example(root).pack(fill="both", expand=True)
    root.mainloop()
