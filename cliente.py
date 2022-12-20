import socket
import sys

MESSAGE_SIZE = 1024                             # tamanho do bloco de mensagem
HOST = '127.0.0.1'                              # ip do servidor
PORT = 40000                                    # porta que o servidor escuta

def decodeCommandUser(commandUser):
    commandList = {
        'down': 'get',                          # faz download de um arquivo
        'cd': 'cwd',                            # muda de diretório
        'ls': 'list',                           # lista os arquivos em um diretório
        'exit': 'quit',                         # encerra a conexão com o servidor
        'cat': 'read',                          # mostra o conteúdo de um arquivo
        'mkdir': 'makedir',                     # cria um diretório
        'pwd': 'path',                          # mostra o caminho do diretório atual
        'up': 'add'                          # faz upload de um arquivo
    }

    tokens = commandUser.split()
    if (tokens[0].lower()) in commandList:
        tokens[0] = commandList[tokens[0].lower()]
        return " ".join(tokens)
    else:
        return False

if (len(sys.argv) > 1):
    HOST = sys.argv[1]

print('-'*50)                                   # menu inicial
print('Servidor FTP - Projeto Final SO/PIRC')
print('-'*50)

print('O servidor possui as seguintes funções:\n\n- GET:      Solicita o download de um arquivo\n- ADD:      Realiza o upload de um arquivo:\n- CWD:      Altera o diretório atual do servidor\n- LIST:     Solicita a lista de arquivos/diretórios\n- QUIT:     Encerra a conexão com o servidor')
print('-'*50)

print('Dados do servidor:', HOST+':'+str(PORT))
server = (HOST, PORT)
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.connect(server)

print('Para encerrar a conexão, use o comando "EXIT" ou pressione CTRL+C')

while (True):
    try:
        print('-'*50)
        commandUser = input('\nComando >>> ')
    except:
        commandUser = 'EXIT'
    command = decodeCommandUser(commandUser)

    if not command:
        print('Comando "{}" não existe.'.format(commandUser))
    else:
        serverSock.send(str.encode(command))
        data = serverSock.recv(MESSAGE_SIZE)
        if not data:
            break
        messageStatus = data.decode().split('\n')[0]
        data = data[len(messageStatus)+1:]

        print(messageStatus)
        command = command.split()
        command[0] = command[0].upper()
        if (command[0] == 'QUIT'):
            break
        elif (command[0] == 'READ'):
            fileName = ' '.join(command[1:])
            fileSize = int(messageStatus.split()[1])
            print('\nConteúdo do arquivo "{}":'.format(fileName))
            while (fileSize > 0):
                data = serverSock.recv(MESSAGE_SIZE)
                fileSize -= len(data)
                data = data.decode()
                print(data)
        elif (command[0] == 'GET'):
            fileName = ' '.join(command[1:])
            fileSize = int(messageStatus.split()[1])
            print('Recebendo:', fileName)
            with open(fileName, 'wb') as file:
                while (True):
                    data = serverSock.recv(1024)
                    file.write(data)
                    fileSize -= len(data)
                    if (fileSize == 0):
                        break
        elif (command[0] == 'LIST'):    #****AJUSTE ESSA PARTE DO CODIGO PARA FICAR COM OS MESMOS NOMES DAS VARIÁVEIS
            fileName = int(messageStatus.split()[1])
            data = data.decode()
            while (True):
                arquivos = data.split('\n')
                residual = arquivos[-1]      
                for arq in arquivos[:-1]:
                    print(arq)
                    fileName -= 1
                if fileName == 0:
                    break
                data = serverSock.recv(MESSAGE_SIZE)
                if not data:
                    break
                data = residual + data.decode()
            '''fileNum = int(messageStatus.split()[1])
            data = data.decode()
            while (True):
                files = data.split('\n')
                filesRemain = files[-1]
                for file in files[:-1]:
                    print(file)
                    fileNum -= 1
                    if (fileNum == 0):
                        break
                    data = serverSock.recv(MESSAGE_SIZE)
                    if not data:
                        break
                    data = filesRemain + data.decode()'''
        elif (command[0].upper() == 'ADD'):
            text = None
            print('Digite "end" (sem as aspas) numa linha em branco e pressione ENTER para enviar o texto.\n')
            print('Insira o texto abaixo:')
            while (text != 'end'):
                text = input()
                serverSock.send(str.encode(text))

serverSock.close()