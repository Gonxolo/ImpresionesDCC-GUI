from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    
    def __init__(self, title) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.server_connection = None
    
    def closeEvent(self, event) -> None:
        if self.server_connection is not None:
            try:
                self.server_connection.close()
            except Exception as err:
                print(err)
        event.accept()