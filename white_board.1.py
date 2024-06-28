import tkinter as tk

class Whiteboard:
    def __init__(self, root, width=800, height=600):
        self.root = root
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        # Bind mouse wheel event to zoom
        self.canvas.bind("<MouseWheel>", self.zoom)

        # Bind mouse click events to drawing and erasing
        self.canvas.bind("<Button-1>", self.draw_start)
        self.canvas.bind("<B1-Motion>", self.draw_move)
        self.canvas.bind("<Button-3>", self.erase_start)
        self.canvas.bind("<B3-Motion>", self.erase_move)
        self.canvas.bind("<ButtonRelease-1>", self.draw_end)
        self.canvas.bind("<ButtonRelease-3>", self.erase_end)

        # Set drawing and erasing colors and thickness
        self.draw_color = "black"
        self.erase_color = "white"
        self.thickness = 1

        # Create color palette
        self.color_palette = tk.Frame(self.root)
        self.color_palette.pack(side=tk.TOP, fill=tk.X)

        self.colors = ["red", "orange", "yellow", "green", "cyan", "blue", "violet", "black"]
        self.color_buttons = []
        for i, color in enumerate(self.colors):
            button = tk.Button(self.color_palette, width=13, bg=color, command=lambda c=color: self.set_draw_color(c))
            button.grid(row=0, column=i)
            self.color_buttons.append(button)

        # Create pen and eraser buttons
        self.pen_button = tk.Button(self.root, text="Pen", font=("Helvetica", 12), bg="lightblue", activebackground="blue", bd=0, relief="solid", highlightthickness=0.5, command=self.set_pen_mode)
        self.pen_button.pack(side=tk.LEFT, padx=5)

        self.erase_button = tk.Button(self.root, text="Eraser", font=("Helvetica", 12), bg="pink", activebackground="purple", bd=0, relief="solid", highlightthickness=0, command=self.set_erase_mode)
        self.erase_button.pack(side=tk.RIGHT, padx=5)

        # Create thickness bar
        self.thickness_var = tk.IntVar()
        self.thickness_slider = tk.Scale(self.root, from_=1, to=50, orient=tk.HORIZONTAL, command=self.set_thickness, variable=self.thickness_var)
        self.thickness_slider.pack(side=tk.LEFT, padx=5)

        # Create clear all button
        self.clear_button = tk.Button(self.root, text="Clear All", font=("Helvetica", 13), bg="lightsalmon", activebackground="darkorange", bd=0, relief="solid", highlightthickness=0, command=self.clear_canvas)
        self.clear_button.pack(side=tk.BOTTOM, padx=5)

        # Create zoom in and zoom out buttons
        self.zoom_in_button = tk.Button(self.root, text="Zoom In", font=("Helvetica", 12), bg="lightgreen", activebackground="green", bd=0, relief="solid", highlightthickness=0, command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)

        self.zoom_out_button = tk.Button(self.root, text="Zoom Out", font=("Helvetica", 12), bg="lightcoral", activebackground="red", bd=0, relief="solid", highlightthickness=0, command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)

    def set_pen_mode(self):
        self.draw_color = "black"

    def set_erase_mode(self):
        self.erase_color = "white"

    def set_draw_color(self, color):
        self.draw_color = color

    def set_thickness(self, thickness):
        self.thickness = int(thickness)

    def draw_start(self, event):
        self.drawing = True
        self.start_x = event.x
        self.start_y = event.y

    def draw_move(self, event):
        if self.drawing:
            self.end_x = event.x
            self.end_y = event.y
            self.canvas.create_line(self.start_x, self.start_y, self.end_x, self.end_y, width=self.thickness, fill=self.draw_color, capstyle=tk.ROUND)
            self.start_x = self.end_x
            self.start_y = self.end_y

    def draw_end(self, event):
        self.drawing = False

    def erase_start(self, event):
        self.erase = True
        self.start_x = event.x
        self.start_y = event.y

    def erase_move(self, event):
        if self.erase:
            self.end_x = event.x
            self.end_y = event.y
            self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, width=0, fill=self.erase_color, outline="")
            self.canvas.create_rectangle(self.start_x-24, self.start_y-24, self.end_x+24, self.end_y+24, width=0, fill=self.erase_color, outline="")
            self.start_x = self.end_x
            self.start_y = self.end_y

    def erase_end(self, event):
        self.erase = False

    def clear_canvas(self):
        self.canvas.delete("all")

    def zoom(self, event):
        if event.delta > 0:
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        else:
            self.canvas.scale("all", event.x, event.y, 1/1.1, 1/1.1)

    def zoom(self, event):
        if event.delta > 0:
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        else:
            self.canvas.scale("all", event.x, event.y, 1/1.1, 1/1.1)

    def zoom_in(self):
        self.canvas.scale("all", self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, 1.1, 1.1)

    def zoom_out(self):
        self.canvas.scale("all", self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, 1/1.1, 1/1.1)

if __name__ == "__main__":
    root = tk.Tk()
    app = Whiteboard(root)
    root.mainloop()