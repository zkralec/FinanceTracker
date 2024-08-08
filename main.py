import tkinter as tk
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

# Start the tkinter loop
root.mainloop()