import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from socket import AF_INET, SOCK_DGRAM

Host = '127.0.0.1'
Port = 50000
format_ = 'utf-8'


class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        # message box that will ask for the nickname of the user
        message = tkinter.Tk()
        message.withdraw()

        self.nickname = simpledialog.askstring("Login", "Please choose your nickname to the chat", parent=message)

        # just a way to tell you that the GUI in not ready yet
        self.gui_done = False
        self.running = True  # will became False when we want to stop everything

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title("Welcome to our chat")
        self.win.configure(bg="lightgray", width=50)
        self.win.eval('tk::PlaceWindow . center')

        self.chat_lable = tkinter.Label(self.win, text="WhatsApp", bg="lightgray")
        self.chat_lable.config(font=("Ariel", 12))
        self.chat_lable.pack(padx=12, pady=2)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=12, pady=2)
        self.text_area.config(state='disabled')

        self.msg_lable = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_lable.config(font=("Ariel", 12))
        self.msg_lable.pack(padx=12, pady=2)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=12, pady=2)

        # send to everyone
        self.send_everyone_button = tkinter.Button(self.win, text="Send Message", command=self.write_everyone)
        self.send_everyone_button.config(font=("Ariel", 8))
        self.send_everyone_button.pack(padx=12, pady=2)

        # end_the_chat ||  CLOSE SOCKET
        tkinter.Button(self.win, text="Quit", font=("Ariel", 8), padx=12, pady=2, command=self.end_of_chat).pack()

        # list of participant
        tkinter.Button(self.win, text="PARTICIPANTS", font=("Ariel", 8), padx=12, pady=2,
                       command=self.show_participant).pack()

        # list of files
        tkinter.Button(self.win, text="List Of Files", font=("Ariel", 8), padx=12, pady=2,
                       command=self.show_files).pack()

        tkinter.Button(self.win, text="Get File", font=("Ariel", 8), padx=12, pady=2,
                       command=self.get_file).pack()

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    # handling with messages that we get from the server
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode(format_)
                if message == 'NICK':
                    self.sock.send(self.nickname.encode(format_))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except:
                print("Error!")
                self.sock.close()


    def write_everyone(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode(format_))
        self.input_area.delete('1.0', 'end')

    def show_participant(self):
        msg = "PARTICIPANTS"
        self.sock.send(msg.encode(format_))

    def end_of_chat(self):
        message = f"{self.nickname} left the chat"
        self.sock.send(message.encode(format_))
        self.win.destroy()
        self.sock.close()

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def show_files(self):
        msg = "show_files"
        self.sock.send(msg.encode(format_))

    def get_file(self):
        msg = f" # {self.input_area.get('1.0', 'end')} "
        self.sock.send(msg.encode(format_))
        self.input_area.delete('1.0', 'end')

       # add the udp part


client = Client(Host, Port)
