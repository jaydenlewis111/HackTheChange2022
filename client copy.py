import socket
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon


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
        window.setWindowTitle('ChatPink - The GUI Messenger')

        # make the window full screen
        #window.showFullScreen()

        window.setStyleSheet("background-color: #000000; color: #000000;")
        window.setWindowIcon(QIcon('pink.png')) 

        self.message_label = QLabel('Message to Translate:')
        self.input_area = QTextEdit()

        self.chat_label = QLabel('Translated Message:')
        self.chat_area = QTextEdit()


        # change font size of chat area
        font = self.chat_area.font()
        font.setPointSize(10)
        self.chat_area.setFont(font)

        #change font size of input area
        font = self.input_area.font()
        font.setPointSize(10)
        self.input_area.setFont(font)

        #change font size of message label 

        self.chat_area.setStyleSheet("background-color: #f4a7bb; color: #2c3e50; ")
        # change size of chat area

        self.input_area.setStyleSheet("background-color: #f4a7bb; color: #2c3e50;")

        self.chat_area.setFixedHeight(400)
        self.chat_area.setFixedWidth(400)
        



        self.chat_label.setStyleSheet("background-color: #000000; color: #f4a7bb;")
        font = self.chat_label.font()
        font.setPointSize(15)
        self.chat_label.setFont(font)

        self.message_label.setStyleSheet("background-color: #000000; color: #f4a7bb;")
        font = self.message_label.font()
        font.setPointSize(15)
        self.message_label.setFont(font)

        self.input_area.setReadOnly(False)
        self.chat_area.setReadOnly(True)




        self.send_button = QPushButton('->')
        self.send_button.setStyleSheet("border: 5px; border-radius: 6px; background-color: 'green'; color:#000000; font-size: 30px; font-weight: bold;")
        self.send_button.clicked.connect(self.write)
        self.send_button.setFixedSize(400, 50)
  

        self.stop_button = QPushButton('!')
        self.stop_button.setStyleSheet("border: 5px; border-radius: 6px; background-color: 'red'; color: #000000;  font-size: 30px; font-weight: bold;")
        self.stop_button.setFixedSize(400, 50)

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
        # Voice to text and send to server
        

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

