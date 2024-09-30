import tkinter as tk
import csv
import matplotlib.pyplot as plt

from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create the main window
root = tk.Tk()
root.title("Personal Finance Tracker")

# Configure the root window to allow expansion
root.grid_rowconfigure(0,weight=1)
root.grid_columnconfigure(0,weight=1)

# Create a scrollable frame
scrollable_frame = tk.Frame(root)
scrollable_frame.grid(row=0,column=0,sticky="nsew")

# Create a canvas widget and a scrollbar
canvas = tk.Canvas(scrollable_frame)
scrollbar = tk.Scrollbar(scrollable_frame,orient="vertical",command=canvas.yview)
scrollable_content = tk.Frame(canvas)

# Configure the scrollable content and canvas to expand
scrollable_content.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0,0),window=scrollable_content,anchor='nw')
canvas.configure(yscrollcommand=scrollbar.set)

# Grid layout for canvas and scrollbar
canvas.grid(row=0,column=0,sticky="nsew")
scrollbar.grid(row=0,column=1,sticky="ns")

# Ensure the scrollable frame and its contents expand to fill the window
scrollable_frame.grid_rowconfigure(0,weight=1)
scrollable_frame.grid_columnconfigure(0,weight=1)
scrollable_content.grid_columnconfigure(0,weight=1)
scrollable_content.grid_columnconfigure(1,weight=1)

# Frames for expenses and budgets
expense_frame = tk.Frame(scrollable_content)
budget_frame = tk.Frame(scrollable_content)
income_frame = tk.Frame(scrollable_content)

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
reset_button = tk.Button(income_frame,text="Reset All Data",command=reset_data)

# Reset all data button top left
reset_button.grid(row=1, column=4, sticky="w")

# Expense section middle left
expense_frame.grid(row=1, column=0, sticky="nw")

# Budget section middle
budget_frame.grid(row=1, column=1, sticky="nw")

# Income section middle right
income_frame.grid(row=1, column=2, sticky="nw")

# Ensure the frames expand properly within their columns
scrollable_content.grid_columnconfigure(0, weight=1)
scrollable_content.grid_columnconfigure(1, weight=1)
scrollable_content.grid_columnconfigure(2, weight=1)

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

# Handles what happens on button click and updates Treeview after saving
def save_expense():
    # Get data from fields
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    description = description_entry.get()

    # Append data to the .csv file
    with open('Expenses.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date,category,amount,description])

    # Clear the fields after writing
    date_entry.delete(0,tk.END)
    category_entry.delete(0,tk.END)
    amount_entry.delete(0,tk.END)
    description_entry.delete(0,tk.END)

    expense_list.insert('',tk.END,values=(date,category,amount,description))

# Create the 'Add Expense' button
submit_button = tk.Button(expense_frame,text="Add Expense",command=save_expense)
submit_button.grid(row=5,column=1,padx=10,pady=20)

# Create a Treeview widget to show expenses
columns = ('Date','Category','Amount','Description')
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

# Label and field for income
income_label = tk.Label(income_frame, text="Enter Annual Income:")
income_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
income_entry = tk.Entry(income_frame)
income_entry.grid(row=1, column=1, padx=10, pady=10)

# Function to save income
def save_income():
    income = income_entry.get()

    with open('Income.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([income])

    income_entry.delete(0, tk.END)
    update_income()

# Add income button
income_button = tk.Button(income_frame, text="Add Income", command=save_income)
income_button.grid(row=2, column=1, padx=10, pady=10)

# Function to load and display income
def update_income():
    total_income = 0

    try:
        with open('Income.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                total_income += float(row[0])
    except FileNotFoundError:
        pass

    income_display_label.config(text=f"Total Income This Year: ${total_income:.2f}")

# Label to display income
income_display_label = tk.Label(income_frame, text="Total Income This Year: $0.00")
income_display_label.grid(row=3, column=1, columnspan=2, pady=10)

update_income()

# Function to calculate budget based on income
def suggest_budget():
    total_income = 0

    try:
        with open('Income.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                total_income += float(row[0])

            # Typical 50/30/20 rule
            needs_budget = total_income * 0.5
            wants_budget = total_income * 0.3
            savings_budget = total_income * 0.2

            messagebox.showinfo("Suggested Budget",
                                f"Based on your income of ${total_income:.2f}:\n"
                                f"Needs (50%): ${needs_budget:.2f}\n"
                                f"Wants (30%): ${wants_budget:.2f}\n"
                                f"Savings (20%): ${savings_budget:.2f}\n")
            
    except FileNotFoundError:
        messagebox.showerror("Error", "No income data found. Please enter your income first.")

# Suggest budget button
suggest_budget_button = tk.Button(income_frame, text="Suggest Budget", command=suggest_budget)
suggest_budget_button.grid(row=4, column=1, pady=10, padx=10)

# Start the tkinter loop
scrollable_content.mainloop()