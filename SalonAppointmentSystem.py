import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3


class SalonBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Salon Appointment Booking System")
        self.root.geometry("900x650")
        self.root.resizable(0, 0)

        # Set the background color for the main window
        self.root.config(bg="lightyellow")

        # Database Initialization
        self.db_connection = sqlite3.connect('salon_appointments.db')
        self.db_cursor = self.db_connection.cursor()
        self.create_tables()  # Create all required tables
        
        self.appointments = []
        self.services_with_prices = self.fetch_services()
        self.stylists = self.fetch_stylists()

        self.create_welcome_screen()  # Start directly with the welcome screen
        
    def create_tables(self):
        # Create appointments table
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                email TEXT,
                service TEXT,
                stylist TEXT,
                date TEXT,
                time TEXT
            )
        ''')

        # Create services table
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                service_name TEXT PRIMARY KEY,
                price REAL
            )
        ''')
        self.populate_services()

        # Create stylists table
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS stylists (
                name TEXT PRIMARY KEY,
                experience TEXT,
                specialty TEXT,
                email TEXT
            )
        ''')
        self.populate_stylists()

        self.db_connection.commit()
        
    def populate_services(self):
        # Insert default services and prices if the table is empty
        self.db_cursor.execute("SELECT COUNT(*) FROM services")
        if self.db_cursor.fetchone()[0] == 0:
            default_services = [
                ("Haircut", 80),
                ("Manicure", 150),
                ("Pedicure", 150),
                ("Facial", 1500),
                ("Massage", 500)
            ]
            self.db_cursor.executemany("INSERT INTO services (service_name, price) VALUES (?, ?)", default_services)

    def populate_stylists(self):
        # Insert default stylists if the table is empty
        self.db_cursor.execute("SELECT COUNT(*) FROM stylists")
        if self.db_cursor.fetchone()[0] == 0:
            default_stylists = [
                ("Anna Reyes", "6 years", "Haircuts, Color, Rebond", "anna@example.com"),
                ("Jane Bien", "4 years", "Manicure, Pedicure, Nail Art", "jane@example.com"),
                ("Emily Davis", "8 years", "Facial, Massage", "emily@example.com"),
                ("Lara Hernandez", "4 years", "Haircuts, Color, Hair Treatment", "lara@example.com")
            ]
            self.db_cursor.executemany("INSERT INTO stylists (name, experience, specialty, email) VALUES (?, ?, ?, ?)", default_stylists)

    def fetch_services(self):
        # Retrieve services and prices from the database
        self.db_cursor.execute("SELECT * FROM services")
        return {row[0]: row[1] for row in self.db_cursor.fetchall()}

    def fetch_stylists(self):
        # Retrieve stylists from the database
        self.db_cursor.execute("SELECT * FROM stylists")
        return {
            row[0]: {"experience": row[1], "specialty": row[2], "email": row[3]}
            for row in self.db_cursor.fetchall()
        }
        self.db_connection.commit()
        
    def create_welcome_screen(self):
        self.clear_screen()

        # Welcome Label
        tk.Label(self.root, text="Welcome to the Salon Appointment System", font=("Times", 20, "bold"), pady=20, bg="lightyellow").pack()

        # Instructions Label
        tk.Label(self.root, text="Please choose an option below:", font=("Times", 14), pady=10, bg="lightyellow").pack()

        # Buttons
        tk.Button(self.root, text="Book Appointment", command=self.show_login_screen, bg="lightblue", font=("Arial", 14), width=20, height=2).pack(pady=20)
        tk.Button(self.root, text="Admin", command=self.show_admin_login_screen, bg="lightgreen", font=("Arial", 14), width=20, height=2).pack()
    
    def show_admin_login_screen(self):
        self.clear_screen()

        # Admin Login Frame
        login_frame = tk.Frame(self.root, bg="lightyellow")
        login_frame.pack(pady=70)

        # Admin Login Title
        tk.Label(self.root, text="Admin Login", font=("Times", 20, "bold"), pady=20, bg="lightyellow").pack()

        # Instructions Label
        tk.Label(self.root, text="Enter admin credentials to proceed:", font=("Times", 14), pady=10, bg="lightyellow").pack()

        # Username Label and Entry
        tk.Label(self.root, text="Username:", font=("Arial", 12), bg="lightyellow").pack(pady=5)
        self.admin_username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.admin_username_entry.pack(pady=5)

        # Password Label and Entry
        tk.Label(self.root, text="Password:", font=("Arial", 12), bg="lightyellow").pack(pady=5)
        self.admin_password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        self.admin_password_entry.pack(pady=5)

        # Login Button
        login_button = tk.Button(self.root, text="Login", command=self.admin_login, bg="lightblue", font=("Arial", 14), width=20, height=2)
        login_button.pack(pady=20)

    def admin_login(self):
        admin_username = self.admin_username_entry.get()
        admin_password = self.admin_password_entry.get()

        # Hardcoded admin credentials for simplicity
        if admin_username == "admin" and admin_password == "admin123":
            self.admin_action()  # Proceed to the admin panel after successful login
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def admin_action(self):
        self.clear_screen()  # Clear the current screen

        # Frame for Admin Panel
        admin_frame = tk.Frame(self.root, bg="lightyellow")
        admin_frame.pack(fill="both", expand=True, pady=20, padx=20)

        # Label for Admin Panel
        tk.Label(admin_frame, text="Admin Information Panel", font=("Times", 14, "bold"), bg="lightyellow").pack(pady=20)

        # Buttons for different sections
        button_frame = tk.Frame(admin_frame, bg="lightyellow")
        button_frame.pack(side="top", pady=10)

        tk.Button(button_frame, text="Customer Information", command=self.display_customer_info, bg="lightblue", width=30, height=2).pack(pady=10)
        tk.Button(button_frame, text="Stylist Information", command=self.display_stylist_info, bg="lightgreen", width=30, height=2).pack(pady=10)
        tk.Button(button_frame, text="Services and Prices", command=self.display_service_info, bg="lightpink", width=30, height=2).pack(pady=10)

        # Treeview Frame for Displaying Data
        treeview_frame = tk.Frame(admin_frame, bg="lightyellow")
        treeview_frame.pack(side="top", fill="both", expand=True, pady=20, padx=20)

        self.treeview = ttk.Treeview(treeview_frame, show="headings")
        self.treeview.pack(side="top", fill="both", expand=True)

        # Buttons for Update, Delete, and Exit actions
        action_frame = tk.Frame(admin_frame, bg="lightyellow")  # Below the treeview
        action_frame.pack(side="bottom", pady=10)

        tk.Button(action_frame, text="Update", command=self.update_appointment, bg="lightblue", width=15, height=2).pack(side="left", padx=10)
        tk.Button(action_frame, text="Delete", command=self.delete_appointment, bg="lightcoral", width=15, height=2).pack(side="left", padx=10)
        tk.Button(action_frame, text="Exit", command=self.exit_admin_panel, bg="lightcoral", width=15, height=2).pack(side="right", padx=10)

    def exit_admin_panel(self):
        messagebox.showinfo("Thank You", "Thank you for using the Salon Appointment System!")
        self.root.quit()  # Close the application

    def display_customer_info(self):
        self.treeview.delete(*self.treeview.get_children())  # Clear any previous data
        self.treeview["columns"] = ("Name", "Phone", "Email", "Service", "Stylist", "Date", "Time")
        
        # Set column headings with alignment
        for col in self.treeview["columns"]:
            self.treeview.heading(col, text=col, anchor="center")
            self.treeview.column(col, anchor="center", width=120)  # Adjust width as needed

        # Fetch data from the database
        self.db_cursor.execute("SELECT * FROM appointments")
        appointments = self.db_cursor.fetchall()

        # Insert data rows
        for app in appointments:
            self.treeview.insert("", tk.END, values=(app[1], app[2], app[3], app[4], app[5], app[6], app[7]))

    def delete_appointment(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "No appointment selected!")
            return

        for item in selected_item:
            values = self.treeview.item(item, "values")
            self.treeview.delete(item)

            # Remove from database
            self.db_cursor.execute("DELETE FROM appointments WHERE name = ? AND phone = ?", (values[0], values[1]))
            self.db_connection.commit()

        # Show success message after deletion
        messagebox.showinfo("Success", "Appointment deleted successfully!")


    def update_appointment(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "No appointment selected!")
            return

        for item in selected_item:
            values = self.treeview.item(item, "values")
            selected_name = values[0]  # Use "Name" as the unique identifier

        # Find the appointment in the database
        self.db_cursor.execute("SELECT * FROM appointments WHERE name = ? AND phone = ?", (selected_name, values[1]))
        appointment = self.db_cursor.fetchone()

        if not appointment:
            messagebox.showerror("Error", "Could not find the selected appointment!")
            return

        # Create a pop-up window for updating the appointment
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Appointment")
        update_window.geometry("400x400")
        update_window.config(bg="lightyellow")

        # Fields for editing
        fields = {
            "Name": "name",
            "Phone": "phone",
            "Email": "email",
            "Service": "service",
            "Stylist": "stylist",
            "Date": "date",
            "Time": "time"
        }
        entries = {}

        # Labels and Entry widgets
        for i, (label, key) in enumerate(fields.items()):
            tk.Label(update_window, text=label, bg="lightyellow", font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(update_window, font=("Arial", 12), width=30)
            entry.insert(0, appointment[i+1])  # Prefill with existing data
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entries[key] = entry

        def save_changes():
            # Save updated values back to the database
            self.db_cursor.execute('''UPDATE appointments SET name = ?, phone = ?, email = ?, service = ?, stylist = ?, date = ?, time = ? 
                                    WHERE id = ?''', 
                                    (entries["name"].get(), entries["phone"].get(), entries["email"].get(), entries["service"].get(), 
                                     entries["stylist"].get(), entries["date"].get(), entries["time"].get(), appointment[0]))
            self.db_connection.commit()

            # Refresh the Treeview to show updated data
            self.display_customer_info()
            messagebox.showinfo("Success", "Appointment updated successfully!")
            update_window.destroy()

        # Save button
        tk.Button(update_window, text="Save Changes", command=save_changes, bg="lightgreen", font=("Arial", 12), width=20).grid(row=len(fields), column=0, columnspan=2, pady=20)
        
    def display_stylist_info(self):
        self.treeview.delete(*self.treeview.get_children())  # Clear any previous data
        self.treeview["columns"] = ("Stylist", "Experience", "Specialty", "Email")
        
        # Set column headings with alignment
        for col in self.treeview["columns"]:
            self.treeview.heading(col, text=col, anchor="center")
            self.treeview.column(col, anchor="center", width=100)  # Adjust width as needed

        # Insert data rows
        for stylist, info in self.stylists.items():
            self.treeview.insert("", tk.END, values=(stylist, info["experience"], info["specialty"], info["email"]))

    def display_service_info(self):
        self.treeview.delete(*self.treeview.get_children())  # Clear any previous data
        self.treeview["columns"] = ("Service", "Price")
        
        # Set column headings with alignment
        for col in self.treeview["columns"]:
            self.treeview.heading(col, text=col, anchor="center")
            self.treeview.column(col, anchor="center", width=100)  # Adjust width as needed

        # Insert data rows
        for service, price in self.services_with_prices.items():
            self.treeview.insert("", tk.END, values=(service, price))

    def show_login_screen(self):
        self.clear_screen()
        
        # Frame for Login Screen
        login_frame = tk.Frame(self.root, bg="lightyellow")
        login_frame.pack(pady=70)

        # Login Title
        tk.Label(self.root, text="Login to Book Appointment", font=("Times", 20, "bold"), pady=20, bg="lightyellow").pack()

        # Instructions Label
        tk.Label(self.root, text="Enter username and password to proceed:", font=("Times", 14), pady=10, bg="lightyellow").pack()

        # Username Label and Entry
        tk.Label(self.root, text="Username:", font=("Arial", 12), bg="lightyellow").pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        # Password Label and Entry
        tk.Label(self.root, text="Password:", font=("Arial", 12), bg="lightyellow").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)

        # Login Button
        login_button = tk.Button(self.root, text="Login", command=self.login, bg="lightblue", font=("Arial", 14), width=20, height=2)
        login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Hardcoded credentials for simplicity
        if username == "" and password == "":
            self.create_booking_screen()  # Proceed to booking screen after successful login
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def create_booking_screen(self):
        self.clear_screen()

        # Create a frame to hold the entire booking form
        main_frame = tk.Frame(self.root, bg="lightblue")
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Create a grid layout: 2 columns, with left and right frames
        main_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        main_frame .grid_columnconfigure(1, weight=1, uniform="group1")

        # Left Side Frame
        left_frame = tk.Frame(main_frame, bg="lightblue")
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Right Side Frame
        right_frame = tk.Frame(main_frame, bg="lightblue")
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        

        # Title Label
        tk.Label(left_frame, text="Salon Appointment Booking", font=("Times", 16, "bold"), pady=10, bg="lightblue").grid(row=0, column=0, columnspan=2, sticky="w")

        # Customer Name
        tk.Label(left_frame, text="Customer Name:", anchor="w", bg="lightblue").grid(row=1, column=0, pady=5, padx=10, sticky="w")
        self.name_entry = tk.Entry(left_frame, width=30)
        self.name_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        # Customer Phone Number
        tk.Label(left_frame, text="Phone Number:", anchor="w", bg="lightblue").grid(row=2, column=0, pady=5, padx=10, sticky="w")
        self.phone_entry = tk.Entry(left_frame, width=30)
        self.phone_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        # Customer Email
        tk.Label(left_frame, text="Email:", anchor="w", bg="lightblue").grid(row=3, column=0, pady=5, padx=10, sticky="w")
        self.email_entry = tk.Entry(left_frame, width=30)
        self.email_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")

        # Service Options (on the left side)
        tk.Label(left_frame, text="Service:", anchor="w", bg="lightblue").grid(row=4, column=0, pady=5, padx=10, sticky="w")
        self.service_listbox = tk.Listbox(left_frame, height=5, width=30, selectmode=tk.SINGLE)
        for service, price in self.services_with_prices.items():
            self.service_listbox.insert(tk.END, f"{service} - ${price}")
        self.service_listbox.grid(row=4, column=1, pady=5, padx=10, sticky="w")

        # Stylist Selection
        tk.Label(right_frame, text="Select Stylist:", anchor="w", bg="lightblue").grid(row=1, column=0, pady=5, padx=10, sticky="w")
        self.stylist_var = tk.StringVar(value="STYLIST")
        stylists = ["Anna Reyes", "Jane Bien", "Emily Davis", "Lara Hernandez"]
        self.stylist_menu = tk.OptionMenu(right_frame, self.stylist_var, *stylists)
        self.stylist_menu.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        # Date
        tk.Label(right_frame, text="Date (YYYY-MM-DD):", anchor="w", bg="lightblue").grid(row=2, column=0, pady=5, padx=10, sticky="w")
        self.date_entry = tk.Entry(right_frame, width=30)
        self.date_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        # Time
        tk.Label(right_frame, text="Time:", anchor="w", bg="lightblue").grid(row=3, column=0, pady=5, padx=10, sticky="w")
        self.time_var = tk.StringVar(value="TIME")
        time_slots = [
            "10:00", "11:00",
            "01:00", "01:30",
            "02:00", "03:00",
            "04:00 - 4:30"
        ]
        self.time_menu = tk.OptionMenu(right_frame, self.time_var, *time_slots)
        self.time_menu.grid(row=3, column=1, pady=5, padx=10, sticky="w")

        # Payment Method Selection (on the right side)
        tk.Label(right_frame, text="Payment Method:", anchor="w", bg="lightblue").grid(row=4, column=0, pady=5, padx=10, sticky="w")
        self.payment_var = tk.StringVar(value="Payment Method")
        payment_methods = ["Credit Card", "Cash", "Pay Pal"]
        self.payment_menu = tk.OptionMenu(right_frame, self.payment_var, *payment_methods)
        self.payment_menu.grid(row=4, column=1, pady=5, padx=10, sticky="w")
        

        # Receipt Box (Below Customer Details)
        receipt_frame = tk.Frame(main_frame, bg="lightblue")
        receipt_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Center the receipt within the frame
        receipt_title_label = tk.Label(receipt_frame, text="Appointment Receipt", anchor="w", bg="lightblue", font=("Arial", 14, "bold"))
        receipt_title_label.pack(anchor="w", padx=10, pady=5)

        # Receipt Text Box
        self.receipt_text = tk.Label(receipt_frame, text="Appointment Receipt details.", anchor="w", bg="lightyellow", font=("Times", 12), width=80, height=10)
        self.receipt_text.pack(anchor="w", padx=10, pady=5)

        # Back to Welcome Button (on the right side below the receipt)
        back_button = tk.Button(receipt_frame, text="Exit", command=self.create_welcome_screen, bg="lightcoral", width=20)
        back_button.pack(pady=10, padx=10, side="right")

        # Submit Button (on the right side)
        submit_button = tk.Button(right_frame, text="Book Appointment", command=self.book_appointment, bg="lightgreen", width=20)
        submit_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

    def update_receipt_text(self, name, service, date, time, stylist, payment_method):
    # Update the receipt box text with aligned formatting

        receipt_details = (
        f"\t{'Appointment Details:':<25}\n"
        f"\t{'Name':<15}:      {name}\n"
        f"\t{'Service':<15}:   {service}\n"
        f"\t\t{'Date':<15} :     {date}\n"
        f"\t{'Time':<16} :     {time}\n"
        f"\t{'Stylist':<15}:   {stylist}\n"
        f"\t{'Payment Method':<15}: {payment_method}"
        )   
        self.receipt_text.config(text=receipt_details)


    def book_appointment(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        service = self.service_listbox.get(tk.ACTIVE)
        stylist = self.stylist_var.get()
        date = self.date_entry.get()
        time = self.time_var.get()
        payment_method = self.payment_var.get()

        if not name or not phone or not email or not service or not stylist or not date or not time or not payment_method:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Update the receipt with the entered data
        self.update_receipt_text(name, service.split(" - ")[0], date, time, stylist, payment_method)
        
        # Insert the appointment data into the database
        self.db_cursor.execute('''INSERT INTO appointments (name, phone, email, service, stylist, date, time) 
                                VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                                (name, phone, email, service.split(" - ")[0], stylist, date, time))
        self.db_connection.commit()

        self.appointments.append({
            "name":    name,
            "phone":   phone,
            "email":   email,
            "service": service.split(" - ")[0],
            "stylist": stylist,
            "date":    date,
            "time":    time
        })

        #messagebox.showinfo("Success", "Appointment booked successfully!")
        #self.create_welcome_screen()  # Return to welcome screen after booking

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Create the main window and pass it to the SalonBookingSystem
root = tk.Tk()
app = SalonBookingSystem(root)
root.mainloop()