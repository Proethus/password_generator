import json
from json import JSONDecodeError
from tkinter import *
import random
from tkinter import messagebox

NUMBER_OF_SPECIAL_CHARACTERS = 3
NUMBER_OF_UPPERCASE_LETTERS = 2
NUMBER_OF_LOWERCASE_LETTERS = 11
UPPERCASE_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWERCASE_ALPHABET = "abcdefghijklmnopqrstuvwxyz"
SPECIAL_CHARACTERS = ",?;.:<>_-*~+^!°%/=()"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password = random.choices(LOWERCASE_ALPHABET, k=NUMBER_OF_LOWERCASE_LETTERS)
    password += random.choices(UPPERCASE_ALPHABET, k=NUMBER_OF_UPPERCASE_LETTERS)
    password += random.choices(SPECIAL_CHARACTERS, k=NUMBER_OF_SPECIAL_CHARACTERS)
    random.shuffle(password)
    password_var.set("".join(password))


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    if len(website_var.get()) and len(user_id_var.get()) and len(password_var.get()) > 0:
        record = {
            website_var.get(): {
                "email": user_id_var.get(),
                "password": password_var.get()
            }
        }

        with open("passwords.json", "r") as password_file:
            try:
                passwords = json.load(password_file)
            except JSONDecodeError:
                passwords = json.loads('{}')
            passwords.update(record)
        with open("passwords.json", "w") as password_file:
            json.dump(passwords, password_file, indent=4)
        website_input.configure(highlightcolor="red", highlightbackground="red", highlightthickness=0)
        user_id_input.configure(highlightcolor="red", highlightbackground="red", highlightthickness=0)
        password_input.configure(highlightcolor="red", highlightbackground="red", highlightthickness=0)
        website_var.set("")
        password_var.set("")
        messagebox.showinfo("Password added!", "Password successfully added!")

    else:
        if len(website_var.get()) == 0:
            website_input.configure(highlightcolor="red", highlightbackground="red", highlightthickness=3)
        if len(user_id_input.get()) == 0:
            user_id_input.configure(highlightcolor="red", highlightbackground="red", highlightthickness=3)
        if len(password_var.get()) == 0:
            password_input.configure(highlightcolor="red", highlightbackground="red", highlightthickness=3)
        messagebox.showwarning("An error occurred!", "Please fill all highlighted information!")


# ---------------------------- FIND PASSWORD ------------------------------- #
def get_password():
    if len(website_var.get()) > 0 and len(user_id_var.get()) > 0:
        with open("passwords.json") as file:
            passwords = json.load(file)
            try:
                record = passwords[website_var.get()]
            except KeyError:
                messagebox.showerror("Invalid value inserted!", "Cannot find password for this website!")
            else:
                    if record["email"] == user_id_var.get():
                        password = record["password"]
                        messagebox.showinfo("Password found",
                                            f"Website: {website_var.get()}\nUsername: {user_id_var.get()}\nPassword: {password}")
                    else:
                        messagebox.showerror("Invalid value inserted!", "Cannot find password for this user!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.configure(height=600, width=600, pady=50, padx=50)
window.title("Password Manager")
canvas = Canvas()
canvas.configure(height=200, width=200)
background_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=background_image)
canvas.grid(row=0, column=1, sticky=NSEW)

website_label = Label(text="Website:")
user_id_label = Label(text="Email/Username:")
password_label = Label(text="Password:")

website_var = StringVar()
website_input = Entry(width=35, textvariable=website_var)
website_input.focus()
user_id_var = StringVar()
user_id_input = Entry(width=35, textvariable=user_id_var, )
user_id_input.insert(0, "test@example.com")
password_var = StringVar()
password_input = Entry(width=21, textvariable=password_var, show="*")

search_button = Button(text="Search", command=get_password)
generate_button = Button(text="Generate Password", command=generate_password)
add_button = Button(text="Add", width=36, command=save_password)

website_label.grid(row=1, column=0, sticky=W)
user_id_label.grid(row=2, column=0, sticky=W)
password_label.grid(row=3, column=0, sticky=W)

website_input.grid(row=1, column=1, columnspan=2, sticky=EW)
user_id_input.grid(row=2, column=1, columnspan=2, sticky=EW)
password_input.grid(row=3, column=1, sticky=W)
generate_button.grid(row=3, column=2, sticky=E)
add_button.grid(row=4, column=1, columnspan=2, sticky=N + S + E + W)
search_button.grid(row=1, column=3)

window.grid_columnconfigure(3, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

window.mainloop()
