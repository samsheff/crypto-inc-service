import sys
import socket

###################
#    Constants    #
###################

TIMEOUT = 5
EXIT_CODES = {
    'Wrong args':       111,
    'Need more args':   110,
    'Host unreachable': 104,
    'Bad answer':       103,
    'Flag not found':   102,
    'OK':               101,
}

####################
# Common Utilities #
####################

def usage_and_exit(exit_code):
    print("Usage: python checker.py [command] [args]\nCommands:\n  check [hostname] [port]\n  put [hostname] [port] [data] [flag_id]\n  get [hostname] [port] [id] [key]")
    exit(exit_code)
    
def connect_to_service(address, host):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        s.connect((address, port))

        return s
    except socket.error:
        print("Service is DOWN! Code: 104")
        exit(104)

####################
# Command Funtions #
####################

def check(address, port):
    connection = connect_to_service(address, port)
    data = connection.recv(1024)
    connection.close()
    
    if not data or data == "":
        print("Service gave bad answer! Code: 103")
        exit(103)
    else:
        print("Service is UP! Code: 101")
        exit(101)

def put(connection, put_data, flag_id):
    # Receive the banner and throw it away since we dont need it
    connection.recv(1024)

    # Connected, Send the command
    connection.send("put " + put_data + " " + flag_id)
    
    # Wait for the ID to be returned and print it
    data = connection.recv(1024)

    # Close the connection
    connection.close()
    
    if not data or int(data.strip()) < 1:
        print("Service gave bad answer! Code: 103")
        exit(103)
    else:
        print("Service Returned ID: " + data.strip())
        print("Service is UP! Code: 101")
        exit(101)

def get(connection, db_id, key):
    # Receive the banner and throw it away since we dont need it
    connection.recv(1024)

    # Connected, Send the command
    connection.send("get " + db_id + " " + key)
    
    # Wait for the ID to be returned and print it
    data = connection.recv(1024)

    # Close the connection
    connection.close()
    
    if not data or data == "":
        print("Service gave bad answer! Code: 103")
        exit(103)
    else:
        print("Service Returned Data: " + data.strip())
        print("Service is UP! Code: 101")
        exit(101)
    
    

####################
#       MAIN       #
####################
if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage_and_exit(110)
    else:
        command = sys.argv[1]

        if command == "check":
            if len(sys.argv) != 4:
                usage_and_exit(110)
            else:
                address, port = sys.argv[2], int(sys.argv[3])
                check(address, port)

        elif (command == "put"):
            if len(sys.argv) != 6:
                usage_and_exit(110)
            else:
                address, port = sys.argv[2], int(sys.argv[3])
                put_data, flag_id = sys.argv[4], sys.argv[5]

                connection = connect_to_service(address, port)
                
                put(connection, put_data, flag_id)
        elif (command == "get"):
            if len(sys.argv) != 6:
                usage_and_exit(110)
            else:
                address, port = sys.argv[2], int(sys.argv[3])
                db_id, key = sys.argv[4], sys.argv[5]

                connection = connect_to_service(address, port)
                
                get(connection, db_id, key)
