
import socket
import threading
## DESDE EL CLIENTE
# 5. El cliente crea su propio socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 6. El cliente conecta su socket a la misma direccion IP y puerto colocado en el servidor (se establece conexion)
host = '127.0.0.1'
port = 8080
client_socket.connect((host, port))
print('CONECTADO AL SERVIDOR')
# El cliente tendra hilos para
## 1) Enviar mensajes al servidor (lo que el usuario va a escribri)
def enviar_mensaje(cliente_socket):
    ## Opcion para salir del chat con comando o escribiendo "salir"
    while True:
        try:
            mensaje = input()
        except EOFError:
            print("[ERROR] Se cerro la entrada.")
            break
    ## Mientras no se haya escrito esto: pedir al usuario que escriba algo y enviar eso al servidor
        if mensaje != '':
            print(f'[<<] ME: {mensaje}')
            client_socket.send(mensaje.encode('utf-8'))     # formato de transformacion unicode de 8 bits
        else:
            print('[i] El mensaje enviado por el cliente esta vacio')
    ## Si el mensaje es salir
        ## cerrar socket
        ## terminar hilo
        if mensaje == 'salir':
            print('[BYE] Cerrando conexion...')
            cliente_socket.close()
            break

## 2) Recibir mensajes desde el servidor
def recibir_mensaje(cliente_socket):
    ## estar siempre escuchando
    while True:
        try:
            response = client_socket.recv(2048).decode('utf-8')
            if response:
                ## mostrar los mensajes recibidos del servidor
                print(f'[>>] Mensaje recibido de {response}')
            else:
                print('[BYE] Cerrando conexion')
                cliente_socket.close()
                break
        except (ConnectionError, OSError):
            print('[ERROR] Se perdio la conexion con el servidor')
            cliente_socket.close()
            break

thread_envio = threading.Thread(target=enviar_mensaje,args=(client_socket,))
thread_recepcion = threading.Thread(target=recibir_mensaje, args=(client_socket,))
thread_envio.start()
thread_recepcion.start() 
