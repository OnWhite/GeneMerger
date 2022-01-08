import math
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory, Tk
import getters
import pandas
import pandas as pd
from tksheet import Sheet

root = tk.Tk()
root.title("GeneMerger")
root.option_add("*tearOff", False) # This is always a good idea

# Make the app responsive
root.columnconfigure(index=0, weight=1)
root.columnconfigure(index=1, weight=1)
root.columnconfigure(index=2, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=1)
g = tk.DoubleVar(value=75.0)
session = getters.Getters()

# Create a style
style = ttk.Style(root)

# Import the tcl file
root.tk.call("source", "C:\\Users\\work\\PycharmProjects\\Forest-ttk-theme\\forest-dark.tcl")
filetypes = [".tab",  ".xlsx", ".csv"]
# Set the theme with the theme_use method
style.theme_use("forest-dark")
style.configure('lefttab.TNotebook', tabposition='wn')
readmeicon = tk.PhotoImage(file='./icons/16x16/cil-file.png')
settingsicon = tk.PhotoImage(file='./icons/16x16/cil-equalizer.png')
tableicon = tk.PhotoImage(file='./icons/16x16/cil-view-module.png')
# Notebook
notebook = ttk.Notebook(root, style='lefttab.TNotebook')

# Tab #1
tab_1 = ttk.Frame(notebook,)
tab_1.columnconfigure(index=0, weight=1)
tab_1.columnconfigure(index=1, weight=1)
tab_1.rowconfigure(index=0, weight=1)
tab_1.rowconfigure(index=1, weight=1)
notebook.add(tab_1, image =readmeicon)


# Label
ReadMe=open("ReadME.txt",'r')
textRM=ReadMe.read()
label = ttk.Label(tab_1, text=textRM, justify="center")
label.grid(row=0, column=0, pady=10, columnspan=2)

# Tab #2
tab_2 = ttk.Frame(notebook)
tab_2.columnconfigure(index=0, weight=1)
tab_2.columnconfigure(index=1, weight=1)
tab_2.rowconfigure(index=0, weight=1)
tab_2.rowconfigure(index=1, weight=1)
notebook.add(tab_2, image =settingsicon)


widgets_frame = ttk.Frame(tab_2, padding=(10, 0, 0, 0))
widgets_frame.grid(row=1, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
widgets_frame.columnconfigure(index=0, weight=1)

tablename = ttk.Entry(widgets_frame)
tablename.insert(0, "tablename")
tablename.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="we")
filetypevar = tk.StringVar()
filetype = ttk.Combobox(widgets_frame, textvariable = filetypevar,state="readonly", values=filetypes)
filetype.current(0)
filetype.grid(row=0, column=1, padx=5, pady=(0, 10), sticky="ew")


table1b = ttk.Button(widgets_frame, text="table 1",command=session.gettable1)
table1b.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="nsew")
filetypevar1 = tk.StringVar()
filetype1 = ttk.Combobox(widgets_frame, textvariable = filetypevar1, state="readonly", values=filetypes)
filetype1.current(0)
filetype1.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew")

table2b = ttk.Button(widgets_frame, text="table 2",command=session.gettable2)
table2b.grid(row=2, column=0, padx=5, pady=(0, 10), sticky="nsew")
filetypevar2 = tk.StringVar()
filetype2 = ttk.Combobox(widgets_frame,textvariable = filetypevar2, state="readonly", values=filetypes)
filetype2.current(0)
filetype2.grid(row=2, column=1, padx=5, pady=(0, 10), sticky="ew")

operations = ttk.Button(widgets_frame, text="operations",command=session.getOpF)
operations.grid(row=3, column=1, padx=5, pady=(0, 10), sticky="nsew")
def sign(p1):
    if p1 > 0:
        signcomp = "+"
    elif p1 < 0:
        signcomp = "-"
    else:
        signcomp = "0"
    return signcomp

def signcomp(p1,p2):
    l1=sign(p1)
    l2=sign(p2)
    if l1!=0 &l2!=0:
        if l1==l2:
            return "+"
        else:
            return "-"
    else:
        return l1+l2
def browseDir():
    # draw the explorer (tkinter)
    Tk().withdraw()
    # get the selected filename
    directoryname = askdirectory()
    # save it in a global variable
    global outputdirectory
    outputdirectory = directoryname
def mainalgorithm():
    browseDir()
    mergeColums = pandas.read_excel(session.opfile().replace("/", "\\"), sheet_name='Merge')
    addedColums = pandas.read_excel(session.opfile().replace("/", "\\"), sheet_name='Columns')
    table1=""
    table2=""
    if filetypevar1.get()==".tab":
        table1=pd.read_csv(session.table1().replace("/", "\\"), sep="\t")
    elif filetypevar1.get()==".txt":
        table1=pd.read_csv(session.table1().replace("/", "\\"), sep=",")
    elif filetypevar1.get()==".xlsx":
        table1=pd.read_excel(session.table1().replace("/", "\\"))
    if filetypevar2.get() == ".tab":
        table2 = pd.read_csv(session.table2().replace("/", "\\"), sep="\t")
    elif filetypevar2.get() == ".txt":
        table2 = pd.read_csv(session.table2().replace("/", "\\"), sep=",")
    elif filetypevar2.get() == ".xlsx":
        table2 = pd.read_excel(session.table2().replace("/", "\\"))
    coltable1=mergeColums['mergecolumn form  table1 '][0]
    coltable2=mergeColums['mergecolumn from table2'][0]

    if (table1.empty!=True) & (table2.empty!= True):
        #merge the files
        table=pd.merge(table1, table2, left_on=coltable1, right_on=coltable2)
        # add columns (Multithread!!)
        for i in range(len(addedColums)):
            col=[]
            if addedColums['operation'][i]=="*":
                for l in range(len(table)):
                    col.append(float(table[addedColums['column1'][i]][l])*float(table[addedColums['column2'][i]][l]))
                table.insert(0,addedColums['columnname'][i],col)
            elif addedColums['operation'][i] == "+":
                for l in range(len(table)):
                    col.append(float(table[addedColums['column1'][i]][l]) + float(table[addedColums['column2'][i]][l]))
                table.insert(0, addedColums['columnname'][i], col)
            elif addedColums['operation'][i] == "-":
                for l in range(len(table)):
                    col.append(float(table[addedColums['column1'][i]][l]) - float(table[addedColums['column2'][i]][l]))
                table.insert(0, addedColums['columnname'][i], col)
            elif addedColums['operation'][i] == "/":
                for l in range(len(table)):
                    if float(table[addedColums['column2'][i]][l])!= float(0):
                     col.append(float(table[addedColums['column1'][i]][l]) / float(table[addedColums['column2'][i]][l]))
                    else: col.append("Nan")
                table.insert(0, addedColums['columnname'][i], col)
            elif addedColums['operation'][i] == "log":
                for l in range(len(table)):
                    if float(table[addedColums['column2'][i]][l]) != float(0) & float(table[addedColums['column1'][i]][l]) != float(0):
                        col.append(str(math.log(  float(table[addedColums['column1'][i]][l]) , float(table[addedColums['column2'][i]][l]))))
                    else:
                        col.append("Nan")
                table.insert(0, addedColums['columnname'][i], col)
            elif addedColums['operation'][i] == "exp":
                for l in range(len(table)):
                    col.append(str(math.pow( float(table[addedColums['column1'][i]][l]) , float(table[addedColums['column2'][i]][l]))))

                table.insert(0, addedColums['columnname'][i], col)
            elif addedColums['operation'][i] == "log2":
                for l in range(len(table)):
                    if float(table[addedColums['column1'][i]][l]) != float(0):
                        col.append(str(math.log2(  float(table[addedColums['column1'][i]][l]) )))
                    else:
                        col.append("Nan")
                table.insert(0, addedColums['columnname'][i], col)
            elif addedColums['operation'][i] == "sign":
                for l in range(len(table)):
                    col.append(sign( float(table[addedColums['column1'][i]][l]) ))
                table.insert(0, addedColums['columnname'][i], col)
            elif addedColums['operation'][i] == "sign comp":
                for l in range(len(table)):
                    col.append(signcomp(float(table[addedColums['column1'][i]][l]),float(table[addedColums['column2'][i]][l])))
                table.insert(0, addedColums['columnname'][i], col)
        headers=list(table.columns.values)
        # remove weird excel shit
        for f in headers:
            if str(f).__contains__("Unnamed"):
                del table[str(f)]
        #update preview
        widgets_frame.sheet = Sheet(widgets_frame.frame, data=table.head().T.reset_index().values.T.tolist())
        widgets_frame.sheet.enable_bindings()
        widgets_frame.sheet.grid(row=0, column=0, sticky="nswe")
        widgets_frame.sheet.change_theme(theme="dark blue")
        widgets_frame.sheet.enable_bindings(("single_select",
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
        global finaltable
        finaltable=table

ReadFiles = ttk.Button(widgets_frame, text="read files", style="Accent.TButton", command=mainalgorithm)
ReadFiles.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="nsew")

# Tab #3
tab_3 = ttk.Frame(notebook)
notebook.add(tab_3, image = tableicon)
widgets_frame = ttk.Frame(tab_3, padding=(10, 0, 0, 0))
widgets_frame.grid(row=1, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
widgets_frame.columnconfigure(index=0, weight=1)
lines=[]
widgets_frame.grid_columnconfigure(0, weight=1)
widgets_frame.grid_rowconfigure(0, weight=1)
widgets_frame.frame = tk.Frame(widgets_frame)
widgets_frame.frame.grid_columnconfigure(0, weight=1)
widgets_frame.frame.grid_rowconfigure(0, weight=1)
widgets_frame.sheet = Sheet(widgets_frame.frame, data=lines)
widgets_frame.sheet.enable_bindings()
widgets_frame.frame.grid(row=0, column=0, sticky="nswe")
widgets_frame.sheet.grid(row=0, column=0, sticky="nswe")
widgets_frame.sheet.change_theme(theme="dark blue")

def savefile():
   tablename.get()
   if filetypevar.get() == ".tab":
       finaltable.to_csv(outputdirectory+"//"+tablename.get()+".tab",index=False,sep="\t")
   elif filetypevar.get() == ".txt":
       finaltable.to_csv(outputdirectory+"//"+tablename.get()+".txt",index=False)
   elif filetypevar.get() == ".xlsx":
       finaltable.to_excel(outputdirectory + "//" + tablename.get() + ".xlsx", index=False)

B = ttk.Button(widgets_frame, text="Proceed", command=savefile)
B.grid(row=1, column=0, sticky="nswe")
# table enable choices listed below:
widgets_frame.sheet.enable_bindings(("single_select",
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

notebook.pack(expand=True, fill="both", padx=5, pady=5)

# Sizegrip
sizegrip = ttk.Sizegrip(root)


# Center the window, and set minsize
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
x_cordinate = int((root.winfo_screenwidth()/2) - (root.winfo_width()/2))
y_cordinate = int((root.winfo_screenheight()/2) - (root.winfo_height()/2))
root.geometry("+{}+{}".format(x_cordinate, y_cordinate))


# Start the main loop
root.mainloop()
