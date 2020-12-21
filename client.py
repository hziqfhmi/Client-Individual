import socket
import threading
import os
import sys
import readline

HOST = "192.168.1.7"
PORT = 2222
run = False

def receive(s):
    global run
    while run:
        data = s.recv(4096)
        income = data.decode("utf8")
        if income == "exitsshserver":
            run = False
            s.close()
            exit(0)
        else:
            newlinesplt = income.split("\\n")
            runs = 0
            for i in newlinesplt:
                print (newlinesplt[runs])
                runs += 1
                if runs == len(newlinesplt) - 1:
                    runs = 0
                    break

def _exit(s):
    global run
    run = False
    s.send("exit".encode("utf8"))
    s.shutdown(socket.SHUT_RDWR)
    exit(0)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        run = True
        listenThread = threading.Thread(target=receive, args=(s,))
        listenThread.setDaemon(True)
        listenThread.start()
        while run:
            try:
                inputs = input()
                if inputs.startswith("/"):
                    command = inputs.split("/")
                    os.system(command[1])
                elif inputs == "exitnow":
                    _exit(s)
                else:
                    s.send(inputs.encode("utf8"))
            except KeyboardInterrupt:
                _exit(s)
            except OSError:
                pass
