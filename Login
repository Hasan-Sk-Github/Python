from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


def login():
    if username_entry.get() == "" or password_entry.get() == "":
        messagebox.showerror("Error", "Fields cannot be empty")
    elif username_entry.get() == "hasansk786" and password_entry.get() == "Hasan@786":
        messagebox.showinfo("Login Successfully", "Welcome to Student Management System!", parent=window)
        window.destroy()
        import sms
    else:
        messagebox.showinfo("Login Failed", "Please enter correct credentials!", parent=window)


window = Tk()
window.title("User Login")
window.geometry("1165x700+0+0")
window.resizable(False, False)

background_image = Image.open("images/bg2.jpg")
background_photo = ImageTk.PhotoImage(background_image)
bg_label = Label(window, image=background_photo)
bg_label.place(x=0, y=0)

login_Frame = Frame(window, bg="yellow")
login_Frame.place(x=555, y=150)
logo_Image = PhotoImage(file="images/login1.png")
logo_label = Label(login_Frame, image=logo_Image)
logo_label.grid(row=0, column=0, columnspan=2)

username_image = PhotoImage(file="images/aa.png")
username_label = Label(login_Frame, image=username_image, text="Username :", compound=LEFT
                        , font=("times new roman", 18, "bold"), bg="white")
username_label.grid(row=1, column=0, pady=10, padx=20)

username_entry = Entry(login_Frame, font=("times new roman", 15, "bold"), bd=5)
username_entry.grid(row=1, column=1, pady=10, padx=20)

password_image = PhotoImage(file="images/lock.png")
password_label = Label(login_Frame, image=password_image, text="Password :", compound=LEFT
                        , font=("times new roman", 18, "bold"), bg="white")
password_label.grid(row=2, column=0, pady=10, padx=20)

password_entry = Entry(login_Frame, font=("times new roman", 15, "bold"), bd=5, show="*")
password_entry.grid(row=2, column=1, pady=10, padx=20,)


# Function to toggle password visibility
def toggle_password_visibility():
    if password_entry["show"] == "*":
        password_entry.config(show="")
        show_hide_button.config(image=hide_icon)
    else:
        password_entry.config(show="*")
        show_hide_button.config(image=show_icon)


# Load the icons for show and hide
show_icon = PhotoImage(file="images/show.png")
hide_icon = PhotoImage(file="images/hide.png")

# Button to toggle password visibility
show_hide_button = Button(login_Frame, image=show_icon, command=toggle_password_visibility)
show_hide_button.grid(row=2, column=2)


login_button = Button(login_Frame, text="Login", font=("times new roman", 15, "bold"), width=15
                      , fg="white", bg="cornflowerblue", activebackground="cornflowerblue"
                      , activeforeground="white", cursor="hand2", bd=5, command=login)
login_button.grid(row=3, column=1, pady=10, padx=20)


window.mainloop()
