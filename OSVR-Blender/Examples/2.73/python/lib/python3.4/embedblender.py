#!/usr/bin/env python

import sys
import os
from PyQt4 import QtCore, QtGui

class Embed_Blender(QtGui.QFrame):
    def __init__(self, parent, blender_file_name):
        super(Embed_Blender, self).__init__(parent)

        # Python module 'subprocess' would be fine too; this stays closer to C++ Qt.
        self.process = QtCore.QProcess(self)
        self.process.start('blenderplayer', ['-i', str(self.winId()), blender_file_name])

## Demonstration code.
class Embed_Blender_Example(QtGui.QWidget):
    def __init__(self, blender_file_name):
        super(Embed_Blender_Example, self).__init__()

        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(Embed_Blender(self, blender_file_name))
        layout.addWidget(QtGui.QPushButton('Qt button in a different widget than Blender'))

if __name__ == "__main__":
    BLENDER_FILE_NAME = sys.argv[1]

    app = QtGui.QApplication(sys.argv)
    main = Embed_Blender_Example(BLENDER_FILE_NAME)
    main.show()
    sys.exit(app.exec_())