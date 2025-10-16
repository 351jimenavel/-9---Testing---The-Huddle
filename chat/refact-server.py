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
        self.running_flag = False
        self.lock = threading.Lock()                # proteger estructuras compartidas

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, 0))   # 0 = puerto efimero
        port_real = sock.getsockname()[1]
        sock.listen(20)
        sock.settimeout(0.5)        # para salir sin colgarse

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