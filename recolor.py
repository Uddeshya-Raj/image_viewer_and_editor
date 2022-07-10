from tkinter import *
from tkinter import ttk
import cv2

class RecolorWindow(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master=master)
        
        self.brightness_val = 0
        self.prev_brightness_val = 0
        
        self.original_image = self.master.processed_image.copy()
        self.recolored_image = self.master.processed_image.copy()
        
        self.brightness_label = Label(self, text="Brightness")
        self.brightness_scale = ttk.Scale(self, from_=0, to=2, length=250, orient=HORIZONTAL)
        self.r_label = Label(self, text="R")
        self.r_scale = ttk.Scale(self, from_=-100, to=100, length=250, orient=HORIZONTAL)
        self.g_label = Label(self, text="G")
        self.g_scale = ttk.Scale(self, from_=-100, to_=100, length=250, orient=HORIZONTAL)
        self.b_label = Label(self, text="B")
        self.b_scale = ttk.Scale(self, from_=-100, to_=100, length=250, orient=HORIZONTAL)
        self.apply_button = ttk.Button(self, text="Apply")
        self.cancel_button = ttk.Button(self, text="Cancel")

        self.brightness_scale.set(1)

        self.brightness_scale.bind("<ButtonRelease>", self.show_func)
        self.r_scale.bind("<ButtonRelease>", self.show_func)
        self.g_scale.bind("<ButtonRelease>", self.show_func)
        self.b_scale.bind("<ButtonRelease>", self.show_func)
        self.apply_button.bind("<ButtonRelease>", self.apply_func)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_func)

        self.brightness_label.pack()
        self.brightness_scale.pack()
        self.r_label.pack()
        self.r_scale.pack()
        self.g_label.pack()
        self.g_scale.pack()
        self.b_label.pack()
        self.b_scale.pack()
        self.cancel_button.pack(side=RIGHT, padx=7, pady=5)
        self.apply_button.pack(side=LEFT, padx=7, pady=5)
        
    def apply_func(self, event):
        self.master.processed_image = self.recolored_image
        self.close()

    def show_func(self, event):
        self.recolored_image = cv2.convertScaleAbs(self.original_image, alpha=self.brightness_scale.get())
        b, g, r = cv2.split(self.recolored_image)

        for b_value in b:
            cv2.add(b_value, int(self.b_scale.get()), b_value)
        for g_value in g:
            cv2.add(g_value, int(self.g_scale.get()), g_value)
        for r_value in r:
            cv2.add(r_value, int(self.r_scale.get()), r_value)

        self.recolored_image = cv2.merge((b, g, r))
        self.show_image(self.recolored_image)

    def cancel_func(self, event):
        self.close()

    def show_image(self, img=None):
        self.master.edit_area.show_image(img=img)

    def close(self):
        self.show_image()
        self.destroy()
        