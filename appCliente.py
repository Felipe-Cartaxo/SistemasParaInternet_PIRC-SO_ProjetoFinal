import btpProtocolv2                                # importando 
from threading import Thread                        # importando o módulo de Threads

class AppCliente(Thread):                           # Construtor 
    def __init__(self, connection, client):
        super.__init__()
        self.connection = connection                # especifica o socket do cliente ao ser chamada pelo método accept
        self.client = client                        # especifica o ip do cliente ao ser chamada pelo método accept
    
    def run(self):
        print(f'Cliente {self.client} conectado!')  # mensagem que será exibida caso um cliente consiga se conectar com o servidor

        while(True):
            message = self.connection.recv(1024)
            if ((message == False) or (btpProtocolv2.processing(message, self.client))):                # caso o cliente encontre problemas para se conectar, será então feito outra tentativa de se conectar
                break

        self.connection.close()                      # encerra a conexão
        print(f'Cliente {self.client} desconectado!') # mensagem que será exibida caso um cliente se desconecte do servidor