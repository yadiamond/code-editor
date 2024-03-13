from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pyautogui
import sys
import os


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        
        #параметры окна
        self.setWindowTitle('Редактор кода')
        self.setGeometry(100, 100, 1000, 800)
        self.font_size = 25
        self.folder_name = None
        self.file_name = None
        self.open_folders = False
        self.init_ui()
        
    def init_ui(self):
        self.set_up_app()
        self.create_menu()
        self.setdefaultcolor()
        self.show()
    def create_menu(self):
        self.menu = QMenuBar(self)
        self.setMenuBar(self.menu)


        #File
        self.menu_file = QMenu("File", self)
        self.menu.addMenu(self.menu_file)
        
        self.open_file = self.menu_file.addAction('Open File', self.func_open)
        
        self.open_folder = self.menu_file.addAction('Open Folder', self.menu_action)
        
        self.menu_file.addAction('Create', self.editor.clear)
        
        self.menu_file.addSeparator()
        
        self.save_file = self.menu_file.addAction('Save', self.menu_action)
        
        save_as_file = self.menu_file.addAction('Save as', self.menu_action)
        
        self.menu_file.addSeparator()
        
        self.menu_file.addAction('Exit', self.close)
        
        
        #editing
        self.menu_editing = QMenu('Editing', self)
        self.menu.addMenu(self.menu_editing)
        
        cancel = self.menu_editing.addAction('Cancel', self.menu_action)
        
        repeat = self.menu_editing.addAction('Repeat', self.menu_action)
        
        self.menu_editing.addSeparator()
        
        copy = self.menu_editing.addAction('Copy', self.menu_action)
        
        paste = self.menu_editing.addAction('Paste', self.menu_action)
        
        cut = self.menu_editing.addAction('Cut', self.menu_action)
        
        
        #settings
        self.menu_settings = QMenu('Settings', self)
        self.menu.addMenu(self.menu_settings)
        
        self.theme = self.menu_settings.addMenu('Theme')
        self.theme.addAction('dark blue', self.theme_action)
        self.theme.addAction('dark', self.theme_action)
        self.theme.addAction('dark+', self.theme_action)
        self.theme.addAction('light', self.theme_action)
        self.theme.addAction('red', self.theme_action)
        self.theme.addAction('blue', self.theme_action)
        
        
    
    #функционал кнопок
    @QtCore.pyqtSlot()
    def menu_action(self):
        if self.sender().text() == 'Open File':
            self.file_name = QFileDialog.getOpenFileName(filter = 'Python Files (*.py);;Text files (*.txt)')[0]
            try:
                with open(self.file_name, 'r') as f:
                    data = f.read()
                    self.editor.setText(data)
            except:
                pass    
        
        elif self.sender().text() == 'Open Folder':
            if self.open_folders == False:
                self.folder_name = QFileDialog.getExistingDirectory(self, 'Select Folder')
                try:
                    self.model = QFileSystemModel()
                    self.model.setRootPath(self.folder_name)
                
                    self.tree_view = QTreeView()  
                    self.tree_view.setModel(self.model)
                    self.tree_view.setRootIndex(self.model.index(self.folder_name))
                    # handling click
                    self.tree_view.clicked.connect(self.tree_view_clicked)
                    self.tree_view.setIndentation(10)
                    self.tree_view.setBaseSize(100, 200)
                    self.tree_view.setMaximumWidth(400)
                    self.tree_view.setMinimumWidth(100)
                    self.tree_view.setStyleSheet('''
                        QTreeView {
                            background-color: #21252b;
                            border-radius: 5px;
                            border: none;
                            padding: 5px;
                            color: #D3D3D3;
                        }
                        QTreeView:hover {
                            color: white;
                        }    
                    ''')
                    self.tree_view.header().setHidden(True)
                    self.tree_view.setColumnHidden(1, True)
                    self.tree_view.setColumnHidden(2, True)
                    self.tree_view.setColumnHidden(3, True)
                    
                    self.splitter.insertWidget(0, self.tree_view)
                    self.open_folders = True
                except:
                    pass
            else:
                self.folder_name = QFileDialog.getExistingDirectory(self, 'Select Folder')
                try:
                    self.tree_view.deleteLater()
                    self.model = QFileSystemModel()
                    self.model.setRootPath(self.folder_name)
                
                    self.tree_view = QTreeView()  
                    self.tree_view.setModel(self.model)
                    self.tree_view.setRootIndex(self.model.index(self.folder_name))
                    # handling click
                    self.tree_view.clicked.connect(self.tree_view_clicked)
                    self.tree_view.setIndentation(10)
                    self.tree_view.setBaseSize(100, 200)
                    self.tree_view.setMaximumWidth(400)
                    self.tree_view.setMinimumWidth(100)
                    self.tree_view.setStyleSheet('''
                        QTreeView {
                            background-color: #21252b;
                            border-radius: 5px;
                            border: none;
                            padding: 5px;
                            color: #D3D3D3;
                        }
                        QTreeView:hover {
                            color: white;
                        }    
                    ''')
                    self.tree_view.header().setHidden(True)
                    self.tree_view.setColumnHidden(1, True)
                    self.tree_view.setColumnHidden(2, True)
                    self.tree_view.setColumnHidden(3, True)
                    
                    self.splitter.insertWidget(0, self.tree_view)
                except:
                    pass
                
        
        elif self.sender().text() == 'Save as':
            file_name = QFileDialog.getSaveFileName(filter = 'Python Files (*.py);;Text files (*.txt)')[0]
            try:
                f = open(file_name, 'w')
                data = self.editor.toPlainText()
                f.write(data)
                f.close()
            except:
                pass
        
        elif self.sender().text() == 'Save':
            try:
                f = open(self.file_name, 'w')
                data = self.editor.toPlainText()
                f.write(data)
                f.close()
            except:
                pass
        
        elif self.sender().text() == 'Copy':
            pyautogui.keyDown('ctrl')
            pyautogui.press('c')
            pyautogui.keyUp('ctrl')
        
        elif self.sender().text() == 'Paste':
            pyautogui.keyDown('ctrl')
            pyautogui.press('v')
            pyautogui.keyUp('ctrl')
        
        elif self.sender().text() == 'Cancel':
            pyautogui.keyDown('ctrl')
            pyautogui.press('z')
            pyautogui.keyUp('ctrl')
        
        elif self.sender().text() == 'Repeat':
            pyautogui.keyDown('ctrl')
            pyautogui.press('y')
            pyautogui.keyUp('ctrl')
            
        elif sekf.sender().text() == 'Cut':
            pyautogui.keyDown('ctrl')
            pyautogui.press('x')
            pyautogui.keyUp('ctrl')
    
    
    #установка темы
    def setdefaultcolor(self):
        f = open('themes.txt')
        f1 = f.readlines()
        x = []
        for i in f1:
            x.append(i.replace('\n', ''))
        self.editor.setStyleSheet(f'background-color: rgb({x[0]}); color: rgb({x[2]}); font-size: {self.font_size}px')
        self.menu.setStyleSheet(f'background-color: rgb({x[1]}); color: rgb({x[2]})')
        self.menu_file.setStyleSheet(f'background-color: rgb({x[1]}); color: rgb({x[2]})')
        self.menu_editing.setStyleSheet(f'background-color: rgb({x[1]}); color: rgb({x[2]})')
        self.menu_settings.setStyleSheet(f'background-color: rgb({x[1]}); color: rgb({x[2]})')
    
    
    #выбор темы
    @QtCore.pyqtSlot()
    def theme_action(self):
        f = open('themes.txt', 'w')
        if self.sender().text() == 'dark blue':
            f.write('39, 44, 52\n32, 37, 43\n202, 200, 198')
            f.close()
            self.setdefaultcolor()
        elif self.sender().text() == 'dark':
            f.write('30, 30, 30\n60, 60, 60\n 197, 203, 199')
            f.close()
            self.setdefaultcolor()
        elif self.sender().text() == 'dark+':
            f.write('0, 0, 0\n0, 0, 0\n184,191,177')
            f.close()
            self.setdefaultcolor()
        elif self.sender().text() == 'light':
            f.write('255, 255, 255\n221, 221, 221\n44, 44, 44')
            f.close()
            self.setdefaultcolor()
        elif self.sender().text() == 'blue':
            f.write('0, 37, 81\n0, 24, 51\n201, 196, 181')
            f.close()
            self.setdefaultcolor()
        elif self.sender().text() == 'red':
            f.write('65, 0, 0\n139, 13, 13\n204, 202, 198')
            f.close()
            self.setdefaultcolor()
        
    
    #основная часть интерфейса
    def set_up_app(self):
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setStyleSheet('''
            QSplitter:handle {
                background-color: rgb(39, 44, 52)
            }
        ''')
        
        self.editor = QTextEdit()
        self.editor.setFrameShape(QTextEdit.NoFrame)
        
        self.splitter.addWidget(self.editor)

        self.setCentralWidget(self.splitter)
        
    def tree_view_clicked(self):
        pass
    
    
    #функции для кнопок в меню
    def func_open(self):
        self.file_name = QFileDialog.getOpenFileName(filter = 'Python Files (*.py);;Text files (*.txt)')[0]
        try:
            with open(self.file_name, 'r') as f:
                data = f.read()
                self.editor.setText(data)
        except:
            pass
    
    def func_folder(self):
        self.folder_name = QFileDialog.getExistingDirectory(self, 'Select Folder')
        try:
            self.model = QFileSystemModel()
            self.model.setRootPath(self.folder_name)
        
            self.tree_view = QTreeView()  
            self.tree_view.setModel(self.model)
            self.tree_view.setRootIndex(self.model.index(os.getcwd()))
            # handling click
            self.tree_view.clicked.connect(self.tree_view_clicked)
            self.tree_view.setIndentation(10)
            self.tree_view.setBaseSize(100, 200)
            self.tree_view.setMaximumWidth(400)
            self.tree_view.setMinimumWidth(100)
            self.tree_view.setStyleSheet('''
                QTreeView {
                    background-color: #21252b;
                    border-radius: 5px;
                    border: none;
                    padding: 5px;
                    color: #D3D3D3;
                }
                QTreeView:hover {
                    color: white;
                }    
            ''')
            self.tree_view.header().setHidden(True)
            self.tree_view.setColumnHidden(1, True)
            self.tree_view.setColumnHidden(2, True)
            self.tree_view.setColumnHidden(3, True)
            
            self.splitter.insertWidget(0, self.tree_view)
        except:
            pass    

    def save_action(self):
        try:
            f = open(self.file_name, 'w')
            data = self.editor.toPlainText()
            f.write(data)
            f.close()
        except:
            pass
    def zoom_in(self):
        self.font_size += 5
        self.setdefaultcolor()
    def zoom_out(self):
        self.font_size -= 5
        self.setdefaultcolor()
#запуск
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Window()
    main_window.show()
    sys.exit(app.exec_())
