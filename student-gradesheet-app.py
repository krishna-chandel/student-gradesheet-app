import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import csv

sns.set(style="whitegrid")

gradebook = []

def add_student():
    student_info = entry_info.get()
    if student_info:
        try:
            student_name, grade = student_info.split(',')
            grade = float(grade)
            gradebook.append((student_name, grade))
            entry_info.delete(0, tk.END)
        except ValueError:
            messagebox.showwarning("Warning", "Please enter valid student information (name, grade).")
    else:
        messagebox.showwarning("Warning", "Please enter student information.")

def remove_student():
    student_name = entry_info.get()
    for i, (name, _) in enumerate(gradebook):
        if name == student_name:
            del gradebook[i]
            entry_info.delete(0, tk.END)
            return
    messagebox.showwarning("Warning", "Student not found.")

def calculate_statistics():
    if not gradebook:
        messagebox.showwarning("Warning", "No student data available.")
        return

    all_grades = [grade for _, grade in gradebook]
    mean = np.mean(all_grades)
    std_dev = np.std(all_grades)

    statistics_text.delete(1.0, tk.END)
    statistics_text.insert(tk.END, f"All Students: Mean = {mean:.2f}, Std Dev = {std_dev:.2f}\n")

def visualize_data():
    plt.clf()
    all_grades = [grade for _, grade in gradebook]
    sns.histplot(all_grades, bins=10, kde=True, color='skyblue', alpha=0.5)
    plt.xlabel('Grades')
    plt.ylabel('Density')
    plt.title('Grade Distribution')
    canvas.draw()

def export_to_csv():
    if not gradebook:
        messagebox.showwarning("Warning", "No student data available for export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    if file_path:
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Student Name', 'Grade'])
            csv_writer.writerows(gradebook)

app = tk.Tk()
app.title("Students GradeSheet Application")

style = ttk.Style()
style.theme_use("clam")  
label_info = ttk.Label(app, text="Student Information (Name, Grade):")
entry_info = ttk.Entry(app)
button_add_student = ttk.Button(app, text="Add Student", command=add_student)
button_remove_student = ttk.Button(app, text="Remove Student", command=remove_student)
button_calculate_stats = ttk.Button(app, text="Calculate Statistics", command=calculate_statistics)
button_visualize_data = ttk.Button(app, text="Visualize Data", command=visualize_data)
button_export_csv = ttk.Button(app, text="Export to CSV", command=export_to_csv)
statistics_text = tk.Text(app, height=5, width=30)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=app)
canvas_widget = canvas.get_tk_widget()

label_info.grid(row=0, column=0, padx=5, pady=5)
entry_info.grid(row=0, column=1, padx=5, pady=5)
button_add_student.grid(row=1, column=0, columnspan=2, pady=5)
button_remove_student.grid(row=2, column=0, columnspan=2, pady=5)
button_calculate_stats.grid(row=3, column=0, columnspan=2, pady=5)
button_visualize_data.grid(row=4, column=0, columnspan=2, pady=5)
button_export_csv.grid(row=5, column=0, columnspan=2, pady=5)
statistics_text.grid(row=6, column=0, columnspan=2, pady=5)
canvas_widget.grid(row=7, column=0, columnspan=2, pady=5)

app.mainloop()
