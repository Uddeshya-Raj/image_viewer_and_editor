from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, GifImagePlugin
from edit import EditWindow
import os
import cv2

from edit import EditWindow

GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS

def get_file_type(file_name):
    return(file_name.split('.')[-1])

def get_resize_values(img_size):
    width, height = img_size
    if(height >= width):        
        width = int(width*720/height)
        height = 720
    else:
        height = int(height*1280/width)
        width = 1280
    return (width, height)

def prev_click():
    global img_index
    img_index -= 1
    next_button.config(state=NORMAL)
    update_disp()

def next_click():
    global img_index
    img_index += 1
    prev_button.config(state=NORMAL)
    update_disp()

def update_disp():
    global img_index, image_list, img, file_name, viewed_img, img_container, prev_button, next_button
    file_name.config(text=image_list[img_index])
    img = Image.open(image_list[img_index])
    new_size = get_resize_values(img.size)
    viewed_img = ImageTk.PhotoImage(img.resize(new_size))
    img_container.config(image=viewed_img)
    
    if(img_index == 0): 
        prev_button.config(state=DISABLED)
    
    elif(img_index == image_list.__len__() - 1):
        next_button.config(state=DISABLED)

def open_edit_window():
    global edit_window, root, image_list, img, img_index
    filename = os.getcwd()+"\\"+image_list[img_index]
    editable_image = cv2.imread(filename)
    edit_window = EditWindow(editable_image, image_list[img_index])   
    edit_window.grab_set()
    edit_window.mainloop()
    
    
global file_list, image_list, img, img_index
current_working_directory = os.getcwd()
file_list = os.listdir(current_working_directory)

supported_file_types = ["bmp", "dds", "gif", "ico", "jpg", "jpeg", "jp2", "jpx", "png", "webp"]


image_list = []
for file in file_list:
    file_type = get_file_type(file)
    if file_type.lower() in supported_file_types:
        image_list.append(file)

img_index = 0
img = Image.open(image_list[img_index])
new_size = get_resize_values(img.size)

root = Tk()
root.title("Image Viewer")

file_name = ttk.Label(root, text=image_list[img_index])
img_area = ttk.Frame(root)
button_area = ttk.Frame(root)
file_name.pack()
img_area.pack()
button_area.pack()

viewed_img = ImageTk.PhotoImage(img.resize(new_size))
img_container = ttk.Label(img_area, image=viewed_img)
img_container.pack(fill=BOTH, expand=True)

prev_button = ttk.Button(button_area, text="<<-", command=prev_click, state=DISABLED)
edit_button = ttk.Button(button_area, text="EDIT", command=open_edit_window)
next_button = ttk.Button(button_area, text="->>", command=next_click)
prev_button.grid(row=0, column=0, padx=7, pady=5, sticky="ew")
edit_button.grid(row=0, column=1, padx=7, pady=5, sticky="ew")
next_button.grid(row=0, column=2, padx=7, pady=5, sticky="ew")

root.mainloop()

