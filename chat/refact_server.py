import threading
import socket
from registry import ClientRegistry

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port_inicial = port
        self.registry = ClientRegistry(100)
        self.sockets_por_id = {}    # dict[id -> socket] ; mapa útil para broadcast
        self.clients_thread = {}    # dict[id -> Thread] ; control de hilos cliente
        self._id_counter = 0
        self.lock = threading.Lock()                # proteger estructuras compartidas

        self.running_flag = threading.Event()
        self.sock_servidor = None
        self.port_real = None
        self.accept_thread = None

    def start(self):
        self.sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Opcional: en Win a veces no hace falta, pero no molesta
        self.sock_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sock_servidor.bind((self.host, self.port_inicial or 0))   # Puerto 0 => efimero; si pasan uno fijo, se use self.port_inicial
        self.port_real = self.sock_servidor.getsockname()[1]
        self.sock_servidor.listen(20)
        self.sock_servidor.settimeout(0.5)        # para salir sin colgarse

        self.running_flag.set()
        self.accept_thread = threading.Thread(target=self.accept_loop, daemon=True)
        self.accept_thread.start()
        
    def stop(self):
        pass

    def accept_loop(self):
        pass

    def client_loop(self, client_id, client_sock):
        pass

    def broadcast(self, from_id, text):
        pass

    def cleanup_client(self, client_id, sock):
        pass