from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qsci import * 
import sys
import json
import os
import webbrowser
from pathlib import Path
import math

from editor import Editor
from console import TerminalWidget
from chat import ChatWidget

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        #Loading settings
        with open('settings.json', encoding='utf-8') as f:
            self.data = json.load(f)

        self.launch_options = self.data['launch_options']
        self.theme = self.data['launch_options']['theme']
        self.file_name = self.data['launch_options']['file_path'].split('/')[-1] if self.data['launch_options']['file_path'] else None
        self.folder_name = self.data['launch_options']['folder_path'].split('/')[-1] if self.data['launch_options']['folder_path'] else None
        self.folder_path = self.data['launch_options']['folder_path']
        self.file_path = self.data['launch_options']['file_path']
        self.api_key = self.data['launch_options']['api_key']
        self.wrap_mode = self.data['launch_options']['wrap_mode']
        self.fontstyle = self.data['launch_options']['font']
        self.fontsize = self.data['launch_options']['font_size']
        self.is_new_window = False
        self.opened_files = self.data['launch_options']['opened_files']
        self.set_up_app()


    def set_up_app(self):
        #Set up Window Title
        if self.folder_path:
            if self.file_path:
                self.windowtitle = self.file_name + " - " + self.folder_name + ' - Code Editor'
            else:
                self.windowtitle = 'untitled - ' + self.folder_name + ' - Code Editor'
        else:
            if self.file_path:
                self.windowtitle = self.file_name + ' - Code Editor'
            else:
                self.windowtitle = 'untitled - Code Editor'
        self.setWindowTitle(self.windowtitle)

        #Set up Window Geometry
        self.setGeometry(self.launch_options['geometry'][0], self.launch_options['geometry'][1], self.launch_options['geometry'][2], self.launch_options['geometry'][3])
        
        #Set up Font
        self.setFont(QFont(self.fontstyle, self.fontsize))

        #Set up krasotu
        self.setStyleSheet(open(f'css/{self.theme}.qss', 'r').read())


        self.set_up_menu()
        self.set_up_status_bar()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.splitter = QSplitter()
        self.splitter.setHandleWidth(0)
        self.layout.addWidget(self.splitter)

        self.hsplitter = QSplitter()
        self.hsplitter.setOrientation(Qt.Vertical)
        self.hsplitter.setHandleWidth(0)
        self.splitter.addWidget(self.hsplitter)

        if self.folder_path:
            self.set_up_tree_view(self.folder_path)
            self.splitter.insertWidget(0, self.tree_view)
        if self.opened_files != {}:
            self.set_up_tab_view()
            for i in self.opened_files:
                self.editorspace = Editor(i, self.theme, self.launch_options)
                file_name = i.split('/')[-1] if i else 'untitled'
                self.editorspace.textChanged.connect(self.is_saved)
                self.editorspace.cursorPositionChanged.connect(self.get_cursor_position)
                current_lines = self.editorspace.lines()
                n = math.floor(math.log(current_lines, 10))
                self.editorspace.setMarginWidth(0, ('0' * n + '00'))
                self.editorspace.setMarginType(0, QsciScintilla.NumberMargin)
                
                self.tabview.addTab(self.editorspace, file_name)
                self.tabview.setTabToolTip(self.tabview.count() - 1, i)
                if self.tabview.tabText(self.opened_files[i]).split('.')[-1] == 'py':
                    self.tabview.setTabIcon(self.opened_files[i], QIcon('css/python.png'))
            self.hsplitter.addWidget(self.tabview)
        else:
            self.editorspace = Editor(None, self.theme, self.launch_options)
            self.editorspace.textChanged.connect(self.is_saved)
            self.hsplitter.addWidget(self.editorspace)
            self.hsplitter_index = self.splitter.indexOf(self.hsplitter)

    #Tab View
    def set_up_tab_view(self):
        
        self.tabview = QTabWidget()
        self.tabview.setTabsClosable(True)
        self.tabview.setMovable(True)
        self.tabview.setDocumentMode(True)
        self.tabview.setElideMode(Qt.ElideNone)
        self.tabview.currentChanged.connect(self.current_tab_changed)
        self.add_editorspace(self.file_path)

        self.tabview.tabCloseRequested.connect(self.close_tab)


    #Menu Bar
    def set_up_menu(self):
        self.menu = QMenuBar(self)
        self.setMenuBar(self.menu)
        #File
        self.menu_file = QMenu("File", self)
        self.menu.addMenu(self.menu_file)
        
        self.open_file = self.menu_file.addAction('Open File')
        self.open_file.setShortcut('Ctrl+O')
        self.open_file.triggered.connect(self.func_open)
        
        self.open_folder = self.menu_file.addAction('Open Folder')
        self.open_folder.setShortcut('Ctrl+K')
        self.open_folder.triggered.connect(self.func_folder)
        
        self.create_file = self.menu_file.addAction('New File')
        self.create_file.setShortcut('Ctrl+N')
        self.create_file.triggered.connect(self.func_create)

        self.create_window = self.menu_file.addAction('New Window')
        self.create_window.setShortcut('Ctrl+Shift+N')
        self.create_window.triggered.connect(self.func_create_window)
        
        self.menu_file.addSeparator()
        
        self.save_file = self.menu_file.addAction('Save')
        self.save_file.setShortcut('Ctrl+S')
        self.save_file.triggered.connect(self.func_save)
        
        self.save_as_file = self.menu_file.addAction('Save as')
        self.save_as_file.setShortcut('Ctrl+Shift+S')
        self.save_as_file.triggered.connect(self.func_save_as)
        
        self.menu_file.addSeparator()
        
        self.menu_file.addAction('Exit', self.close)
        
        
        #Editing
        self.menu_editing = QMenu('Editing', self)
        self.menu.addMenu(self.menu_editing)
        
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


        #Terminal
        self.menu_terminal = QMenu('Terminal', self)
        self.menu.addMenu(self.menu_terminal)

        self.new_terminal = self.menu_terminal.addAction('New Terminal')
        self.new_terminal.triggered.connect(self.new_terminal_func)

        self.clear_terminal = self.menu_terminal.addAction('Clear Terminal')
        self.clear_terminal.triggered.connect(self.clear_terminal_func)

        self.close_terminal = self.menu_terminal.addAction('Close Terminal')
        self.close_terminal.triggered.connect(self.close_terminal_func)

        self.run_task = self.menu_terminal.addAction('Run File')
        self.run_task.triggered.connect(self.run_task_func)

        #AI Assistant
        self.ai = QMenu('AI Assistant', self)
        self.menu.addMenu(self.ai)

        self.new_chat = self.ai.addAction('New Chat')
        self.new_chat.triggered.connect(self.new_chat_func)

        self.close_chat = self.ai.addAction('Close Chat')
        self.close_chat.triggered.connect(self.close_chat_func)

        self.set_up_model = self.ai.addAction('Set up model')
        self.set_up_model.triggered.connect(self.set_up_model_func)

        #Settings
        self.settings = QMenu('Settings', self)
        self.menu.addMenu(self.settings)

        self.theme_menu = QMenu('Theme', self)
        self.settings.addMenu(self.theme_menu)

        self.default_theme = self.theme_menu.addAction('Default Light')
        self.default_theme.triggered.connect(self.default_func)

        self.light_theme = self.theme_menu.addAction('Queit Light')
        self.light_theme.triggered.connect(self.light_theme_func)

        self.blue_theme = self.theme_menu.addAction('Night Blue')
        self.blue_theme.triggered.connect(self.blue_theme_func)

        self.dark_vscodetheme = self.theme_menu.addAction('Default Dark')
        self.dark_vscodetheme.triggered.connect(self.darkvs_func)

        self.atom_theme = self.theme_menu.addAction('Atom One Dark')
        self.atom_theme.triggered.connect(self.atom_theme_func)

        self.custom_theme = self.theme_menu.addAction('Custom')
        self.custom_theme.triggered.connect(self.custom_theme_func)

        self.wrapmode = self.settings.addAction('Wrap Mode: Off' if self.wrap_mode == False else 'Wrap Mode: On')
        self.wrapmode.triggered.connect(self.wrapmode_func)

        self.settings.addSeparator()

        self.reset = self.settings.addAction('Reset')
        self.reset.triggered.connect(self.reset_func)

        self.settings.addSeparator()

        self.github = self.settings.addAction('Github')
        self.github.triggered.connect(self.open_github)

    def set_up_status_bar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage('Ready', 5000)
        self.python = QLabel(f'Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')
        self.python.setObjectName('statusbar1')
        self.python.setAlignment(Qt.AlignRight)
        self.python.setFixedWidth(100)

        self.position = QLabel()
        self.position.setAlignment(Qt.AlignRight)
        self.position.setFixedWidth(100)
        self.position.setObjectName('statusbar2')
        self.statusbar.addPermanentWidget(self.position, 1)
        self.statusbar.addPermanentWidget(self.python, 2)
    
    #TreeView
    def set_up_tree_view(self, folder_path):
        self.model = QFileSystemModel()
        self.model.setRootPath(folder_path)
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(folder_path))
        self.tree_view.setIndentation(10)
        self.tree_view.setMaximumWidth(200)
        self.tree_view.setMinimumWidth(80)
        self.tree_view.header().setHidden(True)
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)
        self.tree_view.clicked.connect(self.tree_view_click)

    #QMenu Bar Functions
    def func_open(self):
        self.options = QFileDialog.Options()
        self.new_file = QFileDialog.getOpenFileName(self, "Pick A File", "", "All Files (*);;Python Files (*.py)", options=self.options)[0]
        if self.new_file != '':
            if isinstance(self.hsplitter.widget(0), QTabWidget):
                self.file_path = self.new_file
                self.file_name = self.new_file.split('/')[-1]
                self.add_editorspace(self.file_path)
                self.tabview.setCurrentIndex(self.tabview.count() - 1)
                self.tabview.setTabToolTip(self.tabview.count() - 1, self.file_path)
            else:
                self.file_path = self.new_file
                self.set_up_tab_view()
                self.hsplitter.replaceWidget(0, self.tabview)
            self.opened_files[self.file_path] = self.tabview.count() - 1
            self.statusbar.showMessage('Ready', 5000)
        else:
            self.statusbar.showMessage('Cancelled', 5000)

    def func_folder(self):
        self.options = QFileDialog.Options()
        self.new_folder = QFileDialog.getExistingDirectory(self, "Pick A Folder", "", options = self.options)
        if self.new_folder:
            if self.folder_path:
                self.folder_path = self.new_folder
                model = QFileSystemModel()
                model.setRootPath(self.folder_path)
                self.tree_view.setModel(model)
                self.tree_view.setRootIndex(model.index(self.folder_path))
            else:
                self.folder_path = self.new_folder
                self.set_up_tree_view(self.folder_path)
                self.splitter.insertWidget(0, self.tree_view)
            self.windowtitle = self.windowTitle().split(' - ')
            if len(self.windowtitle) > 2:
                self.windowtitle = ''.join(self.windowtitle[:1]) + self.folder_path.split('/')[-1] + ''.join(self.windowtitle[2:])
                self.setWindowTitle(self.windowtitle)
            self.statusbar.showMessage('Ready', 5000)
        else:
            self.statusbar.showMessage('Cancelled', 5000)

    def func_create(self):
        if isinstance(self.hsplitter.widget(0), QTabWidget):
            self.add_editorspace(None)
            self.file_path = None
            self.tabview.setCurrentIndex(self.tabview.count() - 1)
            self.tabview.setTabToolTip(self.tabview.count() - 1, 'untitled')
        else:
            self.editorspace.clear()
        self.statusbar.showMessage('Ready', 5000)

    def func_create_window(self):
        with open('settings.json', 'r+', encoding = 'utf8') as f:
            data = json.load(f)
            data['launch_options']['opened_files'] = {}
            data['launch_options']['file_path'] = None
            data['launch_options']['folder_path'] = None
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent = 2)
            f.truncate()
        self.is_new_window = True
        self.new_window = Window()
        self.new_window.show()

    def func_save(self):
        if self.file_path:
            with open(self.file_path, 'w', encoding = 'utf8') as f:
                data = self.tabview.currentWidget().text()
                f.write(data)
            self.tabview.setTabText(self.tabview.currentIndex(), self.tabview.tabText(self.tabview.currentIndex())[1:])
        else:
            self.func_save_as()

    def func_save_as(self):
        self.save_path = QFileDialog.getSaveFileName(filter = 'Python Files (*.py);;Text files (*.txt)')[0]
        if self.save_path:
            path = Path(self.save_path)
            path.write_text(self.tabview.currentWidget().text())
            self.file_path = self.save_path
            file_name = self.file_path.split('/')[-1]
            self.tabview.setTabText(self.tabview.currentIndex(), file_name)
            self.windowtitle = self.windowTitle().split(' - ')[1:]
            self.setWindowTitle(file_name + ' - ' + ' - '.join(self.windowtitle))
            self.tabview.setTabText(self.tabview.currentIndex(), self.tabview.tabText(self.tabview.currentIndex())[1:])
            self.statusbar.showMessage('Saved', 5000)
        else:
            self.statusbar.showMessage('Cancelled', 5000)

    def func_undo(self):
        if isinstance(self.hsplitter.widget(0), QTabWidget):
            self.tabview.currentWidget().undo()
        else:
            self.editorspace.undo()
    
    def func_redo(self):
        if isinstance(self.hsplitter.widget(0), QTabWidget):
            self.tabview.currentWidget().redo()
        else:
            self.editorspace.redo()

    def func_copy(self):
        if isinstance(self.hsplitter.widget(0), QTabWidget):
            self.tabview.currentWidget().copy()
        else:
            self.editorspace.copy()


    def func_paste(self):
        if isinstance(self.hsplitter.widget(0), QTabWidget):
            self.tabview.currentWidget().paste()
        else:
            self.editorspace.paste()

    def func_cut(self):
        if isinstance(self.hsplitter.widget(0), QTabWidget):
            self.tabview.currentWidget().cut()
        else:
            self.editorspace.cut()


    def new_terminal_func(self):
        if self.hsplitter.count() == 1:
            self.terminal = TerminalWidget()
            self.hsplitter.addWidget(self.terminal)
        else:
            self.terminal = TerminalWidget()
            self.hsplitter.replaceWidget(1, self.terminal)
            self.terminal.setVisible(True)

    def clear_terminal_func(self):
        if self.hsplitter.count() > 1:
            self.terminal = TerminalWidget()
            self.hsplitter.replaceWidget(1, self.terminal)
            self.terminal.setVisible(True)
    
    def run_task_func(self):
        if self.hsplitter.count() > 1 and self.file_path and self.file_path.split('.')[-1] == 'py':
            self.terminal.insert_text('python' + f' "{self.file_path}" ')

    def close_terminal_func(self):
        if self.hsplitter.count() > 1:
            self.terminal.deleteLater()

    
    def new_chat_func(self):
        if self.splitter.count() < 3:
            self.chat = ChatWidget(self.api_key)
            self.splitter.addWidget(self.chat)
            self.chat.setVisible(True)
        else:
            self.chat = ChatWidget(self.api_key)
            self.splitter.replaceWidget(2, self.chat)
            self.chat.setVisible(True)

    def close_chat_func(self):
        self.chat.deleteLater()

    def set_up_model_func(self):
        aimodel_file = sys.argv[0].split('/')[:-1]
        aimodel_file = '/'.join(aimodel_file) + '/aimodel.py'
        if self.hsplitter.widget(0) == QTabWidget:
            self.file_path = aimodel_file
            self.add_editorspace(self.file_path)
        else:
            self.file_path = aimodel_file
            self.set_up_tab_view()
            self.hsplitter.replaceWidget(0, self.tabview)
            self.tabview.setCurrentIndex(self.tabview.count() - 1)



    def wrapmode_func(self):
        if self.launch_options['wrap_mode'] == False:
            self.launch_options['wrap_mode'] = True
        else:
            self.launch_options['wrap_mode'] = False

        self.close()
        self.new_window = Window()
        self.new_window.show()
    
    def default_func(self):
        with open('settings.json', 'r+', encoding = 'utf8') as f:
            data = json.load(f)
            data['launch_options']['theme'] = 'default'
            f.seek(0)
            json.dump(data, f, ensure_ascii = False, indent = 2)
            f.truncate()
        self.new_window = Window()
        self.new_window.show()
        self.close()


    def light_theme_func(self):
        with open('settings.json', 'r+', encoding = 'utf8') as f:
            data = json.load(f)
            data['launch_options']['theme'] = 'queit_light'
            f.seek(0)
            json.dump(data, f, ensure_ascii = False, indent = 2)
            f.truncate()
        self.new_window = Window()
        self.new_window.show()
        self.close()

    def blue_theme_func(self):
        with open('settings.json', 'r+', encoding = 'utf8') as f:
            data = json.load(f)
            data['launch_options']['theme'] = 'night_blue'
            f.seek(0)
            json.dump(data, f, ensure_ascii = False, indent = 2)
            f.truncate()
        self.new_window = Window()
        self.new_window.show()
        self.close()

    def darkvs_func(self):
        with open('settings.json', 'r+', encoding = 'utf8') as f:
            data = json.load(f)
            data['launch_options']['theme'] = 'default_dark'
            f.seek(0)
            json.dump(data, f, ensure_ascii = False, indent = 2)
            f.truncate()
        self.new_window = Window()
        self.new_window.show()
        self.close()

    def atom_theme_func(self):
        with open('settings.json', 'r+', encoding = 'utf8') as f:
            data = json.load(f)
            data['launch_options']['theme'] = 'atom_dark'
            f.seek(0)
            json.dump(data, f, ensure_ascii = False, indent = 2)
            f.truncate()
        self.new_window = Window()
        self.new_window.show()
        self.close()

    def custom_theme_func(self):
        with open('settings.json', 'r+', encoding = 'utf8') as f:
            data = json.load(f)
            data['launch_options']['theme'] = 'custom'
            f.seek(0)
            json.dump(data, f, ensure_ascii = False, indent = 2)
            f.truncate()
        self.new_window = Window()
        self.new_window.show()
        self.close()

    def reset_func(self):
        with open('settings.json', 'w', encoding = 'utf8') as f:
            default = { 
                "launch_options": { 
                    "geometry": [100, 100, 1000, 800], 
                    "wrap_mode": False,
                    "file_path": None,
                    "folder_path": None,
                    "api_key": None,
                    "theme": "default"
                    },
                "theme": {
                    "background_color": "#ffffff",
                    "foreground_color": "#000000",
                    "caret_color": "#000000",
                    "font": "Fire Code",
                    "font_size": 15
                    }
                }    
            json.dump(default, f, ensure_ascii = False, indent = 2)
        self.new_window = Window()
        self.new_window.show()
        self.close()

    def open_github(self):
        webbrowser.open('https://github.com/yadiamond')

    #Когда не открыт ни один файл
    def add_editorspace(self, file_path):
        self.editorspace = Editor(file_path, self.theme, self.launch_options)
        file_name = file_path.split('/')[-1] if file_path else 'untitled'
        self.editorspace.textChanged.connect(self.is_saved)
        self.editorspace.cursorPositionChanged.connect(self.get_cursor_position)
        current_lines = self.editorspace.lines()
        n = math.floor(math.log(current_lines, 10))
        self.editorspace.setMarginWidth(0, ('0' * n + '00'))
        self.editorspace.setMarginType(0, QsciScintilla.NumberMargin)
        if file_path in self.opened_files:
            self.tabview.setCurrentIndex(self.opened_files[file_path])
        else:
            self.tabview.addTab(self.editorspace, file_name)
            self.opened_files[file_path] = self.tabview.count() - 1
            self.tabview.setTabToolTip(self.tabview.count() - 1, file_path)
            self.tabview.setCurrentIndex(self.opened_files[file_path])

    #Функция вызывается при закрытии окон QTabView
    def close_tab(self, index):
        del self.opened_files[self.tabview.tabToolTip(index)]
        self.tabview.removeTab(index)
        if self.tabview.count() == 0:
            self.editorspace = Editor(None, self.theme, self.launch_options)
            self.hsplitter.replaceWidget(0, self.editorspace)
            self.setWindowTitle('untitled - Code Editor')
            self.file_path = None

    #Функция для изменения названия программы при смене страницы
    def current_tab_changed(self, index):
        self.current_tab = self.tabview.tabText(index)
        self.windowtitle = self.windowTitle()
        self.windowtitle = self.current_tab + " - " + " - ".join(self.windowtitle.split(" - ")[1:])
        if self.tabview.tabText(index).split('.')[-1] == 'py':
            self.tabview.setTabIcon(index, QIcon('css/python.png'))
        self.setWindowTitle(self.windowtitle)
    

    def tree_view_click(self, index):
        if os.path.isfile(self.model.filePath(index)):
            if isinstance(self.hsplitter.widget(0), QTabWidget):
                self.file_path = self.model.filePath(index)
                self.add_editorspace(self.file_path)
            else:
                self.file_path = self.model.filePath(index)
                self.hsplitter_index = self.splitter.indexOf(self.hsplitter)
                self.set_up_tab_view()
                self.hsplitter.replaceWidget(0, self.tabview)
                self.tabview.setTabToolTip(self.tabview.count() - 1, self.file_path)
            self.statusbar.showMessage('Ready', 5000)

    def is_saved(self):
        if isinstance(self.hsplitter.widget(0), QTabWidget):
            index = self.tabview.currentIndex()
            if self.tabview.tabText(index)[0] != '*':
                self.tabview.setTabText(index, '*' + self.tabview.tabText(index))

            current_lines = self.tabview.currentWidget().lines()
            n = math.floor(math.log(current_lines, 10))
            self.tabview.currentWidget().setMarginWidth(0, ('0' * n + '00'))
            self.tabview.currentWidget().setMarginType(0, QsciScintilla.NumberMargin)
        else:
            current_lines = self.editorspace.lines()
            n = math.floor(math.log(current_lines, 10))
            self.editorspace.setMarginWidth(0, ('0' * n + '00'))
            self.editorspace.setMarginType(0, QsciScintilla.NumberMargin)
            
    def get_cursor_position(self):
        if isinstance(self.hsplitter.widget(0), QTabWidget):
            line, col = self.tabview.currentWidget().getCursorPosition()   
            self.position.setText(f'Ln {line}, Col {col}')
        else:
            line, col = self.editorspace.getCursorPosition()   
            self.position.setText(f'Ln {line}, Col {col}')

    def closeEvent(self, event):
        if self.is_new_window != True:
            self.opened_files = {}
            for i in range(self.tabview.count()):
                file_path = self.tabview.tabToolTip(i)
                if file_path != 'untitled':
                    self.opened_files[file_path] = i

            window_size = self.size()
            ww = window_size.width()
            wh = window_size.height()

            window_position = self.pos()
            wx = window_position.x()
            wy = window_position.y()
            with open('settings.json', 'w', encoding = 'utf8') as f:
                self.launch_options['opened_files'] = self.opened_files
                self.launch_options['geometry'] = [wx, wy, ww, wh]
                self.launch_options['file_path'] = self.file_path
                self.launch_options['folder_path'] = self.folder_path
                self.launch_options['theme'] = self.theme
                self.launch_options['api_key'] = self.chat.get_api_key() if isinstance(self.splitter.widget(self.splitter.count() - 1), ChatWidget) else self.api_key
                self.data['launch_options'] = self.launch_options
                json.dump(self.data, f, ensure_ascii = False, indent = 2)



#Launching Programm
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Window()
    main_window.show()
    sys.exit(app.exec_())

