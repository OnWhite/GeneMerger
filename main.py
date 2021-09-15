import tkinter as tk
import numpy as np
import pandas as pd
from tkinter.filedialog import askdirectory, askopenfilename
from kivy.lang import Builder
from kivymd.app import MDApp
from tkinter import *
import warnings
import threading
import math
from tksheet import Sheet

KV = '''
Screen:
        canvas.before:
                Color:
                        #backgroundcolor
                        rgba:(27/255,27/255,46/255,255/255)
                Rectangle:
                        pos: self.pos
                        size: self.size

        RelativeLayout:                       
                #textfield for OutPutFilename
                MDTextField:
                        id:name
                        hint_text: "Table Name"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
                        size_hint: 0.3, 0.1
                        line_color_focus: (93/255,160/255,161/255,255/255)
                        color_mode: 'custom'
                        #mode:"rectangle"
                        current_hint_text_color:(93/255,160/255,161/255,255/255) 
                MDIconButton:
                        id: outputfolder
                        icon:'export'
                        pos_hint: {'center_x': 0.575, 'center_y': 0.7}
                        text_color: (93/255,160/255,161/255,255/255)
                        theme_text_color: "Custom"
                        markup: False
                        on_release: app.getOutPutDir()         
                MDIconButton:
                        id: inputfile
                        icon:'file-table-outline'
                        pos_hint: {'center_x': 0.412, 'center_y': 0.8}
                        text_color: (93/255,160/255,161/255,255/255)
                        theme_text_color: "Custom"
                        markup: False
                        on_release: app.getInpF()
                MDIconButton:
                        id: inputDNA
                        icon:'dna'
                        pos_hint: {'center_x': 0.575, 'center_y': 0.8}
                        text_color: (93/255,160/255,161/255,255/255)
                        theme_text_color: "Custom"
                        markup: False
                        on_release: app.getGeneF()
                MDIconButton:
                        id: column
                        icon:'table-row'
                        pos_hint: {'center_x': 0.412, 'center_y': 0.7}
                        text_color: (93/255,160/255,161/255,255/255)
                        theme_text_color: "Custom"
                        markup: False
                        on_release: app.getHeadF()
              
                #button starting the reading process of the selected folder
                MDRaisedButton:
                        pos_hint: {'center_x': 0.4, 'center_y': 0.6}
                        id: read
                        md_bg_color: (93/255,160/255,161/255,255/255)
                        theme_text_color: "Custom"
                        markup: False
                        text: "Read Files"
                        pos: (200,200)
                        on_release: app.readFiles()
                MDRaisedButton:
                        pos_hint: {'center_x': 0.55, 'center_y': 0.6}
                        id: read
                        md_bg_color: (93/255,160/255,161/255,255/255)
                        theme_text_color: "Custom"
                        markup: False
                        text: "Operations"
                        pos: (200,200)
                        on_release: app.getOpF()
                Label:
                        id: name_label
                        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
                        text: ""
                        font_size: 16


        '''


class GeneMerger(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global operationsFile
        operationsFile = \
            "C:\\Users\\work\\OneDrive - Werner Heisenberg Gymnasium\\Desktop\\genemergertestfiles\\opdat.xlsx"
        global inputFile
        inputFile = "C:\\Users\\work\\PycharmProjects\\GeneMerger\\genemergertestfiles\\testinputfile.xlsx"
        global headFile
        headFile = "C:\\Users\\work\\PycharmProjects\\GeneMerger\\genemergertestfiles\\headers.xlsx"
        global geneFile
        geneFile = "C:\\Users\\work\\PycharmProjects\\GeneMerger\\genemergertestfiles\\test.tsv"
        global proceed
        proceed = False
        global lst
        lst = []
        self.screen = Builder.load_string(KV)

    @staticmethod
    def browseFiles():
        # method to browse files
        Tk().withdraw()
        filename = askopenfilename()
        global selectedfile
        selectedfile = filename

    # folderexplorer
    @staticmethod
    def browseDir():
        # draw the explorer (tkinter)
        Tk().withdraw()
        # get the selected filename
        directoryname = askdirectory()
        # save it in a global variable
        global selecteddirectory
        selecteddirectory = directoryname

    def getGeneF(self):
        # Method saving the path of the gene file
        self.browseFiles()
        global geneFile
        geneFile = selectedfile
        if not geneFile.__contains__(".tsv"):
            # select correct file type
            self.screen.ids.name_label.text = "The genefile should have an .tsv filetype"
            geneFile = ""

    def getInpF(self):
        # method selecting the path of the inpufile
        self.browseFiles()
        global inputFile
        inputFile = selectedfile
        if not inputFile.__contains__(".xlsx"):
            # block if wrong file type
            self.screen.ids.name_label.text = "The genefile should have an .xlsx filetype"
            inputFile = ""

    def getOpF(self):
        # method selecting the path of the inpufile
        self.browseFiles()
        global operationsFile
        operationsFile = selectedfile
        operationstable = pd.read_excel(operationsFile.replace("/", "\\"))
        for i in operationstable:
            for l in operationstable[i].tolist():
                print(l)
        if not operationsFile.__contains__(".xlsx"):
            # block if wrong file type
            self.screen.ids.name_label.text = "The genefile should have an .xlsx filetype"
            operationsFile = ""

    def getHeadF(self):
        # meth to select/save the filepath of the header file
        self.browseFiles()
        global headFile
        headFile = selectedfile
        if not headFile.__contains__(".xlsx"):
            # if the fileformat is wrong
            self.screen.ids.name_label.text = "The headerfile should have an .xlsx filetype"
            headFile = ""

    def outputdir(self):
        # way to select/save the path to the output dir
        self.browseDir()
        global outputdir
        outputdir = selecteddirectory

    def readFiles(self):
        if inputFile != "" and headFile != "" and geneFile != "":
            # checking the essential data
            warnings.simplefilter(action='ignore', category=FutureWarning)
            # ignore numpy futurewarning
            outputfilename = self.screen.ids.name.text + ".tab"

            if len(str(outputfilename).strip("/\\: * ?\"<>|")) != len(str(outputfilename)):
                # filename check
                self.screen.ids.name_label.text = "Your Filename shouldn't contain  / \\ : * ? \" < > |"
                return ""
            if operationsFile != "":
                operationstable = pd.read_excel(operationsFile.replace("/", "\\"))
                operations = operationstable['Operation'].tolist()
                ophead = operationstable['Name'].tolist()
                opone = operationstable['one'].tolist()
                optwo = operationstable['two'].tolist()

            # read all the files & set variables
            #  headers table
            headt = pd.read_excel(headFile.replace("/", "\\"))
            # list of all headers
            headh = headt.columns.ravel()
            # gene table
            genet = pd.read_csv(geneFile.replace("/", "\\"), sep="\t")
            # headings of the gene table
            geneh = genet.columns.ravel()
            # input table
            inpt = pd.read_excel(inputFile.replace("/", "\\"))
            # headings of the imputtable
            inph = inpt.columns.ravel()

            c = 0
            d = False
            # selected headings in the gene file
            geneouth = []
            # selected heading in the input file
            inpouth = []

            # default outputtablename
            if self.screen.ids.name.text == "":
                outputfilename = "outputfile.tab"
            # open the outputfile
            mainfile = open(outputfilename, "w+")
            listlength = 0

            for i in headh:
                if not i.__contains__("Unnamed:"):
                    # removing xlsx methadata
                    listlength += 1
                    # counter whether there are headers
                    for l in geneh:
                        # find matching headers in the gene file
                        if i == str(l):
                            geneouth.append(i)
                            c += 1
                            d = True

                    if not d:
                        # if nothing found in the gene file
                        for t in inph:
                            # find the header in the inpt
                            if t == i:
                                inpouth.append(i)
                                c += 1
                    d = False
            # Header for the output file
            header = "#"
            # map: heading, element
            sortmap = {}
            # map for operations: heading, element
            opsortmap = {}
            # fill sortmap/ headingstring
            for i in headh:
                # remove empty values
                if not i.__contains__("Unnamed:"):
                    # remove methadata again
                    header += i + "\t"
                    sortmap[i] = ""
            if operationsFile != "":
                for l in ophead:
                    # remove empty values
                    if l != "nan":
                        header += l + "\t"
                        opsortmap[l] = ""

            header += "\n"
            # insert the header in the file
            mainfile.write(header)

            if c != listlength:
                # same amont of headers found and there
                self.screen.ids.name_label.text = "Your Columnheader file has (a) non existing header(s) please " \
                                                  "remove it/ them "
                return ""

            genenamefromgenefile = []
            # genename: options for the gene header (other options to be inserted)
            genename = ['Gene', 'gene', 'Genom', 'genom', 'GeneName', 'Genename', 'genename', 'genomname', 'genomName',
                        'GenomName']

            for gn in genename:
                for ih in inph:
                    if ih == gn:
                        # get the corresponding header for the file
                        # insert that column in a list
                        genenamelistinput = inpt[gn].tolist()
                        break
                for gh in geneh:
                    if gn == gh:
                        # get the corresponding header for the file
                        # insert that column in a list
                        genenamefromgenefile = genet[gn].tolist()

                        break

            def to_str(var):
                # making numpy float to string
                return str(list(np.reshape(np.asarray(var), (1, np.size(var)))[0]))[1:-1]

            def displayinserts():
                # method for the first 10 datapoints for the manual controll
                column = ""
                for genef in genenamefromgenefile:

                    if genel == genef:
                        # find two genenames that
                        print(optwo[0]
                              )
                        if operationsFile != "":
                            i = 0
                            for h in ophead:

                                if i < len(operations) and operations[i] != "nan":

                                    p1 = ""
                                    p2 = ""
                                    if geneh.__contains__(
                                            opone[i]
                                    ):
                                        p1 = genet.loc[
                                            genenamefromgenefile.index(genel), opone[i]]
                                    elif inph.__contains__(opone[i]):
                                        p1 = inpt.loc[
                                            genenamelistinput.index(genel), opone[i]]
                                    if geneh.__contains__(optwo[i]):
                                        p2 = genet.loc[
                                            genenamefromgenefile.index(genel), optwo[i]]
                                    elif inph.__contains__(optwo[i]):
                                        p2 = inpt.loc[
                                            genenamelistinput.index(genel), optwo[i]]
                                    if p1 == "":
                                        p1 = int(optwo[i])

                                    if p2 == "":
                                        p2 = int(optwo[i])
                                    print(p1)
                                    print(p2)
                                    p11 = str(p1)
                                    p22 = str(p2)
                                    if p11.__contains__(".") and (p11.__contains__("e") or p11.__contains__("E")):

                                        if p11.__contains__("E"):

                                            p11arrr = p11.split("E")
                                        else:
                                            p11arrr = p11.split("e")
                                        p1 = float(p11arrr[0]) * math.pow(10, float(p11arrr[1]))
                                    if p22.__contains__(".") and (p22.__contains__("e") or p22.__contains__("E")):
                                        if p22.__contains__("e"):
                                            p22arrr = p22.split("e")
                                        else:
                                            p22arrr = p22.split("E")
                                        p2 = float(p22arrr[0]) * math.pow(10, float(p22arrr[1]))
                                    if operations[i] == "*":
                                        opsortmap[h] = p1 * p2
                                        print(opsortmap[h])
                                    elif operations[i] == "-":
                                        opsortmap[h] = p1 - p2
                                    elif operations[i] == "+":
                                        opsortmap[h] = p1 - p2
                                    elif operations[i] == "/":
                                        opsortmap[h] = p1 / p2
                                    elif operations[i] == "log":
                                        opsortmap[h] = str(math.log(p1, p2))
                                    elif operations[i] == "exp":
                                        opsortmap[h] = str(math.pow(p1, p2))
                                    elif operations[i] == "log2":
                                        opsortmap[h] = str(math.log2(p1))
                                    elif operations[i] == "sign comp":
                                        signcomp = ""
                                        if p1 > 0:
                                            signcomp = "+"
                                        elif p1 < 0:
                                            signcomp = "-"
                                        else:
                                            signcomp = "0"

                                        if p2 > 0:
                                            signcomp += "+"
                                        elif p2 < 0:
                                            signcomp += "-"
                                        else:
                                            signcomp += "0"
                                        opsortmap[h] = signcomp
                                    elif operations[i] == "sign":
                                        if p1 > 0:
                                            opsortmap[h] = "+"
                                        elif p1 < 0:
                                            opsortmap[h] = "-"
                                        else:
                                            opsortmap[h] = "0"
                                i += 1
                        for el in geneouth:
                            sortmap[el] = genet.loc[genenamefromgenefile.index(genel), el]

                        for el in inpouth:
                            sortmap[el] = inpt.loc[genenamelistinput.index(genel), el]
                        output = []
                        for head in headh:

                            if to_str(sortmap.get(head)) != 'None':
                                output.append(sortmap.get(head))
                                column += "\"" + to_str(sortmap.get(head)) + "\"" + ","
                        for op in ophead:
                            if to_str(opsortmap.get(op)) != "None":
                                output.append(opsortmap.get(op))

                        lst.append(output)

                    if len(lst) == 10:
                        return ""

            def mergethread(genel):
                column = ""
                for genef in genenamefromgenefile:

                    if genel == genef:
                        # find two genenames that
                        print(optwo[0]
                              )
                        if operationsFile != "":
                            i = 0
                            for h in ophead:

                                if i < len(operations) and operations[i] != "nan":

                                    p1 = ""
                                    p2 = ""
                                    if geneh.__contains__(
                                            opone[i]
                                    ):
                                        p1 = genet.loc[
                                            genenamefromgenefile.index(genel), opone[i]]
                                    elif inph.__contains__(opone[i]):
                                        p1 = inpt.loc[
                                            genenamelistinput.index(genel), opone[i]]
                                    if geneh.__contains__(optwo[i]):
                                        p2 = genet.loc[
                                            genenamefromgenefile.index(genel), optwo[i]]
                                    elif inph.__contains__(optwo[i]):
                                        p2 = inpt.loc[
                                            genenamelistinput.index(genel), optwo[i]]
                                    if p1 == "":
                                        p1 = int(optwo[i])

                                    if p2 == "":
                                        p2 = int(optwo[i])
                                    print(p1)
                                    print(p2)
                                    p11 = str(p1)
                                    p22 = str(p2)
                                    if p11.__contains__(".") and (p11.__contains__("e") or p11.__contains__("E")):

                                        if p11.__contains__("E"):

                                            p11arrr = p11.split("E")
                                        else:
                                            p11arrr = p11.split("e")
                                        p1 = float(p11arrr[0]) * math.pow(10, float(p11arrr[1]))
                                    if p22.__contains__(".") and (p22.__contains__("e") or p22.__contains__("E")):
                                        if p22.__contains__("e"):
                                            p22arrr = p22.split("e")
                                        else:
                                            p22arrr = p22.split("E")
                                        p2 = float(p22arrr[0]) * math.pow(10, float(p22arrr[1]))
                                    if operations[i] == "*":
                                        opsortmap[h] = p1 * p2
                                        print(opsortmap[h])
                                    elif operations[i] == "-":
                                        opsortmap[h] = p1 - p2
                                    elif operations[i] == "+":
                                        opsortmap[h] = p1 - p2
                                    elif operations[i] == "/":
                                        opsortmap[h] = p1 / p2
                                    elif operations[i] == "log":
                                        opsortmap[h] = str(math.log(p1, p2))
                                    elif operations[i] == "exp":
                                        opsortmap[h] = str(math.pow(p1, p2))
                                    elif operations[i] == "log2":
                                        opsortmap[h] = str(math.log2(p1))
                                    elif operations[i] == "sign comp":
                                        signcomp = ""
                                        if p1 > 0:
                                            signcomp = "+"
                                        elif p1 < 0:
                                            signcomp = "-"
                                        else:
                                            signcomp = "0"

                                        if p2 > 0:
                                            signcomp += "+"
                                        elif p2 < 0:
                                            signcomp += "-"
                                        else:
                                            signcomp += "0"
                                        opsortmap[h] = signcomp
                                    elif operations[i] == "sign":
                                        if p1 > 0:
                                            opsortmap[h] = "+"
                                        elif p1 < 0:
                                            opsortmap[h] = "-"
                                        else:
                                            opsortmap[h] = "0"
                                i += 1
                        for el in geneouth:
                            sortmap[el] = genet.loc[genenamefromgenefile.index(genel), el]

                        for el in inpouth:
                            sortmap[el] = inpt.loc[genenamelistinput.index(genel), el]
                        for head in headh:

                            if to_str(sortmap.get(head)) != 'None':
                                column += to_str(sortmap.get(head)) + "\t"
                        for op in ophead:
                            if to_str(opsortmap.get(op)) != "None":
                                column += to_str(opsortmap.get(op)) + "\t"
                        mainfile.write(column + "\n")

            hlist = []
            for i in headh:
                if not i.__contains__("Unnamed"):
                    hlist.append(i)
            for i in ophead:
                if not i.__contains__("Unnamed"):
                    hlist.append(i)
            lst.append(hlist)

            for genel in genenamelistinput:
                o1 = threading.Thread(target=displayinserts(), args=())
                o1.start()
            self.lists(lst)

            if proceed:
                for genel in genenamelistinput:
                    o = threading.Thread(target=mergethread(genel), args=())
                    o.start()
            else:
                self.screen.ids.name_label.text = "Process finished with exit code -1"
                return ""
            mainfile.close()
            self.screen.ids.name_label.text = "Your file is ready!"

        else:
            self.screen.ids.name_label.text = "!!!You forgot a file! Please add your gene, input and columnheader file"
            return ""

    def build(self):
        return self.screen

    @staticmethod
    def lists(lines):

        top = tk.Tk()
        top.grid_columnconfigure(0, weight=1)
        top.grid_rowconfigure(0, weight=1)
        top.frame = tk.Frame(top)
        top.frame.grid_columnconfigure(0, weight=1)
        top.frame.grid_rowconfigure(0, weight=1)
        top.sheet = Sheet(top.frame, data=lines)
        top.sheet.enable_bindings()
        top.frame.grid(row=0, column=0, sticky="nswe")
        top.sheet.grid(row=0, column=0, sticky="nswe")
        top.sheet.change_theme(theme="dark blue")

        def settrue():
            global proceed
            proceed = True
            print(True)
            top.destroy()

        B = tk.Button(top, text="Proceed", command=settrue, bg="#3d3d3d", fg="#ffffff")
        B.grid(row=1, column=0, sticky="nswe")
        # table enable choices listed below:
        top.sheet.enable_bindings(("single_select",
                                   "row_select",
                                   "column_width_resize",
                                   "arrowkeys",
                                   "right_click_popup_menu",
                                   "rc_select",
                                   "rc_insert_row",
                                   "rc_delete_row",
                                   "copy",
                                   "cut",
                                   "paste",
                                   "delete",
                                   "undo",
                                   "edit_cell"))

        top.mainloop()


if __name__ == '__main__':
    GeneMerger().run()
