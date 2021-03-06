import matplotlib

from pylatex import Document, Section, Figure, Command, PageStyle, Head, Foot, LineBreak, Tabu, TextColor, Math, NewPage
from pylatex.position import Center
from pylatex.tikz import TikZ
from pylatex.utils import italic, NoEscape
from pylatex.package import Package

matplotlib.use('Agg')  # Not to use X server. For TravisCI.
import matplotlib.pyplot as plt  # noqa

class LatexW():
    def __init__(self, maxBE, steplist, osteplist, title="Titel", the_class="", the_date="", the_ex = {}, the_students = [], oberstufe = 0):
        self.title = title
        self.myClass = the_class
        self.myDate = the_date
        self.maxBE = maxBE
        self.sl = the_students
        
        self.author ="OStR M. Putzlocher"
        
    # Basic document
        self.doptions = ["a4paper", "oneside", "onecolumn"]
        self.doc = Document(documentclass = 'article', document_options = self.doptions)

    # Seitenaufbau
        self.doc.packages.append(Package('geometry',"a4paper"))
        self.doc.preamble.append(Command("geometry", options=None, arguments=["left=2cm,right=2.5cm,top=2cm,bottom=2cm"]))

    # Sprachanpassungen
        self.doc.packages.append(Package('babel',"ngerman"))
        self.doc.preamble.append(Command("DeclareMathSymbol", options=None, arguments=[",",NoEscape("\mathpunct"),"letters", '"3B']))
        self.doc.preamble.append(Command("DeclareMathSymbol", options=None, arguments=[".",NoEscape("\mathord"),"letters", '"3B']))
        self.doc.preamble.append(Command("DeclareMathSymbol", options=None, arguments=[NoEscape("\decimal"),NoEscape("\mathord"),"letters", '"3B']))

    # Autor, Datum, Titel
        self.doc.preamble.append(Command('title', title))
        self.doc.preamble.append(Command('author', self.author))
        self.doc.preamble.append(Command('date', NoEscape(r'\today')))
    #    self.doc.append(NoEscape(r'\maketitle'))

    # Füllen des Dokuments
        self.generate_header()
               
        if oberstufe == 1:
            self.create_points_table(maxBE, osteplist)
            self.create_points_plot(maxBE, osteplist)
        else:
            self.create_grade_table(maxBE, steplist)
            self.create_grade_plot(maxBE, steplist)

        

        self.doc.create(NewPage())

        if the_ex != {}:
            self.fill_document(the_ex)

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
            header.append(self.author)

        self.doc.preamble.append(header)
        self.doc.change_document_style("header")

    def fill_document(self, ex_dict):
        doc = self.doc
        print("Aufgaben übermittelt: {}".format(ex_dict))

        ex_list = list(ex_dict.keys())
        ex_count = len(ex_list)

        ex_list.insert(0,"Aufg.")

        points_list = list(ex_dict.values())
        points_list.insert(0,"BE")

        if self.sl == []:
            row_format = "l || " + " | ".join(["c" for i in range(ex_count)])
            with doc.create(Center()):

                with doc.create(Tabu(row_format, row_height = 1.2#,
                                     #to = NoEscape(r".8\textwidth")
                                     )) as betable:
                    betable.add_row(ex_list)
                    betable.add_hline()
                    betable.add_row(points_list)
        else: # Schüler in Liste
            ex_list.insert(0,"")
            ex_list.insert(0,"")
            ex_list.append( Math(inline = True, data =NoEscape(r"\sum")))
            points_list.insert(0," ")
            points_list.insert(0," ")
            points_list.append(Math(inline = True, data =float(self.maxBE)))

            label_list= ["Nachname","Vorname","Gruppe"]+[" " for i in range(ex_count+1)]

            #l2 = len(ex_list)
            row_format = "l l l || " + " | ".join(["c" for i in range(ex_count)]) + "|| r"

            with doc.create(Center()):
                with doc.create(Tabu(row_format, row_height = 1.2#,
                                     #to = NoEscape(r".8\textwidth")
                                     )) as betable:
                    betable.add_row(ex_list)
                    betable.add_hline()
                    betable.add_row(points_list)
                    betable.add_hline()
                    betable.add_hline()
                    betable.add_row(label_list)
                    betable.add_hline()
                    betable.add_hline()

                    # Schüler
                    for num, s in enumerate(self.sl):
                        fn = s.getFamilyName()
                        n = s.getName()
                        g = s.getGroup()
                        s_entry = [fn, n, g] + [" " for i in range(ex_count+1)]
                        betable.add_row(s_entry)
                        # Trennlinie nach jedem 5. Eintrag
                        if ((num + 1) % 5) == 0:
                            betable.add_hline()


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
        
                     
    def create_points_table(self, maxBE, osteplist):
        doc = self.doc

        print(osteplist)

        table_list = list()
        for i, step in enumerate(osteplist):
            if i == 0:
                ns = "1*"
                entry = [ns,15-i, Math(inline = True, data =step), Math(inline = True, data =float(maxBE)), ""]
            else:
                # Note
                n = i // 3 +1
                # Noten-String
                ns = str(n)
                # Tendenz
                if i % 3 == 0:
                    # Bei Note 6 keine Tendenz nach oben
                    if n != 6:
                        ns = "+" + ns
                    else:
                        pass
                elif i%3 == 2:
                    ns = ns + "-"
                else:
                    pass
                entry = [Math(inline=True, data=ns), 15-i, Math(inline=True, data=step), Math(inline=True, data=osteplist[i-1]-0.5), ""]
            table_list.append(entry)

        with doc.create(Center()):
            with doc.create(Tabu("c l r r m{5cm}", row_height = 1.8#,
                        #to = NoEscape(r".8\textwidth")
                        )) as gtable:
                 gtable.add_row(["Note","Punkte", "von", "bis", "Anzahl"])
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

    def create_points_plot(self, maxBE, steplist):
        doc = self.doc

        fig = plt.figure(figsize=(6,4))
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

        ax.vlines(x = steplist, ymin=-0.2, ymax=4.2, linestyles="dashed")
        majorsteplist = [steplist[2],steplist[5],steplist[8],steplist[11],steplist[14]]
        ax.vlines(x = majorsteplist, ymin=-0.2, ymax=4.2, colors="black")
        
        for i,val in enumerate(steplist):
            if i == 0:
                ax.text(x = (val+maxBE) //2, y = 3.5, s="15", horizontalalignment='center',
                        verticalalignment='center', fontsize=8)
         #   elif i >= 15:
         #       ax.text(x = (val //2), y = 3.5, s=str(15-i), horizontalalignment='center',
         #               verticalalignment='center', fontsize=8)
            else:
                ax.text(x = (val+steplist[i-1]) //2, y = 3.5, s=str(15-i), horizontalalignment='center',
                        verticalalignment='center', fontsize=8)
        
        #ax.text(x = (steplist[0]+maxBE) //2, y = 3.5, s="1")
        #ax.text(x = (steplist[0]+steplist[1]) //2, y = 3.5, s="2")
        #ax.text(x = (steplist[1]+steplist[2]) //2, y = 3.5, s="3")
        #ax.text(x = (steplist[2]+steplist[3]) //2, y = 3.5, s="4")
        #ax.text(x = (steplist[3]+steplist[4]) //2, y = 3.5, s="5")
        #ax.text(x = (steplist[4]+steplist[5]) //2, y = 3.5, s="6")

        ax.set_xlabel('BE')
        #ax.set_ylabel('Anzahl')
        #fig.text(
        #    0.5, -0.05,
        #    'Notenverteilung',
        #    ha='center')
        
        # Vorbereitung für Datenplot
        #testdata = [20,19,31,32,10,9,5,12,14,15,20,21,22,25,26,38,26,25,25,24,30]
        #ycoor = []
        #for i in range(len(testdata)):
        #    ymax = 6
        #    ymin = 0.2
        #    y = i*1/(ymax-ymin)+ymin
        #    ycoor.append(y)
        #ax.plot(testdata,ycoor,'o',markersize=5)

        with doc.create(Figure(position='htbp')) as plot:
            plot.add_plot(width=NoEscape(r"1\textwidth"), dpi=300)

        #doc.append("Blubb")

#a = LatexW(40, [30,20,10])
