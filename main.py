from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QGroupBox, QRadioButton

from main_window import MainWindow
from connection import Connection
from status import ConnectionStatus
from file_loader import  FileLoader

app = QApplication([])
app.setApplicationName("ImpresionesDCC-GUI")

server_connection = Connection("Conexión al servidor")

connection_status = ConnectionStatus("Estado de la conexión")

server_connection.status_manager = connection_status

file_loader = FileLoader("Selección del archivo a imprimir")

salita_radio_button = QRadioButton("Salita")
toqui_radio_button = QRadioButton("Toqui")
salita_radio_button.setChecked(True)

print_place_layout = QVBoxLayout()
print_place_layout.addWidget(salita_radio_button)
print_place_layout.addWidget(toqui_radio_button)

print_place_group = QGroupBox("Lugar de impresión:")
print_place_group.setLayout(print_place_layout)

simple_radio_button = QRadioButton("Simple")
doble_corto_radio_button = QRadioButton("Doble - Borde Corto")
doble_largo_radio_button = QRadioButton("Doble - Borde Largo")
simple_radio_button.setChecked(True)

print_faces_layout = QVBoxLayout()
print_faces_layout.addWidget(simple_radio_button)
print_faces_layout.addWidget(doble_corto_radio_button)
print_faces_layout.addWidget(doble_largo_radio_button)

print_faces_group = QGroupBox("Impresión por cara:")
print_faces_group.setLayout(print_faces_layout)

print_options_layout = QGridLayout()
print_options_layout.addWidget(print_place_group, 0, 0)
print_options_layout.addWidget(print_faces_group, 0, 1)


print_options_group = QGroupBox("Opciones de impresión")
print_options_group.setEnabled(server_connection.status_manager.isConnected)
print_options_group.setLayout(print_options_layout)

print_button = QPushButton("Imprimir")
print_button.setEnabled(server_connection.status_manager.isConnected)

main_layout = QGridLayout()
main_layout.addWidget(server_connection, 0, 0)
main_layout.addWidget(connection_status, 0, 1)
main_layout.addWidget(file_loader, 1, 0)
main_layout.addWidget(print_options_group, 1, 1)
main_layout.addWidget(print_button, 3, 0, 1, 2)

widget_impresion = QWidget()
widget_impresion.setLayout(main_layout)

main_window = MainWindow("ImpresionesDCC-GUI")
main_window.setCentralWidget(widget_impresion)

if __name__ == '__main__':
    main_window.show()
    app.exec()
