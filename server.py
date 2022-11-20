import socket
import threading
from googletrans import Translator

HOST = '127.0.0.1'
PORT = 8080

# Creata a chat server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# List of clients and their names
clients = []
nicknames = []

# Broadcast messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle messages from clients
def handle(client):
    while True:
        try:
            # Broadcast messages
            message = client.recv(1024).decode('utf-8')
            print(f"{message}")
            nickname = nicknames[clients.index(client)]
            message = message[len(nickname)+2:]

            # Translate message to English
            translator = Translator()
            # Detect language full name
            lang = translator.detect(message).lang
            
            message = translator.translate(message, dest='en').text
            # print(f"{nickname}: {message}")

            # Broadcast message
            print(f"{nickname} says {message}")
            # broadcast(message)
            # convert f-string to string

            broadcast(f"{nickname} says in {lang.upper()}: {message}".encode('utf-8'))

        except:
            # Remove and close clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# Receive / broadcast messages
def receive():
    while True:
        # Accept connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request and store nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Print and broadcast nickname
        print(f"Nickname of the client is {nickname}!")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        # Start handling thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")

receive()