from PyQt5.Qsci import *
from PyQt5.QtGui import *
class PythonLexer(QsciLexerPython):
    def __init__(self, theme, font, font_size):
        super(PythonLexer, self).__init__()
        if theme == 'default':
            self.setDefaultColor(QColor('#000000'))
            self.font = QFont(font, font_size)
            self.setFont(self.font)
            self.papercolor = '#ffffff'
            self.caretcolor = '#000000'
            self.caretlinecolor = '#e9e9e9'
            self.margincolor = '#ffffff'
            self.marginforcolor = '#000000'
            self.selection = '#0000ff'
        if theme == 'queit_light':
            self.setDefaultColor(QColor('#333333'))
            self.font = QFont(font, font_size)
            self.setFont(self.font)
            self.papercolor = '#f5f5f5'
            self.caretcolor = '#54494b'
            self.caretlinecolor = '#e4f6d4'
            self.margincolor = '#f5f5f5'
            self.marginforcolor = '#333333'
            self.selection = '#c9d0d9'
            self.setColor(QColor('#aaaaaa'), QsciLexerPython.Comment)
            self.setColor(QColor('#7b3f9e'), QsciLexerPython.Keyword)
            self.setColor(QColor('#a87143'), QsciLexerPython.Number)
            self.setColor(QColor('#84419e'), QsciLexerPython.ClassName)
            self.setColor(QColor('#b34d44'), QsciLexerPython.FunctionMethodName)
        if theme == 'night_blue':
            self.setDefaultColor(QColor('#cbcbcb'))
            self.font = QFont(font, font_size)
            self.setFont(self.font)
            self.papercolor = '#002451'
            self.caretcolor = '#ffffff'
            self.caretlinecolor = '#00346e'
            self.margincolor = '#002451'
            self.marginforcolor = '#636568'
            self.selection = '#003f8e'
            self.setColor(QColor('#6c80b2'), QsciLexerPython.Comment)
            self.setColor(QColor('#d18eb9'), QsciLexerPython.Keyword)
            self.setColor(QColor('#f3a56c'), QsciLexerPython.Number)
            self.setColor(QColor('#cfa1e0'), QsciLexerPython.ClassName)
            self.setColor(QColor('#7bbade'), QsciLexerPython.FunctionMethodName)
        if theme == 'default_dark':
            self.setDefaultColor(QColor('#cccccc'))
            self.font = QFont(font, font_size)
            self.setFont(self.font)
            self.papercolor = '#1f1f1f'
            self.caretcolor = '#aeafad'
            self.caretlinecolor = '#282828'
            self.margincolor = '#1f1f1f'
            self.marginforcolor = '#cccccc'
            self.selection = '#264f78'
            self.setColor(QColor('#6a8a36'), QsciLexerPython.Comment)
            self.setColor(QColor('#ba86a1'), QsciLexerPython.Keyword)
            self.setColor(QColor('#b5cea8'), QsciLexerPython.Number)
            self.setColor(QColor('#2596a2'), QsciLexerPython.ClassName)
            self.setColor(QColor('#dcdcaa'), QsciLexerPython.FunctionMethodName)
        if theme == 'atom_dark':
            self.setDefaultColor(QColor('#9da5b4'))
            self.font = QFont(font, font_size)
            self.setFont(self.font)
            self.papercolor = '#282c34'
            self.caretcolor = '#528bff'
            self.caretlinecolor = '#2c313c'
            self.margincolor = '#282c34'
            self.marginforcolor = '#9da5b4'
            self.selection = '#3e4451'
            self.setColor(QColor('#5c6370'), QsciLexerPython.Comment)
            self.setColor(QColor('#c678dd'), QsciLexerPython.Keyword)
            self.setColor(QColor('#d17c44'), QsciLexerPython.Number)
            self.setColor(QColor('#d9c064'), QsciLexerPython.ClassName)
            self.setColor(QColor('#56b6c2'), QsciLexerPython.FunctionMethodName)