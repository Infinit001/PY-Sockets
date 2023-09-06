import socket


#------ GLOBAL VARAIBLES ------#
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
BUFFER_SIZE = 4096
FORMAT = "utf-8"

#------ COMMANDS ------#
DISCONNECT_MESSAGE = "!DISCONNECT"
SHUTDOWN_MESSAGE = "!SHUTDOWN"
RESTART_MESSAGE = "!RESTART"
GET_COMMAND = "!get"
EXIST_COMMAND = "!check"
UPLOAD_COMMAND = "!upload"

#------ ERRORS ------#
NOT_FOUND_ERROR = "File error"
COMMAND_NOT_FOUND_ERROR = "Command not found"

#------ GLOBAL MESSAGES ------#
FILE_FOUND_MESSAGE = "File found"
FILE_EXISTS_MESSAGE = "File exists"

#------ NON-GLOBAL VARIABLES ------#
start_server = False
connected = False
exist_cmd = False
upload_cmd = False