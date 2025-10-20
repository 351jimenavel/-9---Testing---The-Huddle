import threading
import socket
from .registry import ClientRegistry
from .protocol import validate_message

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
        # Apagar accept loop
        self.running_flag.clear()
        try:
            if self.sock_servidor:
                self.sock_servidor.close()
        except OSError:
            pass

        # Esperar el hilo receptor
        if self.accept_thread:
            self.accept_thread.join(timeout=1.0)

        # Cerrar todos los clientes y limpiar estructuras
        with self.lock:
            for cid, sock in list(self.sockets_por_id.items()):
                try:
                    sock.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                try:
                    sock.close()
                except OSError:
                    pass
                self.registry.remove(cid)
            self.sockets_por_id.clear()
            self.clients_thread.clear()


    def accept_loop(self):
        while self.running_flag.is_set():
            try:
                cliente_sock, addr = self.sock_servidor.accept()
            except socket.timeout:
                continue
            except OSError:
                # socket de server cerrado durante stop()
                break

            cliente_sock.settimeout(1.0)

            # id simple incremental (suficiente para tests)
            with self.lock:
                self._id_counter += 1
                client_id = f"c{self._id_counter}"
            
            if not self.registry.add(client_id):
                try:
                    cliente_sock.close()
                except OSError:
                    pass
                continue

            with self.lock:
                self.sockets_por_id[client_id] = cliente_sock

            t = threading.Thread(target=self.client_loop, args=(client_id, cliente_sock), daemon=True)
            with self.lock:
                self.clients_thread[client_id] = t
            t.start()

    def client_loop(self, client_id, client_sock):
        buffer = "" # acumulador de texto para framing por '\n'
        while self.running_flag.is_set():
            try:
                data = client_sock.recv(1024)
                if data == b"":
                    break
                buffer += data.decode("utf-8", errors="replace")

                while "\n" in buffer:
                    linea, buffer = buffer.split("\n", 1) # SIN incluir el '\n'
                    mensaje = linea

                    # Validar con tu protocolo antes de difundir
                    if validate_message(mensaje):
                        self.broadcast(from_id=client_id, text=mensaje)
                    else:
                        # opcional: avisar error al emisor
                        client_sock.sendall(b"ERROR: invalid message\n")
                        pass

            except socket.timeout:
                continue
            except (ConnectionResetError, OSError):
                break

        # Limpieza siempre al salir del loop
        self.cleanup_client(client_id, client_sock)

    def broadcast(self, from_id, text):
        mensaje = (text + "\n").encode("utf-8")

        # Tomar snapshot seguro de los sockets actuales
        with self.lock:
            destinos = list(self.sockets_por_id.items())

        for dest_id, sock in destinos:
            if dest_id == from_id:
                continue
            try:
                sock.sendall(mensaje)
            except (socket.timeout, ConnectionResetError, OSError):
                # si un envio falla, limpiamos ese cliente y seguimos
                self.cleanup_client(dest_id, sock)
                continue

    def cleanup_client(self, client_id, sock):
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            sock.close()
        except OSError:
            pass

        self.registry.remove(client_id)
        with self.lock:
            self.sockets_por_id.pop(client_id, None)
            self.clients_thread.pop(client_id, None)