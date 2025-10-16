import socket
import time

def make_client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.0)
    sock.connect((host, port))
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
    buffer = ""

    while time.monotonic() < deadline:
        try:
            chunk = sock.recv(1024)

            if chunk == b"":
                return None
            buffer += chunk.decode('utf-8')

            if "\n" in buffer:
                linea, _resto = buffer.split("\n", 1)
                return linea
        except socket.timeout:
            continue
    return None