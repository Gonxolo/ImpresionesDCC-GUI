import os
from PyQt5.QtWidgets import QRadioButton, QVBoxLayout, QGroupBox, QGridLayout


class PrintOptions(QGroupBox):

    def __init__(self, title="Opciones de impresión") -> None:
        super().__init__(title)

        self.is_enabled = False
        self.setEnabled(self.is_enabled)

        self.status_manager = None

        self.print_command = ""

        self.file_loader = None

        self.salita_radio_button = QRadioButton("Salita")
        self.toqui_radio_button = QRadioButton("Toqui")
        self.salita_radio_button.setChecked(True)

        print_place_layout = QVBoxLayout()
        print_place_layout.addWidget(self.salita_radio_button)
        print_place_layout.addWidget(self.toqui_radio_button)

        print_place_group = QGroupBox("Lugar de impresión:")
        print_place_group.setLayout(print_place_layout)

        self.simple_radio_button = QRadioButton("Simple")
        self.doble_corto_radio_button = QRadioButton("Doble - Borde Corto")
        self.doble_largo_radio_button = QRadioButton("Doble - Borde Largo")
        self.simple_radio_button.setChecked(True)

        print_faces_layout = QVBoxLayout()
        print_faces_layout.addWidget(self.simple_radio_button)
        print_faces_layout.addWidget(self.doble_corto_radio_button)
        print_faces_layout.addWidget(self.doble_largo_radio_button)

        print_faces_group = QGroupBox("Impresión por cara:")
        print_faces_group.setLayout(print_faces_layout)

        print_options_layout = QGridLayout()
        print_options_layout.addWidget(print_place_group, 0, 0)
        print_options_layout.addWidget(print_faces_group, 0, 1)

        self.setLayout(print_options_layout)

    def get_print_command(self):
        fname = os.path.split(self.file_loader.file_path)[1]
        outname = "out.ps"
        if self.salita_radio_button.isChecked():
            if self.simple_radio_button.isChecked():
                self.print_command = f"pdf2ps {fname} {outname} && lpr -P hp-335 {outname}"
            elif self.doble_largo_radio_button.isChecked():
                self.print_command = f"pdf2ps {fname} {outname} && duplex {outname}|lpr -P hp-335"
            elif self.doble_corto_radio_button.isChecked():
                self.print_command = f"pdf2ps {fname} {outname} && duplex -l {outname}|lpr -P hp-335"
        elif self.toqui_radio_button.isChecked():
            if self.simple_radio_button.isChecked():
                self.print_command = f"pdf2ps {fname} {outname} && lpr {outname}"
            elif self.doble_largo_radio_button.isChecked():
                self.print_command = f"pdf2ps {fname} {outname} && duplex {outname}|lpr"
            elif self.doble_corto_radio_button.isChecked():
                self.print_command = f"pdf2ps {fname} {outname} && duplex -l {outname}|lpr"
        
        return self.print_command

    def enable(self):
        self.is_enabled = True
        self.setEnabled(self.is_enabled)
    
    def disable(self):
        self.is_enabled = False
        self.setEnabled(self.is_enabled)
