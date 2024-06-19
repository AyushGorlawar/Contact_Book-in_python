import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

CONTACTS_FILE = "contacts.json"

class ContactBook:
    def __init__(self):
        self.contacts = self.load_contacts()

    def load_contacts(self):
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, "r") as file:
                return json.load(file)
        return []

    def save_contacts(self):
        with open(CONTACTS_FILE, "w") as file:
            json.dump(self.contacts, file)

    def add_contact(self, name, phone, email, address):
        self.contacts.append({"name": name, "phone": phone, "email": email, "address": address})
        self.save_contacts()

    def update_contact(self, index, name, phone, email, address):
        self.contacts[index] = {"name": name, "phone": phone, "email": email, "address": address}
        self.save_contacts()

    def delete_contact(self, index):
        del self.contacts[index]
        self.save_contacts()

    def search_contacts(self, query):
        return [contact for contact in self.contacts if query.lower() in contact["name"].lower() or query in contact["phone"]]

contact_book = ContactBook()

def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()
    
    if name and phone:
        contact_book.add_contact(name, phone, email, address)
        update_contact_listbox()
        clear_entries()
    else:
        messagebox.showwarning("Warning", "Name and phone are required.")

def update_contact():
    selected_contact_index = contact_listbox.curselection()
    if selected_contact_index:
        index = selected_contact_index[0]
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()
        
        if name and phone:
            contact_book.update_contact(index, name, phone, email, address)
            update_contact_listbox()
            clear_entries()
        else:
            messagebox.showwarning("Warning", "Name and phone are required.")
    else:
        messagebox.showwarning("Warning", "You must select a contact to update.")

def delete_contact():
    selected_contact_index = contact_listbox.curselection()
    if selected_contact_index:
        index = selected_contact_index[0]
        contact_book.delete_contact(index)
        update_contact_listbox()
        clear_entries()
    else:
        messagebox.showwarning("Warning", "You must select a contact to delete.")

def search_contact():
    query = search_entry.get()
    results = contact_book.search_contacts(query)
    update_contact_listbox(results)

def update_contact_listbox(filtered_contacts=None):
    contact_listbox.delete(0, tk.END)
    for contact in (filtered_contacts or contact_book.contacts):
        contact_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

def on_contact_select(event):
    selected_contact_index = contact_listbox.curselection()
    if selected_contact_index:
        index = selected_contact_index[0]
        contact = contact_book.contacts[index]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, contact["name"])
        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, contact["phone"])
        email_entry.delete(0, tk.END)
        email_entry.insert(0, contact["email"])
        address_entry.delete(0, tk.END)
        address_entry.insert(0, contact["address"])

def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

# Initialize the main window
root = tk.Tk()
root.title("Contact Book")

# Create widgets
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(root, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Phone:").grid(row=1, column=0, padx=10, pady=5)
phone_entry = tk.Entry(root, width=30)
phone_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Email:").grid(row=2, column=0, padx=10, pady=5)
email_entry = tk.Entry(root, width=30)
email_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Address:").grid(row=3, column=0, padx=10, pady=5)
address_entry = tk.Entry(root, width=30)
address_entry.grid(row=3, column=1, padx=10, pady=5)

add_button = tk.Button(root, text="Add Contact", command=add_contact)
add_button.grid(row=4, column=0, padx=10, pady=10)

update_button = tk.Button(root, text="Update Contact", command=update_contact)
update_button.grid(row=4, column=1, padx=10, pady=10)

delete_button = tk.Button(root, text="Delete Contact", command=delete_contact)
delete_button.grid(row=5, column=0, padx=10, pady=10)

tk.Label(root, text="Search:").grid(row=6, column=0, padx=10, pady=5)
search_entry = tk.Entry(root, width=30)
search_entry.grid(row=6, column=1, padx=10, pady=5)

search_button = tk.Button(root, text="Search", command=search_contact)
search_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

contact_listbox = tk.Listbox(root, width=50, height=10)
contact_listbox.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
contact_listbox.bind("<<ListboxSelect>>", on_contact_select)

# Update the listbox with initial contacts
update_contact_listbox()

# Run the main loop
root.mainloop()
