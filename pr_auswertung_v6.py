# Prüfungsauswertung
# Version 6
# 19.11.2019
# Martin Putzlocher
# CC-BY-SA 4.0, Namensnennung erforderlich, Weitergabe nur unter gleichen Bedingungen
# ----------------------------------------

import tkinter as tk
from tkinter import messagebox as tkm
from math import ceil

try:
    from pr_pdfwriter import Pdfw
    NOPDF = False
except:
    NOPDF = True
try:
    from pr_latexwriter import LatexW
    NOLATEX = False
except:
    NOLATEX = True

myfont = "Helvetica 14"
mygradefont = "Helvetica 40"
mylatexfont = ("C059", "10", "italic")

NotenBezeichnungen = {1: "sehr gut",
                      2: "gut",
                      3: "befriedigend",
                      4: "ausreichend",
                      5: "mangelhaft",
                      6: "ungenügend"}

#+++++++++++++++++++++++
# Model
#+++++++++++++++++++++++

class GradeKey():
    # +++ Verschiedene Notenschlüssel
    Mathe = [0.85, 0.7, 0.55, 0.4, 0.2, 0]
    MatheJT = [0.75, 0.6, 0.45, 0.333333, 0.166666, 0]
    DeutschJT = [0.85, 0.7, 0.6, 0.5, 0.333333, 0]
    EnglischJT = [0.9, 0.783333, 0.666666, 0.55, 0.333333, 0]
    Linear = [0.833333, 0.666666, 0.5, 0.333333, 0.166666, 0]
    
    def __init__(self):
        self.max = 40        # Maximalpunktzahl
        self.steps = []      # Liste zur Verwaltung der Notenstufen
        self.calc_steps()    # Berechnung der Notenstufen
        self.scaletype = 1    # Art des Notenschlüssels


    def change_scaletype(self, scaletype = 1):
        self.calc_steps(scaletype)
        self.scaletype = scaletype
        return 0
    
    def calc_steps(self, scaletype = 1):
        self.steps = []
        m = self.max
        
        if scaletype == 0: # Mathe und > / Abi alt
            diff = 1
            for i in range(6):
                limit = GradeKey.Mathe[i]
                if i != 5:
                    s = ceil(limit * m * 2 + diff) / 2
                else:
                    s = 0
                self.steps.append(s)
                
        elif scaletype == 1: # Mathe und >= / Abi neu
            for i in range(6):
                limit = GradeKey.Mathe[i]
                s = ceil(limit * m * 2) / 2
                self.steps.append(s)
                
        elif scaletype == 2: # Mathe Jahrgangsstufentest
            diff = 1
            for i in range(6):
                limit = GradeKey.MatheJT[i]
                if i != 5:
                    s = ceil(limit * m * 2 + diff) / 2
                else:
                    s = 0
                self.steps.append(s)
                
        elif scaletype == 3: # Deutsch Jahrgangsstufentest
            diff = 1
            for i in range(6):
                limit = GradeKey.DeutschJT[i]
                if i != 5:
                    s = ceil(limit * m * 2 + diff) / 2
                else:
                    s = 0
                self.steps.append(s)
            
        elif scaletype == 4: # Englisch Jahrgangsstufentest
            diff = 1
            for i in range(6):
                limit = GradeKey.EnglischJT[i]
                if i != 5:
                    s = ceil(limit * m * 2 + diff) / 2
                else:
                    s = 0
                self.steps.append(s)
            
        elif scaletype == 5: # Linear und >
            diff = 1
            for i in range(6):
                limit = GradeKey.Linear[i]
                if i != 5:
                    s = ceil(limit * m * 2 + diff) / 2
                else:
                    s = 0
                self.steps.append(s)
                
        elif scaletype == 6: # Linear und >=
            for i in range(6):
                limit = GradeKey.Linear[i]
                s = ceil(limit * m * 2) / 2
                self.steps.append(s)
        else:
            tkm.showerror("Falscher Wert",
                    "Keine Notenskale nicht neu berechnen.")

    def set_max(self, newmax):
        try:
            self.max = int(newmax)
        except:
            tkm.showerror("Falscher Wert",
                    "Maximalpunktzahl nicht lesbar.")
        # Neue Berechnung der Stufen
        self.calc_steps(self.scaletype)

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
    
#+++++++++++++++++++++++            
# Controller
#+++++++++++++++++++++++


class Controller():
    def __init__(self, app):
        self.app = app
        self.gk = GradeKey()
        self.exercises = Exercises(1)
        self.vali = PR_Validator(self)
    
    # Neue Maximalpunktzahl
    def set_max(self, event = None, maxBE = 0):
        try:
            if maxBE == 0:
                # Neues Max. auslesen
                newmax = int(self.app.exam.e_max.get())
            else:
                newmax = maxBE
                self.app.exam.e_max_value.set(str(newmax))
            
            # Schieberegler anpassen
            self.app.exam.scaler_achieved.config(from_ = newmax)
            
            # Stufen neu berechnen
            self.gk.set_max(newmax)
           
            # Update der Anzeige
            self.update_steps()
          
            # Nachverarbeiten der erreichten Punktzahl
            self.update_achieved_entry()
            
            # Überprüfen, ob Maximalwerte gleich
            self.check_max_values()
            
        except:
            tkm.showerror("Falscher Wert",
                    "Keine Zahl eingegeben.")
        
    # Setze Tendenz
    def set_td(self, event = None):
        self.update_achieved()
        
    def update_steps(self):
        for i in range(len(self.app.exam.step_labels)):
            label = self.app.exam.step_labels[i]
            label.config(text = str(self.gk.steps[i]))
            
    def update_achieved(self, event = None):
        scale = self.app.exam.scaler_achieved 
        v = scale.get()
        
        # Update Entry-Feld
        en = self.app.exam.e_achieved 
        en.delete(0,"end")
        en.insert(0,str(v))
        # Update
        self.update_achieved_rest(v)
    
    def raise_achieved_entry(self, event = None):
        en = self.app.exam.e_achieved
        try: 
            v = float(en.get())
            if v + 0.5 > self.gk.max:
                tkm.showerror("Falscher Wert",
                    "Eingegebener Wert ist zu groß.")
            else:
                v += 0.5
            en.delete(0,"end")
            en.insert(0,str(v))
        except:
            pass
        self.update_achieved_entry()
    
    def lower_achieved_entry(self, event = None):
        en = self.app.exam.e_achieved
        try: 
            v = float(en.get())
            if v - 0.5 < 0:
                tkm.showerror("Falscher Wert",
                    "Eingegebener Wert ist zu klein.")
            else:
                v -= 0.5
            en.delete(0,"end")
            en.insert(0,str(v))
        except:
            pass
        self.update_achieved_entry()
    
    def update_achieved_entry(self, event = None):
        en = self.app.exam.e_achieved
        try:
            v = float(en.get())
            
            if v > self.gk.max:
                tkm.showerror("Falscher Wert",
                    "Eingegebener Wert ist zu groß.")
                en.delete(0,"end")
                en.insert(0,str(self.gk.max))
                # Update Scale
                self.app.exam.scaler_achieved.set(self.gk.max)
                # Update 
                self.update_achieved_rest(self.gk.max)
            else:
                # Update Scale
                self.app.exam.scaler_achieved.set(v)
                # Update
                self.update_achieved_rest(v)
        except:
            tkm.showerror("Falscher Wert",
                    "Keine Zahl eingegeben.\n Erreichte Punkte.")
    
    def update_achieved_rest(self, value = -1):
        if value == -1:
            value = self.gk.max
        else:
            pass

        # Update Note
        self.update_grade(value)
        # Update Leinwand
        self.app.exam.draw_canvas(value)
        
    def update_grade(self, value):
        m = self.gk.max
        s = self.gk.steps
        
        v = value
        
        td = self.app.exam.tendency.get() # Tendenz an / aus ?
        tr = 1  # Bereich für Tendenz
        try:
            tr = float(self.app.exam.td_range.get())
        except:
            tkm.showerror("Fehler beim Lesen des Tendenzbereichs")
        
        grade = 1
        grade_num_str = str(grade)
        
        if v >= s[0]:
            grade = 1
            grade_num_str = str(grade)
            
            if td == 1:
                if v <= s[grade - 1] + tr:
                    grade_num_str = grade_num_str + "-"
                elif v >= m - tr:
                    grade_num_str = "+" + grade_num_str
                else:
                    pass
            else:
                pass
            
        
        elif v >= s[1]:
            grade = 2
            grade_num_str = str(grade)
            
            if td == 1:
                if v <= s[grade - 1] + tr:
                    grade_num_str = grade_num_str + "-"
                elif v >= s[grade - 2] - tr:
                    grade_num_str = "+" + grade_num_str
                else:
                    pass
            else:
                pass
                
        elif v >= s[2]:
            grade = 3
            grade_num_str = str(grade)
            
            if td == 1:
                if v <= s[grade - 1] + tr:
                    grade_num_str = grade_num_str + "-"
                elif v >= s[grade - 2] - tr:
                    grade_num_str = "+" + grade_num_str
                else:
                    pass
            else:
                pass
            
        elif v >= s[3]:
            grade = 4
            grade_num_str = str(grade)
            
            if td == 1:
                if v <= s[grade - 1] + tr:
                    grade_num_str = grade_num_str + "-"
                elif v >= s[grade - 2] - tr:
                    grade_num_str = "+" + grade_num_str
                else:
                    pass
            else:
                pass
                
        elif v >= s[4]:
            grade = 5
            grade_num_str = str(grade)
            
            if td == 1:
                if v <= s[grade - 1] + tr:
                    grade_num_str = grade_num_str + "-"
                elif v >= s[grade - 2] - tr:
                    grade_num_str = "+" + grade_num_str
                else:
                    pass
            else:
                pass
                    
        else:
            grade = 6
            grade_num_str = str(grade)
            
            if td == 1:
                if v <= s[grade - 1] + tr:
                    grade_num_str = grade_num_str + "-"
                elif v >= s[grade - 2] - tr:
                    grade_num_str = "+" + grade_num_str
                else:
                    pass
            else:
                pass
        
        self.update_view_grade(grade, grade_num_str)
    
    def update_view_grade(self, grade, grade_num_str):
        sca = self.app.exam.scaler_achieved 
        g   = self.app.exam.grade
        gn  = self.app.exam.grade_number
        ls  = self.app.exam.step_labels
        
        # Note als Zahl
        gn.config(text=grade_num_str)
        
        # Farbe auslesen
        the_color = ls[grade-1].cget("background")
        
        # Bezeichnung
        g.config(text=NotenBezeichnungen[grade], fg = "black", 
                 bg = the_color)
        # Hintergrundfarbe des Schiebereglers
        sca.config(troughcolor = the_color)
    
    # Ändern des Notenschlüssels
    def change_scaletype(self, ev=None):
        st = self.app.exam.scaletype # Verbinden mit Listbox
        t = 1
        try:
            t = int(st.curselection()[0]) # Auslesen der aktuellen Auswahl
            # --- Änderung am Notenschlüssel ---
            self.gk.change_scaletype(t)
            # --- Update aller Einträge und Anzeigen --- 
            self.update_steps()
            self.update_achieved_entry()
            
        except:
            tkm.showerror("Fehler beim Lesen des Notenschlüssels")
            
        else:
            st.activate(t) # Aktivieren des entsprechenden Feldes der GUI
    
    def create_pdf(self, ev=None):
        title = self.app.exam.e_title.get()
        doc = Pdfw(title)
        doc.writePDF(self.gk.max, self.gk.steps)
        
    def create_latex(self, ev=None):
        title = self.app.exam.e_title.get()
        theClass = self.app.exam.e_class.get()
        theDate = self.app.exam.e_date.get()
        if self.exercises.max == self.gk.max:
            exercises = self.exercises.exercises
            doc = LatexW(self.gk.max, self.gk.steps, title=title, the_class = theClass, the_date = theDate, the_ex = exercises)
        else:
            doc = LatexW(self.gk.max, self.gk.steps, title=title, the_class = theClass, the_date = theDate)
        
    def message(self, ev=None):
        tkm.showinfo("Hallo","Hallo!")
        
    def update_ex_number(self, ev=None):
        n = self.app.exer.sb_exercise_number.get()
#        try:
#            n = int(n)
#            self.app.exer.change_entry_widgets(n)
#            print("Anzahl Aufgaben auf {} geändert".format(n))
#        except:
#            tkm.showerror("Keine Zahl angegeben.")
#        else:
#            pass

        n = int(n)
        self.exercises.set_number(n)
        self.app.exer.change_entry_widgets(n)
        self.app.exer.set_max(self.exercises.max)
        self.check_max_values()
        print("Anzahl Aufgaben auf {} geändert".format(n))
    
    def update_ex_points(self, ev=None):
        ex_names = self.app.exer.entries_ex_values
        ex_points = self.app.exer.entries_p_values
        
        namelist = [entry.get() for entry in ex_names]
        pointslist = [entry.get() for entry in ex_points]
# debugging
        print("Hier die neuen Listen:")
        print(namelist)
        print(pointslist)
        
        self.exercises.fill(listOfNames=namelist, listOfPoints=pointslist)
        self.app.exer.set_max(self.exercises.max)
        self.check_max_values()
    
    def check_max_values(self, ev=None):
        if self.exercises.max == self.gk.max:
            self.app.exer.e_all_points.config(disabledbackground="lightgreen")
        else:
            self.app.exer.e_all_points.config(disabledbackground="yellow")

#+++++++++++++++++++++++
# Validator
#+++++++++++++++++++++++
class PR_Validator():
    def __init__(self, controller):
        self.con = controller
        
    def validateBE(self, P):
        if len(P) > 0:
            try:
                inval = float(P)
                if int(inval*2) == inval*2:
                    return True
                else:
                    print("Endet nicht auf .5 oder .0")
                    return False
            except ValueError:
                print("Fehler bei Eingabe, gelesen: {}".format(P))
                return False
        else:
            return True
    
    def validateInt(self, P):
        if P.isdigit():
            return True
        else:
            return False
        
    def validateExNames(self, P):
        nameslist = self.con.exercises.names
        if nameslist.count(P) >= 2:
            tkm.showerror("Eingabefehler", "Name schon vergeben!")
            return False
        else:
            return True
    
#+++++++++++++++++++++++
# View
#+++++++++++++++++++++++

class PR_ExamConfig(tk.Frame):
    def __init__(self, controller, master=None):
        super().__init__(master)
        self.pack()
        
        self.con = controller
        self.create_widgets()
        
        self.activate_controller()
        self.set_focus()
        
    def activate_controller(self): # Bindings
        # Maximalpunktzahl
        self.e_max.bind("<Return>", self.con.set_max)
        self.b_max["command"] =     self.con.set_max
        
        # Tendenz an / aus
        self.td.bind("<KeyRelease-space>", self.con.set_td)
        self.td.bind("<Return>",           self.con.set_td)
        self.td.bind("<ButtonRelease-1>",  self.con.set_td)
        self.td_range.bind("<Return>",     self.con.set_td)
        
        # Erreichte Punktzahl über Schieberegler
        self.scaler_achieved.bind("<ButtonRelease-1>",  self.con.update_achieved)
        self.scaler_achieved.bind("<ButtonRelease-3>",  self.con.update_achieved)
        self.scaler_achieved.bind("<KeyRelease-Left>",  self.con.update_achieved)
        self.scaler_achieved.bind("<KeyRelease-Right>", self.con.update_achieved)
        self.scaler_achieved.bind("<KeyRelease-Up>",    self.con.update_achieved)
        self.scaler_achieved.bind("<KeyRelease-Down>",  self.con.update_achieved)
        
        # Erreichte Punktzahl über Eingabefeld
        self.e_achieved.bind("<Return>", self.con.update_achieved_entry)
        self.e_achieved.bind("<Up>",     self.con.raise_achieved_entry)
        self.e_achieved.bind("<Down>",   self.con.lower_achieved_entry)
        
        # Art des Notenschlüssels über ListBox
        self.scaletype.bind("<ButtonRelease-1>", self.con.change_scaletype)
        #self.scaletype.bind("<ButtonRelease-3>", self.con.change_scaletype)
        self.scaletype.bind("<KeyRelease-space>", self.con.change_scaletype)
        self.scaletype.bind("<KeyRelease-Return>", self.con.change_scaletype)
        
        # PDF erstellen
        self.b_pdf["command"] = self.con.create_pdf
        
        # LaTeX und PDF erstellen
        self.b_latex["command"] = self.con.create_latex
    
    def draw_canvas(self, value = 0):
        c  = self.cv             # Leinwand
       # gn = self.grade_number   # Note als Zahl
        m  = self.con.gk.max     # Maximalpunktzahl
        s  = self.con.gk.steps   # Liste der Schritte
        v  = value
        t  = self.tendency.get()
        tr = float(self.td_range.get())
        sca = self.scaler_achieved
        
        h = int(c.cget("height"))
        w = int(c.cget("width"))
        
        y_unit = h//m
        
        # Canvas aufräumen
        c.delete("all")
        # Mittellinie
        c.create_line(w//2, h, w//2, 0, fill = "gray")
        
        # Höhen der Stufen
        h1 = h - y_unit * s[0]
        h2 = h - y_unit * s[1]
        h3 = h - y_unit * s[2]
        h4 = h - y_unit * s[3]
        h5 = h - y_unit * s[4]
        h6 = h - y_unit * s[5]
        heights = [h1,h2,h3,h4,h5,h6]
        for hn in heights:
            c.create_line(0, hn, w, hn, fill="red")
        
        # Tendenz-Linien
        if t == 1:    
            td_heights = list()
            for step in s:
                td_h_up   = h - y_unit * (step + tr)
                td_h_down = h - y_unit * (step - tr)
                td_heights.append(td_h_up)
                td_heights.append(td_h_down)
            for thn in td_heights:
                c.create_line(0, thn, w, thn, fill="magenta", dash=(3, 2))
        else:
            pass
        
        # Maximal-Höhe anpassen
        hmax = h - y_unit * m
        # Hintergrund anpassen
        c.create_line(0, hmax, w , hmax, fill="green")
        c.create_rectangle(0, 0, w, hmax, fill="gray")
        
        # Beschriftung der Bereiche
        c.create_text(w // 4, (hmax + h1) // 2, text = "1")
        c.create_text(w // 4, (h1 + h2) // 2, text = "2")
        c.create_text(w // 4, (h2 + h3) // 2, text = "3")
        c.create_text(w // 4, (h3 + h4) // 2, text = "4")
        c.create_text(w // 4, (h4 + h5) // 2, text = "5")
        c.create_text(w // 4, (h5 + h6) // 2, text = "6")
        
        hv = h - y_unit * v
        radius = 3
        color = sca.cget("troughcolor")
        spot = c.create_oval(w//2 - radius, hv - radius, w//2 + radius, hv + radius, fill = color)
        spotline = c.create_line(w//2 - 3*radius, hv, w//2 + 3*radius, hv)
    
    def create_widgets(self):
        # Label für Eingabefeld: Maximalpunktzahl
        self.l_max = tk.Label(self, text = "Maximalpunktzahl: ")
        self.l_max.grid(row = 0, column = 0)
        
        # Eingabefeld: Maximalpunktzahl
        self.e_max_value = tk.StringVar()
        self.e_max = tk.Entry(self, width = 10, textvariable=self.e_max_value, justify = "center",
            relief = "flat")
        self.e_max_value.set(str(40)) # Anfangswert: 40
        self.e_max.grid(row = 0, column = 1)
        
        # Button zur Bestätigung der Eingabe
        self.b_max = tk.Button(self, text="Setze Max.")
        self.b_max.grid(row = 0, column = 2)
        self.b_max.config(takefocus = False)

        # Labels für Notenstufen l_1 bis l_6
        self.grade_labels =[]
        
        for i in range(1,7,1):
            l = tk.Label(self, text = NotenBezeichnungen[i], font=myfont)
            l.config(background = "#" + str(hex(i *255//6))[2:] +
                str(hex((7-i)*255//6))[2:] + "a0")
            l.grid(row = i, column = 0, ipady = 10, sticky="nswe")
            self.grade_labels.append(l)
        
        ## Anzeige der Mindestpunktzahlen
        # Labels werden in Liste verwaltet
        self.step_labels = []
        
        for i in range(6):
            sl = tk.Label(self, text = self.con.gk.steps[i], font=myfont)
            # Anpassen der Farbe
            sl.config(background = "#" + str(hex((i+1)*255//6))[2:] +
                str(hex((6-i)*255//6))[2:] + "a0")
            sl.grid(row = i+1, column = 1, pady = 10, padx = 5, sticky = "we")
            self.step_labels.append(sl)

        # Eingabefeld für erreichte Punktzahl
        self.e_achieved = tk.Entry(self, width = 10, justify = "center")
        self.e_achieved.insert(0,str(0))
        self.e_achieved.grid(row = 1, column = 3)
        
        # Schieberegler für erreichte Punktzahl
        self.scaler_achieved = tk.Scale(self, from_ = self.con.gk.max, to = 0, orient = "vertical", resolution = 0.5, length = 200)
        self.scaler_achieved.grid(row = 2, column = 3, rowspan = 5)
        self.scaler_achieved.config(takefocus = True, troughcolor = "blue")
        self.scaler_achieved.config(cursor = "mouse")
        
        # Tendenz: ja / nein
        self.tendency = tk.IntVar()
        self.td = tk.Checkbutton(self, text="Tendenzbereich: ", var = self.tendency, onvalue=1, offvalue=0)
        self.td.grid(row = 0, column = 4, sticky = "we")
        self.td.config(cursor = "trek")
        
        # Eingabefeld: Reichweite der Tendenz
        self.td_range = tk.Entry(self, width = 5, justify = "center",
            relief = "flat")
        self.td_range.insert(0,1)
        self.td_range.grid(row = 0, column = 5, sticky = "we")
        
        ## Notenanzeige
        
        # Anzeige der Note als Text
        self.grade = tk.Label(self, text="sehr gut", font= "Times 12", fg = "green", width = 20)
        self.grade.grid(row = 2, column = 4, columnspan = 2, sticky="we")
        
        # Anzeige der Note als Zahl
        self.grade_number = tk.Label(self, text = "6", font = mygradefont, cursor = "shuttle")
        self.grade_number.grid(row = 3, column = 4, rowspan = 3, columnspan = 2, sticky="we")
        
        # Leinwand für grafische Anzeige der Punktgrenzen
        self.cv = tk.Canvas(self, width=100, height=300, bg = "white", cursor = "cross")
        self.cv.grid(row = 1, column = 2, rowspan = 6)
        
        ## Festlegung des Notenschlüssels / Skalentyps
        
        # Labelframe mit Beschriftung für Skalentypauswahl
        self.lf_scaletype = tk.LabelFrame(self, text="Notenschlüssel")
        self.lf_scaletype.grid(row=7, column = 0, columnspan = 2, sticky = "nswe")
        
        # Auswahl des Skalentyps
        self.scaletype = tk.Listbox(self.lf_scaletype, selectmode = "SINGLE", height = 7, width=25, highlightcolor = "red", selectbackground = "yellow", exportselection=False)
        self.scaletype.insert(0, "Mathe-Abitur alt")
        self.scaletype.insert(1, "Mathe-Abitur ab 2019")
        self.scaletype.insert(2, "Mathe-Jahrgangsstufentest")
        self.scaletype.insert(3, "Deutsch-Jahrgangsstufentest")
        self.scaletype.insert(4, "Englisch-Jahrgangsstufentest")
        self.scaletype.insert(5, "Linear >")
        self.scaletype.insert(6, "Linear >=")
        
        self.scaletype.grid(row=0, column = 0, sticky = "nswe")
        
        # Erstes Element wird sichtbar
        self.scaletype.see(0)
        
        # Element mit Nummer 1 wird ausgewählt
        self.scaletype.selection_set(1)
        self.scaletype.selection_anchor(1)
        self.scaletype.activate(1)
        
               
        ## Frame für Buttons
        self.f_buttons = tk.Frame(self, colormap="new")
        self.f_buttons.grid(row=7, column=3, columnspan = 3, sticky = "se")
        
        ## Labelframe: Dokumententitel
        self.lf_title = tk.LabelFrame(self.f_buttons, text="Dokumententitel")
        self.lf_title.grid(row=0, column=0, columnspan=3, sticky = "we")
        
        ## Eingabefeld: Dokumententitel
        self.e_title = tk.Entry(self.lf_title, width = 25, text="Titel")
        self.e_title.grid(row=0, column=0, sticky = "nswe")
        
        ## Labelframe: Datum
        self.lf_date = tk.LabelFrame(self.f_buttons, text="Datum der Prüfung")
        self.lf_date.grid(row=1, column=0, columnspan=3, sticky = "we")
        
        ## Eingabefeld: Datum
        self.e_date = tk.Entry(self.lf_date, width = 25, text="Datum")
        self.e_date.grid(row=0, column=0, sticky = "nswe")
        
        ## Labelframe: Klasse
        self.lf_class = tk.LabelFrame(self.f_buttons, text="Klasse")
        self.lf_class.grid(row=2, column=0, columnspan=3, sticky = "we")
        
        ## Eingabefeld: Klasse
        self.e_class = tk.Entry(self.lf_class, width = 25, text="5a")
        self.e_class.grid(row=0, column=0, sticky = "nswe")
       
        ## PDF-Button
        self.b_pdf = tk.Button(self.f_buttons, text="PDF", fg="blue")
        self.b_pdf.grid(row=3, column = 0, sticky = "se")
        if NOPDF:
            self.b_pdf.config(state=tk.DISABLED)
            tkm.showwarning("PDF-Writer",
                    "PDF-Ausgabe nicht verfügbar.")
        else:
            pass
        
        ## LaTeX-Button
        self.b_latex = tk.Button(self.f_buttons, text="LaTeX", fg="blue", font= mylatexfont)
        self.b_latex.grid(row=3, column = 1, sticky = "se")
        if NOLATEX:
            self.b_latex.config(state=tk.DISABLED)
            tkm.showwarning("LaTeX-Writer",
                    "LaTeX-Ausgabe nicht verfürbar.")
        else:
            pass
        
        ## Exit-Button
     #   self.quit = tk.Button(self.f_buttons, text="Beenden", fg="red",
     #                        command=root.destroy)
     #  self.quit.grid(row=3, column = 2, sticky = "se")
    
    # Setzen des aktiven Elements in der grafischen Oberfläche
    def set_focus(self):
        # Eingabefeld für Maximalpunktzahl erhält Fokus
        self.e_max.focus()

class PR_Exercises(tk.Frame):
    def __init__(self, controller, master=None):
        super().__init__(master)
        self.pack()
        
        self.entries_ex = list() # Liste der Aufgabenbezeichnungs-Entries
        self.entries_ex_values = list()
        self.entries_p = list()  # Liste der BE-Entries
        self.entries_p_values = list()
        
        self.con = controller    # Bezug zum Controller
        self.create_widgets()    # Erstellung der Widgets im Frame
        
        self.activate_controller() # Controller an Ereignisse binden
        #self.set_focus()
    
    def create_widgets(self):
        # Titel
        self.exercise_title = tk.Label(self, text="Aufgabenerfassung", font=myfont)
        self.exercise_title.grid(row=0, column = 0, sticky = "nwe")
    
        # Anzahl der Aufgaben
        # Frame
        self.f_exercise_number = tk.Frame(self, bd=2)#, relief=tk.SUNKEN)
        self.f_exercise_number.grid(row=1, column=0, sticky="nswe")
        self.l_exercise_number = tk.Label(self.f_exercise_number, text="Aufgabenanzahl:")
        self.l_exercise_number.grid(row=0, column=0)
        self.sb_exercise_number = tk.Spinbox(self.f_exercise_number, from_=1, to=20, width=4, justify=tk.CENTER)
        self.sb_exercise_number.grid(row=0, column=1)
        self.b_exercise_number = tk.Button(self.f_exercise_number, text="setze")
        self.b_exercise_number.grid(row=0, column=2)
        
        # LabelFrame: Eingabe
        self.lf_exercise_details = tk.LabelFrame(self, text="Aufgabendetails", cursor="trek",)
        self.lf_exercise_details.grid(row=2, column=0, sticky="nswe")
        # Frame: Beschriftungen
        self.f_exercise_details_labels = tk.Frame(self.lf_exercise_details)
        self.f_exercise_details_labels.grid(row=0, column=0)
        # Aufgabeneingabe
        self.l_exercises = tk.Label(self.f_exercise_details_labels, text="Aufgabenbezeichnung")
        self.l_exercises.grid(row=0, column=0)
        self.l_exercises_points = tk.Label(self.f_exercise_details_labels, text="Errechbare BE")
        self.l_exercises_points.grid(row=1, column=0)
        
        # Frame: Eingabe
        self.f_exercise_details_entries = tk.Frame(self.lf_exercise_details, relief=tk.SUNKEN, bd=2, highlightcolor="blue" )
        self.f_exercise_details_entries.grid(row=0, column=1)
        entries_f = self.f_exercise_details_entries
        
        # Zwei Eingabefelder
        ex1 = tk.StringVar()
        nameEntry = tk.Entry(entries_f, textvariable=ex1, width=3, bg="yellow", relief=tk.FLAT, bd=2, highlightcolor="blue")
        nameEntry.grid(row=0, column=0)
        ex1.set("1")
        self.entries_ex.append(nameEntry)
        self.entries_ex_values.append(ex1)
        
        
        ex1_p = tk.IntVar()
        pointsEntry = tk.Entry(entries_f, textvariable=ex1_p, width=3, bg="white", justify=tk.RIGHT, relief=tk.FLAT, bd=2, highlightcolor="blue")
        pointsEntry.grid(row=1, column=0) 
        ex1_p.set(1)
        self.entries_p.append(pointsEntry)
        self.entries_p_values.append(ex1_p)
        
        
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
        n = len(self.entries_ex) 
        
        if n < number:
            # Widgets müssen hinzugefügt werden
            d = number - n
            for i in range(d):
                ex = tk.StringVar()
                nameEntry = tk.Entry(entries_f, textvariable=ex, width=3, bg="yellow", relief=tk.FLAT, bd=2, highlightcolor="blue")
                nameEntry.grid(row=0, column=n+i)
                ex.set(str(n+i+1))
                self.entries_ex.append(nameEntry)
                self.entries_ex_values.append(ex)
                
                ex_p = tk.IntVar()
                pointsEntry = tk.Entry(entries_f, textvariable=ex_p, width=3, bg="white", justify=tk.RIGHT, relief=tk.FLAT, bd=2, highlightcolor="blue")
                pointsEntry.grid(row=1, column=n+i) 
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
            entry.bind("<Tab>", self.con.update_ex_points)
            entry.bind("<FocusOut>", self.con.update_ex_points)
        
        for entry in self.entries_ex:
            vcmd = (entry.register(self.con.vali.validateExNames), '%P')
            entry["validate"]="focusout"
            entry["validatecommand"]=vcmd
            entry.bind("<Return>", self.con.update_ex_points)
            entry.bind("<Tab>", self.con.update_ex_points)
            entry.bind("<FocusOut>", self.con.update_ex_points)
        
    def set_max(self, max_points):
        self.max_points.set(str(max_points))
        

class MainWindow(tk.PanedWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = Controller(self)
        self.config(sashrelief=tk.RAISED)
        self.create_parts()
        self.create_menubar(master)
        self.pack(fill=tk.BOTH, expand=1)
    
    def create_parts(self):
        self.exam = PR_ExamConfig(self.controller, master=self)
        self.add(self.exam)
        self.paneconfigure(self.exam, sticky="nw", minsize=550)
        
        # rechte Hälfte
        self.right = tk.PanedWindow(self,orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self.add(self.right)
        self.paneconfigure(self.right)
        
        self.exer = PR_Exercises(self.controller, master=self)
        self.right.add(self.exer)
        self.right.paneconfigure(self.exer, sticky="nw", minsize=150)
        
        pupils_title = tk.Label(self, text="Schülererfassung")
        self.right.add(pupils_title)
        
    def create_menubar(self, master):
        self.menubar = tk.Menu(self)
        self.menubar.config(activebackground="darkgrey", activeforeground="white")
        #self.menubar.add_command(label="Hallo!", command=self.controller.message)
        
        self.export_menu = tk.Menu(self.menubar, tearoff=0)
        # PDF erstellen
        self.export_menu.add_command(label="Export in PDF", foreground="blue", command = self.controller.create_pdf)
        # LaTeX und PDF erstellen
        self.export_menu.add_command(label="Export in LaTeX + PDF", foreground="blue", command = self.controller.create_latex)
        self.menubar.add_cascade(label="Export", menu=self.export_menu)
        
        self.menubar.add_separator()
        self.menubar.add_command(label="Beenden", foreground="red", command=root.destroy)
        master.config(menu=self.menubar)

## +++++++++++++++
# Ausführung
## +++++++++++++++
root = tk.Tk()

app = MainWindow(master=root)
app.mainloop()

#exam = PR_ExamConfig(master=root)
#exam.mainloop()

