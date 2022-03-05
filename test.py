import unittest
from time import sleep
from unittest import TestCase
from socket import *


Host = '127.0.0.1'
Port = 50000


class Test_Client_Server(TestCase):

    def test_connection_broadcast(self):
        with socket(AF_INET, SOCK_STREAM) as server:
            '''Tests the connection to the server'''

            server.connect((Host, Port))
            server.send(b'NICK')  # The client send a message to the server
            nick = server.recv(1024)  # The client receive the b'NICK'
            self.assertEqual(nick, b'NICK')  # and then we check what we get what we want
            sleep(1)
            connected_to_msg = server.recv(1024)  # After we dealing with the nickname
            self.assertEqual(connected_to_msg, b"b'NICK' connected to the chat!\nConnected to the server")
            self.assertNotEqual(connected_to_msg, "NICK")
            sleep(3)
            
            server.send(b'hello everyone! i am NICK')
            hello = server.recv(1024)  # The client receive the b'NICK'
            self.assertEqual(hello, b'hello everyone! i am NICK')


    def test_participants(self):
            with socket(AF_INET, SOCK_STREAM) as server:
                '''Tests the PARTICIPANTS status after connecting'''
                server.connect((Host, Port))
                sleep(2)
                server.send(b"NICK")
                nick = server.recv(1024)
                self.assertEqual(nick, b'NICK')
                server.send(b"PARTICIPANTS")
                print(server.recv(10000))





if __name__ == '__main__':
    unittest.main()
