from chat.refact_server import Server
import pytest 

@pytest.fixture
def server_running():
    server = Server(host="127.0.0.1", port=0)
    server.start()
    host="127.0.0.1"
    port = server.port_real
    yield (host, port, server)
    server.stop()

