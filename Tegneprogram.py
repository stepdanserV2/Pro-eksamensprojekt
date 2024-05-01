import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import Image, ImageDraw, ImageTk


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Drawing App")

        # Create canvas
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Keep track of the drawing state, the starting point of the current line,
        # the previous point, and the size of the tool
        self.drawing = False
        self.start_x = None
        self.start_y = None
        self.prev_x = None
        self.prev_y = None
        self.size = 2  # Default size
        self.color = "black"  # Default color

        # History of drawn segments
        self.segment_history = []
        self.current_segment = []

        # Add buttons for changing tools, size, and undo
        # Add buttons for changing tools
        self.pencil_button = tk.Button(
            root, text="Pencil", command=self.use_pencil)

        # Add buttons for changing tools and size
        self.pencil_button = tk.Button(
            root, text="Pencil", command=self.use_pencil)
        self.pencil_button.pack(side=tk.LEFT)

        self.eraser_button = tk.Button(
            root, text="Eraser", command=self.use_eraser)
        self.eraser_button.pack(side=tk.LEFT)

        self.square_button = tk.Button(
            root, text="Square", command=self.use_square)
        self.square_button.pack(side=tk.LEFT)

        self.triangle_button = tk.Button(
            root, text="Triangle", command=self.use_triangle)
        self.triangle_button.pack(side=tk.LEFT)

        self.size_button = tk.Scale(
            root, from_=1, to=10, orient=tk.HORIZONTAL, command=self.change_size)
        self.size_button.pack(side=tk.LEFT)
        self.size_button.set(self.size)  # Set default size

        self.clear_button = tk.Button(
            root, text="Clear", command=self.clear_sheet)
        self.clear_button.pack(side=tk.RIGHT)

        self.undo_button = tk.Button(
            root, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.RIGHT)

        self.color_button = tk.Button(
            root, text="Color", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)

        self.insert_image_button = tk.Button(
            root, text="Insert Image", command=self.insert_image)
        self.insert_image_button.pack(side=tk.LEFT)

        self.move_image_button = tk.Button(
            root, text="Move Image", command=self.start_move_image)
        self.move_image_button.pack(side=tk.LEFT)

        self.cirkel_button = tk.Button(
            root, text="o", command=self.use_cirkle)
        self.cirkel_button.pack(side=tk.LEFT)
        # Set default tool
        self.current_tool = "pencil"

        self.clear_button = tk.Button(
            root, text="Clear", command=self.clear_sheet)
        self.clear_button.pack(side=tk.RIGHT)

        """
        self.smear_button = tk.Button(
            root, text="tvære", command=self.start_smear)
        self.smear_button.pack(side=tk.RIGHT)
        """

        self.history = []

    def bind_mouse_events(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        if self.current_tool in ["pencil", "eraser", "smear", "Image", "None"]:
            self.canvas.bind("<Button-1>", self.start_draw)
            self.canvas.bind("<B1-Motion>", self.draw)
            self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        else:
            self.canvas.bind("<Button-1>", self.save_starting_position)
            self.canvas.bind("<ButtonRelease-1>", self.save_ending_position)

    def start_draw(self, event):
        # Update the starting point and set drawing state to True
        self.start_x = event.x
        self.start_y = event.y
        self.drawing = True

    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            # If it's not the first point
            if self.prev_x is not None and self.prev_y is not None:
                if self.current_tool == "pencil":
                    # Draw using the pencil tool
                    oval_id = self.canvas.create_oval(
                        x - self.size, y - self.size, x + self.size, y + self.size, fill=self.color, outline="")
                    # Draw a line from the previous point to the current point
                    line_id = self.canvas.create_line(
                        self.prev_x, self.prev_y, x, y, fill=self.color, width=self.size * 2)
                    # Store segment info
                    self.current_segment.append(oval_id)
                    self.current_segment.append(line_id)
                elif self.current_tool == "eraser":
                    # Erase using the eraser tool
                    rect_id = self.canvas.create_rectangle(
                        x - self.size, y - self.size, x + self.size, y + self.size, fill="white", outline="")
                    reline_id = self.canvas.create_line(
                        self.prev_x, self.prev_y, x, y, fill="white", width=self.size * 2)
                    # Store segment info
                    self.current_segment.append(rect_id)
                    self.current_segment.append(reline_id)
                elif self.current_tool == "none":
                    pass
            # Update the previous point
            self.prev_x = x
            self.prev_y = y

    def stop_draw(self, event):
        # Reset the drawing state and previous point
        self.drawing = False
        self.prev_x = None
        self.prev_y = None
        # Add the current segment to the segment history
        self.segment_history.append(tuple(self.current_segment))
        self.current_segment = []

    def save_starting_position(self, event):
        self.startx = event.x
        self.starty = event.y

    def save_ending_position(self, event):
        self.endx = event.x
        self.endy = event.y
        if self.current_tool == "square":
            square_id = self.canvas.create_rectangle(
                self.startx, self.starty, self.endx, self.endy, fill=self.color, outline="")
            # Store segment info
            self.current_segment.append(square_id)

        elif self.current_tool == "triangle":
            # Draw a triangle
            triangle_id = self.canvas.create_polygon(
                self.startx, self.starty, self.endx, self.endy, self.startx - (self.endx - self.startx), self.endy, fill=self.color, outline="")
            # Store segment info
            self.current_segment.append(triangle_id)

        elif self.current_tool == "cirkel":
            cirkel_id = self.canvas.create_oval(
                self.startx, self.starty, self.endx, self.endy, fill=self.color, outline="")
            self.current_segment.append(cirkel_id)

        else:
            pass

    def use_pencil(self):
        self.current_tool = "pencil"
        self.bind_mouse_events()

    def use_eraser(self):
        self.current_tool = "eraser"
        self.bind_mouse_events()

    def use_square(self):
        self.current_tool = "square"
        self.bind_mouse_events()

    def use_triangle(self):
        self.current_tool = "triangle"
        self.bind_mouse_events()

    def use_cirkle(self):
        self.current_tool = "cirkel"
        self.bind_mouse_events()

    def change_size(self, size):
        self.size = int(size)

    def choose_color(self):
        _, self.color = colorchooser.askcolor(title="Choose color")

    def insert_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            image.thumbnail((100, 100))  # Resize the image as needed
            photo = ImageTk.PhotoImage(image)
            self.current_image = photo
            self.current_image_id = self.canvas.create_image(
                200, 200, image=photo)
            self.canvas.image = photo  # Keep a reference to avoid garbage collection

    def start_move_image(self):
        self.current_tool = "none"
        if self.current_image_id:
            self.canvas.tag_bind(self.current_image_id,
                                 "<Button-1>", self.move_start)
            self.canvas.tag_bind(self.current_image_id,
                                 "<B1-Motion>", self.move)
            self.canvas.tag_bind(self.current_image_id,
                                 "<ButtonRelease-1>", self.move_stop)

    def move_start(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def move(self, event):
        if self.current_image_id:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas.move(self.current_image_id, dx, dy)
            self.start_x = event.x
            self.start_y = event.y

    def move_stop(self, event):
        pass

    def clear_sheet(self):
        while (len(self.segment_history) > 0):
            last_segment = self.segment_history.pop()
            for item_id in last_segment:
                self.canvas.delete(item_id)

    def undo(self):
        if self.segment_history:
            last_segment = self.segment_history.pop()
            for item_id in last_segment:
                self.canvas.delete(item_id)


# ctrl z
def ctrl_z_handler(e):
    print("ctrl z", app.undo())


app = None

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.bind("<Control-z>", ctrl_z_handler)
    root.mainloop()