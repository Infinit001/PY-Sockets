from config import *
import socket, time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def handle_response(response):
    if response == NOT_FOUND_ERROR:
        print("[DEBUG] File was not found...")
    elif response == COMMAND_NOT_FOUND_ERROR:
        print("[DEBUG] Command not found...")
        exit()
    elif response == FILE_FOUND_MESSAGE:
        print("[DEBUG] File does exist...")
        exit()
    else:
        print("[CLIENT] PACKAGE RECEIVED")
        save_ans = input("[CLIENT] Would you like to save the received bytes into a file? (y/n): ").lower()
        if save_ans == "y":
            filename = input("[FILE SYSTEM] Please input filename to save as: ")
            with open(f"{filename}.txt", 'w') as f:
                string = response.split('bytearray(')[1]
                string_2 = string.split("b'")[1]
                final_string = string_2.split("'")[0]
                f.write(final_string)


            #------ ATTEMPT DISCONNECTION TO SERVER ------#
            disconnect()
        else:
            print("[CLIENT] Received message: ")
            print(f"{final_string}")
        # except:
        #     print("[DEBUG] Something went wrong. Please try again...")
            disconnect()
            
def connect():
    try:
        print("[DEBUG] Attempting connection...")
        client.connect(ADDR)
        time.sleep(2)
        connected = True
        if connected:
            print("[DEBUG] Connected to server...")
            messg = input("[CLIENT]: ")
            send(messg)
    except ConnectionRefusedError:
        print("[DEBUG] Server offline...")
        exit()
    except ConnectionResetError:
        print("[DEBUG] Something went wrong...")
    except ConnectionAbortedError:
        print("[DEBUG] Something went wrong...Please try again later...")
    except OSError as e:
        print(f"[DEBUG] Connection error: {e}")
        exit()


def disconnect():
    message = DISCONNECT_MESSAGE.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    try:
        response = client.recv(HEADER).decode(FORMAT)
    except ConnectionResetError:
        print("[DEBUG] Connection lost...")

    print(f"[DEBUG] I have received the following: {response}")
    handle_response(response)

connect()