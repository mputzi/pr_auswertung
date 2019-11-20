import matplotlib

from pylatex import Document, Section, Figure, Command, PageStyle, Head, Foot, LineBreak, Tabu, TextColor, Math
from pylatex.position import Center
from pylatex.tikz import TikZ
from pylatex.utils import italic, NoEscape
from pylatex.package import Package 

matplotlib.use('Agg')  # Not to use X server. For TravisCI.
import matplotlib.pyplot as plt  # noqa

class LatexW():
    def __init__(self, maxBE, steplist, title="Titel", the_class="", the_date="", the_ex = {}):
        self.title = title
        self.myClass = the_class
        self.myDate = the_date
    # Basic document
        self.doptions = ["a4paper", "oneside", "onecolumn"]
        self.doc = Document(documentclass = 'article', document_options = self.doptions)
    
    # Sprachanpassungen
        self.doc.packages.append(Package('babel',"ngerman"))
        self.doc.preamble.append(Command("DeclareMathSymbol", options=None, arguments=[",",NoEscape("\mathpunct"),"letters", '"3B']))
        self.doc.preamble.append(Command("DeclareMathSymbol", options=None, arguments=[".",NoEscape("\mathord"),"letters", '"3B']))
        self.doc.preamble.append(Command("DeclareMathSymbol", options=None, arguments=[NoEscape("\decimal"),NoEscape("\mathord"),"letters", '"3B']))

    # Autor, Datum, Titel
        self.doc.preamble.append(Command('title', title))
        self.doc.preamble.append(Command('author', 'StR M. Putzlocher'))
        self.doc.preamble.append(Command('date', NoEscape(r'\today')))
    #    self.doc.append(NoEscape(r'\maketitle'))
        
    # Füllen des Dokuments
        self.generate_header()
        self.create_grade_table(maxBE, steplist)
        if the_ex != {}:
            self.fill_document(the_ex)
        self.create_grade_plot(maxBE, steplist)

    # Erzeugen der PDF-Datei
        self.doc.generate_pdf('meins', clean_tex=False)
    # Erzeugen der tex-Datei
        self.doc.generate_tex()

        self.tex = self.doc.dumps()  # The document as string in LaTeX syntax
    
    
    def generate_header(self):
        header = PageStyle("header")
        # Create left header
        with header.create(Head("L")):
            header.append("Klasse: "+ self.myClass)
            header.append(LineBreak())
            header.append(self.title + " vom " + self.myDate)
        # Create center header
        #with header.create(Head("C")):
        #    header.append()
        # Create right header
        with header.create(Head("R")):
            header.append("Stand")
            header.append(LineBreak())
            header.append(NoEscape(r"\today"))
        # Create left footer
        #with header.create(Foot("L")):
        #    header.append("Left Footer")
        # Create center footer
        #with header.create(Foot("C")):
        #    header.append("Center Footer")
        # Create right footer
        with header.create(Foot("R")):
            header.append("StR Putzlocher")

        self.doc.preamble.append(header)
        self.doc.change_document_style("header")
        
    def fill_document(self, ex_dict):
        doc = self.doc
        print("Aufgaben übermittelt: {}".format(ex_dict))
        
        ex_list = list(ex_dict.keys())
        ex_list.insert(0,"Aufgaben")
        
        l = len(ex_list)
        
        row_format = "l || " + " | ".join(["c" for i in range(l-1)])
        
        points_list = list(ex_dict.values())
        points_list.insert(0,"BE")
        
        with doc.create(Center()):
            with doc.create(Tabu(row_format, row_height = 1.2#,
                        #to = NoEscape(r".8\textwidth")
                        )) as betable:
                betable.add_row(ex_list)
                betable.add_hline()
                betable.add_row(points_list)
        
        #doc = self.doc
   # 
   #     with doc.create(Section('Abschnitt')):
   #         doc.append('Das ist ein normaler Text, der etwas länger ist. ')
   #         doc.append(italic('Das ist ein hervorgehobener Text. '))
   #
   #    with doc.create(Subsection('Ein Unterabschnitt')):
   #         doc.append('Also some crazy characters: $&#{}')
    
    def create_grade_table(self, maxBE, steplist):
        doc = self.doc
        
        print(steplist)
        
        table_list = list()
        for i, step in enumerate(steplist):
            if i == 0:
                entry = [i+1, Math(inline = True, data =step), Math(inline = True, data =float(maxBE)), ""] 
            else:
                entry = [i+1, Math(inline = True, data =step), Math(inline = True, data =steplist[i-1]-0.5), ""]
            table_list.append(entry)
        
        with doc.create(Center()):
            with doc.create(Tabu("l r r m{5cm}", row_height = 2.0#,
                        #to = NoEscape(r".8\textwidth")
                        )) as gtable:
                 gtable.add_row(["Note", "von", "bis", "Anzahl"])
                 gtable.add_hline()
                 gtable.add_hline()
                 for row in table_list:
                     gtable.add_row(row)
                     gtable.add_hline()
    
    def create_grade_plot(self, maxBE, steplist):
        doc = self.doc
        
        
        fig = plt.figure(figsize=(6,3))
        ax = fig.add_axes((0.15, 0.15, 0.7, 0.5), visible=True)
        #ax.spines['right'].set_color('none')
        #ax.spines['top'].set_color('none')
        #ax.set_xticks([0,1,2,3,4,5,6],minor=True)
        ax.set_yticks([],minor=False)
        ax.set_ylim(0, 4)
        ax.set_xlim(0, maxBE)
        #x = [0.5,0,1,2,3,25]
        #y = [0.5,4,0,2,1,2]
        #ax.plot(x,y)
        
        ax.vlines(x = steplist, ymin=-0.2, ymax=4.2)
        ax.text(x = (steplist[0]+maxBE) //2, y = 3.5, s="1")
        ax.text(x = (steplist[0]+steplist[1]) //2, y = 3.5, s="2")
        ax.text(x = (steplist[1]+steplist[2]) //2, y = 3.5, s="3")
        ax.text(x = (steplist[2]+steplist[3]) //2, y = 3.5, s="4")
        ax.text(x = (steplist[3]+steplist[4]) //2, y = 3.5, s="5")
        ax.text(x = (steplist[4]+steplist[5]) //2, y = 3.5, s="6")
        
        ax.set_xlabel('BE')
        #ax.set_ylabel('Anzahl')
        #fig.text(
        #    0.5, -0.05,
        #    'Notenverteilung',
        #    ha='center')
        
        with doc.create(Figure(position='htbp')) as plot:
            plot.add_plot(width=NoEscape(r"1\textwidth"), dpi=300)
            #plot.add_caption('I am a caption.')
        
        doc.append("Blubb")
        
#a = LatexW(40, [30,20,10])

