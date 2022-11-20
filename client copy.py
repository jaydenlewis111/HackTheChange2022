import socket
import threading
from PyQt5.QtWidgets import *

# Create client class with GUI using pyqt5
class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        # Create a socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

        # get nickname from user using pyqt5
        self.nickname = self.set_nickname()

        # Create GUI
        self.gui_done = False
        # self.gui_ready = threading.Event()
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()  
    
    def set_nickname(self):
        # Set nickname using pyqt5 with input validation
        app = QApplication([])
        nickname = QInputDialog.getText(None, 'Set nickname', 'Choose nickname:')[0]
        if nickname == '':
            nickname = 'Guest'
        return nickname

    def gui_loop(self):
        # Create GUI using pyqt5
        app = QApplication([])
        window = QWidget()
        window.setWindowTitle('Chat')
        self.chat_label = QLabel('Chat:')
        self.chat_area = QTextEdit()
        self.message_label = QLabel('Message:')
        self.input_area = QTextEdit()
        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.write)
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop)

        layout = QVBoxLayout()
        layout.addWidget(self.chat_label)
        layout.addWidget(self.chat_area)
        layout.addWidget(self.message_label)
        layout.addWidget(self.input_area)
        layout.addWidget(self.send_button)
        layout.addWidget(self.stop_button)

        window.setLayout(layout)
        window.show()

        self.gui_done = True
        self.running = True
        # self.gui_ready.set()

        app.exec_()

    def write(self):
        # Send message to server
        message = f'{self.nickname}: {self.input_area.toPlainText()}'
        self.client.send(message.encode('utf-8'))
        self.input_area.clear()

    def stop(self):
        self.running = False
        self.client.close()
        self.gui_done = False
        exit(0)

    def receive(self):
        # Receive message from server
        while self.running:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        # Update chat area and scroll to bottom
                        self.chat_area.append(message)
                        # self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum())
            except ConnectionAbortedError:
                break
            except:
                print('An error occured!')
                self.client.close()
                break 


def main():
    # Create client object and start GUI
    client = Client('127.0.0.1', 8080)
    # app = QApplication([])
    # window = QWidget()
    # window.setGeometry(100, 100, 500, 500)
    # window.setWindowTitle("Chat Client")

    # label = QLabel('Enter your nickname:')


    # window.show()
    # app.exec_()

if __name__ == '__main__':
    main()

