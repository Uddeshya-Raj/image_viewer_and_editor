from os import sep
from pydoc import TextDoc
from tkinter import *
from tkinter import ttk
import numpy as np
import cv2

class FiltersWindow(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master=master)
        
        self.original_image = self.master.processed_image.copy()
        self.filtered_image = self.master.processed_image.copy()
        self.blurred_image = self.master.processed_image.copy()
        self.is_blurred = False
        
        self.filter_frame = Frame(self)
        self.filter_frame.pack(fill=BOTH, expand=True)
        
        self.filter_option = IntVar()
        none_r = ttk.Radiobutton(self.filter_frame, text="None", variable=self.filter_option,
                                 value=0)
        black_white_r = ttk.Radiobutton(self.filter_frame, text="Black and White", variable=self.filter_option,
                                        value=1)
        sepia_r = ttk.Radiobutton(self.filter_frame, text="Sepia", variable=self.filter_option, value=2)
        negative_r = ttk.Radiobutton(self.filter_frame, text="Negative", variable=self.filter_option, value=3)
        emboss_r = ttk.Radiobutton(self.filter_frame, text="Emboss", variable=self.filter_option, value=4)
        none_r.grid(row=0, column=0, padx=7, pady=5, sticky="ew")
        black_white_r.grid(row=1, column=0, padx=7, pady=5, sticky="ew")
        sepia_r.grid(row=2, column=0, padx=7, pady=5, sticky="ew")
        negative_r.grid(row=3, column=0, padx=7, pady=5, sticky="ew")
        emboss_r.grid(row=4, column=0, padx=7, pady=5, sticky="ew")
        
        none_r.bind("<ButtonRelease>", self.no_filter)
        black_white_r.bind("<ButtonRelease>", self.black_white)
        sepia_r.bind("<ButtonRelease>", self.sepia)
        negative_r.bind("<ButtonRelease>", self.negative)
        emboss_r.bind("<ButtonRelease>", self.emboss)
        
        # Setting Blur Options
        self.blur_frame = LabelFrame(self, text="Blur", padx=5, pady=5)
        self.blur_frame.pack(fill=BOTH, expand=True)
        
        Label(self.blur_frame, text="Blur type:").grid(row=0, column=0, padx=7, pady=5, sticky="ew")
        self.blur_option = IntVar()
        avg_blur_r = ttk.Radiobutton(self.blur_frame, text="Average Blur", variable=self.blur_option,
                                 value=1)
        median_blur_r = ttk.Radiobutton(self.blur_frame, text="Median Blur", variable=self.blur_option,
                                    value=2)
        gauss_blur_r = ttk.Radiobutton(self.blur_frame, text="Gaussian Blur", variable=self.blur_option,
                                   value=3)
        avg_blur_r.grid(row=1, column=0, padx=7, pady=5, sticky="ew")
        median_blur_r.grid(row=2, column=0, padx=7, pady=5, sticky="ew")
        gauss_blur_r.grid(row=3, column=0, padx=7, pady=5, sticky="ew")
        
        Label(self.blur_frame, text="Blur strength:").grid(row=4, column=0, padx=7, pady=5, sticky="ew")
        self.blur_strength_scale = ttk.Scale(self.blur_frame, from_=1, to=100, length=250, orient=HORIZONTAL)
        self.blur_strength_scale.grid(row=5, column=0, padx=7, pady=5, sticky="ew")
        
        avg_blur_r.bind("<ButtonRelease>", self.avg_blur_func)
        median_blur_r.bind("<ButtonRelease>", self.median_blur_func)
        gauss_blur_r.bind("<ButtonRelease>", self.gauss_blur_func)
        self.blur_strength_scale.bind("<ButtonRelease>", self.blur_func)

        # Apply and Cancel buttons
        self.apply_button = ttk.Button(self, text="Apply")
        self.cancel_button = ttk.Button(self, text="Cancel")
        self.apply_button.bind("<ButtonRelease>", self.apply_func)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_func)
        self.cancel_button.pack(side=RIGHT, padx=7, pady=5)
        self.apply_button.pack(side=LEFT, padx=7, pady=5)
        
    def show_image(self, img=None):
        self.master.edit_area.show_image(img=img)
        
    def close(self):
        self.show_image()
        self.destroy()
    
    def apply_func(self, event):
        if self.is_blurred:
            self.filtered_image = self.blurred_image.copy()
        self.master.processed_image = self.filtered_image
        self.is_blurred = False
        self.close()
        
    def cancel_func(self, event):
        self.is_blurred = False
        self.close()
    
    def no_filter(self, event):
        self.filtered_image = self.original_image.copy()
        self.show_image(self.filtered_image)
    
    def black_white(self, event):
        self.filtered_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.filtered_image = cv2.cvtColor(self.filtered_image, cv2.COLOR_GRAY2BGR)
        self.show_image(self.filtered_image)
    
    def sepia(self, event):
        self.filtered_image = np.array(self.filtered_image, dtype=np.float64) #converting to float to prevetn loss
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        self.filtered_image = cv2.transform(self.original_image, kernel)
        self.filtered_image[np.where(self.filtered_image > 255)] = 255 #normalizing greater values to 255
        self.filtered_image = np.array(self.filtered_image, dtype=np.uint8)
        self.show_image(self.filtered_image)
    
    def negative(self, event):
        self.filtered_image = cv2.bitwise_not(self.original_image)
        self.show_image(self.filtered_image)
    
    def emboss(self, event):
        self.filtered_image = np.array(self.filtered_image, dtype=np.float64)
        kernel = np.array([[0, -0.5, -0.5, -1, -1],
                           [0.5, 0, -0.5, -0.5, -1],
                           [0.5, 0.5, 0, -0.5, -0.5],
                           [1, 0.5, 0.5, 0, -0.5],
                           [1, 1, 0.5, 0.5, 0]])
        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)
        self.filtered_image[np.where(self.filtered_image > 255)] = 255 
        self.filtered_image = np.array(self.filtered_image, dtype=np.uint8)
        self.show_image(self.filtered_image)
    
    def get_blur_strength(self):
        return int(self.blur_strength_scale.get())
    
    def avg_blur_func(self, event=None):
        self.is_blurred = True
        blur_str = self.get_blur_strength()
        blur_str = blur_str if blur_str % 2 else blur_str+1
        ksize = (blur_str, blur_str)
        self.blurred_image = cv2.blur(self.filtered_image, ksize=ksize)
        self.show_image(self.blurred_image)
    
    def median_blur_func(self, event=None):        
        self.is_blurred = True
        blur_str = self.get_blur_strength()
        kernel_size = blur_str if blur_str % 2 else blur_str+1
        self.blurred_image = cv2.medianBlur(self.filtered_image, kernel_size)
        self.show_image(self.blurred_image)
        
    def gauss_blur_func(self, event=None):
        self.is_blurred = True
        blur_str = self.get_blur_strength()
        blur_str = blur_str if blur_str % 2 else blur_str+1
        kernel_size = (blur_str, blur_str)
        self.blurred_image = cv2.GaussianBlur(self.filtered_image, kernel_size, 0)
        self.show_image(self.blurred_image)
        
    def blur_func(self, event=None):
        option = self.blur_option.get()
        if(option == 1): self.avg_blur_func()
        elif(option == 2): self.median_blur_func()
        else: self.gauss_blur_func()
        
    
        