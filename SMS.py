from tkinter import *
import time
import ttkthemes
from tkinter import ttk
import mysql.connector
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
from tkinter.ttk import Combobox
import pandas


# functionality part
def clock():
    date = time.strftime("%d-%m-%Y")
    current_time = time.strftime("%H:%M:%S")
    datetime_label.config(text=f"    Date: {date}\nTime: {current_time}")
    datetime_label.after(1000, clock)


count = 0
text = ""


def slider():
    global text, count
    if count == len(title):
        count = 0
        text = ""
    text = text+title[count]
    slider_label.config(text=text)
    count += 1
    slider_label.after(300, slider)


def exit_closed():
    result = messagebox.askyesno("Confirmation", "Do you want to exit from Student Management System?")

    if result:
        messagebox.showinfo("Success", "Exit from Student Management System Successfully!")
        root.destroy()
        import login
    else:
        pass


def export_data():
    if not student_table.get_children():
        messagebox.showerror("Error", "No data found in the table.")
        return  # Exit the function if no data is found

    result = messagebox.askyesno("Confirmation", "Do you want to save the data as Excel file!")

    if result:
        url = filedialog.asksaveasfilename(defaultextension=".csv")
        indexing = student_table.get_children()
        new_list = []
        for index in indexing:
           content = student_table.item(index)
           data_list = content["values"]
           new_list.append(data_list)

        table = pandas.DataFrame(new_list, columns=["Student ID", "Name", "Father's Name", "Gender"
                                                     , "D.O.B", "Courses", "Mobile No.", "Email ID", "Address", "Added Date", "Added Time"])
        table.to_csv(url, index=False)

        messagebox.showinfo("Success", "Excel file saved Successfully!")


def update_student():
    def update_data():
        # Check if any row is selected
        if not student_table.selection():
            messagebox.showerror("Error", "Please select a student details to update.", parent=update_student_window)
            return

        # Get the selected item from the student table
        selected_item = student_table.focus()
        if not selected_item:
            messagebox.showerror("Error", "No student details selected.", parent=update_student_window)
            return

        # Get the data from the selected item
        item_data = student_table.item(selected_item)
        data = item_data.get('values')
        if not data:
            messagebox.showerror("Error", "No data found for selected student.", parent=update_student_window)
            return

        # Ask for confirmation before submitting
        preview_message = f"Student ID: {student_id_entry.get()}\n Name: {name_entry.get()}\nFather's Name: {father_Name_entry.get()}\nGender: {gender_combobox.get()}\nD.O.B: {dob_entry.get()}\nCourses: {courses_entry.get()}\nMobile No.: {mobile_no_entry.get()}\nEmail ID: {email_id_entry.get()}\nAddress: {address_entry.get()}"

        confirm_update = messagebox.askyesno("Preview and Confirm",
                                             f"Do you want to modify the following details?\n{preview_message}",
                                             parent=update_student_window)
        if confirm_update:
            # Update the database record
            # Ensure to add a WHERE clause to specify which record to update
            sql = "UPDATE student SET Name=%s, Father_Name=%s, Gender=%s, DOB=%s, course=%s, Mobile_No=%s, Email=%s, Address=%s WHERE Student_ID=%s"
            mycursor.execute(sql, (
                name_entry.get(), father_Name_entry.get(), gender_combobox.get(), dob_entry.get(), courses_entry.get(),
                mobile_no_entry.get(), email_id_entry.get(), address_entry.get(),
                data[0]))  # Assuming data[0] is the student ID

            mydb.commit()
            messagebox.showinfo("Update", "This student was modified successfully!", parent=update_student_window)

            update_student_window.destroy()

            # Refresh the student_table after update
            refresh_student_table()

    update_student_window = Toplevel()
    update_student_window.geometry("950x460+200+200")
    update_student_window.title("Update Student Details")
    update_student_window.grab_set()
    update_student_window.resizable(False, False)

    student_id_label = Label(update_student_window, text="Student ID :", font=("times new roman", 20, "bold"))
    student_id_label.grid(row=0, column=0, pady=20, padx=20, sticky=W)
    student_id_entry = Entry(update_student_window, font=("arial", 15, "bold"), bg="white", bd=5)
    student_id_entry.grid(row=0, column=1, pady=20, padx=20)

    name_label = Label(update_student_window, text="Name :", font=("times new roman", 20, "bold"))
    name_label.grid(row=1, column=0, pady=20, padx=20, sticky=W)
    name_entry = Entry(update_student_window, font=("roman", 15, "bold"),  bg="white", bd=5)
    name_entry.grid(row=1, column=1, pady=20, padx=20)

    father_Name_label = Label(update_student_window, text="Father's Name :", font=("times new roman", 20, "bold"))
    father_Name_label.grid(row=1, column=2, pady=20, padx=20, sticky=W)
    father_Name_entry = Entry(update_student_window, font=("roman", 15, "bold"), bg="white", bd=5)
    father_Name_entry.grid(row=1, column=3, pady=20, padx=20)

    gender_options = ["Male", "Female", "Other"]

    gender_label = Label(update_student_window, text="Gender :", font=("times new roman", 20, "bold"))
    gender_label.grid(row=2, column=0, pady=20, padx=20, sticky=W)

    gender_combobox = Combobox(update_student_window, values=gender_options, font=("arial", 15, "bold"), state="readonly",
                               width=18)
    gender_combobox.grid(row=2, column=1, pady=20, padx=20)

    gender_combobox.current(0)

    dob_label = Label(update_student_window, text="D.O.B :", font=("times new roman", 20, "bold"))
    dob_label.grid(row=2, column=2, pady=20, padx=20, sticky=W)

    dob_entry = DateEntry(update_student_window, font=("roman", 15, "bold"), bg="white", bd=5, date_pattern='dd-mm-yyyy', width=20)
    dob_entry.grid(row=2, column=3, pady=20, padx=20)

    courses_label = Label(update_student_window, text="Courses :", font=("times new roman", 20, "bold"))
    courses_label.grid(row=3, column=0, pady=20, padx=20, sticky=W)
    courses_entry = Entry(update_student_window, font=("roman", 15, "bold"), bg="white", bd=5)
    courses_entry.grid(row=3, column=1, pady=20, padx=20)

    mobile_no_label = Label(update_student_window, text="Mobile No. :", font=("times new roman", 20, "bold"))
    mobile_no_label.grid(row=3, column=2, pady=20, padx=20, sticky=W)
    mobile_no_entry = Entry(update_student_window, font=("roman", 15, "bold"), bg="white", bd=5)
    mobile_no_entry.grid(row=3, column=3, pady=20, padx=20)

    email_id_label = Label(update_student_window, text="Email ID :", font=("times new roman", 20, "bold"))
    email_id_label.grid(row=4, column=0, pady=20, padx=20, sticky=W)
    email_id_entry = Entry(update_student_window, font=("roman", 15, "bold"), bg="white", bd=5)
    email_id_entry.grid(row=4, column=1, pady=20, padx=20)

    address_label = Label(update_student_window, text="Address :", font=("times new roman", 20, "bold"))
    address_label.grid(row=4, column=2, pady=20, padx=20, sticky=W)
    address_entry = Entry(update_student_window, font=("roman", 15, "bold"), bg="white", bd=5)
    address_entry.grid(row=4, column=3, pady=20, padx=20)

    update_button = ttk.Button(update_student_window, text="UPDATE", width=20, command=update_data)
    update_button.grid(row=5, column=3, pady=20, padx=20)

    # Populate entry fields with data from the selected item
    selected_item = student_table.focus()
    if selected_item:
        item_data = student_table.item(selected_item)
        data = item_data.get('values')
        if data:
            student_id_entry.insert(0, data[0])
            name_entry.insert(0, data[1])
            father_Name_entry.insert(0, data[2])
            gender_combobox.set(data[3])
            dob_entry.set_date(data[4])
            courses_entry.insert(0, data[5])
            mobile_no_entry.insert(0, data[6])
            email_id_entry.insert(0, data[7])
            address_entry.insert(0, data[8])


def delete_student():
    # Check if any row is selected
    if not student_table.selection():
        messagebox.showerror("Error", "Please select a student details to delete.")
        return

    indexing = student_table.focus()
    content = student_table.item(indexing)
    content_id = content["values"][0]
    content_name = content["values"][1]
    content_father_name = content["values"][2]
    content_gender = content["values"][3]
    content_dob = content["values"][4]
    content_mobile_no = content["values"][6]

    # Ask for confirmation before submitting
    preview_message = f"Student ID: {content_id}\n Name: {content_name}\n Father's Name: {content_father_name}\n Gender: {content_gender}\n D.O.B: {content_dob}\n Mobile No.: {content_mobile_no}"

    confirm_delete = messagebox.askyesno("Preview and Confirm", f"Do you want to delete the following details?\n{preview_message}")

    refresh_student_table()

    if confirm_delete:
        sql = "DELETE FROM student WHERE Student_ID = %s"
        mycursor.execute(sql, (content_id,))  # Provide the parameter as a tuple
        mydb.commit()
        messagebox.showinfo("Deleted", "This student was deleted successfully!")

        # Refresh the student_table after deletion
        refresh_student_table()
    else:
        # User chose not to delete, do nothing
        pass


def refresh_student_table():
    # Refresh student_table with updated data from the database
    sql = "SELECT * FROM student"
    mycursor.execute(sql)
    fetched_data = mycursor.fetchall()
    student_table.delete(*student_table.get_children())
    for data in fetched_data:
        student_table.insert("", END, values=data)


def show_student():
    refresh_student_table()


def search_student():
    def search_data():
        sql = "select * from student where Student_ID=%s or Name=%s or Father_Name=%s or DOB=%s or Mobile_No=%s or Email=%s"
        mycursor.execute(sql, (
            student_id_entry.get(), name_entry.get(), father_Name_entry.get(), dob_entry.get(), mobile_no_entry.get(),
            email_id_entry.get()))
        student_table.delete(*student_table.get_children())
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            student_table.insert("", END, values=data)

        if fetched_data:
            messagebox.showinfo("Data Fetched", "Data Fetched Successfully!", parent=search_student_window)
            search_student_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter correct Details!", parent=search_student_window)

    search_student_window = Toplevel()
    search_student_window.geometry("950x320+200+250")
    search_student_window.title("Search Student Details")
    search_student_window.grab_set()
    search_student_window.resizable(False, False)

    student_id_label = Label(search_student_window, text="Student ID :", font=("times new roman", 20, "bold"))
    student_id_label.grid(row=0, column=0, pady=20, padx=20, sticky=W)
    student_id_entry = Entry(search_student_window, font=("roman", 15, "bold"),  bg="white", bd=5)
    student_id_entry.grid(row=0, column=1, pady=20, padx=20)

    name_label = Label(search_student_window, text="Name :", font=("times new roman", 20, "bold"))
    name_label.grid(row=1, column=0, pady=20, padx=20, sticky=W)
    name_entry = Entry(search_student_window, font=("roman", 15, "bold"),  bg="white", bd=5)
    name_entry.grid(row=1, column=1, pady=20, padx=20)

    father_Name_label = Label(search_student_window, text="Father's Name :", font=("times new roman", 20, "bold"))
    father_Name_label.grid(row=1, column=2, pady=20, padx=20, sticky=W)
    father_Name_entry = Entry(search_student_window, font=("roman", 15, "bold"), bg="white", bd=5)
    father_Name_entry.grid(row=1, column=3, pady=20, padx=20)

    dob_label = Label(search_student_window, text="D.O.B :", font=("times new roman", 20, "bold"))
    dob_label.grid(row=2, column=0, pady=20, padx=20, sticky=W)

    dob_entry = DateEntry(search_student_window, font=("roman", 15, "bold"), bg="white", bd=5, date_pattern='dd-mm-yyyy', width=20)
    dob_entry.grid(row=2, column=1, pady=20, padx=20)

    mobile_no_label = Label(search_student_window, text="Mobile No. :", font=("times new roman", 20, "bold"))
    mobile_no_label.grid(row=2, column=2, pady=20, padx=20, sticky=W)
    mobile_no_entry = Entry(search_student_window, font=("roman", 15, "bold"), bg="white", bd=5)
    mobile_no_entry.grid(row=2, column=3, pady=20, padx=20)

    email_id_label = Label(search_student_window, text="Email ID :", font=("times new roman", 20, "bold"))
    email_id_label.grid(row=3, column=0, pady=20, padx=20, sticky=W)
    email_id_entry = Entry(search_student_window, font=("roman", 15, "bold"), bg="white", bd=5)
    email_id_entry.grid(row=3, column=1, pady=20, padx=20)

    search_button = ttk.Button(search_student_window, text="SEARCH", width=20, command=search_data)
    search_button.grid(row=3, column=3, pady=20, padx=20)


def add_student():
    def submit():
        added_date = time.strftime("%d-%m-%Y")
        added_time = time.strftime("%H:%M:%S")
        if name_entry.get() == "" or father_Name_entry.get() == "" or gender_combobox.get() == "" or dob_entry.get() == "" or courses_entry.get() == "" or mobile_no_entry.get() == "" or email_id_entry.get() == "" or address_entry.get() == "":
            messagebox.showerror("Error", "All Fields are Required", parent=add_student_window)
        else:
            # Create a preview message
            preview_message = f"Name: {name_entry.get()}\nFather's Name: {father_Name_entry.get()}\nGender: {gender_combobox.get()}\nDOB: {dob_entry.get()}\nCourses: {courses_entry.get()}\nMobile No.: {mobile_no_entry.get()}\nEmail ID: {email_id_entry.get()}\nAddress: {address_entry.get()}"

            # Ask for confirmation before submitting
            confirm_submit = messagebox.askyesno("Preview and Confirm", f"Do you want to submit the following details?\n\n{preview_message}", parent=add_student_window)

            if confirm_submit:
                try:
                    sql = "INSERT INTO student (`Name`, `Father_Name`, `Gender`, `DOB`, `Course`, `Mobile_No`, `Email`, `Address`, `Added_Date`, `Added_time`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    values = (
                    name_entry.get(), father_Name_entry.get(), gender_combobox.get(), dob_entry.get(), courses_entry.get(),
                    mobile_no_entry.get(), email_id_entry.get(), address_entry.get(), added_date, added_time)
                    mycursor.execute(sql, values)

                    # Committing the changes
                    mydb.commit()

                    result = messagebox.askyesno("Confirmation",
                                                 "Student Data Submitted Successfully. Do you want to clean the form?",
                                                 parent=add_student_window)
                    if result:
                        # Clearing the form if user chooses to do so
                        name_entry.delete(0, END)
                        father_Name_entry.delete(0, END)
                        gender_combobox.set('')
                        dob_entry.delete(0, END)
                        courses_entry.delete(0, END)
                        mobile_no_entry.delete(0, END)
                        email_id_entry.delete(0, END)
                        address_entry.delete(0, END)

                        refresh_student_table()

                    else:
                        pass

                except mysql.connector.Error as err:
                    print("Error:", err)

            else:
                pass

    add_student_window = Toplevel()
    add_student_window.geometry("950x410+200+250")
    add_student_window.title("Add Student Details")
    add_student_window.grab_set()
    add_student_window.resizable(False, False)

    name_label = Label(add_student_window, text="Name :", font=("times new roman", 20, "bold"))
    name_label.grid(row=1, column=0, pady=20, padx=20, sticky=W)
    name_entry = Entry(add_student_window, font=("roman", 15, "bold"),  bg="white", bd=5)
    name_entry.grid(row=1, column=1, pady=20, padx=20)

    father_Name_label = Label(add_student_window, text="Father's Name :", font=("times new roman", 20, "bold"))
    father_Name_label.grid(row=1, column=2, pady=20, padx=20, sticky=W)
    father_Name_entry = Entry(add_student_window, font=("roman", 15, "bold"), bg="white", bd=5)
    father_Name_entry.grid(row=1, column=3, pady=20, padx=20)

    gender_options = ["Male", "Female", "Other"]

    gender_label = Label(add_student_window, text="Gender :", font=("times new roman", 20, "bold"))
    gender_label.grid(row=2, column=0, pady=20, padx=20, sticky=W)

    gender_combobox = Combobox(add_student_window, values=gender_options, font=("arial", 15, "bold"), state="readonly",
                               width=18)
    gender_combobox.grid(row=2, column=1, pady=20, padx=20)

    gender_combobox.current(0)

    dob_label = Label(add_student_window, text="D.O.B :", font=("times new roman", 20, "bold"))
    dob_label.grid(row=2, column=2, pady=20, padx=20, sticky=W)

    dob_entry = DateEntry(add_student_window, font=("roman", 15, "bold"), bg="white", bd=5, date_pattern='dd-mm-yyyy', width=20)
    dob_entry.grid(row=2, column=3, pady=20, padx=20)

    courses_label = Label(add_student_window, text="Courses :", font=("times new roman", 20, "bold"))
    courses_label.grid(row=3, column=0, pady=20, padx=20, sticky=W)
    courses_entry = Entry(add_student_window, font=("roman", 15, "bold"), bg="white", bd=5)
    courses_entry.grid(row=3, column=1, pady=20, padx=20)

    mobile_no_label = Label(add_student_window, text="Mobile No. :", font=("times new roman", 20, "bold"))
    mobile_no_label.grid(row=3, column=2, pady=20, padx=20, sticky=W)
    mobile_no_entry = Entry(add_student_window, font=("roman", 15, "bold"), bg="white", bd=5)
    mobile_no_entry.grid(row=3, column=3, pady=20, padx=20)

    email_id_label = Label(add_student_window, text="Email ID :", font=("times new roman", 20, "bold"))
    email_id_label.grid(row=4, column=0, pady=20, padx=20, sticky=W)
    email_id_entry = Entry(add_student_window, font=("roman", 15, "bold"), bg="white", bd=5)
    email_id_entry.grid(row=4, column=1, pady=20, padx=20)

    address_label = Label(add_student_window, text="Address :", font=("times new roman", 20, "bold"))
    address_label.grid(row=4, column=2, pady=20, padx=20, sticky=W)
    address_entry = Entry(add_student_window, font=("roman", 15, "bold"), bg="white", bd=5)
    address_entry.grid(row=4, column=3, pady=20, padx=20)

    submit_button = ttk.Button(add_student_window, text="SUBMIT", width=20, command=submit)
    submit_button.grid(row=5, column=3, pady=20, padx=20)


#Database Connection
def connect_database():
    def connect():
        global mycursor, mydb
        try:
            mydb = mysql.connector.connect(
                host=host_name_entry.get(),
                user=user_name_entry.get(),
                password=password_entry.get(),
                database="student_management"
            )
            mycursor = mydb.cursor()

            messagebox.showinfo("Connection Success", "Database connection is Successfully!", parent=connect_window)
            connect_window.destroy()
        except:
            messagebox.showerror("Error", "Please enter correct credential", parent=connect_window)
            return

        #all button are Activeted
        add_student_button.config(state=NORMAL)
        search_student_button.config(state=NORMAL)
        update_student_button.config(state=NORMAL)
        show_student_button.config(state=NORMAL)
        delete_student_button.config(state=NORMAL)
        export_student_button.config(state=NORMAL)

#Database Connection Window
    connect_window = Toplevel(bg="Red2")
    connect_window.grab_set()
    connect_window.geometry("540x300+608+145")
    connect_window.title("Database Connection")
    connect_window.resizable(False, False)

    host_name_label = Label(connect_window, text="Host Name:", font=("arial", 20, "bold"), bg="Red2", fg="White")
    host_name_label.grid(row=0, column=0, pady=20, padx=20)

    host_name_entry = Entry(connect_window, font=("roman", 15, "bold"), bg="white", bd=5)
    host_name_entry.grid(row=0, column=1, pady=20, padx=40)

    user_name_label = Label(connect_window, text="Username:", font=("arial", 20, "bold"), bg="Red2", fg="White")
    user_name_label.grid(row=1, column=0, pady=20, padx=20)

    user_name_entry = Entry(connect_window, font=("roman", 15, "bold"), bg="white", bd=5)
    user_name_entry.grid(row=1, column=1, pady=20, padx=40)

    password_label = Label(connect_window, text="Password:", font=("arial", 20, "bold"), bg="Red2", fg="White")
    password_label.grid(row=2, column=0, pady=20, padx=20)

    password_entry = Entry(connect_window, font=("roman", 15, "bold"), bg="white", bd=5,show="*")
    password_entry.grid(row=2, column=1, pady=20, padx=40)

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
    show_hide_button = Button(connect_window, image=show_icon, command=toggle_password_visibility)
    show_hide_button.grid(row=2, column=2)

    connect_button = ttk.Button(connect_window, text="CONNECT", width=20, command=connect)
    connect_button.grid(row=3, column=1, pady=20, padx=40)


# GUI part
root = ttkthemes.ThemedTk()

root.get_themes()
root.set_theme("breeze")

root.geometry("1174x680+0+0")
root.resizable(False, False)
root.title("Student Management System")

datetime_label = Label(root, font=("times new roman", 18, "bold"), fg="cornflowerblue")
datetime_label.place(x=5, y=5)
clock()

title = "Student Management System"
slider_label = Label(root, text=title, font=("arial", 28, "italic bold"), width=30, fg="Green")
slider_label.place(x=300, y=0)
slider()

connect_button = ttk.Button(root, text="Connect to Database", command=connect_database)
connect_button.place(x=1000, y=25,)


left_frame = Frame(root)
left_frame.place(x=50, y=80, width=300, height=600)

logo_image = PhotoImage(file="images/student.png")
logo_label = Label(left_frame, image=logo_image)
logo_label.grid(row=0, column=0)

add_student_button = ttk.Button(left_frame, text="Add Student", width=25, state=DISABLED, command=add_student)
add_student_button.grid(row=1, column=0, pady=10, padx=20)

search_student_button = ttk.Button(left_frame, text="Search Student", width=25, state=DISABLED, command=search_student)
search_student_button.grid(row=2, column=0, pady=10, padx=20)

update_student_button = ttk.Button(left_frame, text="Update Student", width=25, state=DISABLED, command=update_student)
update_student_button.grid(row=3, column=0, pady=10, padx=20)

show_student_button = ttk.Button(left_frame, text="Show Student", width=25, state=DISABLED, command=show_student)
show_student_button.grid(row=4, column=0, pady=10, padx=20)

delete_student_button = ttk.Button(left_frame, text="Delete Student", width=25, state=DISABLED, command=delete_student)
delete_student_button.grid(row=5, column=0, pady=10, padx=20)

export_student_button = ttk.Button(left_frame, text="Export Data", width=25, state=DISABLED, command=export_data)
export_student_button.grid(row=6, column=0, pady=10, padx=20)

exit_button = ttk.Button(left_frame, text="Exit", width=25, command=exit_closed)
exit_button.grid(row=7, column=0, pady=10, padx=20)

right_frame = Frame(root)
right_frame.place(x=350, y=80, width=820, height=600)

scroll_barX = Scrollbar(right_frame, orient=HORIZONTAL)
scroll_barY = Scrollbar(right_frame, orient=VERTICAL)


student_table = ttk.Treeview(right_frame, columns=("Student ID", "Name", "Father's Name", "Gender"
                                                 , "D.O.B", "Courses", "Mobile No.", "Email ID", "Address", "Added Date", "Added Time")
                           , xscrollcommand=scroll_barX.set, yscrollcommand=scroll_barY.set)
scroll_barX.config(command=student_table.xview)
scroll_barY.config(command=student_table.yview)

scroll_barX.pack(side=BOTTOM, fill=X)
scroll_barY.pack(side=RIGHT, fill=Y)

student_table.pack(fill=BOTH, expand=1)
student_table.heading("Student ID", text="Student ID")
student_table.heading("Name", text="Name")
student_table.heading("Father's Name", text="Father's Name")
student_table.heading("Gender", text="Gender")
student_table.heading("D.O.B", text="D.O.B")
student_table.heading("Courses", text="Courses")
student_table.heading("Mobile No.", text="Mobile No.")
student_table.heading("Email ID", text="Email ID")
student_table.heading("Email ID", text="Email ID")
student_table.heading("Address", text="Address")
student_table.heading("Added Date", text="Added Date")
student_table.heading("Added Time", text="Added time")

student_table.config(show="headings")

student_table.column("Student ID", width=110, anchor=CENTER)
student_table.column("Name", width=250, anchor=CENTER)
student_table.column("Father's Name", width=250, anchor=CENTER)
student_table.column("Gender", width=110, anchor=CENTER)
student_table.column("D.O.B", width=110, anchor=CENTER)
student_table.column("Courses", width=250, anchor=CENTER)
student_table.column("Mobile No.", width=130, anchor=CENTER)
student_table.column("Email ID", width=250, anchor=CENTER)
student_table.column("Address", width=600, anchor=CENTER)
student_table.column("Added Date", width=120, anchor=CENTER)
student_table.column("Added Time", width=120, anchor=CENTER)

student_table_style = ttk.Style()

student_table_style.configure("Treeview", rowheight=40, font=("arial", 12))
student_table_style.configure("Treeview.Heading", font=("arial", 14, "bold"))


root.mainloop()
