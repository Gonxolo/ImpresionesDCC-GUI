from PyQt5.QtWidgets import QGroupBox, QLabel, QPushButton, QVBoxLayout, QLineEdit
import paramiko
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time

class Worker(QObject):
    finished = pyqtSignal()

    def __init__(self, server_address, username, password, status_manager) -> None:
        super().__init__()
        self.server_address = server_address
        self.username = username
        self.password = password
        self.status_manager = status_manager

    def run(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.server_address, username=self.username, password=self.password)
            self.status_manager.connection_success(self.server_adress, self.username)
            time.sleep(5)
            self.ssh.close()
            self.status_manager.connection_closed()
        except Exception as err:
            self.status_manager.connection_error(err)
        finally:
            self.finished.emit()

class Connection(QGroupBox):

    def __init__(self, title="Conexión al servidor"):
        super().__init__(title)

        self.status_manager = None

        self.server_field = QLineEdit("anakena.dcc.uchile.cl")
        self.server_label = QLabel("Servidor:")
        self.server_label.setBuddy(self.server_field)
        
        self.user_field = QLineEdit()
        self.user_label = QLabel("Usuario:")
        self.user_label.setBuddy(self.user_field)
        
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_label = QLabel("Contraseña:")
        self.password_label.setBuddy(self.password_field)

        self.connection_button = QPushButton("Conectar")
        self.connection_button.clicked.connect(self.connect_to_server)

        self.connection_layout = QVBoxLayout()
        self.connection_layout.addWidget(self.server_label)
        self.connection_layout.addWidget(self.server_field)
        self.connection_layout.addWidget(self.user_label)
        self.connection_layout.addWidget(self.user_field)
        self.connection_layout.addWidget(self.password_label)
        self.connection_layout.addWidget(self.password_field)
        self.connection_layout.addWidget(self.connection_button)

        self.setLayout(self.connection_layout)
    
    def connect_to_server(self):
        server_address = self.server_field.text()
        username = self.user_field.text()
        password = self.password_field.text()
        self.status_manager.user = username
        self.status_manager.server = server_address
        self.status_manager.try_connect(username, server_address)
        self.thread = QThread()
        self.worker = Worker(server_address, username, password, self.status_manager)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
