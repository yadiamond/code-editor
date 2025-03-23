import sys
import os
import getpass
import socket
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class Console(QPlainTextEdit):
    commandSignal = pyqtSignal(str)
    commandZPressed = pyqtSignal(str)

    def __init__(self, parent=None, movable=False):
        super(Console, self).__init__()

        self.installEventFilter(self)
        self.setAcceptDrops(True)
        QApplication.setCursorFlashTime(1000)
        self.process = QProcess()
        self.process.readyReadStandardError.connect(self.onReadyReadStandardError)
        self.process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)

        self.name = (str(getpass.getuser()) + "@" + str(socket.gethostname()) 
                                + ":" + str(os.getcwd()) + "$ ")
        self.appendPlainText(self.name)
        self.commands = []
        self.tracker = 0
        self.setObjectName('console')
        self.text = None
        self.setFont(QFont("Noto Sans Mono", 8))
        self.previousCommandLength = 0


    def eventFilter(self, source, event):
        if (event.type() == QEvent.DragEnter):
            event.accept()
            print ('DragEnter')
            return True
        elif (event.type() == QEvent.Drop):
            print ('Drop')
            self.setDropEvent(event)
            return True
        else:
            return False

    def setDropEvent(self, event):
        if event.mimeData().hasUrls():
            f = str(event.mimeData().urls()[0].toLocalFile())
            self.insertPlainText(f)
            event.accept()
        elif event.mimeData().hasText():
            ft = event.mimeData().text()
            print("text:", ft)
            self.insertPlainText(ft)
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        cursor = self.textCursor()

        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_A:
            return

        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_Z:
            self.commandZPressed.emit("True")
            return

        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_C:
            self.process.kill()
            self.name = (str(getpass.getuser()) + "@" + str(socket.gethostname()) 
                                    + ":" + str(os.getcwd()) + "$ ")
            self.appendPlainText("process cancelled")
            self.appendPlainText(self.name)
            self.textCursor().movePosition(QTextCursor.End)
            return

        if e.key() == Qt.Key_Return:
            text = self.textCursor().block().text()

            if text == self.name + text.replace(self.name, "") and text.replace(self.name, "") != "":
                self.commands.append(text.replace(self.name, ""))
            self.handle(text)
            self.commandSignal.emit(text)
            self.appendPlainText(self.name)

            return

        if e.key() == Qt.Key_Up:
            try:
                if self.tracker != 0:
                    cursor.select(QTextCursor.BlockUnderCursor)
                    cursor.removeSelectedText()
                    self.appendPlainText(self.name)

                self.insertPlainText(self.commands[self.tracker])
                self.tracker -= 1

            except IndexError:
                self.tracker = 0

            return

        if e.key() == Qt.Key_Down:
            try:
                cursor.select(QTextCursor.BlockUnderCursor)
                cursor.removeSelectedText()
                self.appendPlainText(self.name)

                self.insertPlainText(self.commands[self.tracker])
                self.tracker += 1

            except IndexError:
                self.tracker = 0

        if e.key() == Qt.Key_Backspace:
            if cursor.positionInBlock() <= len(self.name):
                return

            else:
                cursor.deleteChar()

        super().keyPressEvent(e)
        cursor = self.textCursor()
        e.accept()

    def ispressed(self):
        return self.pressed

    def onReadyReadStandardError(self):
        try:
            self.error = self.process.readAllStandardError().data().decode('cp866')
            self.appendPlainText(self.error.strip('\n'))
        except UnicodeDecodeError:
            self.error = self.process.readAllStandardError().data().decode('utf-8', errors='replace')
            self.appendPlainText(self.error.strip('\n'))

    def onReadyReadStandardOutput(self):
        self.result = self.process.readAllStandardOutput().data().decode()
        self.appendPlainText(self.result.strip('\n'))
        self.state = self.process.state()

    def run(self, command):
        """Executes a system command."""
        if self.process.state() != 2:
            self.process.start(command)
            self.process.waitForFinished()
            self.textCursor().movePosition(QTextCursor.End)


    def handle(self, command):
        """Split a command into list so command echo hi would appear as ['echo', 'hi']"""
        real_command = command.replace(self.name, "")

        if command == "True" and self.process.state() == 2:
            self.process.kill()
            self.appendPlainText("Program execution killed, press enter")

        if real_command.startswith("python"):
            pass

        command_list = real_command.split() if real_command != "" else None
        """Now we start implementing some commands"""
        if real_command == "clear":
            self.clear()

        elif command_list is not None and command_list[0] == "echo":
            self.appendPlainText(" ".join(command_list[1:]))

        elif real_command == "exit":
            quit()

        elif command_list is not None and command_list[0] == "cd" and len(command_list) > 1:
            try:
                os.chdir(" ".join(command_list[1:]))
                self.name = (str(getpass.getuser()) + "@" + str(socket.gethostname()) 
                                        + ":" + str(os.getcwd()) + "$ ")
                self.textCursor().movePosition(QTextCursor.End)

            except FileNotFoundError as E:
                self.appendPlainText(str(E))

        elif command_list is not None and len(command_list) == 1 and command_list[0] == "cd":
            os.chdir(str(Path.home()))
            self.name = (str(getpass.getuser()) + "@" + str(socket.gethostname()) 
                                    + ":" + str(os.getcwd()) + "$ ")
            self.textCursor().movePosition(QTextCursor.End)

        elif self.process.state() == 2:
            self.process.write(real_command.encode())
            self.process.closeWriteChannel()

        elif command == self.name + real_command:
            self.run(real_command)


class TerminalWidget(QWidget):
    def __init__(self):
        super(TerminalWidget, self).__init__()
        self.setObjectName('terminal')
        self.main_layout = QVBoxLayout(self)

        self.header_layout = QHBoxLayout()
        self.title_label = QLabel("Терминал")
        self.title_label.setObjectName('termtitle')
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.add_button = QPushButton()
        self.add_button.setIcon(QIcon('css/create.png'))
        self.add_button.clicked.connect(self.on_add_clicked)
        self.header_layout.addWidget(self.add_button)
        self.close_button = QPushButton()
        self.close_button.setIcon(QIcon('css/close.png'))
        self.close_button.clicked.connect(self.on_close_clicked)
        self.header_layout.addWidget(self.close_button)
        self.main_layout.addLayout(self.header_layout)

        self.console_widget = Console()
        self.main_layout.addWidget(self.console_widget)


    def on_add_clicked(self):
        self.console_widget.clear()
        self.console_widget.appendPlainText(self.console_widget.name)

    def on_close_clicked(self):
        self.setVisible(False)

    def insert_text(self, text):
        self.console_widget.insertPlainText(text)
        self.console_widget.keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier))