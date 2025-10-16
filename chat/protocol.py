def validate_message(texto): 
    ''' 
    Caso negativo: texto vacio o solo espacios (validacion falla) 
    Caso positivo minimo: 'hola' simple -> la validacion pasa 
    ''' 
    if type(texto) is not str: 
        return False 
    texto_normalizado = texto.strip() 
    if texto_normalizado == '': 
        return False 
    if 1 <= len(texto_normalizado) and len(texto_normalizado) <= 50: 
        return True 
    return False