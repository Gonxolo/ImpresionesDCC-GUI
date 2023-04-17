from PyQt5.QtWidgets import QLabel, QVBoxLayout, QGroupBox

class ConnectionStatus(QGroupBox):

    def __init__(self, title="Estado de la conexión"):
        super().__init__(title)

        self.isConnected = False

        self.connection_status = QLabel("Desconectado del servidor.")

        connection_status_layout = QVBoxLayout()
        connection_status_layout.addWidget(self.connection_status)

        self.setLayout(connection_status_layout)
    
    def try_connect(self, user, server):
        msg = f"Intentando conectar a {server} como {user} ...\n"
        msg += f"[Comando ejecutado: ssh {user}@{server}]"
        self.connection_status.setText(msg)
    
    def connection_error(self, err):
        msg = f"Ocurrió un error al intentar conectarse:\n{err}"
        self.connection_status.setText(msg)

    def connection_success(self, user, server):
        msg = "Conexión exitosa!\n"
        msg += f"Conectado a {server} como {user}"
        self.connection_status.setText(msg)
    
    def connection_closed(self):
        msg = "Conexión cerrada.\n"
        self.connection_status.setText(msg)