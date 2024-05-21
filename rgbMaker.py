import tkinter as tk
from tkinter import Canvas, HORIZONTAL

class RGBColorPicker:
    def __init__(self, root):
        self.root = root
        self.root.title("RCP")

        self.red_value = tk.DoubleVar()
        self.green_value = tk.DoubleVar()
        self.blue_value = tk.DoubleVar()

        self.red_value.set(0)
        self.green_value.set(0)
        self.blue_value.set(0)

        self.create_widgets()

    def create_widgets(self):
        self.color_canvas = Canvas(self.root, width=200, height=200)
        self.color_canvas.pack()

        self.red_bar = tk.Scale(self.root, label="Red", from_=0, to=255, variable=self.red_value, orient=HORIZONTAL,
                                length=200, command=self.update_color)
        self.red_bar.pack()

        self.green_bar = tk.Scale(self.root, label="Green", from_=0, to=255, variable=self.green_value, orient=HORIZONTAL,
                                  length=200, command=self.update_color)
        self.green_bar.pack()

        self.blue_bar = tk.Scale(self.root, label="Blue", from_=0, to=255, variable=self.blue_value, orient=HORIZONTAL,
                                 length=200, command=self.update_color)
        self.blue_bar.pack()

        copy_button = tk.Button(self.root, text="Copy RGB", command=self.copy_rgb)
        copy_button.pack()

    def update_color(self, event=None):
        red = int(self.red_value.get())
        green = int(self.green_value.get())
        blue = int(self.blue_value.get())

        color_hex = f"#{red:02X}{green:02X}{blue:02X}"
        self.color_canvas.config(bg=color_hex)

    def copy_rgb(self):
        red = int(self.red_value.get())
        green = int(self.green_value.get())
        blue = int(self.blue_value.get())

        rgb_value = f"{red}, {green}, {blue}"
        self.root.clipboard_clear()
        self.root.clipboard_append(rgb_value)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = RGBColorPicker(root)
    root.mainloop()