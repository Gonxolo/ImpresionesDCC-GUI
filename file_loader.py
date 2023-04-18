import os
from PyQt5.QtWidgets import QGroupBox, QPushButton, QLabel, QFileDialog, QVBoxLayout
from PyQt5.QtCore import QObject, QThread, pyqtSignal


class Worker(QObject):
    finished = pyqtSignal()
    ready = pyqtSignal()
    failed = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.print_command = None
        self.ssh = None
        self.localpath = None
        self.remotepath = None

    def upload(self):
        try:
            sftp = self.ssh.open_sftp()
            print(self.localpath)
            print(self.remotepath)
            sftp.put(self.localpath, self.remotepath)
            sftp.close()
            self.ready.emit()
        except Exception as err:
            print(err)
            self.failed.emit()
        finally:
            self.finished.emit()

class FileLoader(QGroupBox):
    def __init__(self, title="Selección del archivo a imprimir"):
        super().__init__(title)

        self.is_enabled = False
        self.setEnabled(self.is_enabled)

        self.status_manager = None

        self.server_connection = None 

        self.load_btn = QPushButton("Load File...")
        self.file_path = None
        self.file_name = QLabel("No hay ningun archivo cargado.")
        
        self.load_btn.clicked.connect(self.load_file)

        self.upload_btn = QPushButton("Upload file to server")
        self.file_status = QLabel("")

        self.upload_btn.clicked.connect(self.upload_file)

        load_file_layout = QVBoxLayout()
        load_file_layout.addWidget(self.load_btn)
        load_file_layout.addWidget(self.file_name)
        load_file_layout.addWidget(self.upload_btn)
        load_file_layout.addWidget(self.file_status)

        self.setLayout(load_file_layout)

    def enable(self):
        self.is_enabled = True
        self.setEnabled(self.is_enabled)
    
    def disable(self):
        self.is_enabled = False
        self.setEnabled(self.is_enabled)

    def load_file(self):
        path = QFileDialog.getOpenFileName(self, "Load", filter="PDF files (*.pdf)")[0]
        if path:
            self.file_path = path
            self.file_name.setText(f"Ruta del archivo cargado:\n{path}")

    def upload_file(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.ssh = self.server_connection.ssh
        self.worker.localpath = self.file_path
        filename = os.path.split(self.file_path)[1]
        self.worker.remotepath = f"{filename}"
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.upload)
        self.worker.finished.connect(self.thread.quit)
        self.worker.ready.connect(self.successful_connection)
        self.worker.failed.connect(self.failed_connection)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def failed_connection(self):
        self.file_status.setText("Falló la subida del archivo :c")

    def successful_connection(self):
        self.file_status.setText("Archivo subido!")
