import os, socket, sys, threading, time
from config import *

# from art import text2art


# def print_welcome():
#     welcome_text = text2art("RUNNING", "block")
#     print(welcome_text)
#     print(" /-----FILE TRANSMITTING SERVER-----/")


# ------ DEFINE SERVER ------#
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# ------ INITIATE SERVER ------#
server.bind(ADDR)


# ------ UPLOAD FUNCTION ------#
def upload(filename: str, content: str):
    pass


# ------ HANDLE THE CLIENT ------#
# ------ FUNCTION ------#
def handle_client(conn, addr):
    print(f"****PROCESSING REQUEST FROM {addr} ****")
    print(f"[CONNECTION] {addr} Connected.")

    # ------ WHEN CLIENT CONNECTED ------#
    connected = True
    while connected:
        try:
            # ------ GET MESSAGE LENGTH ------#
            #### SEND MESSAGE ####
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)

                #### DISCONNECT MESSAGE HANDLER ####
                if msg == DISCONNECT_MESSAGE:
                    print(f"[CONNECTION] {addr} disconnected.")
                    connected = False
                    conn.close()

                #### SHUTDOWN MESSAGE  HANDLER ####
                elif msg == SHUTDOWN_MESSAGE:
                    print("[SERVER] Shutting Down...")
                    conn.sendall(
                        "[SERVER] Shutting down server...Connection Lost...".encode(
                            FORMAT
                        )
                    )
                    conn.close()
                    sys.exit()

                #### GET MESSAGE HANDLER ####
                elif msg.split(" ")[0] == GET_COMMAND:
                    print(f"[{addr}] {msg}")
                    file = msg.split(" ")[1]
                    print(file)
                    path = f"/home/gabriel/PY-Sockets/{file}"
                    exists = os.path.exists(path)

                    ## IF FILE EXISTS ##
                    if exists:
                        print("File found")

                        bytes_read = bytearray()

                        with open(file, "rb") as f:
                            for i in f.read():
                                # --- ADD BYTES TO LIST TO SEND ---#
                                bytes_read.append(i)

                            # ------ SEND BYTES ------#
                            conn.sendall(f"{bytes_read}".encode(FORMAT))
                            print("BYTES SENT")
                    else:
                        # ------ FILE NOT FOUND HANDLER ------#
                        print("[DEBUG] File not found")
                        conn.sendall("File error".encode(FORMAT))

                #### EXIST COMMAND HANDLER ####
                elif msg.split(" ")[0] == EXIST_COMMAND:
                    file = msg.split(" ")[1]
                    path = f"/home/gabriel/PY-Sockets/{file}"
                    exists = os.path.exists(path)

                    # ------ IF IT EXISTS ------#
                    if exists:
                        conn.sendall(FILE_EXISTS_MESSAGE.encode(FORMAT))
                        print(f"[CONNECTION] {addr} disconnected.")
                        connected = False
                        conn.close()

                    # ------ IF NOT EXIST ------#
                    else:
                        conn.sendall(NOT_FOUND_ERROR.encode(FORMAT))
                        print(f"[CONNECTION] {addr} disconnected.")
                        connected = False
                        conn.close()

                elif msg.split(" ")[0] == UPLOAD_COMMAND:
                    print("I got upload command")

                else:
                    # ------ COMMAND NOT FOUND ------#
                    conn.sendall(COMMAND_NOT_FOUND_ERROR.encode(FORMAT))
                    #### CLOSE CONNECTION ####
                    conn.close()
                    break

        # ------ EXCEPT ANY ERRORS ------#
        except:
            print(
                f"[SERVER] Something went wrong with {addr}...Closing connection now..."
            )
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}")
            conn.close()
            exit()

    #### CLOSE CONNECTION ####
    conn.close()


# ------ START SERVER ------#
# ------ FUNCTION ------#
def start():
    server.listen()
    os.system("clear")
    # print_welcome()
    print(f"[SERVER] Listening on: {PORT} - {SERVER}")
    while True:
        #### ACCEPT ANY CONNECTIONS ####
        conn, addr = server.accept()

        #### PASS THROUGH THREADS ####
        # ------ ALLOW MULTIPLE PEOPLE TO REQUEST STUFF ------#
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}")


#### INITIALISE SERVER CONFIGURATIONS ####
try:
    print("[DEBUG] Initialising Server Configs...")
    time.sleep(4)
    start_server = True
    print("[CONFIG] Configs files loaded...")
    time.sleep(1)
    print("[SERVER] Booting up...")
    time.sleep(3)
    start()
    print(f"[SERVER] Successfully booted up as {SERVER}")

except Exception as e:
    print("[SERVER] Something went wrong...")
    print("[DEBUG] Cancelling startup...")
    sys.exit()
