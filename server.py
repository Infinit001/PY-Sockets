import os, socket, sys, threading, time

try:
    from config import *
    print("[DEBUG] Initialising Server Configs...")
    time.sleep(4)
    start_server = True
except:
    print("[DEBUG] Failed to load configs...")
    sys.exit()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[CONNECTION] {addr} Connected.")

    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    print(f"[CONNECTION] {addr} disconnected.")
                    connected = False
                    conn.close()
                elif msg == SHUTDOWN_MESSAGE:
                    print("[SERVER] Shutting Down...")
                    conn.sendall("[SERVER] Shutting down server...Connection Lost...".encode(FORMAT))
                    conn.close()
                    sys.exit()
                elif msg.split(" ")[0] == GET_COMMAND:
                    print(f"[{addr}] {msg}")
                    file = msg.split(" ")[1]
                    print(file)
                    path = f"C:/Users/Daniel/Documents/PY Sockets/{file}"
                    exists = os.path.exists(path)
                    if exists:
                        print("File found")
                        
                        bytes_read = bytearray()

                        with open(file, 'rb') as f:
                            for i in f.read():
                                bytes_read.append(i)

                                print(f"--{bytes_read}")

                                if not bytes_read:
                                    break
                            
                            print("SENDING INFO")
                            conn.sendall(f"{bytes_read}".encode(FORMAT))
                            print("BYTES SENT")
                    else:
                        print("File not found")
                        conn.sendall("File error".encode(FORMAT))
                    print(".")
                elif msg.split(" ")[0] == EXIST_COMMAND:
                    file = msg.split(" ")[1]
                    path = f"C:/Users/Daniel/Documents/PY Sockets/{file}"
                    exists = os.path.exists(path)
                    if exists:
                        conn.sendall(FILE_EXISTS_MESSAGE.encode(FORMAT))
                    else:
                        conn.sendall(NOT_FOUND_ERROR.encode(FORMAT))
                else:
                    conn.sendall(COMMAND_NOT_FOUND_ERROR.encode(FORMAT))

        except:
            print(f"[SERVER] Something went wrong with {addr}...Closing connection now...")
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}")
            conn.close()
            exit()
    conn.close()

def start():
    global started
    started = True
    server.listen()
    print(f"[SERVER] Listening on: {PORT} - {SERVER}")
    while started:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}")

if start_server == True:
    print("[CONFIG] Configs files loaded...")
    time.sleep(1)
    print("[SERVER] Booting up...")
    time.sleep(3)
    try:
        start()
        print(f"[SERVER] Successfully booted up as {SERVER}")
    except:
        print("[SERVER] Something went wrong...")
        print("[DEBUG] Cancelling startup...")
        sys.exit()