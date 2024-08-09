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

# Title label
title = tk.Label(scrollable_content,text="Personal Finance Tracker",font=("Arial",16,"bold"))
title.grid(row=0,column=0,columnspan=2,pady=10)

# Frames for expenses and budgets
expense_frame = tk.Frame(scrollable_content)
budget_frame = tk.Frame(scrollable_content)
income_frame = tk.Frame(scrollable_content)

# Place frames side by side
expense_frame.grid(row=1,column=0,padx=20,pady=10,sticky="nsew")
budget_frame.grid(row=1,column=1,padx=20,pady=10,sticky="nsew")
income_frame.grid(row=1,column=2,padx=20,pady=20,sticky='nsew')

# Ensure the frames expand properly within their columns
scrollable_content.grid_columnconfigure(0,weight=1)
scrollable_content.grid_columnconfigure(1,weight=1)

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
reset_button.grid(row=0,column=0,padx=10,pady=10,sticky='e')

# Function for a pie chart for expenses
def show_spending_chart():
    categories = []
    amounts = []

    with open('Expenses.csv','r') as file:
        reader = csv.reader(file)
        for row in reader: # Goes through rows in file
            category = row[1] # Category is the first part
            amount = float(row[2]) # Amount is second part
            if category in categories: # For each item in a category
                index = categories.index(category) # Set index
                amounts[index] += amount # Add to total amount
            else:
                categories.append(category) 
                amounts.append(amount)
    
    # Create the pie chart
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.pie(amounts,labels=categories,autopct='%1.1f%%',startangle=90)
    ax.axis('equal')

    # Clear chart if any
    for widget in scrollable_content.winfo_children():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.get_tk_widget().destroy()

    # Put chart in Tkinter
    canvas = FigureCanvasTkAgg(fig,master=income_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2,column=0,columnspan=2,padx=20,pady=20)

# Button to show chart
chart_show = tk.Button(income_frame,text="Show Spending Chart",command=show_spending_chart)
chart_show.grid(row=1,column=0,columnspan=2,pady=10)

# Start the tkinter loop
scrollable_content.mainloop()