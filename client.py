from config import *
import socket

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    connected = True
except:
    print("[DEBUG] Something went wrong...")
    exit()

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    response = client.recv(HEADER).decode(FORMAT)

    print(f"[DEBUG] I have received the following: {response}")

    if response == NOT_FOUND_ERROR:
        print("[DEBUG] Server was not found...")
    else:
        print("[CLIENT] PACKAGE RECEIVED")
        save_ans = input("[CLIENT] Would you like to save the received bytes into a file? (y/n): ").lower()
        if save_ans == "y":
            filename = input("[FILE SYSTEM] Please input filename: ")
            with open(f"{filename}.txt", 'w') as f:
                string = msg.split('bytearray(')[1]
                string_2 = string.split("b'")[1]
                final_string = string_2.split("'")[0]
                f.write(final_string)
        else:
            print("[CLIENT] Received message: ")
            print(f"{msg}")
        # except:
        #     print("[DEBUG] Something went wrong. Please try again...")
            message = SHUTDOWN_MESSAGE.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client.send(send_length)
            client.send(message)

if connected:
    messg = input("[CLIENT]: ")
    send(messg)