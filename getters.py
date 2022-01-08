from tkinter.filedialog import askopenfilename, Tk


class Getters ():
   def __init__(self):
      global table1
      table1 =""
      global table2
      table2=""
   def browseFiles(self):
      # method to browse files
      Tk().withdraw()
      self.filename = askopenfilename()
      global selectedfile
      selectedfile = self.filename


   def gettable1(self):
      # Method saving the path of the gene file
      self.browseFiles()
      global table1
      table1 = selectedfile
      print(table1)

   def table1(self):
      return table1

   def gettable2(self):
      # method selecting the path of the inpufile
      self.browseFiles()
      global table2
      table2 = selectedfile

   def table2(self):
      return table2

   def getOpF(self):
      # method selecting the path of the inpufile
      self.browseFiles()
      global operationsFile
      operationsFile = selectedfile

   def opfile(self):
      return operationsFile

   def getHeadF(self):
      # meth to select/save the filepath of the header file
      self.browseFiles()
      global headFile
      headFile = selectedfile

   def headerFile(self):
      return headFile
if __name__ == '__main__':
    gettr=Getters()
    gettr.getOpF()
    print(gettr.opfile())