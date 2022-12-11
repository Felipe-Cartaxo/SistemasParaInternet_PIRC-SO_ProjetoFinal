from appCliente import AppCliente                   # importando o Construtor de appCliente.py
import socket                                       # importando o módulo de Sockets

HOST = '0.0.0.0'                                    # ip definido para o servidor
PORT = 40000                                        # porta que servidor utilizará, definida pelo protocolo BTP

''' server = (HOST, PORT)                           # atribuindo o endereço e a porta à variável server '''
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # o Construtor do próprio módulo Socket que irá configurar os sockets utilizados no servidor, onde passamos como parâmetros AF_INET, que abrange os IPs do tipo IPv4, e SOCK_STREAM, que define os sockets de fluxo (?)
serverSock.bind(HOST, PORT)                         # método para atribuir um endereço IP e uma porta a uma instância de socket
serverSock.listen(10)                               # número máximo de conexões no server

while (True):
    try:
        connection, client = serverSock.accept()    # método para aceitar uma conexão recebida de um cliente
    except:
        break                                       # caso não for possível se conectar, o server tentará novamente

    app = AppCliente(connection, client)            # Construtor de appCliente.py
    app.start()                                     # inicia a thread de appCliente.py

serverSock.close()                                  # encerra a conexão com o cliente