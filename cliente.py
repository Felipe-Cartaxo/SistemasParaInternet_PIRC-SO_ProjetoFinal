import socket
import sys

MESSAGE_SIZE = 1024                             # tamanho do bloco de mensagem
HOST = '127.0.0.1'                              # ip do servidor
PORT = 40000                                    # porta que o servidor escuta

def decodeCommandUser(commandUser):
    commandList = {
        'down': 'get',
        'cd': 'cwd',
        'ls': 'list',
        'exit': 'quit',
        'cat': 'read',
        'mkdir': 'crdir',
        'pwd': 'path',
        'touch': 'add'
    }

    tokens = commandUser.split()
    