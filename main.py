from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qsci import * 
import sys
import os
import math


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle('Code Editor - untitled')
        self.setGeometry(100, 100, 1000, 800)
        self.font_size = 15
        self.folder_name = None
        self.file_name = None
        self.current_folder = False
        self.set_up_app()
        self.editor.setMarginWidth(0, "0000")
        self.editor.setMarginType(0, QsciScintilla.NumberMargin)
        self.create_menu()
     

    #menu 
    def create_menu(self):
        self.menu = QMenuBar(self)
        self.setMenuBar(self.menu)
        self.menu.setStyleSheet('background-color: #DDDDDD; color: #2C2C2C')


        #File
        self.menu_file = QMenu("File", self)
        self.menu.addMenu(self.menu_file)
        self.menu_file.setStyleSheet('background-color: #DDDDDD; color: #2C2C2C')
        
        self.open_file = self.menu_file.addAction('Open File')
        self.open_file.setShortcut('Ctrl+O')
        self.open_file.triggered.connect(self.func_open)
        
        self.open_folder = self.menu_file.addAction('Open Folder')
        self.open_folder.setShortcut('Ctrl+K')
        self.open_folder.triggered.connect(self.func_folder)
        
        self.create_file = self.menu_file.addAction('Create')
        self.create_file.setShortcut('Ctrl+N')
        self.create_file.triggered.connect(self.func_create)
        
        self.menu_file.addSeparator()
        
        self.save_file = self.menu_file.addAction('Save')
        self.save_file.setShortcut('Ctrl+S')
        self.save_file.triggered.connect(self.func_save)
        
        self.save_as_file = self.menu_file.addAction('Save as')
        self.save_as_file.setShortcut('Ctrl+Shift+S')
        self.save_as_file.triggered.connect(self.func_save_as)
        
        self.menu_file.addSeparator()
        
        self.menu_file.addAction('Exit', self.close)
        
        
        #editing
        self.menu_editing = QMenu('Editing', self)
        self.menu.addMenu(self.menu_editing)
        self.menu_editing.setStyleSheet('background-color: #DDDDDD; color: #2C2C2C')
        
        self.undo = self.menu_editing.addAction('Undo')
        self.undo.setShortcut('Ctrl+Z')
        self.undo.triggered.connect(self.func_undo)
        
        self.redo = self.menu_editing.addAction('Redo')
        self.redo.setShortcut('Ctrl+Y')
        self.redo.triggered.connect(self.func_redo)
        
        self.menu_editing.addSeparator()
        
        self.copy = self.menu_editing.addAction('Copy')
        self.copy.setShortcut('Ctrl+C')
        self.copy.triggered.connect(self.func_copy)
        
        self.paste = self.menu_editing.addAction('Paste')
        self.paste.setShortcut('Ctrl+V')
        self.paste.triggered.connect(self.func_paste)
        
        self.cut = self.menu_editing.addAction('Cut')
        self.cut.setShortcut('Ctrl+X')
        self.cut.triggered.connect(self.func_cut)
        
        
    #editor_body
    def set_up_app(self):
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setStyleSheet('''
            QSplitter:handle {
                background-color: #F3F3F3
            }
        ''')

        
        #editor
        self.editor = QsciScintilla()
        self.editor.setFrameShape(QTextEdit.NoFrame)
        self.editor.textChanged.connect(self.line_numbers)
        self.font = QFont('MS Shell Dlg 2', self.font_size)
        self.editor.setFont(self.font)
        self.editor.setPaper(QColor('#ffffffff'))
        self.editor.setMarginsForegroundColor(QColor('#2c2c2c'))
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretForegroundColor(QColor('#2c2c2c'))
        self.editor.setCaretLineBackgroundColor(QColor('#e2f3ff'))
        self.editor.setMarginsBackgroundColor(QColor('#ffffffff'))
        
        #lexer
        self.pylexer = QsciLexerPython()
        self.pylexer.setDefaultColor(QColor('#2c2c2c'))
        self.pylexer.setDefaultPaper(QColor('#ffffffff'))
        
        self.editor.setLexer(self.pylexer)
        
        self.splitter.addWidget(self.editor)
        self.setCentralWidget(self.splitter)
    
    #line numbers
    def line_numbers(self):
        current_lines = self.editor.lines()
        if current_lines < 1000:
            self.editor.setMarginWidth(0, "0000")
            self.editor.setMarginType(0, QsciScintilla.NumberMargin)
        if current_lines >= 1000:
            n = math.floor(math.log(current_lines, 10))
            self.editor.setMarginWidth(0, ('0' * n + '00'))
            self.editor.setMarginType(0, QsciScintilla.NumberMargin)
            
    def tree_view_clicked(self, index):
        self.file_name = self.tree_view.model().filePath(index)
        self.setWindowTitle(('Code Editor - ' + self.file_name))
        with open(self.file_name, 'r') as f:
            data = f.read()
            self.editor.setText(data)
    
    
    #qactions_functions
    def func_open(self):
        self.file_name = QFileDialog.getOpenFileName(filter = 'Python Files (*.py);;Text files (*.txt)')[0]
        if self.file_name:
            self.setWindowTitle(('Code Editor - ' + self.file_name))
            with open(self.file_name, 'r') as f:
                data = f.read()
                self.editor.setText(data)
        else:
            pass
    
    def func_folder(self):
        if self.current_folder == False:
                self.folder_name = QFileDialog.getExistingDirectory(self, 'Select Folder')
                if self.folder_name:
                    self.model = QFileSystemModel()
                    self.model.setRootPath(self.folder_name)
                
                    self.tree_view = QTreeView()  
                    self.tree_view.setModel(self.model)
                    self.tree_view.setRootIndex(self.model.index(self.folder_name))
                    self.tree_view.clicked.connect(self.tree_view_clicked)
                    self.tree_view.setIndentation(10)
                    self.tree_view.setMaximumWidth(200)
                    self.tree_view.setMinimumWidth(80)
                    self.tree_view.setStyleSheet('''
                        QTreeView {
                            background-color: #F3F3F3;
                            border-radius: 5px;
                            border: none;
                            padding: 5px;
                            color: #2C2C2C;
                        }    
                    ''')
                    self.tree_view.header().setHidden(True)
                    self.tree_view.setColumnHidden(1, True)
                    self.tree_view.setColumnHidden(2, True)
                    self.tree_view.setColumnHidden(3, True)
                    
                    self.splitter.insertWidget(0, self.tree_view)
                    self.current_folder = True
                else:
                    pass
        else:
            self.folder_name = QFileDialog.getExistingDirectory(self, 'Select Folder')
            if self.folder_name:
                self.tree_view.deleteLater()
                self.model = QFileSystemModel()
                self.model.setRootPath(self.folder_name)
            
                self.tree_view = QTreeView()  
                self.tree_view.setModel(self.model)
                self.tree_view.setRootIndex(self.model.index(self.folder_name))
                self.tree_view.clicked.connect(self.tree_view_clicked)
                self.tree_view.setIndentation(10)
                self.tree_view.setBaseSize(100, 200)
                self.tree_view.setMaximumWidth(400)
                self.tree_view.setMinimumWidth(100)
                self.tree_view.setStyleSheet('''
                    QTreeView {
                        background-color: #F3F3F3;
                        border-radius: 5px;
                        border: none;
                        padding: 5px;
                        color: #2C2C2C;
                    }  
                ''')
                self.tree_view.header().setHidden(True)
                self.tree_view.setColumnHidden(1, True)
                self.tree_view.setColumnHidden(2, True)
                self.tree_view.setColumnHidden(3, True)
                
                self.splitter.insertWidget(0, self.tree_view)
            else:
                pass    

    def func_create(self):
        self.editor.clear()
        self.setWindowTitle('Code Editor - untitled')
    
    def func_save(self):
        if self.file_name:
            f = open(self.file_name, 'w')
            data = self.editor.text()
            f.write(data)
            f.close()
        else:
            self.func_save_as()
        
    def func_save_as(self):
        self.file_name = QFileDialog.getSaveFileName(filter = 'Python Files (*.py);;Text files (*.txt)')[0]
        if self.file_name:
            self.setWindowTitle(('Code Editor' + self.file_name))
            f = open(self.file_name, 'w')
            data = self.editor.text()
            f.write(data)
            f.close()
        else:
            pass

    def func_undo(self):
        self.editor.undo()
    
    def func_redo(self):
        self.editor.redo()

    def func_copy(self):
        self.editor.copy()
    
    def func_paste(self):
        self.editor.paste()
    
    def func_cut(self):
        self.editor.cut()
        
#zapusk
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Window()
    main_window.show()
    sys.exit(app.exec_())
