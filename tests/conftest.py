import pytest
import socket

@pytest.fixture
def puerto_libre():
    '''
    Hace: reserva un puerto efimero y lo devuelve.
    Uso: evita choques entre tests.
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))                          # el sistema operativo asignará uno automáticamente
    puerto_asignado = sock.getsockname()[1]     # get sock name devuelve la direccion IP y el puerto por eso puse [1] para que sea solo el puerto
    return puerto_asignado

@pytest.fixture
def server_en_marcha(puerto):
    '''
    Hace: levanta el server en hilo/proceso; espera hasta que este listo.
    Teardown: cierra ordenado y verifica que el puerto quede libre
    '''
    pass

@pytest.fixture
def cliente_factory(puerto):
    '''
    Hace: Enviar(texto), recibir(timeout), cerrar(), cerrar_abrupto()
    '''
    pass