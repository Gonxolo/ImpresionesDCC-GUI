from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,  QFileDialog, QLabel, QVBoxLayout, QMainWindow, QLineEdit, QGridLayout, QHBoxLayout, QGroupBox

app = QApplication([])
app.setApplicationName("ImpresionesDCC")

server_field = QLineEdit("anakena.dcc.uchile.cl")
user_field = QLineEdit()
password_field = QLineEdit()

server_label = QLabel("Servidor:")
server_label.setBuddy(server_field)
user_label = QLabel("Usuario:")
user_label.setBuddy(user_field)
password_label = QLabel("Contraseña:")
password_label.setBuddy(password_field)

connection_layout = QVBoxLayout()
connection_layout.addWidget(server_label)
connection_layout.addWidget(server_field)
connection_layout.addWidget(user_label)
connection_layout.addWidget(user_field)
connection_layout.addWidget(password_label)
connection_layout.addWidget(password_field)

connection_group = QGroupBox("Conexión al servidor")
connection_group.setLayout(connection_layout)

connection_status = QLabel("Aqui se señalará el estado de la conexion.\nExitosa, Fallida, Desconectadx, etc.\n(quizas se mostraran los errores con la conexion idk)")

connection_status_layout = QVBoxLayout()
connection_status_layout.addWidget(connection_status)

connection_status_group = QGroupBox("Estado de la conexión")
connection_status_group.setLayout(connection_status_layout)

load_file_button = QPushButton("Load File...")
file_path = None
file_name = QLabel("No hay ningun archivo cargado.")

def load_file():
    global file_path
    global file_name
    path = QFileDialog.getOpenFileName(window, "Load")[0]
    print(path)
    if path:
        file_path = path
        file_name.setText(f"Ruta del archivo cargado:\n{path}")

load_file_button.clicked.connect(load_file)

load_file_layout = QVBoxLayout()
load_file_layout.addWidget(load_file_button)
load_file_layout.addWidget(file_name)

load_file_group = QGroupBox("Selección del archivo a imprimir")
load_file_group.setLayout(load_file_layout)

print_place_layout = QVBoxLayout()

print_faces_layout = QVBoxLayout()

print_options_layout = QGridLayout()

print_options_group = QGroupBox("Opciones de impresión")
print_options_group.setLayout(print_options_layout)

print_button = QPushButton("Imprimir")

main_layout = QGridLayout()
main_layout.addWidget(connection_group, 0, 0)
main_layout.addWidget(connection_status_group, 0, 1)
main_layout.addWidget(load_file_group, 1, 0, 1, 2)
main_layout.addWidget(print_options_group, 2, 0, 1, 2)
main_layout.addWidget(print_button, 3, 0, 1, 2)

widget_impresion = QWidget()
widget_impresion.setLayout(main_layout)

window = QMainWindow()
window.setWindowTitle("ImpresionesDCC")
window.setCentralWidget(widget_impresion)


if __name__ == '__main__':
    window.show()
    app.exec()