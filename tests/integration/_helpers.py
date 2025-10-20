import socket
import time

# Buffer persistente por socket
_buffers = {}  # key: id(sock) -> str con datos pendientes

def make_client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.0)
    sock.connect((host, port))
    _buffers[id(sock)] = ""            # inicializa buffer del socket
    return sock

def send_line(sock, text):
    data = (text + "\n").encode('utf-8')
    sock.sendall(data)

def recv_line(sock, timeout=1.0):
    """
    Lee hasta encontrar '\n' o agotar timeout.
    Devuelve la línea SIN el '\n' o None si no llegó nada completo.
    """

    deadline = time.monotonic() + timeout
    buf = _buffers.get(id(sock), "")

    while time.monotonic() < deadline:
        # Ya hay una linea completa en el buffer?
        if "\n" in buf:
            linea, buf = buf.split("\n", 1)
            _buffers[id(sock)] = buf
            return linea

        # Si no, leemos mas datos
        try:
            chunk = sock.recv(1024)

            if chunk == b"":
                # peer cerro; vaciamos buffer y devolvemos lo que haya
                _buffers.pop(id(sock), None)
                return None
            buf += chunk.decode('utf-8')

        except socket.timeout:
            # Se reintenta hasta el deadline
            continue

    # timeout sin linea completa, guardamos lo acumulado
    _buffers[id(sock)] = buf
    return None

def close_client(sock):
    # helper opcional para limpiar y cerrar
    try:
        sock.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    sock.close()
    _buffers.pop(id(sock), None)