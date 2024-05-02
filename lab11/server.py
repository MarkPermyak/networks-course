import pickle
import socket
from tkinter import *

HOST = "127.0.0.1"
PORT = 65432

canvas_width = 400
canvas_height = 500
colour = "#000000"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        master = Tk()
        master.title("Server")
        w = Canvas(master,
                width=canvas_width,
                height=canvas_height)
        w.pack(expand=YES, fill=BOTH)
        message = Label(master, text="Result")
        message.pack(side=BOTTOM)
        while True:
            coord = conn.recv(1024)
            if not coord:
                break
            data = pickle.loads(coord)
            x1, y1 = data[0], data[1]
            x2, y2 = data[2], data[3]   
            lines = w.create_rectangle(x1, y1, x2, y2, fill=colour)
            w.bind('<1>', lines)
            w.update()
        mainloop()
