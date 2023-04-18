from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QObject, QThread, pyqtSignal


class Worker(QObject):
    finished = pyqtSignal()
    success = pyqtSignal()
    failure = pyqtSignal()

    def __init__(self, ssh, cmd) -> None:
        super().__init__()
        self.ssh = ssh
        self.print_command = cmd

    def print(self):
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(self.print_command)
            ssh_stdin.close()
            ssh_stdout.close()
            ssh_stderr.close()
            self.success.emit()
        except Exception as err:
            print(err)
            self.failure.emit()
        finally:
            self.finished.emit()

class PrintButton(QPushButton):
    def __init__(self, title="Imprimir"):
        super().__init__(title)
        self.status_manager = None

        self.server_connection = None

        self.print_options = None

        self.is_enabled = False
        self.setEnabled(self.is_enabled)

        self.clicked.connect(self.print_file)

    def enable(self):
        self.is_enabled = True
        self.setEnabled(self.is_enabled)
    
    def disable(self):
        self.is_enabled = False
        self.setEnabled(self.is_enabled)

    def print_file(self):
        ssh = self.server_connection.ssh
        cmd = self.print_options.get_print_command()
        print(cmd)
        self.thread = QThread()
        self.worker = Worker(ssh, cmd)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.print)
        self.worker.finished.connect(self.thread.quit)
        self.worker.success.connect(self.success)
        self.worker.failure.connect(self.failure)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def success(self):
        self.status_manager.connection_status.setText("El archivo se envió a imprimir.")
    def failure(self):
        self.status_manager.connection_status.setText("El intento de impresión falló :c")