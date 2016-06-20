#import requests
from pystockfish import *
import re, os
from sys import argv
 
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtNetwork import *
from urllib import unquote
from threading import Timer
"""
from requests.packages.urllib3.exceptions import SNIMissingWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(SNIMissingWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)"""





def identify(name):
    return "mid.1367252050886%3A19954a3ed320211216"


def saveCookies():
    with open("cookies", 'w') as f:
        for s in [str(c.toRawForm()) for c in cookies.allCookies()]:
            f.write(s + '\n')


cookies = QNetworkCookieJar()
try:
    with open("cookies", 'r') as f:
        cookies.setAllCookies([QNetworkCookie.parseCookies(c)[0]\
            for c in [line.rstrip('\n') for line in f]])
except FileNotFoundException:
    pass

app = QApplication(argv)
app.aboutToQuit.connect(saveCookies)
                           
class bot:        
    def __init__(self, name):
        ID = identify(name)
        if ID == "":
            return false

        self.page = WebPage(self)
        self.view = QWebView()
        self.am = QNetworkAccessManager()
        self.dc = Cache(self)
        self.am.setCache(self.dc)

            
        self.view.setPage(self.page)
        self.page.setNetworkAccessManager(self.am)
        self.am.setCookieJar(cookies)

        self.engine = Engine(depth = 19)
        self.reset()

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(5 * 60 * 1000)
        
        #self.view.loadStarted.connect(self.reset)
        self.view.load(QUrl("http://m.facebook.com/messages"))

        self.view.show()
        app.exec_()

    def refresh(self):
        print "*NOT* refreshing kappa"
        return
        if self.sending:
            QTimer.singleShot(1000, self.refresh)
            return
        self.view.pageAction(QWebPage.Reload).activate(QAction.Trigger)

    def reset(self):
        self.engine.newgame()
        self.hasJquery = False
        self.originalFen = ""
        self.lastMove = ""
        self.lastFen = ""
        self.moves = []
        self.sending = False

    def send(self, message):
        self.page.mainFrame().evaluateJavaScript("message='" + message + "';" + open("js/sendMessage.js", "r").read())

    def sendPos(self):
        self.engine.put('position fen %s moves %s' % (self.originalFen, self.engine._movelisttostr(self.moves)))
        self.engine.isready()    

    def insert(self):
        if not self.hasJquery:
            self.hasJquery = True
            print self.page.mainFrame().evaluateJavaScript(open("js/jquery-2.2.4-min.js", "r").read())
        if self.page.mainFrame().evaluateJavaScript(open("js/testLoaded.js", "r").read()):
            QTimer.singleShot(100, self.insert)
            return
        ans = self.page.mainFrame().evaluateJavaScript(open("js/lastMove.js", "r").read())

        turn = 1
        last = ""
        try:
            last = ans['last']
            turn = int(ans['turn'])
        except TypeError:
            self.refresh()
            return
        except KeyError:
            pass

        if last[-1:] == "#":
            print "GAME IS OVER :("
            self.reset()
            self.send("@fbchess play")
            return

        print " "
        turnStr = str(turn) + ans['active'] + last
        if self.lastMove == turnStr:
            return
        self.lastMove = turnStr

        fen = unquote(ans['fen'])
        lsFen = fenToArray(fen)
        if len(self.originalFen) == 0:
            castling = ""
            if lsFen[7][4] == "K":
                if lsFen[7][7] == "R":
                    castling += "K"
                if lsFen[7][0] == "R":
                    castling += "Q"
            if lsFen[0][4] == "k":
                if lsFen[0][7] == "r":
                    castling += "k"
                if lsFen[0][0] == "r":
                    castling += "q"
            if castling == "":
                castling = "-"
            print "castling:", castling
            self.originalFen = fen + " " + ans['active'] + " " + castling + " - 0 " + str(turn)
            self.engine.setfenposition(self.originalFen)
        else:
            lsFenLast = fenToArray(self.lastFen)
            changes = []
            changesCoords = []
            for i in range(8):
                for j in range(8):
                    if lsFen[i][j] != lsFenLast[i][j]:
                        changes.append("abcdefgh"[j] + str(8 - i))
                        changesCoords.append((i, j))
                        
            if len(changes) > 2:
                for i in range(len(changes)):
                    try:
                        if lsFen[changesCoords[i][0]][changesCoords[i][1]].lower() == "k":
                            if changesCoords[i][1] == 6 or changesCoords[i][1] == 1:
                                self.moves.append("e" + changes[i][1] + "g" + changes[i][1])
                            else:
                                self.moves.append("e" + changes[i][1] + "c" + changes[i][1])
                    except AttributeError:
                        pass
            else:
                lastMove = last
                try:
                    int(lastMove[-1])
                except ValueError:
                    lastMove = lastMove[:-1]
                if changes[0] == lastMove[-2:]:
                    self.moves.append(changes[1] + changes[0])
                else:
                    self.moves.append(changes[0] + changes[1])
        self.lastFen = fen
        
        if ans['side'] == ans['active']:
            print self.moves
            self.sendPos()
            print "lemme think"
            self.sending = True

            Timer(120, self.engine.stop())
            res = self.engine.bestmove()
            move = res['move']
            print move
            promote = ""
            try:
                int(move[-1])
            except ValueError:
                promote = move[-1:].upper()
                move = move[:-1]
            
            if (move == "e8g8" and lsFen[0][4] == "k") or (move == "e1g1" and lsFen[7][4] == "K"):
                response = "O-O"
            elif (move == "e8c8" and lsFen[0][4] == "k") or (move == "e1c1" and lsFen[7][4] == "K"):
                response = "0-0-0"
            else:
                old = (8 - int(move[1]), "abcdefgh".find(move[0]))
                co = (8 - int(move[3]), "abcdefgh".find(move[2]))
                orig = lsFen[old[0]][old[1]]
                response = orig.upper()
                if response == "P":
                    response = ""

                row = False
                column = False
                if response == "P":
                    if orig is not None:
                        if lsFen[old[0]][2 * co[1] - old[1]] == "P":
                            response += "x"
                            column = True
                elif response == "N":
                    i = 0
                    while i < 8 and not column:
                        x = co[0] + (-2, -2, -1, 1, 2, 2, 1, -1)[i]
                        y = co[1] + (-1, 1, 2, 2, 1, -1, -2, -2)[i]
                        try:
                            print lsFen[x][y] == orig
                            print x == old[0] and y == old[1]
                            if (lsFen[x][y] == orig and not (x == old[0] and y == old[1])):
                                column = True
                        except IndexError:
                            pass
                        i += 1
                elif response == "R" or response == "B":
                    found = False
                    if response == "R":
                        path = ((-1, 0), (1, 0), (0, 1), (0, -1))
                    elif response == "B":
                        path = ((-1, -1), (1, -1), (-1, 1), (1, 1))
                    i = 0
                    j = 1
                    while not found and i < len(path):
                        try:
                            el = lsFen[co[0] + j * path[i][0]][co[1] + j * path[i][1]]
                        except IndexError:
                            i += 1
                            j = 1
                        if el == orig and not (co[0] + j * path[i][0] == old[0] and co[1] + j * path[i][1] == old[1]):
                            found = True
                        elif el is None:
                            j += 1
                        else:
                            i += 1
                            j = 1
                    if found:
                        if path[i][1] == 0:
                            row = True
                        else:
                            column = True
                if row:
                    response += move[1]
                elif column:
                    response += move[0]
                    
                response += move[-2:]
            response += promote
            print response
            self.send("@fbchess " + response)
            if res['ponder'] == '-':
                print "WIN :D"
            self.sending = False

    
def fenToArray(fen):
    return map(lineToArray, fen.split("/"))
def lineToArray(line):
    ls = []
    for char in line:
        try:
            n = int(char)
            ls.extend([None] * n)
        except ValueError:
            ls.append(char)
    return ls
        

class Cache(QNetworkDiskCache):
    def __init__(self, parent):
        self.parent = parent
        super(Cache, self).__init__()
    def prepare(self, metaData):
        #fake cache object
        #only used to detect loading of urls (faster chessboard detection)
        url = metaData.url().toString()
        self.remove(url)
        if "chessboard" in url:
            self.parent.insert()


class WebPage(QWebPage):
    def __init__(self, parent):
        self.parent = parent
        super(WebPage, self).__init__()

    Slot()
    def shouldInterruptJavaScript(self):
        print "crash!! :("
        parent.refresh()
        return True

    
                                          

bot("michal")

