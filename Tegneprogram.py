import tkinter as tk
# julie er her nu


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Drawing App")

        # Create canvas
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Bind mouse button events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        # Keep track of the drawing state, the starting point of the current line,
        # the previous point, and the size of the tool
        self.drawing = False
        self.start_x = None
        self.start_y = None
        self.prev_x = None
        self.prev_y = None
        self.size = 2  # Default size

        # History of drawn segments
        self.segment_history = []
        self.current_segment = []

        # tvære variabler
        self.smearing = False
        self.smear_size = 10  # Default smear size
        self.smear_color = "black"  # Default smear color

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
        self.eraser_button = tk.Button(
            root, text="Eraser", command=self.use_eraser)
        self.eraser_button.pack(side=tk.LEFT)

        self.size_button = tk.Scale(
            root, from_=1, to=10, orient=tk.HORIZONTAL, command=self.change_size)
        self.size_button.pack(side=tk.LEFT)
        self.size_button.set(self.size)  # Set default size

        self.undo_button = tk.Button(
            root, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.LEFT)

        # Set default tool
        self.current_tool = "pencil"

        self.clear_button = tk.Button(
            root, text="Clear", command=self.clear_sheet)
        self.clear_button.pack(side=tk.RIGHT)

        self.smear_button = tk.Button(
            root, text="tvære", command=self.start_smear)
        self.smear_button.pack(side=tk.RIGHT)

        self.history = []

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
                        x - self.size, y - self.size, x + self.size, y + self.size, fill="black")
                    # Draw a line from the previous point to the current point
                    line_id = self.canvas.create_line(
                        self.prev_x, self.prev_y, x, y, fill="black", width=self.size * 2)
                    # Store segment info
                    self.current_segment.append(oval_id)
                    self.current_segment.append(line_id)
                elif self.current_tool == "eraser":
                    # Erase using the eraser tool
                    rect_id = self.canvas.create_rectangle(
                        x - self.size, y - self.size, x + self.size, y + self.size, fill="white", outline="")
                    # Store segment info
                    self.current_segment.append(rect_id)
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

    def use_pencil(self):
        self.current_tool = "pencil"

    def use_eraser(self):
        self.current_tool = "eraser"

    def change_size(self, size):
        self.size = int(size)

    def undo(self):
        if self.segment_history:
            last_segment = self.segment_history.pop()
            for item_id in last_segment:
                self.canvas.delete(item_id)

    def clear_sheet(self):
        if self.history:
            last_action = self.history.pop()
            for item in last_action:
                self.canvas.delete(item)

    def start_smear(self):
        # Set the current tool to smear
        self.current_tool = "smear"
        # Activate smearing mode
        self.smearing = True

    def smear(self, event):
        # knap til tvære
        self.canvas.bind("<B1-Motion>", self.smear)

        if self.smearing:
            x, y = event.x, event.y
            # Create a circular region to smear the existing drawing
            self.canvas.create_oval(
                x - self.smear_size, y - self.smear_size, x +
                self.smear_size, y + self.smear_size,
                fill=self.smear_color, outline="", stipple="gray50")


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
