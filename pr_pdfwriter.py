# Prüfungsauswertung
# Version 5
# 13.11.2019
# Martin Putzlocher
# CC-BY-SA 4.0, Namensnennung erforderlich, Weitergabe nur unter gleichen Bedingungen
# ----------------------------------------

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

class Pdfw():
    def __init__(self, title = "Notenstufen"):
        self.title = title
        self.my_filename = title.strip().replace(" ","_").replace(".","").lower() + ".pdf"
        self.c = canvas.Canvas(self.my_filename, pagesize=A4)
        self.pwidth, self.pheight = A4
        self.c.setLineWidth(.3)
        self.c.setFont('Helvetica', 12)
        self.c.setTitle(title)
        self.spacing = 1.5*cm
        
        
    def writePDF(self, maxval, gradelist):
        self.c.drawCentredString(self.pwidth // 2, 28*cm, self.title)
        
        s = self.spacing
        
        x_spalte1 = 3*cm
        x_spalte2 = x_spalte1 + 2.5*cm
        x_spalte3 = x_spalte2 + 2*cm
        
        y_oben = 27*cm
        
        self.c.drawString(x_spalte1, y_oben, "Note")
        self.c.drawRightString(x_spalte2, y_oben, "Von")
        self.c.drawRightString(x_spalte3, y_oben, "Bis")
        
        self.c.line(2.5*cm, y_oben-0.2*cm, 12.5*cm, y_oben-0.2*cm)
        self.c.line(2.5*cm, y_oben-0.3*cm, 12.5*cm, y_oben-0.3*cm)
        
        self.c.drawRightString(x_spalte3, y_oben-s, str(maxval))
        
        for n in range(len(gradelist)):
            self.c.drawString(x_spalte1,  y_oben-s*(n+1), str(n+1))
            self.c.drawRightString(x_spalte2,  y_oben-s*(n+1), str(gradelist[n]))
            if n > 0:
                self.c.drawRightString(x_spalte3, y_oben-s*(n+1),str(gradelist[n-1]-0.5))
            self.c.line(2.5*cm, y_oben-s*(n+1)-0.2*cm, 12.5*cm, y_oben-s*(n+1)-0.2*cm)
        
        self.c.save()
        
        
