#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 10:19:09 2019

@author: mputzlocher
"""

import tkinter as tk
#import tkinter.ttk as ttk
#from tkinter import messagebox as tkm

myfont = "Helvetica 14"
mygradefont = "Helvetica 40"
mylatexfont = ("C059", "10", "italic")

class Exercises():
    def __init__(self, number):
        self.names = list()  # Strings
        self.points = list() # floats
        self.exercises = dict(zip(self.names, self.points))
        self.number = number # Anzahl der Aufgaben
        self.set_number(self.number)
        self.max = 0
        self.print_ex()
    
    def fill(self, listOfNames, listOfPoints):
        self.names = listOfNames
        self.points = listOfPoints # floats!
        self.update_dict()
        self.update_max()
        
    def set_points(self, num, points):
        self.points[num-1] = points
        self.update_max()
        self.update_dict()
    
    def get_points(self, num):
        return self.points[num-1]
    
    def set_name(self, num, name):
        self.names[num-1] = name
        self.update_dict()
    
    def get_name(self, num):
        return self.names[num-1]
        
    def update_max(self):
        self.max = sum(self.points)
        
    def get_max(self):
        return self.max
    
    def update_dict(self):
        self.exercises = dict(zip(self.names, self.points))
    
    def set_number(self, number):
        self.number = number
        # Listen verlängern / kürzen
        l1 = len(self.names)
        if l1 > self.number:
            self.names = self.names[0:number] 
        elif l1 < self.number:
            for __ in range(self.number-l1):
                entry = str(number)
                self.names.append(entry)
        else:
            pass
        l2 = len(self.points)
        if l2 > self.number:
            self.points = self.points[0:number] 
        elif l2 < self.number:
            for __ in range(self.number-l2):
                entry = 1
                self.points.append(entry)
        else:
            pass
        
        self.update_max()
        self.update_dict()
        self.print_ex()

    def get_number(self):
        return self.number
        
    def print_ex(self):
        print(self.exercises)

class PR_Exercises(tk.Frame):
    def __init__(self, controller, master=None):
        super().__init__(master)
        
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        
        self.grid(row=0, column=0, sticky="nwe")
        
        #self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
           
        self.entries_ex = list() # Liste der Aufgabenbezeichnungs-Entries
        self.entries_ex_values = list()
        self.entries_p = list()  # Liste der BE-Entries
        self.entries_p_values = list()
        self.entries_percents = list() # Liste der Prozentangaben-Labels
        self.entries_percents_values = list()
        
        self.con = controller    # Bezug zum Controller
        self.create_widgets()    # Erstellung der Widgets im Frame
        
        self.activate_controller() # Controller an Ereignisse binden
        #self.set_focus()
    
    def create_widgets(self):
        # Titel
        
        self.exercise_title = tk.Label(self, text="Aufgabenerfassung", font=myfont)
        self.exercise_title.grid(row=0, column = 0, sticky = "nw")
    
        # Anzahl der Aufgaben
        # Frame
        self.f_exercise_number = tk.Frame(self, bd=2)#, relief=tk.SUNKEN)
        self.f_exercise_number.grid(row=1, column=0, sticky="nw")
        self.l_exercise_number = tk.Label(self.f_exercise_number, text="Aufgabenanzahl:")
        self.l_exercise_number.grid(row=0, column=0)
        self.sb_exercise_number = tk.Spinbox(self.f_exercise_number, from_=1, to=20, width=4, justify=tk.CENTER)
        self.sb_exercise_number.grid(row=0, column=1)
        self.b_exercise_number = tk.Button(self.f_exercise_number, text="setze")
        self.b_exercise_number.grid(row=0, column=2)
        
        # LabelFrame: Eingabe
        self.lf_exercise_details = tk.LabelFrame(self, text="Aufgabendetails", cursor="trek")
        self.lf_exercise_details.grid(row=2, column=0, sticky="nwe")
        
        self.lf_exercise_details.columnconfigure(1, weight=1) # Spalte der Canvas
        
        # Frame: Beschriftungen
        self.f_exercise_details_labels = tk.Frame(self.lf_exercise_details)
        self.f_exercise_details_labels.grid(row=0, column=0, sticky="nw")
        
        # Aufgabeneingabe
        # Zeilenbschriftungen
        self.l_exercises = tk.Label(self.f_exercise_details_labels, text="Aufgabenbezeichnung")
        self.l_exercises.configure(pady=3)
        self.l_exercises.grid(row=0, column=0, sticky="nw")
        self.l_exercises_points = tk.Label(self.f_exercise_details_labels, text="Errechbare BE")
        self.l_exercises_points.configure(pady=3)
        self.l_exercises_points.grid(row=1, column=0, sticky="nw")
        
        # Frame für Platzieren der Canvas
        self.f_exercises_forCanvas = tk.Frame(self.lf_exercise_details, bg="white")
        self.f_exercises_forCanvas.grid(row=0, column=1, sticky="we")
        self.f_exercises_forCanvas.columnconfigure(0, weight=1)
        frame_around_canvas = self.f_exercises_forCanvas
        
        # Canvas for Scrolling
        self.c_exercises = tk.Canvas(self.f_exercises_forCanvas, relief=tk.SUNKEN, bd=2, highlightcolor="blue", bg="bisque")
        self.c_exercises.configure(height=60)
        self.c_exercises.grid(row=0, column=0, sticky="we")
        canvas = self.c_exercises
        
        #canvas.columnconfigure(0, weight=1)
        
        # Frame: Eingabe
        self.f_exercise_details_entries = tk.Frame(self.c_exercises, relief=tk.FLAT, bd=1, highlightcolor="blue", bg="bisque" )
        self.f_exercise_details_entries.grid(row=0, column=0, sticky="nswe")
        entries_f = self.f_exercise_details_entries
        # Window on Canvas for Entry-Fields
        self.w_entries = canvas.create_window((0,0), window=entries_f, anchor="nw", height=50)
        
        # Zwei Eingabefelder
        # Aufgabeneingabe
        ex1 = tk.StringVar()
        nameEntry = tk.Entry(entries_f, textvariable=ex1, width=3, bg="yellow", relief=tk.FLAT, bd=2, highlightcolor="blue")
        nameEntry.grid(row=0, column=0, sticky="w")
        ex1.set("1")
        self.entries_ex.append(nameEntry)
        self.entries_ex_values.append(ex1)
        
        # Punkteeingabe
        ex1_p = tk.IntVar()
        pointsEntry = tk.Entry(entries_f, textvariable=ex1_p, width=3, bg="white", justify=tk.RIGHT, relief=tk.FLAT, bd=2, highlightcolor="blue")
        pointsEntry.grid(row=1, column=0, sticky="w")
        ex1_p.set(1)
        self.entries_p.append(pointsEntry)
        self.entries_p_values.append(ex1_p)
        
              
        # Frame for Scrollbar
        self.f_exercises_cBottomFrame = tk.Frame(frame_around_canvas)
        self.f_exercises_cBottomFrame.grid(row=1, column=0, sticky="we")
        self.f_exercises_cBottomFrame.columnconfigure(0, weight=1)
        
        # Horizontal Scrollbar
        self.scrbar_exercises = tk.Scrollbar(self.f_exercises_cBottomFrame, orient=tk.HORIZONTAL, command=canvas.xview)
        self.scrbar_exercises.grid(row=0, column=0, sticky="ew")

        canvas.configure(scrollregion=canvas.bbox(tk.ALL),xscrollcommand=self.scrbar_exercises.set)
        
        
        # Berechnete Gesamtpunktzahl
        # Frame
        self.f_all_points = tk.Frame(self, bd=2)#, relief=tk.SUNKEN)
        self.f_all_points.grid(row=3, column=0, sticky="nswe")
        self.l_all_points = tk.Label(self.f_all_points, text="Gesamtpunktzahl:")
        self.l_all_points.grid(row=0, column=0)
        self.max_points = tk.StringVar()
        self.e_all_points = tk.Entry(self.f_all_points, textvariable=self.max_points, width=4, justify=tk.CENTER, relief=tk.FLAT)
        self.e_all_points.configure(state=tk.DISABLED, takefocus="NO", disabledforeground = "black", disabledbackground = "yellow")
        self.e_all_points.grid(row=0, column=1)
        self.b_all_points = tk.Button(self.f_all_points, text="Übernehmen")
        self.b_all_points.grid(row=0, column=2)
        
    def change_entry_widgets(self, number):
        entries_f = self.f_exercise_details_entries
        canvas = self.c_exercises
        n = len(self.entries_ex) 
        
        if n < number:
            # Widgets müssen hinzugefügt werden
            # Anzahl der neuen
            d = number - n
            for i in range(d):
                ex = tk.StringVar()
                nameEntry = tk.Entry(entries_f, textvariable=ex, width=3, bg="yellow", relief=tk.FLAT, bd=2, highlightcolor="blue")
                nameEntry.grid(row=0, column=n+i, sticky=tk.W)
                ex.set(str(n+i+1))
                self.entries_ex.append(nameEntry)
                self.entries_ex_values.append(ex)
                
                ex_p = tk.IntVar()
                pointsEntry = tk.Entry(entries_f, textvariable=ex_p, width=3, bg="white", justify=tk.RIGHT, relief=tk.FLAT, bd=2, highlightcolor="blue")
                pointsEntry.grid(row=1, column=n+i, sticky=tk.W) 
                ex_p.set(1)
                self.entries_p.append(pointsEntry)
                self.entries_p_values.append(ex_p)
        elif n > number:
            # Widgets müssen entfernt werden
            while n > number:
                last = self.entries_ex.pop()
                last.destroy()
                del(last)
                last = self.entries_p.pop()
                last.destroy()
                del(last)
                last = self.entries_ex_values.pop()
                del(last)
                last = self.entries_p_values.pop()
                del(last)
                n = len(self.entries_ex)
        else: # n == number
            pass # Do nothing
        
        # test
        canvas.update_idletasks()
        
        # Anpassen der Scrollbar
        self.print_cv_info()
        theBbox = canvas.bbox("all")

        canvas.configure(scrollregion=theBbox)
        
        # Alle Eingabefelder aktivieren    
        self.activate_controller_on_entries()
    
    def activate_controller(self):
       # self.sb_exercise_number.bind("<Button-1>",  self.con.update_ex_number)
        self.sb_exercise_number.bind("<KeyRelease-Up>",    self.con.update_ex_number)
        self.sb_exercise_number.bind("<KeyRelease-Down>",  self.con.update_ex_number)
        self.sb_exercise_number["command"] = self.con.update_ex_number
        self.b_exercise_number["command"] = self.con.update_ex_number
        self.b_all_points["command"] = lambda: self.con.set_max(maxBE=self.con.exercises.get_max())
        
        self.activate_controller_on_entries()
        
    def activate_controller_on_entries(self):
        for entry in self.entries_p:
            vcmd = (entry.register(self.con.vali.validateBE), '%P')
            entry["validate"]="key"
            entry["validatecommand"]=vcmd
            entry.bind("<Return>", self.con.update_ex_points)
            entry.bind("<KP_Enter>", self.con.update_ex_points)
            entry.bind("<Tab>", self.con.update_ex_points)
            entry.bind("<FocusOut>", self.con.update_ex_points)
        
        for entry in self.entries_ex:
            vcmd = (entry.register(self.con.vali.validateExNames), '%P')
            entry["validate"]="focusout"
            entry["validatecommand"]=vcmd
            entry.bind("<Return>", self.con.update_ex_points)
            entry.bind("<KP_Enter>", self.con.update_ex_points)
            entry.bind("<Tab>", self.con.update_ex_points)
            entry.bind("<FocusOut>", self.con.update_ex_points)
        
    def set_max(self, max_points):
        self.max_points.set(str(max_points))
        
    def print_cv_info(self):
        cv = self.c_exercises
        print("Entries-Frame:BBox {}".format(cv.bbox(tk.ALL)))
        print("Entries-Frame:Width {}".format(cv.winfo_width()))
        
        first = self.entries_ex[0]
        last = self.entries_ex[-1]
        print("First Entry:Width {}".format(first.winfo_width()))
        print("First Entry:Height {}".format(first.winfo_height()))
        print("Last  Entry:Width {}".format(last.winfo_width()))