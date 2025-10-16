import pytest
from chat.protocol import validate_message

def test_mensaje_vacio_rechazado():
    assert validate_message("")

def test_solo_espacios_rechazado():
    assert validate_message("   ")

def test_muy_largo_rechazado():
    assert validate_message("a" * 51)

def test_controles_rechazados():
    assert validate_message("hola\n")
    assert validate_message("\t hola")

def test_no_str_rechazado():
    assert validate_message(None)
    assert validate_message(123)

def test_mensaje_valido_aceptado():
    assert validate_message("hola mundo")

def test_mensaje_valido_con_espacios_borde():
    assert validate_message("  hola  ")

def test_largo_exactamente_50():
    assert validate_message("a" * 50)
