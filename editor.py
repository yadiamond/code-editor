from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *
from pathlib import Path
from lexer import PythonLexer
import keyword
import pkgutil
import math


class Editor(QsciScintilla):
    def __init__(self, file_path, theme, launch_options):
        super(Editor, self).__init__()
        self.file_path = file_path
        self.theme = theme
        self.launch_options = launch_options
        self.fontstyle = self.launch_options['font']
        self.fontsize = self.launch_options['font_size']
        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setIndentationGuides(True)
        self.setTabIndents(True)
        self.setAutoIndent(True)
        
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginSensitivity(0, True)
        self.marginClicked.connect(self.margin_click)

        self.setEdgeMode(QsciScintilla.EdgeMode.EdgeLine)

        self.setCaretWidth(2)
        
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)

        if self.launch_options['wrap_mode'] == True:
            self.setWrapMode(QsciScintilla.WrapWord)
        else:
            self.setWrapMode(QsciScintilla.WrapNone)

        self.set_up_theme()
        self.set_up_autocomplete()
        
    def set_up_theme(self):
        #Set up Theme
        self.lexer = PythonLexer(self.theme, self.fontstyle, self.fontsize)
        self.setLexer(self.lexer)
        self.lexer.setPaper(QColor(self.lexer.papercolor))
        self.setCaretForegroundColor(QColor(self.lexer.caretcolor))
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor(self.lexer.caretlinecolor))
        self.setMarginsBackgroundColor(QColor(self.lexer.margincolor))
        self.setMarginsForegroundColor(QColor(self.lexer.marginforcolor))
        self.setSelectionBackgroundColor(QColor(self.lexer.selection))
        if self.file_path is None:
            self.setText("print('Hello, World!')")
        else:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.setText(file.read())

        self.setMarginWidth(0, '0' * math.floor(math.log(self.lines(), 10)) + '00')
    
    #Margin Click
    def margin_click(self, margin_nr, line, state):
        self.setSelection(line, 0, line + 1, 0)

    def set_up_autocomplete(self):
        self.api = QsciAPIs(self.lexer)
        for key in keyword.kwlist + dir(__builtins__):
            self.api.add(key)

        for importer, name, ispkg in pkgutil.iter_modules():
            self.api.add(name)
        self.api.prepare()
