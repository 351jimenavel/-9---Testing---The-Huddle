import pytest
from chat.protocol import validate_message

# Tests negativos
def test_mensaje_vacio_rechazado():
    assert not validate_message("")

def test_solo_espacios_rechazado():
    assert not validate_message("   ")

def test_muy_largo_rechazado():
    assert not validate_message("a" * 51)

def test_controles_rechazados():
    assert not validate_message("hola\n")
    assert not validate_message("\t hola")

# Tipos no str
def test_no_str_rechazado():
    assert not validate_message(None)
    assert not validate_message(123)
    assert not validate_message([])

def test_concatenacion_al_borde_rechazado():
    assert not validate_message(" " + "a"*51 + " ")

# Positivos
def test_mensaje_valido_aceptado():
    assert validate_message("hola mundo")

def test_mensaje_valido_con_espacios_borde():
    assert validate_message("  hola  ")

def test_largo_exactamente_50():
    assert validate_message("a" * 50)

# 2. Tests
## Bordes de longitud
def test_concatenacion_al_borde_aceptado():
    assert validate_message(" " + "a"*50 + " ") 

# Unicode
def test_acentos_aceptado():
    assert validate_message("canción número veintidós")

def test_emoji_aceptado():
    assert validate_message("hola 🙂")

def test_acento_y_longitud_aceptado():
    assert validate_message("á"*50)