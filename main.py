import tkinter as tk
import csv

from tkinter import ttk

# Creating window with requirements
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("400x300")

# Label and entry field for the date
date_label = tk.Label(root,text="Date:") # Label
date_label.grid(row=0,column=0,padx=10,pady=10,sticky="e") # Formatting (position,position,padding,padding,east side)
date_entry = tk.Entry(root) # Entry
date_entry.grid(row=0,column=1,padx=10,pady=10) # Formatting 

# Label and entry field for the category
category_label = tk.Label(root,text="Category:")
category_label.grid(row=1,column=0,padx=10,pady=10,sticky="e")
category_entry = tk.Entry(root)
category_entry.grid(row=1,column=1,padx=10,pady=10)

# Label and entry field for the amount
amount_label = tk.Label(root,text="Amount:")
amount_label.grid(row=2,column=0,padx=10,pady=10,sticky="e")
amount_entry = tk.Entry(root)
amount_entry.grid(row=2,column=1,padx=10,pady=10)

# Label and entry field for the description
description_label = tk.Label(root,text="Description:")
description_label.grid(row=3,column=0,padx=10,pady=10,sticky="e")
description_entry = tk.Entry(root)
description_entry.grid(row=3,column=1,padx=10,pady=10)

# Checkbox for completed
completed_var = tk.BooleanVar() # Checkbox state
completed_checkbox = tk.Checkbutton(root,text="Completed",variable=completed_var)
completed_checkbox.grid(row=4,column=0,padx=10,pady=10,sticky="w")

# Handles what happens on button click
def save_expense():
    # Get data from fields
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    description = description_entry.get()
    completed = completed_var.get()

    # Append data to the csv file
    with open('Expenses.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date,category,amount,description,completed])

    # Clear the fields after writing
    date_entry.delete(0,tk.END)
    category_entry.delete(0,tk.END)
    amount_entry.delete(0,tk.END)
    description_entry.delete(0,tk.END)
    completed_var.set(False)

# Create the 'Add Expense' button
submit_button = tk.Button(root,text="Add Expense",command=save_expense)
submit_button.grid(row=5,column=1,padx=10,pady=20)

# Start the tkinter loop
root.mainloop()