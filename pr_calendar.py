#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 13:26:29 2020

@author: mputzlocher
""" 

import tkinter as tk
from tkinter import ttk
import datetime

try:
    from tkcalendar import Calendar, DateEntry
except ImportError:
    print("tkcalendar not available")
    raise

class CalController():
    def __init__(self, app):
        self.app = app

    def update_events(self, event=None):
        selDate = self.app.dvar.get()
        selday = int(selDate[0:2])
        selmonth = int(selDate[3:5])
        selyear = int(selDate[6:])
        
        self.app.cal.selection_set(selDate)
        seldateObj = datetime.date(day=selday, month=selmonth, year=selyear)
        
        twoweekslater = datetime.timedelta(weeks=2)
        threeweekslater = datetime.timedelta(weeks=3)
        corr_deadline = seldateObj + twoweekslater
        re_deadline = seldateObj + threeweekslater
        
        #remove old events
        self.app.cal.calevent_remove("all")
        
        todayObj = datetime.date.today()
        
        self.app.cal.calevent_create(todayObj, "heute", "today")
        self.app.cal.calevent_create(seldateObj, "Prüfung", "exam")
        self.app.cal.calevent_create(corr_deadline, "Korrektur abgeschlossen", "deadline")
        self.app.cal.calevent_create(re_deadline, "Rückgabe abgeschlossen", "deadline")
        self.app.cal.tag_config("today", foreground="black", background="aquamarine")
        self.app.cal.tag_config("exam", foreground="white", background="red")
        self.app.cal.tag_config("deadline", foreground="black", background="yellow")
        #self.cal.see(seldateObj)
        #events = self.app.cal.get_calevents()
        #print(events)     
        
    def update_seldate(self, events=None):
        selDate = self.app.cal.selection_get()
        selDateString = selDate.strftime("%d.%m.%Y")
        self.app.dvar.set(selDateString)
        self.app.d.focus_set()
    

class DateFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.con = CalController(self)
        
        self.l = tk.Label(self, text="Hallo")
        self.l.grid(row=0, column=0, sticky="nwse")

        self.dstyle = ttk.Style()
        self.dstyle.configure('my.DateEntry',
                fieldbackground='light green',
                background='dark green',
                foreground='dark blue',
                arrowcolor='white')

        self.dvar = tk.StringVar()
        self.d = DateEntry(self, width=12, borderwidth=2, locale="de_DE",
                  date_pattern="dd.mm.y", textvariable=self.dvar, style="my.DateEntry")
        self.d.grid(row=1, column=0, sticky="nwse")

        self.cal = Calendar(self, font="Helvetica 10", selectmode='day', locale='de_DE',
                   cursor="hand1", date_pattern="dd.mm.y")
        self.cal.grid(row=2,column=0)

        self.d.bind("<Return>", self.con.update_events)
        self.d.bind("<KP_Enter>", self.con.update_events)
        self.d.bind("<Tab>", self.con.update_events)
        self.d.bind("<<DateEntrySelected>>", self.con.update_events)

        self.cal.bind("<<CalendarSelected>>", self.con.update_seldate)

if __name__ == "__main__":        
    prog = tk.Tk()
    DateFrame(prog).pack()
    prog.mainloop()