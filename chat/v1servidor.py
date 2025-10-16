
import socket
import threading        # threading ayuda implementar concurrencia a traves de hilos. Permite ejecutar multiples tareas simultaneamente dentro de un mismo programa.

# Se crea el socket del servidor
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 8080
socket_server.bind((host, port))

socket_server.listen()
print("---[SERVIDOR ACTIVO]---")
print(" ¡Esperando conexiones! ")

lista_de_clientes = []

'''En la version anterior el servidor actuaba como un receptor nada mas haciendo:
            print(f'{cliente_socket}:{addr} ha enviado el siguiente mensaje: {mensaje}')'''
            
#### Funcion manejar cliente:
def handle_clients(cliente_socket, addr):
    connected = True
# Mientras el cliente este conectado
    while connected:

        ### OBS: En el testeo de este codigo pude notar que si el cliente ingresa el mensaje 'salir', se rompe la conexion en el servidor
        ##### para el manejo de ese error voy a probar 'ConnectionResetError'
        ##### ConnectionResetError indica que un cliente cerro su conexion abruptamente (Ej: cerrando terminal, Ctrl+C, enviando mensaje 'salir')

        try:
            ## Escuchar los mensajes que envia
            mensaje = cliente_socket.recv(2048).decode('utf-8')     # formato de transformacion unicode de 8 bits
            if mensaje != '':
                print(f'[NEW MESSAGE] {addr} : {mensaje}')
                # Difundir mensaje a todos los clientes (BROADCAST)
                for cliente, _ in lista_de_clientes:
                    # DETALLE: que solo les aparezca a los demas clientes, no a uno mismo
                    if cliente != cliente_socket:
                        # mostrar mensaje
                        try:
                            cliente.send(f'{addr}: {mensaje}'.encode())
                        except ConnectionResetError:
                            print(f'[!] Error al enviar mensaje a {cliente}, eliminando')
                            # Practicar manejo de errores (EJ: eliminar al cliente de la lista si se cierra conexion, verificar que este en la lista, etc)
                            # antes de eliminar cliente, verificar si esta en la lista
                            try:
                                lista_de_clientes.remove((cliente,addr))
                            except ValueError:  # error que se lanza cuando intentas usar un valor con el tipo correcto pero contenido incorrecto
                                pass
                            print(f'[i] Total de clientes conectados: {len(lista_de_clientes)}')

            ## Si el mensaje es 'salir', cortar conexion y salir del hilo
            ### Seguimos practicando manejo de errores con respecto a remover un cliente si se cierra conexion
            if mensaje.lower() == 'salir':
                print(f'[!] Cerrando conexion de {addr}')
                cliente_socket.close()
                try:
                    lista_de_clientes.remove((cliente_socket, addr))
                except ValueError:
                    print('[!] Ese cliente ya no estaba en la lista (probablemente se ha desconectado)')
                connected = False       # para romper el loop
                print(f'[i] Total de clientes conectados: {len(lista_de_clientes)}')
        
        except (ConnectionResetError, KeyboardInterrupt, EOFError):
            print(f'[!] {addr} se desconecto inesperadamente')
            try:
                lista_de_clientes.remove((cliente_socket, addr))
            except ValueError:
                pass
            cliente_socket.close()
            print(f'[i] Total de clientes conectados: {len(lista_de_clientes)}')
            connected = False

## Mientras el servidor este corriendo:
while True:
    ### Aceptar una nueva conexion (cliente y direccion)
    cliente, address = socket_server.accept()
    print(f'[NEW CONNECTION ESTABLISHED] {address}')
    print(f'[i] Total de clientes conectados: {len(lista_de_clientes)+1}')
    ### Crear un hilo nuevo que se encargue de ese cliente
    thread_clients = threading.Thread(target=handle_clients, args=(cliente, address))
    thread_clients.start()
    ### El hilo tendra la tarea de ejercutar una funcion que maneje solo a ese cliente.

    #### Llevar registro de todos los clientes conectados 
    lista_de_clientes.append((cliente, address))
