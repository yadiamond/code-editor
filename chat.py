import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from aimodel import get_response
import json


class Chat(QWidget):
    def __init__(self, api_key):
        super(Chat, self).__init__()
        self.api_key = api_key
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.font = QFont('Consolas', 10)
        self.chat_display.setFont(self.font)
        if self.api_key is None:
            self.chat_display.setText('Введите API ключ для доступа к модели \nAPI ключ можно получить здесь: https://openrouter.ai/settings/keys')
        self.layout.addWidget(self.chat_display)

        self.input_layout = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите ваш вопрос...")
        self.input_field.returnPressed.connect(self.send_message)
        self.input_layout.addWidget(self.input_field)

        self.send_button = QPushButton('Отправить')
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)

        self.layout.addLayout(self.input_layout)
        self.setLayout(self.layout)
        self.is_collapsed = False


    def send_message(self):
        user_message = self.input_field.text()
        if user_message:
            self.chat_display.append(f"Вы: {user_message}")
            self.input_field.clear()
            self.send_button.setEnabled(False)
            self.input_field.setEnabled(False)
            self.process_message(user_message)

    def process_message(self, message):
        if self.api_key:
            response = get_response(message, self.api_key)
            self.chat_display.append(f"Нейросеть: {response}")
            self.send_button.setEnabled(True)
            self.input_field.setEnabled(True)
        else:
            self.api_key = message
            self.chat_display.clear()
            self.chat_display.setText('API ключ установлен')
            self.send_button.setEnabled(True)
            self.input_field.setEnabled(True)
            with open('settings.json', 'r+', encoding = 'utf8') as f:
                data = json.load(f)
                data['launch_options']['api_key'] = self.api_key
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent = 2)
                f.truncate()

class ChatWidget(QFrame):
    def __init__(self, api_key):
        super(ChatWidget, self).__init__()
        self.setObjectName('chat')
        self.main_layout = QVBoxLayout(self)
        self.header_layout = QHBoxLayout()

        self.title_label = QLabel("Чат")
        self.font = QFont('Arial', 12)
        self.title_label.setFont(self.font)
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

        self.chat = Chat(api_key)
        self.main_layout.addWidget(self.chat)
        self.is_collapsed = False

        self.api_key = self.chat.api_key
    
    def get_api_key(self):
        self.api_key = self.chat.api_key
        return self.api_key

    def on_add_clicked(self):
        self.chat.clear()

    def on_close_clicked(self):
        self.setVisible(False)