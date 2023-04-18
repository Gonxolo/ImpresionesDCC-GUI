from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout

from main_window import MainWindow
from connection import Connection
from status import ConnectionStatus
from file_loader import  FileLoader
from print_options import PrintOptions
from print_button import PrintButton

app = QApplication([])
app.setApplicationName("ImpresionesDCC-GUI")

connection_status = ConnectionStatus("Estado de la conexión")

server_connection = Connection("Conexión al servidor")
server_connection.status_manager = connection_status

file_loader = FileLoader("Selección del archivo a imprimir")
file_loader.status_manager = connection_status
file_loader.server_connection = server_connection

print_options = PrintOptions("Opciones de impresión")
print_options.status_manager = connection_status
print_options.file_loader = file_loader

print_button = PrintButton("Imprimir")
print_button.status_manager = connection_status
print_button.print_options = print_options
print_button.server_connection = server_connection

main_layout = QGridLayout()
main_layout.addWidget(server_connection, 0, 0)
main_layout.addWidget(connection_status, 0, 1)
main_layout.addWidget(file_loader, 1, 0)
main_layout.addWidget(print_options, 1, 1)
main_layout.addWidget(print_button, 3, 0, 1, 2)

server_connection.elements = [file_loader, print_options, print_button]

widget_impresion = QWidget()
widget_impresion.setLayout(main_layout)

main_window = MainWindow("ImpresionesDCC-GUI")
main_window.setCentralWidget(widget_impresion)
main_window.server_connection = server_connection

if __name__ == '__main__':
    main_window.show()
    app.exec()
