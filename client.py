import sys
from config import *
import socket, time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False

def save_file(response):
    filename = input(
        "[FILE SYSTEM] Please input filename to save as (with file extension): "
    )

    # ------ WRITE TO FILE ------#
    with open(filename, "wb") as f:  # Use "wb" to write in binary mode
        try:
            # Extracting the bytearray content
            byte_str = response.split("bytearray(")[1].split(")")[0]
            final_bytes = eval(byte_str)

            f.write(final_bytes)
            print("[CLIENT] File saved successfully.")
        except (IndexError, ValueError) as e:
            print(f"[ERROR] Unable to extract bytes: {e}")


def received_package(response):
    global connected
    if exist_cmd:
        print(f"{response}")
    elif upload_cmd:
        print("Upload command executed and received response.")
    else:
        print("[SERVER] File contains the following: ")
        try:
            first_msg = response.split("bytearray(b'")[1]
            second_msg = first_msg.split("'")[0]
        except IndexError:
            first_msg = response.split('bytearray(b"')[1]
            second_msg = first_msg.split('"')[0]
        
        print(f"{second_msg}")
        save_ans = input(
        "Would you like to save the received bytes into a file? (y/n): "
        ).lower()
        if save_ans.lower() == "y" or save_ans.lower() == "yes":
            save_file(response)

def handle_response(response):
    global connected
    #### HANDLERS ####
    if response == NOT_FOUND_ERROR:
        print("[DEBUG] File was not found...")
    elif response == COMMAND_NOT_FOUND_ERROR:
        print("[DEBUG] Command not found...")
    elif response == FILE_FOUND_MESSAGE:
        print("[DEBUG] File does exist...")
    else:
        received_package(response)


def connected_server():
    if connected:
        messg = input("[CLIENT]: ")
        send(messg)
    else:
        print("[DEBUG] Reconnecting...")
        connect()


def get_stuff_and_connected():
    global connected
    try:
        SERVER_ADDR = (
            sys.argv[1],
            int(sys.argv[2]),
        )  # IP address as string, port as integer
        client.connect(SERVER_ADDR)
        connected = True
    except IndexError:
        print("Please enter both the IP address AND the port you wish to connect to.")
        sys.exit()


def connect():
    try:
        # ------ ATTEMPT CONNECTIONS ------#
        print("[DEBUG] Attempting connection...")
        get_stuff_and_connected()
        time.sleep(2)
        print("[DEBUG] Connected to server...")
        while connected:
            connected_server()

    except ConnectionRefusedError:
        print("[DEBUG] Server offline...")
        exit()

    except ConnectionResetError:
        print("[DEBUG] Connection reset...")

    except ConnectionAbortedError:
        print("[DEBUG] Connection aborted...Please try again later...")

    except OSError as e:
        print(f"[DEBUG] Connection error: {e}")
        exit()


def disconnect():
    global connected
    if connected:
        try:
            message = DISCONNECT_MESSAGE.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b" " * (HEADER - len(send_length))
            client.send(send_length)
            client.send(message)
        except OSError:
            pass  # Ignore errors during disconnection if socket is already closed
        finally:
            client.close()
            connected = False


def send(msg):
    global exist_cmd, upload_cmd
    exist_cmd = False
    upload_cmd = False
    if connected == False:
        print("[DEBUG] Not connected. Reconnecting...")
        connect()
        return

    message = msg.encode(FORMAT)
    if message:
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        try:
            client.send(send_length)
            client.send(message)
            response = client.recv(HEADER).decode(FORMAT)

            if msg.split(" ")[0] == EXIST_COMMAND:
                exist_cmd = True
                handle_response(response)

            elif msg.split(" ")[0] == UPLOAD_COMMAND:
                upload_cmd = True
                handle_response(response)
            else:
                handle_response(response)

        except (ConnectionResetError, OSError) as e:
            print("[DEBUG] Not connected. Reconnecting...")
            connect()
            send(msg)
    else:
        print("[DEBUG] Please input a command.")


if __name__ == "__main__":
    connect()
    connected = False
