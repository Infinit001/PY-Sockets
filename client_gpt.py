import sys
import socket
import time
import tkinter as tk
from config import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False


def save_file(response):
    filename = input(
        "[FILE SYSTEM] Please input filename to save as (with file extension): "
    )

    try:
        byte_str = response.split("bytearray(")[1].split(")")[0]
        final_bytes = eval(byte_str)

        with open(filename, "wb") as f:
            f.write(final_bytes)
        print("[CLIENT] File saved successfully.")
    except (IndexError, ValueError) as e:
        print(f"[ERROR] Unable to extract bytes: {e}")


def received_package(response):
    global connected
    if exist_cmd:
        print(response)
    elif upload_cmd:
        print("Upload command executed and received response.")
    else:
        print("[SERVER] File contains the following:")
        try:
            byte_message = response.split("bytearray(b'")[1].split("'")[0]
        except IndexError:
            byte_message = response.split('bytearray(b"')[1].split('"')[0]

        print(byte_message)
        if input(
            "Would you like to save the received bytes into a file? (y/n): "
        ).lower() in {"y", "yes"}:
            save_file(response)


def handle_response(response):
    global exist_cmd, upload_cmd

    # Reset flags
    exist_cmd = False
    upload_cmd = False

    if response == NOT_FOUND_ERROR:
        return "[DEBUG] File was not found..."
    elif response == COMMAND_NOT_FOUND_ERROR:
        return "[DEBUG] Command not found..."
    elif response == FILE_FOUND_MESSAGE:
        return "[DEBUG] File does exist..."
    else:
        received_package(response)

    # Reset any additional state or variables related to the response here
    return ""  # Return empty after handling response


def send_command(command):
    global exist_cmd, upload_cmd
    exist_cmd = upload_cmd = False

    if not connected:
        print("[DEBUG] Not connected. Reconnecting...")
        connect()
        return "[DEBUG] Not connected. Reconnecting..."

    message = command.encode(FORMAT)
    print(f"[DEBUG] Sending command: {command}")  # Debug statement
    if message:
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT) + b" " * (
            HEADER - len(str(msg_length).encode(FORMAT))
        )

        try:
            # Send the message length and command
            client.send(send_length)
            client.send(message)

            # Receive the response from the server
            response = client.recv(HEADER).decode(FORMAT)
            print(f"[DEBUG] Received response: {response}")  # Debug statement

            if command.startswith(EXIST_COMMAND):
                exist_cmd = True
            elif command.startswith(UPLOAD_COMMAND):
                upload_cmd = True

            # Handle the response and reset any response variables
            return handle_response(response)

        except (ConnectionResetError, OSError):
            print("[DEBUG] Not connected. Reconnecting...")
            connect()
    else:
        return "[DEBUG] Please input a command."


class ConsoleText(tk.Text):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.insert("1.0", ">>> ")  # First prompt
        self.mark_set("input", "insert")
        self.mark_gravity("input", "left")
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        self.bind("<Return>", self.enter)

    def _proxy(self, *args):
        largs = list(args)
        if args[0] == "insert":
            if self.compare("insert", "<", "input"):
                self.mark_set("insert", "end")
        elif args[0] == "delete":
            if self.compare(largs[1], "<", "input"):
                if len(largs) == 2:
                    return
                largs[1] = "input"
        return self.tk.call((self._orig,) + tuple(largs))

    def enter(self, event):
        command = self.get("input", "end-1c").strip()  # Get the input command
        if command:  # Check if the command is not empty
            self.insert("end", f"\n{command}\n")  # Display the command in the console
            self.mark_set("input", "insert")

            # Execute command and get the response
            response = send_command(command)  # Send the command and receive response
            if response:
                self.insert("end", f"{response}\n>>> ")  # Display response
            else:
                self.insert("end", ">>> ")  # Just prompt if no response

        return "break"  # Prevent default new line


def connected_server():
    if connected:
        root = tk.Tk()
        tfield = ConsoleText(root, bg="black", fg="white", insertbackground="white")
        tfield.pack(expand=True, fill="both")
        root.mainloop()
    else:
        print("[DEBUG] Reconnecting...")
        connect()


def connect():
    global connected
    try:
        print("[DEBUG] Attempting connection...")
        SERVER_ADDR = (sys.argv[1], int(sys.argv[2]))
        client.connect(SERVER_ADDR)
        connected = True
        print("[DEBUG] Connected to server...")
        connected_server()
    except (
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionAbortedError,
        OSError,
    ) as e:
        print(f"[DEBUG] Connection error: {e}")
        exit()


def disconnect():
    global connected
    if connected:
        try:
            message = DISCONNECT_MESSAGE.encode(FORMAT)
            client.send(message)
        except OSError:
            pass
        finally:
            client.close()
            connected = False


if __name__ == "__main__":
    connect()
