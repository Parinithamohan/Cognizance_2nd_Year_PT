import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="mysql",  
    database="skyways_flight_management"
)
cursor = db.cursor()

# Function to book a flight
def book_flight():
    user_name = user_name_entry.get()
    flight_id = flight_id_entry.get()

    if not user_name or not flight_id:
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        cursor.execute("INSERT INTO booked_flights (user_name, flight_id) VALUES (%s, %s)", (user_name, flight_id))
        db.commit()
        messagebox.showinfo("Success", "Flight booked successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error occurred: {err}")

# Function to view available flights
def view_flights():
    cursor.execute("SELECT * FROM available_flights")
    rows = cursor.fetchall()

    available_flights_list.delete(0, tk.END)
    for row in rows:
        available_flights_list.insert(tk.END, row)

# Function to view booked flights
def view_booked_flights():
    user_name = user_name_entry.get()

    if not user_name:
        messagebox.showerror("Error", "User name is required")
        return

    cursor.execute("SELECT bf.booking_id, af.flight_number, af.start, af.destination, af.price "
                   "FROM booked_flights bf "
                   "JOIN available_flights af ON bf.flight_id = af.flight_id "
                   "WHERE bf.user_name = %s", (user_name,))
    rows = cursor.fetchall()

    booked_flights_list.delete(0, tk.END)
    for row in rows:
        booked_flights_list.insert(tk.END, row)

# Function to cancel a booked flight
def cancel_flight():
    booking_id = booking_id_entry.get()

    if not booking_id:
        messagebox.showerror("Error", "Booking ID is required")
        return

    cursor.execute("DELETE FROM booked_flights WHERE booking_id = %s", (booking_id,))
    db.commit()
    messagebox.showinfo("Success", "Booking canceled successfully")

# Tkinter GUI setup
root = tk.Tk()
root.title("Skyways Flight Management System")

# Available flights list
tk.Label(root, text="Available Flights:").grid(row=0, column=0, columnspan=2)
available_flights_list = tk.Listbox(root, height=5, width=50)
available_flights_list.grid(row=1, column=0, columnspan=2)
view_flights()

# User input fields
tk.Label(root, text="User Name:").grid(row=2, column=0)
user_name_entry = tk.Entry(root)
user_name_entry.grid(row=2, column=1)

tk.Label(root, text="Flight ID:").grid(row=3, column=0)
flight_id_entry = tk.Entry(root)
flight_id_entry.grid(row=3, column=1)

# Buttons for booking and viewing flights
tk.Button(root, text="Book Flight", command=book_flight).grid(row=4, column=0)
tk.Button(root, text="View Booked Flights", command=view_booked_flights).grid(row=4, column=1)

# Booked flights list
tk.Label(root, text="Booked Flights:").grid(row=5, column=0, columnspan=2)
booked_flights_list = tk.Listbox(root, height=5, width=50)
booked_flights_list.grid(row=6, column=0, columnspan=2)

# Cancel flight section
tk.Label(root, text="Booking ID to Cancel:").grid(row=7, column=0)
booking_id_entry = tk.Entry(root)
booking_id_entry.grid(row=7, column=1)

tk.Button(root, text="Cancel Flight", command=cancel_flight).grid(row=8, column=0, columnspan=2)

# Start the Tkinter event loop
root.mainloop()
