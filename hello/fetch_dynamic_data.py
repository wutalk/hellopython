import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *


# Take this class for granted.Just use result of rendering.
class Render(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()


# url = 'http://pycoders.com/archive/'
url = 'http://home.baidu.com/2016-03-01/1464746500.html'
r = Render(url)
result = r.frame.toHtml()
# This step is important.Converting QString to Ascii for lxml to process
print str(result.toAscii())
