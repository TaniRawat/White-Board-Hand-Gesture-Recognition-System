import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk
import os

class InteractiveWhiteboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Whiteboard")
        self.root.geometry("1000x700")

        self.pen_color = "black"
        self.eraser_on = False
        self.pen_size = 5
        self.image = Image.new("RGB", (1000, 700), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.history = [self.image.copy()]
        self.history_index = 0

        self.scale_factor = 1.0

        self.create_widgets()
        self.bind_events()

        # Variables to handle drawing
        self.drawing = False
        self.last_x = None
        self.last_y = None

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.bottom_frame = tk.Frame(self.root, bg="lightgrey", height=50)
        self.bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.pen_button = tk.Button(self.bottom_frame, text="Pen", command=self.use_pen, font=("Helvetica", 12), bg="lightblue", activebackground="blue", bd=0, relief="solid", highlightthickness=0.5)
        self.pen_button.grid(row=0, column=0, padx=5)

        self.color_button = tk.Button(self.bottom_frame, text="Color", command=self.choose_color, font=("Helvetica", 12), bg="white", activebackground="lightgrey", bd=0, relief="solid", highlightthickness=0.5)
        self.color_button.grid(row=0, column=1, padx=5)

        self.eraser_button = tk.Button(self.bottom_frame, text="Eraser", command=self.use_eraser, font=("Helvetica", 12), bg="pink", activebackground="purple", bd=0, relief="solid", highlightthickness=0.5)
        self.eraser_button.grid(row=0, column=2, padx=5)

        self.clear_button = tk.Button(self.bottom_frame, text="Clear All", command=self.clear_canvas, font=("Helvetica", 12), bg="lightsalmon", activebackground="darkorange", bd=0, relief="solid", highlightthickness=0.5)
        self.clear_button.grid(row=0, column=3, padx=5)

        self.pen_size_scale = tk.Scale(self.bottom_frame, from_=1, to=50, orient=tk.HORIZONTAL, command=self.change_pen_size)
        self.pen_size_scale.set(self.pen_size)
        self.pen_size_scale.grid(row=0, column=4, padx=5)

        self.zoom_in_button = tk.Button(self.bottom_frame, text="Zoom In", command=self.zoom_in, font=("Helvetica", 12), bg="lightgreen", activebackground="green", bd=0, relief="solid", highlightthickness=0.5)
        self.zoom_in_button.grid(row=0, column=5, padx=5)

        self.zoom_out_button = tk.Button(self.bottom_frame, text="Zoom Out", command=self.zoom_out, font=("Helvetica", 12), bg="lightcoral", activebackground="red", bd=0, relief="solid", highlightthickness=0.5)
        self.zoom_out_button.grid(row=0, column=6, padx=5)

        self.save_button = tk.Button(self.bottom_frame, text="Save", command=self.save_canvas, font=("Helvetica", 12), bg="lightyellow", activebackground="yellow", bd=0, relief="solid", highlightthickness=0.5)
        self.save_button.grid(row=0, column=7, padx=5)

        self.load_button = tk.Button(self.bottom_frame, text="Load", command=self.load_canvas, font=("Helvetica", 12), bg="lightyellow", activebackground="yellow", bd=0, relief="solid", highlightthickness=0.5)
        self.load_button.grid(row=0, column=8, padx=5)

        self.undo_button = tk.Button(self.bottom_frame, text="Undo", command=self.undo, font=("Helvetica", 12), bg="lightblue", activebackground="blue", bd=0, relief="solid", highlightthickness=0.5)
        self.undo_button.grid(row=0, column=9, padx=5)

        self.redo_button = tk.Button(self.bottom_frame, text="Redo", command=self.redo, font=("Helvetica", 12), bg="lightblue", activebackground="blue", bd=0, relief="solid", highlightthickness=0.5)
        self.redo_button.grid(row=0, column=10, padx=5)

        # Create color palette
        self.colors = ["red", "orange", "yellow", "green", "cyan", "blue", "violet", "black"]
        self.color_buttons = []
        for i, color in enumerate(self.colors):
            button = tk.Button(self.bottom_frame, width=3, bg=color, command=lambda c=color: self.set_draw_color(c))
            button.grid(row=0, column=11 + i)
            self.color_buttons.append(button)

    def bind_events(self):
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.canvas.bind("<MouseWheel>", self.zoom)

    def use_pen(self):
        self.eraser_on = False

    def choose_color(self):
        color = colorchooser.askcolor()
        if color[1]:
            self.pen_color = color[1]
            self.eraser_on = False

    def use_eraser(self):
        self.eraser_on = True

    def set_draw_color(self, color):
        self.pen_color = color
        self.eraser_on = False

    def change_pen_size(self, event):
        self.pen_size = int(event)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (1000, 700), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.history = [self.image.copy()]
        self.history_index = 0
        self.update_canvas()

    def zoom(self, event):
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def zoom_in(self):
        self.scale_factor *= 1.1
        self.canvas.scale("all", 0, 0, 1.1, 1.1)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom_out(self):
        self.scale_factor /= 1.1
        self.canvas.scale("all", 0, 0, 1 / 1.1, 1 / 1.1)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.image.save(file_path)

    def load_canvas(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            self.image = Image.open(file_path)
            self.draw = ImageDraw.Draw(self.image)
            self.history = [self.image.copy()]
            self.history_index = 0
            self.update_canvas()

    def update_canvas(self):
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)
        self.canvas.image = self.canvas_image

    def undo(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.image = self.history[self.history_index].copy()
            self.draw = ImageDraw.Draw(self.image)
            self.update_canvas()

    def redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.image = self.history[self.history_index].copy()
            self.draw = ImageDraw.Draw(self.image)
            self.update_canvas()

    def save_action(self):
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        self.history.append(self.image.copy())
        self.history_index += 1

    def start_drawing(self, event):
        self.drawing = True
        self.last_x = event.x / self.scale_factor
        self.last_y = event.y / self.scale_factor

    def paint(self, event):
        if self.drawing:
            x1, y1 = self.last_x, self.last_y
            x2, y2 = event.x / self.scale_factor, event.y / self.scale_factor
            paint_color = "white" if self.eraser_on else self.pen_color
            self.canvas.create_line(x1 * self.scale_factor, y1 * self.scale_factor,
                                    x2 * self.scale_factor, y2 * self.scale_factor,
                                    fill=paint_color, width=self.pen_size, capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([x1, y1, x2, y2], fill=paint_color, width=self.pen_size)
            self.last_x, self.last_y = x2, y2

    def reset(self, event):
        self.drawing = False
        self.last_x, self.last_y = None, None
        self.save_action()

if __name__ == "__main__":
    root = tk.Tk()
    app = InteractiveWhiteboard(root)
    root.mainloop()
