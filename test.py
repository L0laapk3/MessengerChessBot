import sys
 
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from sys import argv

app = QApplication(argv)
view = QWebView()
view.load(QUrl("http://m.facebook.com/messages"))

view.show()
app.exec_()
