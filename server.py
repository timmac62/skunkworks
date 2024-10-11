import socket
import select

# Server setup
def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Define the host and port
    host = '127.0.0.1'
    port = 12345

    # Bind the socket to the address and port
    server_socket.bind((host, port))

    # Server listens for incoming connections
    server_socket.listen(5)
    server_socket.setblocking(False)
    print(f"Non-blocking server started on {host}:{port}")

    # List of sockets to monitor for reading
    sockets_list = [server_socket]

    # Dictionary to store client sockets and their addresses
    clients = {}

    while True:
        # Use select to wait for sockets to be ready for reading
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

        # Iterate through readable sockets
        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                # New connection
                client_socket, client_address = server_socket.accept()
                print(f"Accepted new connection from {client_address}")
                client_socket.setblocking(False)
                sockets_list.append(client_socket)
                clients[client_socket] = client_address
            else:
                # Receive message from a connected client
                try:
                    message = notified_socket.recv(1024)
                    if message:
                        print(f"Received message from {clients[notified_socket]}: {message.decode('utf-8')}")
                        # Echo the message back
                        notified_socket.send(message)
                    else:
                        # Client disconnected
                        print(f"Closed connection from {clients[notified_socket]}")
                        sockets_list.remove(notified_socket)
                        del clients[notified_socket]
                except:
                    continue

        # Handle exceptional sockets
        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]

if __name__ == "__main__":
    start_server()
