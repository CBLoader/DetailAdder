# uncompyle6 version 3.6.5
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: Main.py
# Compiled at: 2014-01-10 02:47:31
__doc__ = '\nCreated on Dec 6, 2013\n\n@author: Steve Sare\n'
import os
import sys
import time

from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QFileDialog, QGridLayout, QLabel,
                             QLineEdit, QPushButton, QTextEdit, QWidget)

from sare.DnD_Main.CharacterFile import CharacterFile


class DnDAddDetail(QWidget):

    def __init__(self, parent=None):
        super(DnDAddDetail, self).__init__(parent)
        self.characterLabel = QLabel('D&D Character File')
        self.fileLocationBox = QLineEdit()
        self.browseButton = QPushButton('Browse')
        self.browseButton.clicked.connect(self.browse)
        self.processButton = QPushButton('Process')
        self.processButton.setMaximumSize(100, 25)
        self.outputBox = QTextEdit()
        self.outputBox.setReadOnly(True)
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.characterLabel, 0, 0)
        mainLayout.addWidget(self.fileLocationBox, 0, 1)
        mainLayout.addWidget(self.browseButton, 0, 2)
        mainLayout.addWidget(self.processButton, 1, 1)
        mainLayout.setAlignment(self.processButton, Qt.AlignCenter)
        mainLayout.addWidget(self.outputBox, 2, 0, 50, 3)
        self.Processor = Processor()
        self.simulThread = QThread()
        self.Processor.moveToThread(self.simulThread)
        self.Processor.setThread(self.simulThread)
        self.Processor.output.connect(self.outputBox.append)
        self.simulThread.started.connect(self.Processor.process)
        self.processButton.clicked.connect(self.simulThread.start)
        self.setLayout(mainLayout)
        self.setGeometry(100, 100, 500, 250)
        self.setWindowTitle('D&D Character Detail Expander')
        self.setWindowIcon(QtGui.QIcon('cbl_icon.ico'))

    def browse(self):
        ddifolder = ''
        try:
            import ctypes.wintypes
            CSIDL_PERSONAL = 5       # My Documents
            SHGFP_TYPE_CURRENT = 0   # Get current, not default value
            buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
            ddifolder = os.path.join(buf.value, 'ddi', 'Saved Characters')
        except Exception as c:
            print(c)
        fname = QFileDialog.getOpenFileName(self, 'Select Character File', ddifolder, '*.dnd4e')
        if isinstance(fname, tuple):
            fname = fname[0]
        self.fileLocationBox.setText(fname)
        self.Processor.setFileLocationBox(fname)


class Processor(QObject):
    """Processor"""
    output = pyqtSignal(str)
    startProcessing = pyqtSignal()
    fileLocationBox = ''
    thread = QThread()

    def setFileLocationBox(self, location):
        self.fileLocationBox = location

    def getFileLocationBox(self):
        return self.fileLocationBox

    def setThread(self, newThread):
        self.thread = newThread

    def __init__(self):
        super(Processor, self).__init__()
        self._step = 0
        self._isRunning = True
        self._maxSteps = 20

    def process(self):
        fname = self.getFileLocationBox()
        if fname:
            try:
                startTime = time.time()
                charFile = CharacterFile()
                charFile.process(fname, self.output)
                endTime = time.time()
                duration = endTime - startTime
                mins = str(int(duration / 60))
                secs = str(int(duration % 60))
                self.output.emit('Processing complete in: ' + mins + ':' + secs)
                self.output.emit('')
            except:
                self.output.emit("Failed to read file\n'%s'" % fname)

        self.thread.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    AddDetailWidget = DnDAddDetail()
    charFile = CharacterFile()
    if not charFile.mainExists():
        QtGui.QMessageBox.information(AddDetailWidget, 'Critical Error', 'No CBLoader main file located.  Please define a valid .main file in app.cfg.', QtGui.QMessageBox.Ok)
        sys.exit()
    else:
        AddDetailWidget.show()
        sys.exit(app.exec_())
# okay decompiling .\detailadder__main__.pyc
