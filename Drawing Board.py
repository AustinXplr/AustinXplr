import tkinter as tk
from tkinter import messagebox

class Drawing_Board:
    def __init__(self, master):
        self.master = master
        master.title("Drawing Board")
        
        # Canvas setup
        self.canvas = tk.Canvas(master, width=600, height=400, bg="white")
        self.canvas.pack()
        
        # Bind mouse events for drawing
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        
        # Color input frame
        color_frame = tk.Frame(master)
        color_frame.pack()
        
        # RGB input labels and entry widgets
        self.r_label = tk.Label(color_frame, text="R:")
        self.r_label.pack(side=tk.LEFT)
        self.r_entry = tk.Entry(color_frame, width=5)
        self.r_entry.pack(side=tk.LEFT)
        self.r_entry.insert(0, "0")
        
        self.g_label = tk.Label(color_frame, text="G:")
        self.g_label.pack(side=tk.LEFT)
        self.g_entry = tk.Entry(color_frame, width=5)
        self.g_entry.pack(side=tk.LEFT)
        self.g_entry.insert(0, "0")
        
        self.b_label = tk.Label(color_frame, text="B:")
        self.b_label.pack(side=tk.LEFT)
        self.b_entry = tk.Entry(color_frame, width=5)
        self.b_entry.pack(side=tk.LEFT)
        self.b_entry.insert(0, "0")
        
        # Color preview
        self.preview_canvas = tk.Canvas(color_frame, width=30, height=30, bg="white")
        self.preview_canvas.pack(side=tk.LEFT)
        self.update_preview()
        
        # Bind entry changes to update preview
        self.r_entry.bind("<KeyRelease>", self.update_preview)
        self.g_entry.bind("<KeyRelease>", self.update_preview)
        self.b_entry.bind("<KeyRelease>", self.update_preview)
        
        # Drawing variables
        self.drawing = False
        self.last_x, self.last_y = 0, 0
        self.color = "black"
        self.line_width = 1  # Default line width
        
        # Line width control
        self.setup_line_width_control()
        
        # Delete All button
        self.setup_delete_button()

    def setup_line_width_control(self):
        # Line width control frame
        line_width_frame = tk.Frame(self.master)
        line_width_frame.pack(pady=10)
        
        # Label for line width
        tk.Label(line_width_frame, text="Line Width:").pack(side=tk.LEFT, padx=10)
        
        # Scale for line width
        self.line_width_scale = tk.Scale(line_width_frame, from_=1, to=100, orient=tk.HORIZONTAL, command=self.update_line_width)
        self.line_width_scale.set(self.line_width)  # Set default line width
        self.line_width_scale.pack(side=tk.LEFT, padx=10)
        
        # Entry for displaying and editing line width value
        self.line_width_value = tk.Entry(line_width_frame, width=5)
        self.line_width_value.pack(side=tk.LEFT)
        self.line_width_value.insert(0, str(self.line_width))
        self.line_width_value.bind("<Return>", self.validate_line_width)
        
    def setup_delete_button(self):
        # Delete All button
        delete_button = tk.Button(self.master, text="Delete All", command=self.delete_all)
        delete_button.pack()

    def delete_all(self):
        self.canvas.delete("all")

    def update_line_width(self, value):
        self.line_width = int(value)
        self.line_width_value.delete(0, tk.END)
        self.line_width_value.insert(0, str(self.line_width))
        self.canvas.itemconfig(self.line_preview, width=self.line_width)
        
    def validate_line_width(self, event):
        try:
            new_width = int(self.line_width_value.get())
            if new_width < 1 or new_width > 100:
                messagebox.showerror("Error", "Please enter an integer from 1 to 100.")
                self.line_width = 1  # Reset to default width
                self.line_width_value.delete(0, tk.END)
                self.line_width_value.insert(0, str(self.line_width))
                self.line_width_scale.set(self.line_width)  # Update scale position
                self.canvas.itemconfig(self.line_preview, width=self.line_width)
            else:
                self.line_width = new_width
                self.line_width_scale.set(self.line_width)  # Update scale position
                self.canvas.itemconfig(self.line_preview, width=self.line_width)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer from 1 to 100.")
            self.line_width = 1  # Reset to default width
            self.line_width_value.delete(0, tk.END)
            self.line_width_value.insert(0, str(self.line_width))
            self.line_width_scale.set(self.line_width)  # Update scale position
            self.canvas.itemconfig(self.line_preview, width=self.line_width)
        
    def start_draw(self, event):
        self.drawing = True
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        if self.drawing:
            current_x, current_y = event.x, event.y
            self.canvas.create_line(self.last_x, self.last_y, current_x, current_y, width=self.line_width, fill=self.color, capstyle=tk.ROUND)
            self.last_x, self.last_y = current_x, current_y

    def update_preview(self, event=None):
        r = int(self.r_entry.get())
        g = int(self.g_entry.get())
        b = int(self.b_entry.get())
        self.color = f"#{r:02x}{g:02x}{b:02x}"
        self.preview_canvas.delete("all")
        self.preview_canvas.create_rectangle(0, 0, 30, 30, fill=self.color)

root = tk.Tk()
app = Drawing_Board(root)
root.mainloop()
