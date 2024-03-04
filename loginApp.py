from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys

#Each windows will need its own class
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('login.ui', self)#Loads the UI for this class

        #add button functionality here

        #display the ui
        self.show()
#write main application which creates class instance
def mainApplication():
    "Main app which instantiates the GUI classes"
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
mainApplication()