import os
import socket
import threading

Host = '127.0.0.1'
Port = 50000
format_ = 'utf-8'


# if there are 2 dots so the message to someone, if its 1 so its to everybody
def check_count_dots(msg_str: str) -> int:
    count = 0
    for char in msg_str:
        if char == ':':
            count += 1
    return count


# check the number of Tag (#) will tell the server that we want to send a file
def check_count_tag(msg_str: str) -> int:
    count = 0
    for char in msg_str:
        if char == '#':
            count += 1

    return count


class Server:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()

        self.clients = []
        self.nicknames = []
        self.files = os.listdir("files")  # put all the files  "files" directory in a list

        print("Server is running..")
        self.receive()

    # handle the connection to the client
    def handle(self, client):
        stop = False
        while not stop:
            try:
                message = client.recv(1024)
                msg_st = str(message)
                msg_spilt_by_space = msg_st.split(" ")
                if message == f"{msg_spilt_by_space[0]} left the chat".encode(format_):
                    stop = True

                elif message == "show_files".encode(format_):
                    self.show_files(client)

                elif message == "PARTICIPANTS".encode(format_):
                    self.nickNam(client)

                elif check_count_dots(msg_st) > 1:

                    msg_spilt = msg_st.split(':')
                    nick_name_dest = msg_spilt[1].replace(" ", "")
                    nick_name_sender = msg_spilt[0].replace(" ", "")
                    nick_name_index = self.find_index_nickname(nick_name_dest)
                    message_to_send = msg_spilt[2]
                    self.broadcast_someone(nick_name_index, message_to_send, nick_name_sender, client)

                elif check_count_tag(msg_st) > 0:
                    msg_spilt = msg_st.split(' ')
                    file = msg_spilt[2].replace(" ", "")
                    self.send_file(file[:-2], client)

                else:
                    self.broadcast(message)

            # we will want to remove the client from the clients list and his nickname
            except:
                pass

        # if the user quit the app
        index = self.clients.index(client)
        self.clients.remove(index)
        nickname = self.nicknames[index]
        self.broadcast('{} left!'.format(nickname).encode('ascii'))
        self.nicknames.remove(nickname)
        client.close()

    # will accepts new connection
    def receive(self):
        while True:
            client, addr = self.server.accept()
            print(f"Connected with{str(addr)}")

            # Asking for a nickname of the client
            # if the message that i just got is "NICK" its going to answer with a nickname that the client will choose
            client.send("NICK".encode(format_))
            nickname = client.recv(1024)
            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f"The Nickname is:{nickname}")
            self.broadcast(f"{nickname} connected to the chat!\n".encode(format_))
            # send a message to the client that just got connected
            client.send("Connected to the server".encode(format_))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    # giving the nickname, this function will return its index on nicknames list
    def find_index_nickname(self, nickname: str) -> int:
        nickname_ = nickname.encode(format_)
        for index in range(len(self.nicknames)):
            if self.nicknames[index] == nickname_:
                return index
        else:
            return -1

    # send message to all clients that are connected
    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    # send a message to a specific person
    def broadcast_someone(self, nick_name_index: int, message_to_send: str, nick_name_sender, client_sender):
        for index in range(len(self.clients)):
            if index == nick_name_index:
                client = self.clients[index]
                client.send(f"{nick_name_sender}:{message_to_send}\n".encode(format_))
                client_sender.send(f"{nick_name_sender}:{message_to_send}\n".encode(format_))
                client.send("\n".encode(format_))
                break

    # function that will show on the screen of the chat the PARTICIPANTS that connecting to the chat
    def nickNam(self, client):
        client.send("PARTICIPANTS: ".encode(format_))
        for n in self.nicknames:
            client.send(n)
            client.send(",".encode(format_))
        client.send("\n".encode(format_))

    # function that will show on the screen of the chat the files that  are available to download
    def show_files(self, client):
        client.send("FILES: ".encode(format_))
        for f in self.files:
            client.send(f"{f}".encode(format_))
            client.send(",".encode(format_))
        client.send("\n".encode(format_))

    def send_file(self, filename, client):
        flag = False
        for f in self.files:
            if f == filename:
                flag = True
                client.send(f"{filename}: exist! \n".encode(format_))

        if not flag:
            client.send(f"{filename}: not exist \n".encode(format_))

        # if the file exist
       # else:








server = Server(Host, Port)
