from PyQt5.QtWidgets import QGroupBox, QPushButton, QLabel, QFileDialog, QVBoxLayout

class FileLoader(QGroupBox):
    def __init__(self, title="Selección del archivo a imprimir"):
        super().__init__(title)
        
        self.btn = QPushButton("Load File...")
        self.file_path = None
        self.file_name = QLabel("No hay ningun archivo cargado.")

        self._usable = True
        
        self.btn.clicked.connect(self.load_file)
        
        load_file_layout = QVBoxLayout()
        load_file_layout.addWidget(self.btn)
        load_file_layout.addWidget(self.file_name)
        
        self.setEnabled(self._usable)
        self.setLayout(load_file_layout)

    def setUsable(self):
        self._usable = not self._usable
    
    def load_file(self):
        path = QFileDialog.getOpenFileName(self, "Load", filter="PDF files (*.pdf)")[0]
        print(path)
        if path:
            self.file_path = path
            self.file_name.setText(f"Ruta del archivo cargado:\n{path}")
