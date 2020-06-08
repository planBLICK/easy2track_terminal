from tkinter import *
import json
from time import sleep

def save_login_data():
    button.grid_remove()
    login_data = {"login": e1.get(), "password": e2.get()}
    with open("./login_data.json", "w") as file:
        file.write(json.dumps(login_data))

    master.destroy()

master = Tk(className="Anmeldung")

windowWidth = master.winfo_reqwidth()
windowHeight = master.winfo_reqheight()

positionRight = int(master.winfo_screenwidth() / 2 - windowWidth / 2)
positionDown = int(master.winfo_screenheight() / 2 - windowHeight / 2)

master.geometry("+{}+{}".format(positionRight, positionDown))

Label(master, text="Login").grid(row=0)
Label(master, text="Passwort").grid(row=1)

e1 = Entry(master)
e2 = Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

button = Button(master, text='Anmelden', command=lambda: save_login_data())
button.grid(row=3, column=1, sticky=W, pady=4)

master.mainloop()
