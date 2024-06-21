import tkinter as tk
from tkinter import messagebox
import csv

class InventoryItem:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

class InventoryManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Inventory Management System")
        self.master.configure(background="#f0f0f0")

        self.inventory = []

        self.load_inventory_from_file()

        self.create_widgets()

    def create_widgets(self):
        self.label_name = tk.Label(self.master, text="Product Name:", bg="#f0f0f0")
        self.label_name.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.entry_name = tk.Entry(self.master)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        self.label_quantity = tk.Label(self.master, text="Quantity(Kg):", bg="#f0f0f0")
        self.label_quantity.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.entry_quantity = tk.Entry(self.master)
        self.entry_quantity.grid(row=1, column=1, padx=5, pady=5)

        self.label_price = tk.Label(self.master, text="Price(per Kg):", bg="#f0f0f0")
        self.label_price.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.entry_price = tk.Entry(self.master)
        self.entry_price.grid(row=2, column=1, padx=5, pady=5)

        self.button_add = tk.Button(self.master, text="Add Item", command=self.add_item, bg="#4CAF50", fg="white")
        self.button_add.grid(row=3, column=0, pady=10, padx=5)

        self.button_update = tk.Button(self.master, text="Update Item", command=self.update_item, bg="#008CBA", fg="white")
        self.button_update.grid(row=3, column=1, pady=10, padx=5)

        self.button_delete = tk.Button(self.master, text="Delete Item", command=self.delete_item, bg="#f44336", fg="white")
        self.button_delete.grid(row=3, column=2, pady=10, padx=5)

        self.label_list = tk.Label(self.master, text="Inventory List:", bg="#f0f0f0")
        self.label_list.grid(row=4, column=0, columnspan=3, pady=10)

        self.listbox = tk.Listbox(self.master, height=10, width=50)
        self.listbox.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        self.populate_listbox()

        self.listbox.bind("<<ListboxSelect>>", self.select_item)

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.inventory:
            self.listbox.insert(tk.END, f"{item.name} - Quantity: {item.quantity}, Price: Rs {item.price}")

    def add_item(self):
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()

        try:
            quantity = int(quantity)
            price = float(price)
            if quantity <= 0 or price <= 0:
                raise ValueError("Quantity and price must be positive")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        item = InventoryItem(name, quantity, price)
        self.inventory.append(item)

        self.save_inventory_to_file()  # Save inventory to file after adding item

        self.populate_listbox()

        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)

        messagebox.showinfo("Success", "Item added successfully.")

    def update_item(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No item selected for update.")
            return

        index = selection[0]
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()

        try:
            quantity = int(quantity)
            price = float(price)
            if quantity <= 0 or price <= 0:
                raise ValueError("Quantity and price must be positive")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.inventory[index].name = name
        self.inventory[index].quantity = quantity
        self.inventory[index].price = price

        self.save_inventory_to_file()  # Save inventory to file after updating item

        self.populate_listbox()

    def delete_item(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No item selected for deletion.")
            return

        index = selection[0]
        del self.inventory[index]

        self.save_inventory_to_file()  # Save inventory to file after deleting item

        self.populate_listbox()

    def select_item(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            item = self.inventory[index]
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(tk.END, item.name)
            self.entry_quantity.delete(0, tk.END)
            self.entry_quantity.insert(tk.END, item.quantity)
            self.entry_price.delete(0, tk.END)
            self.entry_price.insert(tk.END, item.price)

    def load_inventory_from_file(self):
        try:
            with open("inventory.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    name, quantity, price = row
                    item = InventoryItem(name, int(quantity), float(price))
                    self.inventory.append(item)
        except FileNotFoundError:
            messagebox.showwarning("Warning", "Inventory file not found.")

    def save_inventory_to_file(self):
        with open("inventory.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for item in self.inventory:
                writer.writerow([item.name, item.quantity, item.price])

    def __del__(self):
        self.save_inventory_to_file()

f=open("inventory.csv","w")
f.close()

root = tk.Tk()
app = InventoryManagementApp(root)
root.mainloop()
