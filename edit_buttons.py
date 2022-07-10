from tkinter import *
from tkinter import ttk
import cv2
from recolor import RecolorWindow
from filters_window import FiltersWindow

def get_new_file_name(filename):
    return ".".join(filename.split('.')[0:-1])+"-copy."+filename.split('.')[-1]

class EditButtons(Frame):
    def __init__(self, master):
        Frame.__init__(self, master=master)
        
        self.crop_button = ttk.Button(master=self, text="Crop")
        self.recolor_button = ttk.Button(master=self, text="Recolor")
        self.draw_button = ttk.Button(master=self, text="Draw")
        self.filter_button = ttk.Button(master=self, text="Filters")
        self.clear_button = ttk.Button(master=self, text="Clear")
        self.save_button = ttk.Button(master=self, text="Save")
        
        self.crop_button.bind("<ButtonRelease>", self.crop_func)
        self.recolor_button.bind("<ButtonRelease>", self.recolor_func)
        self.draw_button.bind("<ButtonRelease>", self.draw_func)
        self.filter_button.bind("<ButtonRelease>", self.filter_func)
        self.clear_button.bind("<ButtonRelease>", self.clear_func)
        self.save_button.bind("<ButtonRelease>", self.save_func)
        
        self.crop_button.pack(side=LEFT, padx=7)
        self.recolor_button.pack(side=LEFT, padx=7)
        self.draw_button.pack(side=LEFT, padx=7)
        self.filter_button.pack(side=LEFT, padx=7)
        self.clear_button.pack(side=LEFT, padx=7)
        self.save_button.pack(padx=7)
        
    def crop_func(self, event):
        if self.master.is_draw_state:
            self.master.edit_area.deactivate_draw()
        if self.master.is_crop_state:
            self.master.edit_area.deactivate_crop()
        else:
            self.master.edit_area.activate_crop()

    def recolor_func(self, event):
        if self.master.is_draw_state:
            self.master.edit_area.deactivate_draw()
        if self.master.is_crop_state:
            self.master.edit_area.deactivate_crop()

        self.master.recolor_window = RecolorWindow(master=self.master)
        self.master.recolor_window.grab_set()
            
    def draw_func(self, event):
        if self.master.is_crop_state:
            self.master.edit_area.deactivate_crop()
        if self.master.is_draw_state:
            self.master.edit_area.deactivate_draw()
        else:
            self.master.edit_area.activate_draw()

    def filter_func(self, event):
        if self.master.is_draw_state:
            self.master.edit_area.deactivate_draw()
        if self.master.is_crop_state:
            self.master.edit_area.deactivate_crop()

        self.master.filters_window = FiltersWindow(master=self.master)
        self.master.filters_window.grab_set()
    
    def clear_func(self, event):
        if self.master.is_draw_state:
            self.master.edit_area.deactivate_draw()
        if self.master.is_crop_state:
            self.master.edit_area.deactivate_crop()
            
        self.master.processed_image = self.master.original_image.copy()
        self.master.edit_area.show_image()
    
    def save_func(self, event):
        if self.master.is_draw_state:
            self.master.edit_area.deactivate_draw()
        if self.master.is_crop_state:
            self.master.edit_area.deactivate_crop()
            
        filename = self.master.filename
        new_image_file = self.master.processed_image
        new_filename = get_new_file_name(filename)
        cv2.imwrite(new_filename, new_image_file)
        