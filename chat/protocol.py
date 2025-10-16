MAX_LEN = 50
_CONTROL_CHARS = "\r\n\t"

def validate_message(texto): 
    ''' 
    Caso negativo: texto vacio o solo espacios (validacion falla) 
    Caso positivo minimo: 'hola' simple -> la validacion pasa 
    ''' 
    if not isinstance(texto, str):
        return False

    # Regla simple: prohibir caracteres de control para no romper el framing
    if any(c in texto for c in _CONTROL_CHARS):
        return False
    
    texto_normalizado = texto.strip() 
    if not texto_normalizado: 
        return False
    
    return 1 <= len(texto_normalizado) <= MAX_LEN