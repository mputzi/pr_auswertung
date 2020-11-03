#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 23:59:23 2019

@author: mputzlocher
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as tkm
from tkinter import filedialog as tkfd


# +++++++++++++++++++++++
# Model
# +++++++++++++++++++++++

"""
The data model for points is in pr_students.py
"""

# +++++++++++++++++++++++
# Validator
# +++++++++++++++++++++++

class Points_Validator():
    def __init__(self, controller):
        self.con = controller

    def validateBE(self, P, maxBE):
        #print("validateBE: got {}, {}".format(P,maxBE))
        if len(P) > 0:
            try:
                inval = float(P)
                if int(inval*2) == inval*2:
                    pass
                else:
                    #print("Endet nicht auf .5 oder .0")
                    return False
                
                if inval > float(maxBE): # check in < max
                    #print("Wert zu groß, größer als {}!".format(maxBE))
                    errorstring = "Eingegebener Wert {} größer als Maximalpunktzahl für diese Aufgabe (maximal {}).".format(P, maxBE)
                    tkm.showerror("Wert zu groß", errorstring)
                    return False
                else:
                    pass
                return True
            except ValueError:
                #print("Fehler bei Eingabe, gelesen: {}".format(P))
                errorstring = "Eingegebener Wert {} nicht als Zahl interpretierbar".format(P)
                tkm.showerror("Eingabefehler", errorstring)
                return False
        else:
            return True

    def validateInt(self, P):
        if P.isdigit():
            return True
        else:
            return False

    #def validateExNames(self, P):
    #    nameslist = self.con.exercises.names
    #    if nameslist.count(P) >= 2:
    #        tkm.showerror("Eingabefehler", "Name schon vergeben!")
    #        return False
    #    else:
    #        return True


# +++++++++++++++++++++++
# Controller
# +++++++++++++++++++++++

class Points_Controller():
    def __init__(self, dialog):
        self.dialog = dialog
        self.selected_id = dialog.sel_id
        self.con = dialog.con
        self.vali = Points_Validator(self)
        
    def getPointsList(self):
        entryVarList = self.dialog.exBEVarList
        pointslist = [entry.get() for entry in entryVarList]
        return pointslist
        
    def updatePoints(self, event=None):
        print("PCon: Update Points")
        
        sHash = self.dialog.sHash
        
        pointslist = self.getPointsList()
        self.con.updatePoints(sHash, pointslist)
        
        ev = event
        if ev != None:
            print(ev.keysym)
        # Fokus weitergeben nach Enter oder Return
        if ev != None and (ev.keysym == 'KP_Enter' or ev.keysym == 'Return'
                           or ev.keysym == 'Tab'):
            sending_widget = ev.widget
            sending_widget.event_generate('<<TraverseOut>>')
            next_widget = sending_widget.tk_focusNext()
            next_widget.focus()
            next_widget.event_generate('<<TraverseIn>>')
        else:
            pass
        
    def nextE(self, event=None):
        print("Nächster Schüler")
        self.con.nextEditPoints(selected_id=self.selected_id)
        
        self.dialog.ok()


# +++++++++++++++++++++++
# View
# +++++++++++++++++++++++

class EditPointsDialog(tk.Toplevel):
    def __init__(self, master, controller, selected_id, title="Punkte eintragen"):
        super().__init__(master)
        self.transient(master)
        self.master = master
        self.con = controller
        self.sel_id = selected_id
        
        self.sL = controller.sl.getList()
        self.pL = controller.pl
        
        self.student = self.sL[self.sel_id] 
        st = self.student
        self.name = st.getName()
        self.fname = st.getFamilyName()
        self.group = st.getGroup()
        self.sHash = st.getHash()
        
        self.student_pL = self.pL.get_pointsList(self.sHash) 
        self.pcon = Points_Controller(self)        
        
        print("Dialog: Punkte für {} {}".format(self.name, self.fname))
        
        # Testing ---
        
        # print(self.student_pL)
        
        # self.pL.set_points(self.sHash, exNum=1, value=1)

        # print(self.student_pL)
        
        # ---
        
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (master.winfo_rootx()+50,
                                  master.winfo_rooty()+50))
       
        body = tk.Frame(self)

        self.initial_focus = self.getFocusElement(body)
        body.pack(padx=5, pady=5)

        self.nameBox()
        self.entryBox()
        self.buttonBox()
        self.wait_visibility()
        self.grab_set()
       
        #if not self.initial_focus:
        self.initial_focus = self.exBEEntriesList[0]
        self.initial_focus.focus_set()
        self.initial_focus.select_range(0,"end")
        self.activate_controller()

        self.wait_window(self)

    def getFocusElement(self, body):
        element = body
        return element

    def nameBox(self):
        box=tk.Frame(self)
        
        self.ll_name = tk.Label(box, text=self.name)
        self.ll_name.grid(row=0, column=0)
        
        self.ll_fname = tk.Label(box, text=self.fname)
        self.ll_fname.grid(row=0, column=1)
        
        if self.group != "":
            groupstr = "in Gruppe {}".format(self.group)
        else:
            groupstr = "in keiner Gruppe"
        self.ll_group = tk.Label(box, text=groupstr)
        self.ll_group.grid(row=0, column=2)
        
        self.ll_sHash = tk.Label(box, text=self.sHash, font="Monospace 8")
        self.ll_sHash.grid(row=1, column=0, columnspan=3, sticky ="nwse")
        
        box.pack()
        
    def entryBox(self):
        box = tk.Frame(self)

        # Frame für Platzieren der Canvas
        self.f_forCanvas = tk.Frame(box, bg="antique white")
        self.f_forCanvas.grid(row=0, column=1, sticky="we")
        self.f_forCanvas.columnconfigure(0, weight=1)
        frame_around_canvas = self.f_forCanvas

        # Canvas for Scrolling
        self.c_points = tk.Canvas(frame_around_canvas,
                                  relief=tk.SUNKEN, bd=2, highlightcolor="blue",
                                  bg="lavender")
        self.c_points.configure(height=80)
        self.c_points.grid(row=0, column=0, sticky="we")
        canvas = self.c_points

        #canvas.columnconfigure(0, weight=1)

        # Frame: Eingabe
        self.f_points = tk.Frame(
             self.c_points, relief=tk.FLAT, bd=2, highlightcolor="blue", bg="antique white")
        self.f_points.grid(row=0, column=0, sticky="nswe")
        frame_points = self.f_points
        # Window on Canvas for Entry-Fields
        self.w_points = canvas.create_window(
             (3, 3), window=frame_points, anchor="nw", height=80)

        # Aufgabeneingabe
        self.exNameEntriesList = list()
        self.maxPointsEntriesList = list()
        self.maxPointsVarList = list()
        self.exBEEntriesList = list()
        self.exBEVarList = list()
        
        # Eingabefelder
        for counter, (exName, maxPoints) in enumerate(self.pL.exD.items()):
            exNameVar = tk.StringVar()
            maxPointsVar = tk.DoubleVar()
            exBEVar = tk.DoubleVar()
            
            nameEntry = tk.Entry(frame_points, textvariable=exNameVar, width=3,
                                 justify=tk.LEFT,
                                 relief=tk.FLAT, bd=2, takefocus=0)
            nameEntry.grid(row=0, column=counter, sticky="w")
            exNameVar.set(exName)
            nameEntry.config(state="readonly")
            self.exNameEntriesList.append(nameEntry)
            
            maxPointsEntry = tk.Entry(frame_points, textvariable=maxPointsVar,
                                      width=3, disabledbackground="lavender",
                                      disabledforeground="black",
                                      bg="lightblue", justify=tk.CENTER,
                                      relief=tk.FLAT, bd=2, takefocus=0)
            maxPointsEntry.grid(row=1, column=counter, sticky="w")
            
            maxPointsVar.set(maxPoints)
            # No decimals if whole numbers
            if maxPointsVar.get() == int(maxPoints):
                maxPointsEntry.delete(0, "end")
                maxPointsEntry.insert(0,"{:.0g}".format(maxPoints))
            else:
                pass
            
            maxPointsEntry.config(state="disabled")
            self.maxPointsVarList.append(maxPointsVar)
            self.maxPointsEntriesList.append(maxPointsEntry)
            
            BEEntry = tk.Entry(frame_points, textvariable=exBEVar, width=3,
                               relief=tk.GROOVE, bd=2, takefocus=1,
                               highlightcolor="blue", justify="right")
            BEEntry.grid(row=2, column=counter, sticky="w")
            
            BE =self.student_pL[counter]
            try:
                float(BE)
            except:
                BE = 0
            exBEVar.set(BE)
            
            self.exBEVarList.append(exBEVar)
            self.exBEEntriesList.append(BEEntry)

        # Frame for Scrollbar
        self.f_cBottomFrame = tk.Frame(frame_around_canvas)
        self.f_cBottomFrame.grid(row=1, column=0, sticky="we")
        self.f_cBottomFrame.columnconfigure(0, weight=1)
        scrbar_frame = self.f_cBottomFrame

        # Horizontal Scrollbar
        self.scrbar = tk.Scrollbar(scrbar_frame,
                     orient=tk.HORIZONTAL, command=canvas.xview)
        self.scrbar.grid(row=0, column=0, sticky="ew")

        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox(tk.ALL),
                         xscrollcommand=self.scrbar.set)

        box.pack()
        
    def buttonBox(self):
        box = tk.Frame(self)

        self.b_ok = tk.Button(box, text="OK", width=10,
                      command=self.ok, default=tk.ACTIVE)
        self.b_ok.pack(side=tk.LEFT, padx=5, pady=5)
        self.b_cancel = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        self.b_cancel.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.b_next = tk.Button(box, text="Nächster", width=10,
                                command=self.pcon.nextE)
        self.b_next.pack(side=tk.LEFT, padx=5, pady=5)
        
        box.pack()

    def activate_controller(self):
        self.b_ok.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        
        # self.sb_exercise_number.bind("<Button-1>",  self.con.update_ex_number)
       # self.sb_exercise_number.bind(
       #     "<KeyRelease-Up>",    self.con.update_ex_number)
       # self.sb_exercise_number.bind(
       #     "<KeyRelease-Down>",  self.con.update_ex_number)
       # self.sb_exercise_number["command"] = self.con.update_ex_number
       # self.b_exercise_number["command"] = self.con.update_ex_number
       # self.b_all_points["command"] = lambda: self.con.set_max(
       #     maxBE=self.con.exercises.get_max())

        self.activate_controller_on_entries()

    def activate_controller_on_entries(self):
        for counter, entry in enumerate(self.exBEEntriesList):
            maxBE = self.maxPointsVarList[counter].get()
            vcmd = (entry.register(self.pcon.vali.validateBE), '%P', maxBE)
            entry["validate"] = "key"
            entry["validatecommand"] = vcmd
            entry.bind("<Return>", self.pcon.updatePoints)
            entry.bind("<KP_Enter>", self.pcon.updatePoints)
            entry.bind("<Tab>", self.pcon.updatePoints)
            entry.bind("<FocusOut>", self.pcon.updatePoints)



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
        self.con.unmarkEditNoChange(self.sel_id)
        # put focus back to the parent window
        self.master.focus_set()
        self.destroy()

    def validate(self):
        return True

    def apply(self):
        self.pcon.updatePoints()
        self.con.unmarkEditNoChange(self.sel_id)
        return True


#if __name__ == "__main__":
#    root = tk.Tk()
#    print(root.tk.call('info', 'patchlevel'))
#    style = ttk.Style(root)
 #   style.map('Treeview', foreground=fixed_map('foreground'),
 #    background=fixed_map('background'))
 #   Application(root).pack(fill="both", expand=True)
 #   root.mainloop()
