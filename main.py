from PyQt5 import uic
from PyQt5.QtWidgets import *
import pandas
import crawlData

class CountReaction(QMainWindow):
    def __init__(self):
        super(CountReaction,self).__init__()
        uic.loadUi("cr_2.ui",self)
        self.setFixedSize(self.size())
        self.initEverything()
        self.addActionToAll()
        self.show()

    def initEverything(self):
        self.islink=True

        self.line=self.findChild(QLineEdit,"linkText")

        self.getButton= self.findChild(QPushButton,"getButton")
        self.saveButton=self.findChild(QPushButton,"saveButton")
        self.loadButton=self.findChild(QPushButton,"loadButton")

        self.statusLable=self.findChild(QLabel,"statusLable")

        self.tableData=self.findChild(QTableWidget,"displayTable")

        self.header=["LIKE","LOVE","SUPPORT","HAHA","WOW","SORRY","ANGER"]
        self.typeReact = {
            "LIKE": 0,
            "LOVE": 1,
            "SUPPORT": 2,
            "HAHA": 3,
            "WOW": 4,
            "SORRY": 5,
            "ANGER": 6
        }
        self.tableData.setColumnCount(len(self.header))
        self.tableData.setHorizontalHeaderLabels(self.header)



    def addActionToAll(self):
        self.getButton.clicked.connect(self.getReactAction)
        self.line.returnPressed.connect(self.getReactAction)
        self.loadButton.clicked.connect(self.loadFileAction)

    #define action
    def checkLine(self,text):
        if(text.split(".")[-1]=="xlsx"):
            return False

        if(text.find("http")>=0):
            return True

        return True

    def getReactAction(self):
        link=self.line.text()
        if (self.checkLine(link)==False):
            print("There is xlsx")
            self.multipleRequest(link)
        else:
            self.singleRequest(link)


    def singleRequest(self,url):
        self.tableData.setRowCount(0)
        self.getReactions(url)

    def multipleRequest(self,path):
        self.tableData.setRowCount(0)
        dataFile=pandas.read_excel(path)
        data=dataFile['Link'].tolist()
        for link in data:
            self.getReactions(link)


    def getReactions(self,url):
        if (url.find("http")>=0):
            self.statusLable.setText("Requesting to " + str(url))
            cont=crawlData.getContentPage(url)

            if(cont.__class__==None):
                self.showMessage("Error connection or invalid link!")
                return

            if(cont.status_code==200):
                self.statusLable.setText("Request successfully")
                cont=str(cont.content)
                self.statusLable.setText("Getting reaction of post")
                reacts=crawlData.getReaction(cont)

                #check react
                if(reacts==-1):
                    reacts=[("Error","LIKE"),
                            ("Error","HAHA"),
                            ("Error","LOVE"),
                            ("Error","SUPPORT"),
                            ("Error","ANGER"),
                            ("Error","SORRY"),
                            ("Error","WOW")]

                self.statusLable.setText("Finished getting reaction")
                #display result
                print(reacts)

                curRow=self.tableData.rowCount()
                self.tableData.insertRow(curRow)
                for i in range(len(self.header)):
                    self.tableData.setItem(curRow,i,QTableWidgetItem("0"))
                for react in reacts:
                    num = react[0]
                    typeR = react[1]
                    self.tableData.setItem(curRow,self.typeReact[typeR],QTableWidgetItem(num))

    def showMessage(self,message):
        msgBox=QMessageBox(None)
        msgBox.setWindowTitle("Message")
        msgBox.setText(message)
        msgBox.exec()

    def loadFileAction(self):
        fileChooser=QFileDialog(None)
        file=fileChooser.getOpenFileName(None)[0]
        self.line.setText(file)
        self.islink=False
        print("Choosen file: "+file)

app=QApplication([])
UI=CountReaction()
app.exec_()