import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ---------------------- Database Setup ----------------------
def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="srikar123",
        database="railway"
    )
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(100)
        )
    ''')

    # Create trains table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trains (
            train_id INT AUTO_INCREMENT PRIMARY KEY,
            train_name VARCHAR(100) NOT NULL,
            source VARCHAR(100) NOT NULL,
            destination VARCHAR(100) NOT NULL,
            total_seats INT NOT NULL,
            available_seats INT NOT NULL
        )
    ''')

    # Create bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INT AUTO_INCREMENT PRIMARY KEY,
            passenger_name VARCHAR(100) NOT NULL,
            train_id INT,
            seats_booked INT,
            status VARCHAR(50),
            FOREIGN KEY (train_id) REFERENCES trains(train_id)
        )
    ''')

    # Add sample trains (only once)
    cursor.execute("SELECT COUNT(*) FROM trains")
    if cursor.fetchone()[0] == 0:
        trains = [
            ("Rajdhani Express", "Delhi", "Mumbai", 200, 200),
            ("Chennai Express", "Chennai", "Bangalore", 150, 150),
            ("Shatabdi Express", "Kolkata", "Delhi", 180, 180),
            ("Duronto Express", "Hyderabad", "Pune", 120, 120)
        ]
        cursor.executemany(
            "INSERT INTO trains (train_name, source, destination, total_seats, available_seats) VALUES (%s, %s, %s, %s, %s)",
            trains
        )

    conn.commit()
    conn.close()


# ---------------------- Login & Register Window ----------------------
class LoginRegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚆 Railway Booking - Login/Register")
        self.root.geometry("400x350")
        self.root.config(bg="#e6f2ff")

        tk.Label(root, text="Railway Ticket System", font=("Arial", 18, "bold"), bg="#004d99", fg="white").pack(fill=tk.X)

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=True, fill="both", padx=20, pady=20)

        # Tabs
        self.login_tab = tk.Frame(self.tabs, bg="#f9f9f9")
        self.register_tab = tk.Frame(self.tabs, bg="#f9f9f9")

        self.tabs.add(self.login_tab, text="Login")
        self.tabs.add(self.register_tab, text="Register")

        self.create_login_tab()
        self.create_register_tab()

    def create_login_tab(self):
        tk.Label(self.login_tab, text="Email:", bg="#f9f9f9", font=("Arial", 12)).pack(pady=10)
        self.login_email = tk.Entry(self.login_tab, width=30)
        self.login_email.pack()

        tk.Label(self.login_tab, text="Password:", bg="#f9f9f9", font=("Arial", 12)).pack(pady=10)
        self.login_password = tk.Entry(self.login_tab, width=30, show="*")
        self.login_password.pack()

        tk.Button(self.login_tab, text="Login", command=self.login, bg="#4CAF50", fg="white", width=15).pack(pady=15)

    def create_register_tab(self):
        tk.Label(self.register_tab, text="Full Name:", bg="#f9f9f9", font=("Arial", 12)).pack(pady=10)
        self.reg_name = tk.Entry(self.register_tab, width=30)
        self.reg_name.pack()

        tk.Label(self.register_tab, text="Email:", bg="#f9f9f9", font=("Arial", 12)).pack(pady=10)
        self.reg_email = tk.Entry(self.register_tab, width=30)
        self.reg_email.pack()

        tk.Label(self.register_tab, text="Password:", bg="#f9f9f9", font=("Arial", 12)).pack(pady=10)
        self.reg_password = tk.Entry(self.register_tab, width=30, show="*")
        self.reg_password.pack()

        tk.Button(self.register_tab, text="Register", command=self.register, bg="#0275d8", fg="white", width=15).pack(pady=15)

    def login(self):
        email = self.login_email.get()
        password = self.login_password.get()

        if not email or not password:
            messagebox.showwarning("Error", "Please fill all fields")
            return

        conn = mysql.connector.connect(host="localhost", user="root", password="srikar123", database="railway")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", f"Welcome {user[1]}!")
            self.root.destroy()
            main_root = tk.Tk()
            app = RailwayBookingApp(main_root)
            main_root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")

    def register(self):
        name = self.reg_name.get()
        email = self.reg_email.get()
        password = self.reg_password.get()

        if not name or not email or not password:
            messagebox.showwarning("Error", "Please fill all fields")
            return

        conn = mysql.connector.connect(host="localhost", user="root", password="srikar123", database="railway")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            conn.commit()
            messagebox.showinfo("Success", "Registered successfully! Please login now.")
            self.tabs.select(self.login_tab)
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Error", "Email already registered!")
        conn.close()


# ---------------------- Main App ----------------------
class RailwayBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚆 Railway Ticket Booking System")
        self.root.geometry("750x500")
        self.root.config(bg="#f0f0f0")

        title = tk.Label(root, text="Railway Ticket Booking System", font=("Arial", 18, "bold"), bg="#004d99", fg="white")
        title.pack(fill=tk.X, pady=5)

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.book_tab = tk.Frame(self.tabs, bg="#f7f7f7")
        self.cancel_tab = tk.Frame(self.tabs, bg="#f7f7f7")
        self.view_tab = tk.Frame(self.tabs, bg="#f7f7f7")

        self.tabs.add(self.book_tab, text="Book Ticket")
        self.tabs.add(self.cancel_tab, text="Cancel Ticket")
        self.tabs.add(self.view_tab, text="View Bookings")

        self.create_booking_tab()
        self.create_cancel_tab()
        self.create_view_tab()

    # ---------------------- Booking Tab ----------------------
    def create_booking_tab(self):
        tk.Label(self.book_tab, text="Passenger Name:", bg="#f7f7f7", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        self.passenger_entry = tk.Entry(self.book_tab, width=30)
        self.passenger_entry.grid(row=0, column=1)

        tk.Label(self.book_tab, text="Select Train:", bg="#f7f7f7", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
        self.train_combo = ttk.Combobox(self.book_tab, width=28, state="readonly")
        self.train_combo.grid(row=1, column=1)

        tk.Label(self.book_tab, text="Seats to Book:", bg="#f7f7f7", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
        self.seat_entry = tk.Entry(self.book_tab, width=30)
        self.seat_entry.grid(row=2, column=1)

        tk.Button(self.book_tab, text="Book Ticket", command=self.book_ticket, bg="#4CAF50", fg="white", width=20).grid(row=3, column=1, pady=15)

        self.train_list = ttk.Treeview(self.book_tab, columns=("Train Name", "Source", "Destination", "Seats"), show="headings", height=8)
        for col in ("Train Name", "Source", "Destination", "Seats"):
            self.train_list.heading(col, text=col)
        self.train_list.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.load_trains()

    def load_trains(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="srikar123", database="railway")
        cursor = conn.cursor()
        cursor.execute("SELECT train_id, train_name, source, destination, available_seats FROM trains")
        rows = cursor.fetchall()
        conn.close()

        self.train_combo["values"] = [f"{r[0]} - {r[1]}" for r in rows]
        for row in self.train_list.get_children():
            self.train_list.delete(row)
        for r in rows:
            self.train_list.insert("", tk.END, values=(r[1], r[2], r[3], r[4]))

    def book_ticket(self):
        name = self.passenger_entry.get()
        selected_train = self.train_combo.get()
        seats = self.seat_entry.get()

        if not name or not selected_train or not seats:
            messagebox.showwarning("Missing Data", "Please fill all fields.")
            return

        try:
            seats = int(seats)
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a valid number of seats.")
            return

        train_id = int(selected_train.split(" - ")[0])
        conn = mysql.connector.connect(host="localhost", user="root", password="srikar123", database="railway")
        cursor = conn.cursor()

        cursor.execute("SELECT available_seats FROM trains WHERE train_id=%s", (train_id,))
        available = cursor.fetchone()[0]

        if seats > available:
            messagebox.showerror("Error", "Not enough seats available.")
        else:
            new_available = available - seats
            cursor.execute("UPDATE trains SET available_seats=%s WHERE train_id=%s", (new_available, train_id))
            cursor.execute("INSERT INTO bookings (passenger_name, train_id, seats_booked, status) VALUES (%s, %s, %s, %s)",
                           (name, train_id, seats, "Booked"))
            conn.commit()
            messagebox.showinfo("Success", f"Ticket booked successfully for {name}!")
            self.load_trains()

        conn.close()

    # ---------------------- Cancel Tab ----------------------
    def create_cancel_tab(self):
        tk.Label(self.cancel_tab, text="Booking ID:", bg="#f7f7f7", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        self.cancel_entry = tk.Entry(self.cancel_tab, width=30)
        self.cancel_entry.grid(row=0, column=1)

        tk.Button(self.cancel_tab, text="Cancel Ticket", command=self.cancel_ticket, bg="#d9534f", fg="white", width=20).grid(row=1, column=1, pady=10)

    def cancel_ticket(self):
        booking_id = self.cancel_entry.get()
        if not booking_id:
            messagebox.showwarning("Missing Data", "Please enter a booking ID.")
            return

        conn = mysql.connector.connect(host="localhost", user="root", password="srikar123", database="railway")
        cursor = conn.cursor()
        cursor.execute("SELECT train_id, seats_booked, status FROM bookings WHERE booking_id=%s", (booking_id,))
        result = cursor.fetchone()

        if result:
            train_id, seats, status = result
            if status == "Cancelled":
                messagebox.showinfo("Already Cancelled", "This booking is already cancelled.")
            else:
                cursor.execute("UPDATE bookings SET status='Cancelled' WHERE booking_id=%s", (booking_id,))
                cursor.execute("UPDATE trains SET available_seats = available_seats + %s WHERE train_id=%s", (seats, train_id))
                conn.commit()
                messagebox.showinfo("Cancelled", f"Booking ID {booking_id} cancelled successfully!")
        else:
            messagebox.showerror("Not Found", "Booking ID not found.")

        conn.close()

    # ---------------------- View Bookings ----------------------
    def create_view_tab(self):
        self.booking_list = ttk.Treeview(self.view_tab, columns=("ID", "Passenger", "Train", "Seats", "Status"), show="headings")
        for col in ("ID", "Passenger", "Train", "Seats", "Status"):
            self.booking_list.heading(col, text=col)
        self.booking_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Button(self.view_tab, text="Refresh", command=self.view_bookings, bg="#0275d8", fg="white").pack(pady=5)

        self.view_bookings()

    def view_bookings(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="srikar123", database="railway")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.booking_id, b.passenger_name, t.train_name, b.seats_booked, b.status
            FROM bookings b JOIN trains t ON b.train_id = t.train_id
        ''')
        rows = cursor.fetchall()
        conn.close()

        for r in self.booking_list.get_children():
            self.booking_list.delete(r)
        for row in rows:
            self.booking_list.insert("", tk.END, values=row)


# ---------------------- Run Application ----------------------
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = LoginRegisterApp(root)
    root.mainloop()
