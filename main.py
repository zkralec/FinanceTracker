import tkinter as tk
import csv

from tkinter import ttk
from tkinter import messagebox

# Creating window with requirements
root = tk.Tk()
root.title("Personal Finance Tracker")

# Title
title = tk.Label(root, text="Personal Finance Tracker", font=("Arial", 16, "bold"))
title.grid(row=0, column=0, columnspan=2, pady=10)

# Frames
expense_frame = tk.Frame(root)
budget_frame = tk.Frame(root)

# Place the frames side by side
expense_frame.grid(row=1, column=0, padx=20, pady=10, sticky="n")
budget_frame.grid(row=1, column=1, padx=20, pady=10, sticky="n")

# Label and entry field for the date
date_label = tk.Label(expense_frame,text="Date:") # Label
date_label.grid(row=0,column=0,padx=10,pady=10,sticky="e") # Formatting (position,position,padding,padding,east side)
date_entry = tk.Entry(expense_frame) # Entry
date_entry.grid(row=0,column=1,padx=10,pady=10) # Formatting 

# Label and entry field for the category
category_label = tk.Label(expense_frame,text="Category:")
category_label.grid(row=1,column=0,padx=10,pady=10,sticky="e")
category_entry = tk.Entry(expense_frame)
category_entry.grid(row=1,column=1,padx=10,pady=10)

# Label and entry field for the amount
amount_label = tk.Label(expense_frame,text="Amount:")
amount_label.grid(row=2,column=0,padx=10,pady=10,sticky="e")
amount_entry = tk.Entry(expense_frame)
amount_entry.grid(row=2,column=1,padx=10,pady=10)

# Label and entry field for the description
description_label = tk.Label(expense_frame,text="Description:")
description_label.grid(row=3,column=0,padx=10,pady=10,sticky="e")
description_entry = tk.Entry(expense_frame)
description_entry.grid(row=3,column=1,padx=10,pady=10)

# Checkbox for completed
completed_label = tk.Label(expense_frame, text="Completed:")
completed_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
completed_var = tk.BooleanVar()
completed_check = tk.Checkbutton(expense_frame, variable=completed_var)
completed_check.grid(row=4, column=1, padx=10, pady=5)

# Handles what happens on button click and updates Treeview after saving
def save_expense():
    # Get data from fields
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    description = description_entry.get()
    completed = completed_var.get()

    # Append data to the .csv file
    with open('Expenses.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date,category,amount,description,completed])

    # Clear the fields after writing
    date_entry.delete(0,tk.END)
    category_entry.delete(0,tk.END)
    amount_entry.delete(0,tk.END)
    description_entry.delete(0,tk.END)
    completed_var.set(False)

    expense_list.insert('',tk.END,values=(date,category,amount,description,completed))

# Create the 'Add Expense' button
submit_button = tk.Button(expense_frame,text="Add Expense",command=save_expense)
submit_button.grid(row=5,column=1,padx=10,pady=20)

# Create a Treeview widget to show expenses
columns = ('Date','Category','Amount','Description','Completed')
expense_list = ttk.Treeview(expense_frame,columns=columns,show='headings')

# Define the column headings
for col in columns:
    expense_list.heading(col,text=col)
    expense_list.column(col,minwidth=100,width=100)

expense_list.grid(row=6,column=0,columnspan=2,padx=10,pady=10) # Formatting

# Function to load the expenses
def load_expenses():
    try:
        with open('Expenses.csv','r') as file:
            reader = csv.reader(file) # Set to Expenses.csv file
            for row in reader: # Reads the specified file
                    expense_list.insert('',tk.END,values=row)  # Inserts into the Treeview
    except FileNotFoundError:
        pass # If not found we do nothing (shouldn't happen)

load_expenses() # Load expenses

# Budget labels and entry fields
budget_label = tk.Label(budget_frame,text="Set Budget For Category:")
budget_label.grid(row=0,column=0,padx=10,pady=10,sticky='e')
budget_category = tk.Entry(budget_frame)
budget_category.grid(row=0,column=1,padx=10,pady=10)

budget_amount_label = tk.Label(budget_frame,text="Budget Amount:")
budget_amount_label.grid(row=1,column=0,padx=10,pady=10,sticky='e')
budget_amount_entry = tk.Entry(budget_frame)
budget_amount_entry.grid(row=1,column=1,padx=10,pady=10)

# Function to save the set budget
def save_budget():
    # Get the data from fields
    category = budget_category.get()
    budget = budget_amount_entry.get()

    # Append data to the .csv file
    with open('Budgets.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([category,budget])

    # Clear entry fields after saving
    budget_category.delete(0,tk.END)
    budget_amount_entry.delete(0,tk.END)

    # Update budget display
    update_budgets()

# Button to save the budget
save_budget_button = tk.Button(budget_frame,text="Save Budget",command=save_budget)
save_budget_button.grid(row=2,column=1,padx=10,pady=20)

# Add the budgets to the Treeview
budget_columns = ('Category','Budget','Spent')
budget_list = ttk.Treeview(budget_frame,columns=budget_columns,show='headings')

# Define column headings
for col in budget_columns:
    budget_list.heading(col,text=col)
    budget_list.column(col,minwidth=100,width=100)

# Format the Treeview
budget_list.grid(row=3,column=0,columnspan=2,padx=10,pady=10)

# Function to update the budget Treeview
def update_budgets():
    # Clear Treeview
    for item in budget_list.get_children():
        budget_list.delete(item)

    # Load from the .csv file
    try:
        with open('Budgets.csv','r') as file:
            reader = csv.reader(file) # Set to Budgets.csv file
            for row in reader: # Reads the specified file
                category,budget = row # Get category and budget
                spent = calculate_spent(category) # Call calculate_spent for calculations
                budget_list.insert('',tk.END,values=(category,budget,spent)) # Insert values
    except FileNotFoundError:
        pass # If not found we do nothing (shouldn't happen)

# Function to calculate what has been spent
def calculate_spent(category):
    total_spent = 0
    try:
        with open('Expenses.csv','r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == category: # If category matches
                    total_spent += float(row[2]) # Add amount
    except FileNotFoundError:
        pass
    return total_spent

# Load budgets on start
update_budgets()

# Function that will reset all data
def reset_data():
    # Prompt user with text
    answer = messagebox.askyesno("Reset Data","Are you sure you want to reset all data? This action cannot be undone.")
    # If user proceeds
    if answer:
        with open('Expenses.csv','w',newline='') as file:
            writer = csv.writer(file)
        with open('Budgets.csv','w',newline='') as file:
            writer = csv.writer(file)
        for item in expense_list.get_children():
            expense_list.delete(item)
        for item in budget_list.get_children():
            budget_list.delete(item)

        messagebox.showinfo("Data Reset","All data has been reset.")

# Button to call reset_data
reset_button = tk.Button(root,text="Reset All Data",command=reset_data)
reset_button.grid(row=2,column=0,padx=10,pady=20)

# Start the tkinter loop
root.mainloop()