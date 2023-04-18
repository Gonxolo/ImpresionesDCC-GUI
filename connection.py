from PyQt5.QtWidgets import QGroupBox, QLabel, QPushButton, QVBoxLayout, QLineEdit
import paramiko
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time

class Worker(QObject):

    finished = pyqtSignal()
    connection = pyqtSignal()
    disconnection = pyqtSignal()
    update_ui = pyqtSignal()

    def __init__(self, ssh, server, user, password, status_manager) -> None:
        super().__init__()
        self.server_address = server
        self.username = user
        self.password = password
        self.status_manager = status_manager
        self.ssh = ssh

    def connect(self):
        try:
            self.connection.emit()
            self.ssh.connect(self.server_address, username=self.username, password=self.password)
            self.status_manager.connection_success(self.username, self.server_address)
            self.update_ui.emit()
            self.disconnection.emit()
        except Exception as err:
            self.status_manager.connection_error(err)
            self.connection.emit()
        finally:
            self.finished.emit()

    def disconnect(self):
        try:
            self.disconnection.emit()
            self.ssh.close()
            self.status_manager.connection_closed()
            self.update_ui.emit()
            self.connection.emit()
        except Exception as err:
            self.status_manager.connection_error(err)
            self.disconnection.emit()
        finally:
            self.finished.emit()


class Connection(QGroupBox):

    def __init__(self, title="Conexión al servidor"):
        super().__init__(title)

        self.status_manager = None

        self.elements = []

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

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
        self.connection_button_enabled = True
        self.disconnection_button = QPushButton("Desconectar")
        self.disconnection_button.clicked.connect(self.disconnect_from_server)
        self.disconnection_button_enabled = False
        self.disconnection_button.setEnabled(self.disconnection_button_enabled)

        self.connection_layout = QVBoxLayout()
        self.connection_layout.addWidget(self.server_label)
        self.connection_layout.addWidget(self.server_field)
        self.connection_layout.addWidget(self.user_label)
        self.connection_layout.addWidget(self.user_field)
        self.connection_layout.addWidget(self.password_label)
        self.connection_layout.addWidget(self.password_field)
        self.connection_layout.addWidget(self.connection_button)
        self.connection_layout.addWidget(self.disconnection_button)

        self.setLayout(self.connection_layout)
    
    def get_username(self):
        return self.user_field.text()
    
    def get_server_address(self):
        return self.server_field.text()

    def connect_to_server(self):
        server_address = self.server_field.text()
        username = self.user_field.text()
        password = self.password_field.text()
        self.status_manager.user = username
        self.status_manager.server = server_address
        self.status_manager.try_connect(username, server_address)
        self.thread = QThread()
        self.worker = Worker(self.ssh, server_address, username, password, self.status_manager)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.connect)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.connection.connect(self.set_connection_button_status)
        self.worker.disconnection.connect(self.set_disconnection_button_status)
        self.worker.update_ui.connect(self.enable_elements)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def disconnect_from_server(self):
        self.thread = QThread()
        self.worker = Worker(self.ssh, None, None, None, self.status_manager)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.disconnect)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.connection.connect(self.set_connection_button_status)
        self.worker.disconnection.connect(self.set_disconnection_button_status)
        self.worker.update_ui.connect(self.disable_elements)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def set_connection_button_status(self):
        self.connection_button_enabled = not self.connection_button_enabled
        self.connection_button.setEnabled(self.connection_button_enabled)

    def set_disconnection_button_status(self):
        self.disconnection_button_enabled = not self.disconnection_button_enabled
        self.disconnection_button.setEnabled(self.disconnection_button_enabled)
    
    def enable_elements(self):
        for elem in self.elements:
            elem.enable()
    
    def disable_elements(self):
        for elem in self.elements:
            elem.disable()