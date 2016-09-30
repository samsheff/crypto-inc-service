# -*- coding: utf-8 -*-
import SocketServer
from pg import DB

WIDTH = 26
ASC_A = ord('A')

class Cryptoservice(SocketServer.BaseRequestHandler):
    
    # Handle a new connection
    def handle(self):
            # Connect to the database
            db = DB(dbname='crypto', user='docker', passwd='docker')
            
            # Print Welcome Message
            self.request.send("Welcome to Crypto Inc.'s Cryptographic Service.\nCommands:\n put [data] [key]\n get [id] [key]\n>>> ")
            
            # Split Request into its different components
            command, arguments = self.request.recv(1024).strip().partition(' ')[0::2]
            arguments = arguments.split(' ')
            
            # Init a blank list for our key
            key = []
            
            # New Data, generate a key and add it to the database, returns the id
            if (command == "put"):
                key = self.generate_key(arguments[1])
                ciphertext = self.encrypt(key, arguments[0])
                
                db.query("INSERT INTO data(key, encrypted_data) VALUES ('" + str(key[0]) + ',' + str(key[1]) + "', '" + ciphertext + "');")
                result = db.query("SELECT COUNT(*) FROM data;").dictresult()
                self.request.sendall(str(result[0]["count"]) + "\n")
            
            # Retreives Saved Data, get the key decrypt the stored data
            elif (command == "get"):
                for part in arguments[1].split(','):
                    key.append(int(part))
                
                records = db.query("SELECT * FROM data WHERE id = '" + arguments[0] + "'").dictresult()
                self.request.sendall(self.decrypt(key, records[0]["encrypted_data"]))

    #
    # Cipher related functions below
    #

    def generate_key(self, flag_id):
        return [int(sum(bytearray(flag_id[5:9])) % WIDTH) + 1, int(sum(bytearray(flag_id[0:4])) % WIDTH) + 1]

    def encrypt(self, key, words):
        return ''.join([self.shift(key, ch) for ch in words.upper()])

    def decrypt(self, key, words):
        a, b = self.modInverse(key[0], WIDTH), -key[1]
        return ''.join([self.unshift([a, b], ch) for ch in words.upper()])

    def shift(self, key, ch):
        if str.isalpha(ch):
            offset = ord(ch) - ASC_A
            return chr(((key[0] * offset + key[1]) % WIDTH) + ASC_A)
        return ''

    def unshift(self, key, ch):
        offset = ord(ch) - ASC_A
        return chr(((key[0] * (offset + key[1])) % WIDTH) + ASC_A)

    def gcd(self, a, b):
        while a != 0:
            a, b = b % a, a
        return b

    def modInverse(self, a, m):
        if self.gcd(a, m) != 1:
            print("Error")
        u1, u2, u3 = 1, 0, a
        v1, v2, v3 = 0, 1, m
        while v3 != 0:
            q = u3 // v3
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % m

# Main Function if we're not being required
if __name__ == "__main__":

    HOST, PORT = "0.0.0.0", 7777

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), Cryptoservice)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
