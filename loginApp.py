from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import sqlite3
from PyQt5.QtCore import Qt
#Each windows will need its own class
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('login.ui', self)#Loads the UI for this class

        #add event listeners
        self.btnLogin.clicked.connect(self.loginMethod)
        self.btnClear.clicked.connect(self.clearMethod)
        self.attempts_remaining = 3
        #display the ui
        self.show()

    def loginMethod(self):
        '''Handle click events on the login button'''
        enteredPassword = self.passwordInput.text().lower()
        enteredUsername = self.userNameInput.text()
        #perform validation on the username and password
        if enteredPassword == "" or enteredUsername == "":
            messageBoxHandler("Blank fields detected", "Password and Username must be entered", 'warning')
        else:
            #query to check if username exists and password matches
            query = f'''SELECT password FROM users WHERE username =?'''
            data = executeStatementHelper(query,args=(enteredUsername,))
            #clear fields
            print(data) # check return data
            try:
                if data[0][0] == enteredPassword:
                    messageBoxHandler('Success', 'Succesfully logged in')
                    self.close()
                    #this is where opening another window would come in
                else:
                    messageBoxHandler('Login attempt failed', 'incorrect username or password', 'warning')
                    self.attempts_remaining -=1
                    if self.attempts_remaining ==0:
                        messageBoxHandler('Login failed', 'Maximum attempts reached', 'warning')
                        self.close()
                    
            except:
                messageBoxHandler('Login attempt failed', 'try again', 'warning')
            #messageBoxHandler('Success', 'Successfully logged in')
            print(f'Username: {enteredUsername} | Password: {enteredPassword}')
        

    def clearMethod(self):
        '''Resets the form fields'''
        self.userNameInput.setText("")
        self.passwordInput.setText("")

    def keyPressEvent(self, e):
        '''This method handles keyboard button events'''
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_Return:
            self.loginMethod()

class VideoUi(QtWidgets.QMainWindow):
    '''Class to handle display of video list'''
    def __init__(self):
        super(VideoUi, self).__init__()
        uic.loadUi("videoGUI.ui", self)

        #event listeners go here

        #show window
        self.show()
        self.populate_video_data()

    def populate_video_data(self):
        '''Query data from database and display it on the video form'''
        query = "SELECT Title, Studio, ReleaseDate, Classification FROM tblFilm"
        data = executeStatementHelper(query)
        #print(data)
        #initialise variable to hold data for each column
        title_data = ''

        #concatenate data from each record into the data field
        for record in data:
            title_data += str(record[0])+"\n"

        #display the data into the correct label
        self.lblTitleData.setText(title_data)

def messageBoxHandler(title, message, iconType='info'):
    '''This will display a dialog message '''
    msgBox = QtWidgets.QMessageBox() #message box object
    #set icon type based on the flag
    if iconType == 'info':
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
    elif iconType == 'question':
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
    elif iconType == 'warning':
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
    else:
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
     
    msgBox.setWindowTitle(title) #sets the title
    msgBox.setText(message)#sets the content
    msgBox.exec_()

def dbConnector():
    '''Connects to the database and returns a cursor and connection object'''
    conn = sqlite3.connect('usersAndFilms.db')
    cur = conn.cursor()
    return conn, cur

def executeStatementHelper(query,args=None):
    '''connects and executes a give query returning data'''
    conn, cur = dbConnector()
    if not args:
        cur.execute(query)
    else:
        cur.execute(query, args)
    #Fetch results 
    selectedData = cur.fetchall()
    conn.commit()
    conn.close()
    return selectedData



print(dbConnector())
#write main application which creates class instance
def mainApplication():
    "Main app which loads the window instance"
    app = QtWidgets.QApplication(sys.argv)
    #window = Ui()
    #window.show()
    window = VideoUi()
    window.show()
    sys.exit(app.exec_())
mainApplication()