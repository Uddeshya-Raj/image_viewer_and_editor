from tkinter import *
from tkinter import ttk
from edit_buttons import EditButtons
from edit_area import EditArea    

class EditWindow(Toplevel):
    def __init__(self, image, filename):
        Toplevel.__init__(self)
        
        self.filename = filename
        self.original_image = image.copy()
        self.processed_image = image.copy()
        self.is_draw_state = False
        self.is_crop_state = False
        
        self.filters_window = None
        self.recolor_window = None
        
        self.edit_buttons = EditButtons(master=self)
        self.edit_buttons.pack(expand=True, pady=10)
        ttk.Separator(master=self, orient=HORIZONTAL).pack(fill=X, padx=20, pady=5)
        self.edit_area = EditArea(master=self)
        self.edit_area.show_image()
        self.edit_area.pack(fill=BOTH, expand=True, padx=20, pady=10)