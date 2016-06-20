#import requests
from pystockfish import *
import re
import os
from sys import argv
 
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtNetwork import *
"""
from requests.packages.urllib3.exceptions import SNIMissingWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(SNIMissingWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)"""





def identify(name):
    return "mid.1367252050886%3A19954a3ed320211216"

app = QApplication(argv)

def NetworkRequestListener(view):
    print "hey"
        

def open(name):
    ID = identify(name)
    if ID == "":
        return false

    page = QWebPage()
    view = QWebView()
    am = Manager()
        
    view.setPage(page)
    page.setNetworkAccessManager(am)
        
    view.load(QUrl("http://m.facebook.com/messages"))

    view.show()
    app.exec_()


        

class Manager(QNetworkAccessManager):
    def __init__(self):
        print 'waiting for chess image'
        QNetworkAccessManager.__init__(self)
        dc = Cache(self)
        dc.setCacheDirectory("cacheDir")
        dc.setMaximumCacheSize(100 * 1024 * 1024)
        dc.clear()
        self.setCache(dc)
        self.finished.connect(self._finished)
    def _finished(self, reply):
        url = reply.url().toString()
        #print reply.attribute(QNetworkRequest.SourceIsFromCacheAttribute), url
        text = reply.readAll()
        if reply.error() != QNetworkReply.NetworkError.NoError:
            print reply.error(), url
        elif len(text) == 0:
            reqclone = QNetworkRequest(QUrl(url))
            reqclone.setAttribute(QNetworkRequest.CacheLoadControlAttribute, QNetworkRequest.AlwaysCache)
            self.get(reqclone)
        else:
            if "(White)" in text:
                print "FINALLY", url

class Cache(QNetworkDiskCache):
    def __init__(self, parent):
        super(Cache, self).__init__(parent)
    def prepare(self, metaData):
        #force save to cache)
        headers = metaData.rawHeaders()
        headers = filter(lambda x: x[0] not in ("Pragma", "Expires", "Cache-Control", "Strict-Transport-Security"), headers)
        metaData.setRawHeaders([])
        metaData.setExpirationDate(QDateTime.currentDateTime().addYears(30))
        metaData.setSaveToDisk(True)
        return super(Cache, self).prepare(metaData)
                


open("michal")
