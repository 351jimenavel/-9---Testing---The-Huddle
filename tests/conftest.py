import pytest
import socket

@pytest.fixture
def puerto_libre():
    # Hace: reserva un puerto efimero y lo devuelve.
    # Uso: evita choques entre tests.
    pass

@pytest.fixture
def server_en_marcha(puerto):
    pass
    # Hace: levanta el server en hilo/proceso; espera hasta que este listo.
    # Teardown: cierra ordenado y verifica que el puerto quede libre

@pytest.fixture
def cliente_factory(puerto):
    pass
    # Hace: Enviar(texto), recibir(timeout), cerrar(), cerrar_abrupto()