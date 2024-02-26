import tkinter as tk


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Drawing App")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        # Bind mouse button motion to the drawing function
        self.canvas.bind("<B1-Motion>", self.draw)

        # Keep track of the previous position for drawing lines
        self.prev_x = None
        self.prev_y = None

    def draw(self, event):
        x, y = event.x, event.y

        # If it's not the first point, draw a line from previous point to current point
        if self.prev_x is not None and self.prev_y is not None:
            self.canvas.create_line(
                self.prev_x, self.prev_y, x, y, fill="black", width=2)

        # Update previous position
        self.prev_x = x
        self.prev_y = y


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
