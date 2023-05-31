#########################################################
# TO-DO LIST FOR THE BREAK:

# Loading window when generating image/cover image
#########################################################

# ___________________________________________________________________________ DEPENDENCIES ___________________________________________________________________________
# Import Tkinter for Python UI
import tkinter as tk
from tkinter import ttk

# Import this tkvideoplayer module to support video playing
from tkVideoPlayer import TkinterVideo

# Import Tkinter modules for buttons, labels, additional GUI
from tkinter import Label, Button, Canvas, Frame, messagebox

# Import pygame to support playing music in the background
import pygame

# Import textwrap to support dynamic positioning of texts displayed, like centering
import textwrap

# Import CustomTkinter for additional Tkinter configurations
import customtkinter as ctk

# Import Pillow or PIL for image configurations in Tkinter
from PIL import ImageTk, Image, ImageDraw, ImageFont, ImageFilter

# Import Pytorch for the neural networks used in machine learning and AI
import torch
from torch import autocast

# Import StableDiffusionPipeline for the stable diffusion methods that are used in the local GPU.
from diffusers import StableDiffusionPipeline

# Provides functions for interacting with the operating system
import os
import sys
import datetime

# ___________________________________________________________________________ GLOBAL VARIABLES ___________________________________________________________________________

image_list = []      # ARRAY OF IMAGES
text_list = []       # ARRAY OF TEXT INPUTS
content_list = []    # ARRAY OF PAGE CONTENT (mostly the text)
pdf_list = []        # ARRAY OF PDF PAGES
photo_list = []      # create a global list to store photo objects for GUI
label_list = {}      # Globalize label list to pass to delete page function
enable_realistic = 0  # Globalize value to determine whether images generated are realistic or not // set to 0 to disable by default
music_switch = 1     # Globalize value to determine whether toggle background music are On or not // set to 1 to disable by default
# Testing the application without the AI for faster UI work; 1 for testing, 0 for actual run
dev_mode = 0

# Set default title of storybook to Pictales, make it global so its value can be changed by the functions
glob_title = "PicTales"

# Set default author name of storybook to Pictales Author, make it global so its value can be changed by the functions
glob_author = "PicTales Author"

# ___________________________________________________________________________ FUNCTIONS ___________________________________________________________________________


# Function to center all windows opened and set their sizes accordingly
def center_window(window, width, height):
    # Get the screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the window position to center it
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the window coordinates
    window.geometry(f"{width}x{height}+{x}+{y}")
# ________________________________________________________________________________


# Function to make the prompts required to be interacted with
def show_message(title, message, root):
    # Disable the main window
    root.attributes('-disabled', True)

    # Create a top-level window for the dialog
    top = tk.Toplevel(root)
    top.transient(root)
    top.grab_set()
    top.withdraw()

    # Show the messagebox in the custom dialog
    messagebox.showinfo(title, message, parent=top)

    # Enable the main window
    root.attributes('-disabled', False)
    top.destroy()
# ________________________________________________________________________________


def funct_play_music():  # Function to play background music
    # Initialize sound player
    pygame.mixer.init()
    # Play sound (converted mp4 to mp3 video of to video)
    pygame.mixer.music.load("./Assets/PicTalesBGsound.mp3")
    # Loop it indefinitely
    pygame.mixer.music.play(loops=-1)
    print('Music ON')
# ________________________________________________________________________________


def funct_stop_music():  # Function to stop playing background music
    pygame.mixer.music.stop()
    print('Music OFF')
# ________________________________________________________________________________


def funct_realistic_on():   # Function to toggle on realistic image generation
    global enable_realistic  # Recall the global variable for enable realistic
    # Set to 1 to enable realistic image generation to pass to generate image and generate cover image
    enable_realistic = 1
    print("Realistic On")
# ________________________________________________________________________________


def funct_realistic_off():   # Function to toggle off realistic image generation
    global enable_realistic  # Recall the global variable for enable realistic
    # Set to 0 to disable realistic image generation to pass to generate image and generate cover image
    enable_realistic = 0
    print("Realistic Off")
# ________________________________________________________________________________


# Function for limiting the filename characters to avoid errors
def funct_truncate_text(text, trunc_val):
    if len(text) > trunc_val:  # Check the length of the text if its greater than the trunct (set character limit)
        text = text[:trunc_val]  # Truncate the string
# ________________________________________________________________________________


def funct_get_cover_data():   # Function to toggle off realistic image generation
    global glob_title  # Recall global variable glob title
    global glob_author  # Recall global variable glob author

    glob_title = prompt_pdf.get()  # Get title name from title window before it closes
    funct_truncate_text(glob_title, 60)

    # Get author name from title window before it closes
    glob_author = author_name.get()
    funct_truncate_text(glob_author, 60)

    main_operating_screen()
# ________________________________________________________________________________


def generate_image():   # Function to generate the images from the text prompt

    global img          # For storing the image to avoid garbage collection

    global text_input   # For storing the text input to transfer to the Picture Book PDF

    global image        # For storing image to be saved if save image button is clicked

    # Uses the GPU to process the dataset through the model and get the image result
    with autocast(device):

        # Store text input in a variable
        text_input = text_area.get('1.0', tk.END)
        funct_truncate_text(text_input, 120)

        # Clean the input of spaces and newlines
        text_input = text_input.strip()

        # Catch error if no text input is given
        if text_input == '' or len(text_input) == 0 or text_input.isspace() == True:

            image = blank
            # Disable the add character button if no input is given
            edit_content_label.config(state="disabled")
            # Disable the save button if no input is given
            save_label.config(state="disabled")

        else:

            # CPU MODE
            if dev_mode == 1:
                image = blank

            else:

                if enable_realistic == 0:
                    cartoon_input = "Cartoonish illustration of " + text_input
                else:
                    cartoon_input = text_input

                # Variable that contains the image result
                image = pipe(cartoon_input, guidance_scale=10)[
                    "images"][0]

            # Enable the add character button if the image is generated successfully
            edit_content_label.config(state="normal")
            # Enable the save button in generate window if the image is generated successfully
            save_label.config(state="normal")

    # Store image in a variable
    img = ImageTk.PhotoImage(image)

    # Save image file name as PNG based on text input
    image.save('./GeneratedImages/Preview.png')

    # Displays the text input in the Tkinter UI after generation
    # ltext.configure(text=text_input)
    # ltext.update()

    # Displays the image in the Tkinter UI after generation
    lmain.configure(image=img)
    lmain.update()

    # Show prompt message that shows image has been generated
    show_message("PicTales", "Image Generated!", generate_window)
# ________________________________________________________________________________


def toggle_music():  # Function to Toggle on/off background music
    global music_switch  # Recall global variable music_switch
    if music_switch == 1:
        funct_stop_music()
        music_switch = 0
        music_button['image'] = musicOff_icon
    else:
        funct_play_music()
        music_switch = 1
        music_button['image'] = musicOn_icon
# ________________________________________________________________________________


# Function for getting the character selected WITH the expressions, essentially the image we pass for saving a page.
def funct_main_char_select(main_char_value, main_char_image):

    # Call global main_char_select variable to override the initial value
    global main_char_select

    # Call global character variable to override initial value
    global character

    # Get the value passed from character expresion funcion
    main_char_select = main_char_value

    # Set the image for the character that will be later pasted onto the generated image if selected
    character = main_char_image

    # Update the image for the select character window (1-3)
    selected_character_photo.configure(image=character)
    selected_character_photo.update()

    # Go back to edit content page
    addcharacter_screen_deposit()
# ________________________________________________________________________________


def funct_inner_frame():  # Dynamically configures the widgets in the inner frame

    # Recall the global label list since its gonna detect a non-existing local variable otherwise
    global label_list

    # Initiate a counter for text, image label frames positioning, and index pointing
    counter = 0

    # Remove the previous labels from the window
    for index in label_list:
        for label in label_list[index]:
            label.grid_forget()
    label_list = {}  # Reset the stack everytime this window is called

    # Create a frame to hold the content page and image page widgets
    framecover = Frame(inner_frame, bg="#F9F4F1")
    framecover.grid(row=1, column=0, padx=20, pady=(200, 10), sticky='n')

    # Widget for displaying a label frame object that contains the cover image
    previewcover_img = Image.open('./GeneratedImages/PreviewCover.png')
    previewcover_img = previewcover_img.resize(
        (250, 250), resample=Image.LANCZOS)
    previewcover_photo = ImageTk.PhotoImage(previewcover_img)
    # add photo object to the photo list
    photo_list.append(previewcover_photo)
    limg_list_cover = Label(
        framecover, image=previewcover_photo, bg="#F9F4F1")
    limg_list_cover.grid(row=0, column=0, padx=(20, 0), sticky='n')

    # Loop for the text items and image items added by the user to the story to display them in the main operating window
    for text_item, pic, content_item in zip(text_list, image_list, content_list):

        # Reset the elements inside the label list
        label_list[counter] = []

        # Create a frame to hold the content page and image page widgets
        frame = Frame(inner_frame, bg="#F9F4F1")
        frame.grid(row=1, column=counter+1, padx=20,
                   pady=(200, 10), sticky='n')

        # Widget for displaying a update button pointing to the current page
        lupdate_photo = ImageTk.PhotoImage(
            Image.open('./Assets/editbutton.png'))
        photo_list.append(lupdate_photo)
        lupdate_list = Button(frame, image=lupdate_photo,
                              text="UPDATE", command=lambda index=counter: update_page(index), bg='#F9F4F1', activebackground='#F9F4F1', borderwidth=0, highlightthickness=0)
        lupdate_list.grid(row=2, column=1, pady=(10, 0), padx=(0, 100))
        label_list[counter].append(lupdate_list)

        # Widget for displaying a delete button pointing to the current page
        ldelete_photo = ImageTk.PhotoImage(
            Image.open('./Assets/trashbutton.png'))
        photo_list.append(ldelete_photo)
        ldelete_list = Button(frame, image=ldelete_photo,
                              text="DELETE", command=lambda index=counter: delete_page(index), bg='#F9F4F1', activebackground='#F9F4F1', borderwidth=0, highlightthickness=0)
        ldelete_list.grid(row=2, column=1, pady=(10, 0), padx=(100, 0))
        label_list[counter].append(ldelete_list)

        # Widget for displaying a label frame object that contains a content page of the storybook
        ltext_list = Label(frame, height=5, width=10, text="Page {}".format(counter+1), font=(
            "Supersonic Rocketship", 20), fg="#AB7A11", bg="#F9F4F1")
        ltext_list.grid(row=1, column=1, padx=(20, 0), sticky='n')
        label_list[counter].append(ltext_list)

        # Widget for displaying a label frame object that contains an image page of the storybook
        limg_img = Image.open('./GeneratedImages/{}.png'.format(text_item))
        limg_img = limg_img.resize(
            (250, 250), resample=Image.LANCZOS)
        limg_photo = ImageTk.PhotoImage(limg_img)
        # add photo object to the photo list
        photo_list.append(limg_photo)
        # limg_list = Label(frame, image=limg_photo, bg="#F9F4F1")
        limg_list = Button(frame, image=limg_photo, bg="#F9F4F1",
                           text="VIEW", command=lambda index=counter: view_page(index), activebackground='#F9F4F1', borderwidth=0, highlightthickness=0)
        limg_list.grid(row=0, column=1, padx=(20, 0), sticky='n')
        label_list[counter].append(limg_list)

        # Move the counter to 1 already to skip the cover text and cover image
        counter += 1

        # Update the scroll region of the canvas
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))
# ________________________________________________________________________________


def view_page(index):  # View a page
    # Hide main screen when in view page window
    main_screen.withdraw()

    # Globalized to be destroyed
    global view_page_window

    # Initiate generate window's tk GUI
    view_page_window = tk.Toplevel()
    view_page_window.title("View Page")

    # This code will pop up the window how to in top level
    view_page_window.grab_set()

    # The geometry with app winfo width and height will center the window modal in main screen
    center_window(view_page_window, 1228, 750)
    view_page_window.configure(bg='#F8BC3B')  # set background color

    # Disable the Close Window Control Icon in generate window
    view_page_window.protocol("WM_DELETE_WINDOW", disable_event)

    # Title for page window
    ltitle = Label(view_page_window, height=2, width=70, text="\n".join(textwrap.wrap(
        glob_title, width=70)), font=("Supersonic Rocketship", 16), fg="#AB7A11", bg='#F8BC3B')
    ltitle.place(x=200, y=15)

    # Page Number for view page window
    lpage_number = Label(view_page_window, height=2, width=40, text="Page {}".format(
        index+1), font=("Supersonic Rocketship", 16), fg="#AB7A11", bg='#F8BC3B')
    lpage_number.place(x=380, y=650)

    # Container Label for view page image
    global lview_image  # Globalize for next/back page function
    # Show the image in a container
    lview_image = tk.Label(view_page_window, bg='#F8BC3B',
                           image=image_list[index])
    lview_image .place(x=50, y=100)

    # Container Label for view page content
    global lview_content  # Globalize to pass on generate image function
    lview_content = Label(view_page_window, height=16, width=40, text="\n".join(textwrap.wrap(content_list[index], width=40)), font=(
        "Supersonic Rocketship", 16), fg="#AB7A11")
    lview_content.place(x=690, y=100)

    def on_click_back():  # Function for going back to main screen on back button click
        # Destroy view_page_window
        view_page_window.destroy()
        # Show the hidden main screen again
        main_screen.deiconify()

    def on_click_next(index):  # Function to go to the next consecutive page of the story
        # Destroy view_page_window
        view_page_window.destroy()
        # Show the hidden main screen again
        view_page(index+1)

    def on_click_prev(index):  # Function to go to the previous page of the story
        # Destroy view_page_window
        view_page_window.destroy()
        # Show the hidden main screen again
        view_page(index-1)

    def on_click_edit_content_window(index):
        # Hide main screen when in view page window
        view_page_window.withdraw()

        # Globalized to be destroyed
        global edit_storyline_window

        # Initiate generate window's tk GUI
        edit_storyline_window = tk.Toplevel()
        edit_storyline_window.title("Edit Text Content Page")

        # This code will pop up the window how to in top level
        edit_storyline_window.grab_set()

        # The geometry with app winfo width and height will center the window modal in main screen
        center_window(edit_storyline_window, 735, 800)
        edit_storyline_window.configure(bg='#F8BC3B')  # set background color

        def update_storyline(index):  # Update the content of the page

            global lview_content  # Globalize the label

            # Store the edited content in a temporary variable
            temp_content = text_area_content_update.get('1.0', tk.END)

            # if input was not edited (blank)
            if temp_content == '' or len(temp_content) == 0 or temp_content.isspace() == True:
                # Retrieve previous content
                content_list[index] = content_list[index]
            else:
                content_list[index] = temp_content  # Update to new content
            funct_truncate_text(content_list[index], 120)

            # Update the text of the lview_content label
            lview_content.config(text="\n".join(
                textwrap.wrap(content_list[index], width=40)))

            edit_storyline_window.destroy()  # Close edit storyline window
            view_page_window.deiconify()
        # ________________________________________________________________________________

        def view_page_window_deposit():  # Show view page window again

            edit_storyline_window.destroy()  # Close edit storyline window
            view_page_window.deiconify()
        # ________________________________________________________________________________

        # Textbox widget for getting USER TEXT INPUT FOR GENERATING IMAGE
        text_area_content_update = tk.Text(edit_storyline_window, height=14, width=38,
                                           bg='#F8BC3B',  bd=1, relief="solid", font=("Supersonic Rocketship", 20))
        text_area_content_update.place(x=100, y=125)

        # Label for image generated
        text_area_content_update_label = Label(
            edit_storyline_window, text="Update Content", bg='#F8BC3B')
        text_area_content_update_label.place(x=55, y=67)
        text_area_content_update_label.config(
            font=("Supersonic Rocketship", 18))

        # Save content button (SAVES THE IMAGE WITH THE CHARACTER AND THE CONTENT)
        save_photo_edit_storyline_window = ImageTk.PhotoImage(
            Image.open('./Assets/frame0/save.png'))
        # add photo object to the list
        photo_list.append(save_photo_edit_storyline_window)
        save_save_photo_edit_storyline_window_label = Button(edit_storyline_window, image=save_photo_edit_storyline_window, borderwidth=0, highlightthickness=0,
                                                             bg='#F8BC3B', activebackground='#F8BC3B', command=lambda index=index: update_storyline(index))
        save_save_photo_edit_storyline_window_label.place(x=100, y=700)

        # Back button to view page window in edit_storyline_window
        back_photo_edit_storyline_window = ImageTk.PhotoImage(
            Image.open('./Assets/inverted_backbutton.png'))
        # add photo object to the photo list
        photo_list.append(back_photo_edit_storyline_window)
        back_label_edit_storyline_window = Button(edit_storyline_window, borderwidth=0, highlightthickness=0,
                                                  image=back_photo_edit_storyline_window, command=view_page_window_deposit, bg='#F8BC3B', activebackground='#F8BC3B')
        back_label_edit_storyline_window.place(x=85, y=20, anchor="n")

        # Disable clarification window resizing
        view_page_window.resizable(False, False)

        # Disable the Close Window Control Icon in generate window
        edit_storyline_window.protocol("WM_DELETE_WINDOW", disable_event)

        # Disable clarification window resizing
        edit_storyline_window.resizable(False, False)
        # ________________________________________________________________________________

    # Widget for displaying a update button pointing to the current page
    update_photo_view_page_window = ImageTk.PhotoImage(
        Image.open('./Assets/editbutton.png'))
    # add photo object to the photo list
    photo_list.append(update_photo_view_page_window)
    update_label_view_page_window = Button(view_page_window, borderwidth=0, highlightthickness=0,
                                           image=update_photo_view_page_window, command=lambda index=index: on_click_edit_content_window(index), bg='#F8BC3B', activebackground='#F8BC3B')
    update_label_view_page_window.place(x=750, y=640, anchor="n")

    # if there are two pages or more
    if len(image_list) > 1 and (index < (len(image_list) - 1 or index == 1)):
        # Next button for view page window
        next_photo_view_page_window = ImageTk.PhotoImage(
            Image.open('./Assets/next.png'))
        # add photo object to the photo list
        photo_list.append(next_photo_view_page_window)
        next_label_view_page_window = Button(view_page_window, borderwidth=0, highlightthickness=0,
                                             image=next_photo_view_page_window, command=lambda index=index: on_click_next(index), bg='#F8BC3B', activebackground='#F8BC3B')
        next_label_view_page_window.place(x=1150, y=630, anchor="n")

    # Check if it is the last page
    if len(image_list) > 1 and index != 0:
        # Prev button for view page window
        prev_photo_view_page_window = ImageTk.PhotoImage(
            Image.open('./Assets/prev.png'))
        # add photo object to the photo list
        photo_list.append(prev_photo_view_page_window)
        prev_label_view_page_window = Button(view_page_window, borderwidth=0, highlightthickness=0,
                                             image=prev_photo_view_page_window, command=lambda index=index: on_click_prev(index), bg='#F8BC3B', activebackground='#F8BC3B')
        prev_label_view_page_window.place(x=70, y=630, anchor="n")

    # Back button to main screen in view page window
    back_photo_view_page_window = ImageTk.PhotoImage(
        Image.open('./Assets/inverted_backbutton.png'))
    # add photo object to the photo list
    photo_list.append(back_photo_view_page_window)
    back_label_view_page_window = Button(view_page_window, borderwidth=0, highlightthickness=0,
                                         image=back_photo_view_page_window, command=on_click_back, bg='#F8BC3B', activebackground='#F8BC3B')
    back_label_view_page_window.place(x=85, y=20, anchor="n")

    # Disable clarification window resizing
    view_page_window.resizable(False, False)
# ________________________________________________________________________________


def update_page(index):  # Update a page

    global label_list   # Recall the label_list

    # Globalize value to pass to generate save, turning it essentially into an update
    global update_value

    # Set the value to a bool, for a condition in generate save
    update_value = index

    funct_generate_window()

    # Delete the ghost widgets when pressing update
    for label in label_list[index]:
        label.grid_forget()

    # Update the widgets
    funct_inner_frame()

    # Update the scroll region of the canvas
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))
# ________________________________________________________________________________


def delete_page(index):  # Delete a page

    global label_list   # Recall the label_list

    # Remove the corresponding content, text, and image from the lists
    content_list.pop(index)
    image_list.pop(index)
    text_list.pop(index)

    # Delete the ghost widgets when pressing delete
    for label in label_list[index]:
        label.grid_forget()

    # Update the widgets
    funct_inner_frame()

    # Update the scroll region of the canvas
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))

    # Show prompt message that shows page has been updated
    show_message("PicTales", "Page Deleted!", main_screen)
# ________________________________________________________________________________


def generate_save():    # Saves the image in the current directory and displays the current images selected for the picture book

    # Check if user has already generated an image first before saving.
    try:
        image
    except NameError:   # If variable is empty or not defined, return false
        is_generated = False
    else:               # If variable is not empty or defined, return true
        is_generated = True

    # If an image has been generated
    if is_generated:

        # Globalize content variable that stores the edited content
        global content

        # Store the base image on which the character would be pasted on
        global base

        # Recall the main char select value
        global main_char_select

        ##################### CHECK FOR SAME IMAGE NAMES #######################

        global text_input  # Recall text input value

        flag = 0  # Initialize flag to 0 for counting and naming duplicates

        # Store current text input in a variable
        temp = text_input

        # Loop through the text list
        for input in text_list:

            # If text input has a duplicate
            if temp == input:

                # Increment flag per input
                flag += 1
                print("found duplicate! counts: {}".format(flag))

                # Store the next iteration in the dummy variable
                temp = text_input + "{}".format(flag)

        # If theres atleast 1 duplicate
        if flag > 0:
            # Add a number to the text input to make its filename have a somewhat unique name
            text_input = text_input + "{}".format(flag)

        # Save image file name as PNG based on text input
        image.save('./GeneratedImages/{}.png'.format(text_input))

        ########################################################################

        # If a character was chosen and the edit content page has been clicked
        if main_char_select > 0 and main_char_select < 9:

            # Load the base image on which the character will be pasted
            base = Image.open(
                './GeneratedImages/{}.png'.format(text_input)).convert('RGBA')

            # Convert the PhotoImage object to a PIL Image object and convert to RGBA mode
            character_image = ImageTk.getimage(character).convert('RGBA')

            # Create a new transparent image of the same size as the base image
            result = Image.new('RGBA', base.size, (0, 0, 0, 0))

            # Paste the base image onto the new image
            result.paste(base, (0, 0))

            # Paste the character image onto the new image using alpha_composite
            result.alpha_composite(character_image, dest=(0, 360))

            # Save the result image to disk that has the character # DOES NOT CHECK FOR DUPLICATES
            result.save('./GeneratedImages/{}.png'.format(text_input))

            # Store image in img variable if a character is selected
            img = ImageTk.PhotoImage(result)

            if addcharacter_screen.winfo_exists():
                # Get story content if user adds a story
                content = edit_textcontent_area.get('1.0', tk.END)
                funct_truncate_text(content, 120)
            else:  # If page was saved in the generate window
                # Overwrite image again since character was saved but should not be displayed since the user backed out
                img = ImageTk.PhotoImage(image)
                content = text_input

        # If no character was chosen or the user did not clicked edit content page
        if main_char_select == 0 or main_char_select == 9:
            # Store image in img variable if no character is selected
            img = ImageTk.PhotoImage(image)
            # If edit story was not invoked, default the content to the text input for generating image
            content = text_input

            # If the add story button was clicked
            if main_char_select == 9:
                if addcharacter_screen.winfo_exists():  # Check if addcharacter_screen is still open
                    content = edit_textcontent_area.get('1.0', tk.END)
                    funct_truncate_text(content, 120)
                else:  # If page was saved in the generate window
                    content = text_input

        # Makes the text input as a default content input if the user did not enter anything at the content textbox.
        if content == '' or len(content) == 0 or content.isspace() == True:
            content = text_input

        global update_value  # Recall the update value from update page function

        # When updating a page
        if update_value != None:

            # Update the previous content to the list using the update_value as the pointer index
            content_list[update_value] = content

            # Update the previously stored text in the list using the update_value as the pointer index
            text_list[update_value] = text_input

            # Update the previous image in the list using the update_value as the pointer index
            image_list[update_value] = img

            # If addcharacter screen window is opened
            if main_char_select > 0 and main_char_select < 9:
                # Show prompt message that shows page has been updated
                show_message("PicTales", "Page Updated!", addcharacter_screen)
            else:
                # Show prompt message that shows page has been updated
                show_message("PicTales", "Page Updated!", generate_window)

        # Regular adding of a page
        else:

            # Add the content to the list
            content_list.append(content)

            # Add the previously stored text in a list
            text_list.append(text_input)

            # Store previous image in a list
            image_list.append(img)

            # If addcharacter screen window is opened
            if main_char_select > 0 and main_char_select < 9:
                # Show prompt message that shows page has been updated
                show_message("PicTales", "Page Saved!", addcharacter_screen)
            else:
                # Show prompt message that shows page has been saved
                show_message("PicTales", "Page Saved!", generate_window)

        update_value = None  # Reset the value of update

        # Update the widgets
        funct_inner_frame()

        # If addcharacter screen window is opened
        if main_char_select > 0 and main_char_select < 9:
            # Destroy the edit content window
            addcharacter_screen.destroy()

        # Reset the main_char_select value
        main_char_select = 0

        # Go back to main screen
        main_screen_deposit()
# ________________________________________________________________________________


def generate_cover_image():   # Function to generate the cover image from the text prompt in title window

    global img_cover          # For storing the image to avoid garbage collection

    global cover_input   # For storing the text input to transfer to the Picture Book PDF

    global image_cover  # Globalizes cover image variable

    # Uses the GPU to process the dataset through the model and get the image result
    with autocast(device):

        # Store text input in a variable
        cover_input = prompt_area.get('1.0', tk.END)
        funct_truncate_text(cover_input, 120)

        # Catch error if no text input is given
        if cover_input == '' or len(cover_input) == 0 or cover_input.isspace() == True:

            image_cover = blank
            # Disable the button if no input is given
            okay_label.config(state="disabled")

        else:

            # CPU MODE
            if dev_mode == 1:
                image_cover = blank

            else:

                if enable_realistic == 0:
                    cartoon_input = "Cartoonish illustration of " + cover_input
                else:
                    cartoon_input = cover_input

                # Variable that contains the image cover result
                image_cover = pipe(cartoon_input, guidance_scale=10)[
                    "images"][0]

            # Enable the button if the image is generated successfully
            okay_label.config(state="normal")

    # Store image in a variable
    img_cover = ImageTk.PhotoImage(image_cover)

    # Save image file name as PNG based on text input
    image_cover.save('./GeneratedImages/PreviewCover.png')

    # Displays the text input in the Tkinter UI after generation
    ltext_cover.configure(text=cover_input)
    ltext_cover.update()

    # Displays the image in the Tkinter UI after generation
    lmain_cover.configure(image=img_cover)
    lmain_cover.update()

    # Show prompt message that shows image has been generated
    show_message("PicTales", "Image Generated!", start_window)
# ________________________________________________________________________________


def generate_pdf():                # Generate PicTale Story book

    # Store the name of the cover image prompt to find the matching image path for it.
    pdf_name = glob_title

    # Store current time in a variable
    now = datetime.datetime.now()

    # Store the pdf file name into a variable, sets this as default for errors and etc like if the title name is not set.
    if pdf_name == '' or len(pdf_name) == 0 or pdf_name.isspace() == True:
        pdf_name = 'PicTales'

    # Specifies the directory where the pdf will generate
    pdf_path = "./StoryBooks/{}.pdf".format(pdf_name)

    # Save image file name as PNG based on text input
    image_cover.save('./GeneratedImages/TitlePage_{}.png'.format(pdf_name))

    # Pass image cover variable for drawing/writing the page title details
    covertext = ImageDraw.Draw(image_cover)

    # Choose font for cover page details: date, author, and title respectively
    date_font = ImageFont.truetype('./fonts/Supersonic Rocketship.ttf', 16)
    auth_font = ImageFont.truetype('./fonts/Supersonic Rocketship.ttf', 30)
    titlefont = ImageFont.truetype('./fonts/Supersonic Rocketship.ttf', 40)

    # Set the maximum width for each line
    max_width = 15

    # Wrap the text into multiple lines based on the maximum width
    wrapped_text = textwrap.wrap(pdf_name, width=max_width)

    # Calculate the y-coordinate for the second line of text
    y_coord = 90

    # Draw each line of text with white color and increment the y-coordinate
    for line in wrapped_text:
        # Get the size of the font for dynamic coverage of the background
        text_width, text_height = titlefont.getsize(line)
        # Black background for anti camo in title name / pdf name
        bbox = (90, y_coord, 100 + text_width, y_coord + text_height)
        covertext.rectangle(bbox, fill=(255, 165, 0))
        # For writing title page / pdf name input in cover page
        covertext.text((90, y_coord), line,
                       font=titlefont, fill=(255, 255, 255))
        y_coord += titlefont.getsize(line)[1] + 10

    # Black background for anti camo in author name
    bbox = covertext.textbbox((50, 380), glob_author, font=auth_font)
    covertext.rectangle(bbox, fill=(255, 165, 0))
    # For writing author input in cover page
    covertext.text((50, 380), glob_author,
                   font=auth_font, fill=(255, 255, 255))

    # Black background for anti camo in date created
    bbox = covertext.textbbox(
        (50, 410), now.strftime("%m-%d-%Y"), font=date_font)
    covertext.rectangle(bbox, fill=(255, 165, 0))
    # For writing date created in cover page
    covertext.text((50, 410), now.strftime("%m-%d-%Y"),
                   font=date_font, fill=(255, 255, 255))

    # Save cover image to local directory // This has the Generated Cover Image // Page 1
    image_cover.save('./GeneratedImages/TitlePage_{}.png'.format(pdf_name))

    # Store the coverpage into an object variable // Static Image Page 2
    cover = Image.open('./Assets/CoverPage.png')

    # Safely convert the rogue image into a pdf page
    if cover.mode == 'RGBA':
        cover = cover.convert('RGB')

    # Add the title page with the AI generated image to page 1 of storybook
    pdf_list.append(Image.open(
        './GeneratedImages/TitlePage_{}.png'.format(pdf_name)))

    # Add the PicTales cover page page 2 of storybook
    pdf_list.append(cover)

    # Pointer/Flag for content for content list access later and start at 1 so index 0 can store title page / IMPORTANT DO NOT REPLACE FOR FILE IN LOOP
    i = 0

    # For each image file that has been written with the text list names, the text list names their files itself based on order.
    for file in text_list:

        # Store Generated image in a variable to be used as the text background
        photo = Image.open('./GeneratedImages/{}.png'.format(file))

        # Blur the stored image
        photo = photo.filter(ImageFilter.GaussianBlur(20))

        # Invoke draw function to the blank image
        phototext = ImageDraw.Draw(photo)

        # Choose font for content page
        content_font = ImageFont.truetype(
            'comic.ttf', 30)

        # Set the maximum width for each line
        max_width = 20

        # Wrap the text into multiple lines based on the maximum width
        wrapped_text = textwrap.wrap(content_list[i], width=max_width)

        # Calculate the y-coordinate for the second line of text
        y_coord = 70

        # Draw each line of text with white color and increment the y-coordinate
        for line in wrapped_text:
            # Get the size of the font for dynamic coverage of the background
            text_width, text_height = content_font.getsize(line)
            # Black background for anti camo in a content page
            bbox = (70, y_coord, 80 + text_width, y_coord + text_height)
            phototext.rectangle(bbox, fill=(255, 165, 0))
            # For writing the content in a page
            phototext.text((70, y_coord), line,
                           font=content_font, fill=(255, 255, 255))
            y_coord += content_font.getsize(line)[1] + 10

        # Save the drawn page that contains the text input in the local directory
        photo.save('./GeneratedImages/INPUT{}.png'.format(file))

        # Move the pointer
        i = i + 1

    # Convert each PhotoImage object files into normal files
    for file in text_list:

        # Store image file in a variable
        file_image = Image.open(
            './GeneratedImages/{}.png'.format(file))

        # Safely convert the rogue file image into a pdf page
        if file_image.mode == 'RGBA':
            file_image = file_image.convert('RGB')

        # Append main image file
        pdf_list.append(file_image)

        # Store the edited content page in a variable for rgba conversion
        file_text = Image.open(
            './GeneratedImages/INPUT{}.png'.format(file))

        # Safely convert the rogue file text into a pdf page
        if file_text.mode == 'RGBA':
            file_text = file_text.convert('RGB')

        # Append the image file that has the text input drawn on a blank page
        pdf_list.append(file_text)

    # Check if storybook has content
    if pdf_list:
        # Generate the PDF
        pdf_list[0].save(
            pdf_path, "PDF", resolution=100.0, save_all=True, append_images=pdf_list[1:]
        )

    # Show prompt that PDF was generated
    show_message("PicTales", "Your PDF has been generated!",
                 clarification_window)

    # Close the app when storybook is made
    clarification_window.destroy()

    # Close the main operating window
    main_screen.destroy()

    # Attach the file extension pdf to the name
    pdf_name = pdf_name + ".pdf"

    # Search the folder StoryBooks where the pdfs are stored
    pdf_file = os.path.join("StoryBooks", pdf_name)

    # Open the storybook upon the app's exit
    os.startfile(pdf_file)

    # Close the app window
    app.destroy()


# ___________________________________________________________________________ CONFIGURATIONS ___________________________________________________________________________
isExist = os.path.exists('./results/model-1.pt')

if (isExist == False):
    sys.exit(0)

# loads the model used to a pre-defined library online
# modelid = "runwayml/stable-diffusion-v1-5"
modelid = "CompVis/stable-diffusion-v1-4"

auth_token = "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"

if dev_mode == 0:
    if torch.cuda.is_available():

        # Set device to CUDA, app would run GPU
        device = "cuda"

        # Loads the model into torch with CUDA
        torch.load('./results/model-1.pt')

        # Uses the pipe from the online library for model translation to produce the image.
        pipe = StableDiffusionPipeline.from_pretrained(
            modelid, revision="fp16", torch_dtype=torch.float16, use_auth_token=auth_token)

    else:

        # Set device to CPU, app would run on CPU
        device = "cpu"

        # Loads the model into torch with CPU
        torch.load('./results/model-1.pt', map_location=torch.device('cpu'))

        # Uses the pipe from the online library for model translation to produce the image.
        pipe = StableDiffusionPipeline.from_pretrained(
            modelid, revision="fp16", torch_dtype=torch.bfloat16, use_auth_token=auth_token)  # FIX THIS FLOAT VALUE
else:
    # Set device to CPU, app would run on CPU
    device = "cpu"

if dev_mode == 0:
    # Uses the graphics driver (Must atleast be 8GB ram)
    pipe.to(device)

# Create template page for the title page image
blank = Image.new('RGB', (512, 512))

# List of folders to create if they don't exist
folders_to_create = ["GeneratedImages", "StoryBooks"]

# Loop through the folders and create them if they don't exist
for folder in folders_to_create:
    if not os.path.exists(folder):
        os.mkdir(folder)  # Create function of folder
        print(f"Folder '{folder}' created successfully.")

# Save template in generated images folder
blank.save('./GeneratedImages/BlankTemplate.png')

# Define the font file path and size
font_path = "./fonts/Supersonic Rocketship.ttf"
font_size = 24

# Create a custom font for usage throughout the whole program
custom_font = (font_path, font_size, "bold")

# ___________________________________________________________________________ FRONT END FUNCTIONS FOR TK WINDOWS ___________________________________________________________________________


def funct_about_window():     # The question mark button shows the about pictales modal

    # Initiate about window's tk GUI
    about_window = tk.Toplevel()
    about_window.title('About PicTales')

    # This code will pop up the window about in top level
    about_window.grab_set()

    center_window(about_window, 756, 653)
    # Set background color for about window
    about_window.configure(bg='#F8BC3B')

    # Label to show the about title
    modal_label = tk.Label(about_window, text='ABOUT',
                           font=custom_font, fg='white', bg='#F8BC3B')
    modal_label.pack(pady=50)

    # This block of code show the logo PICTALES and resize it, and append the image to be seen coz of resizing
    about_img = Image.open('./Assets/PICTALES LOGO Big w background.png')
    resized_img = about_img.resize(
        (200, 200), resample=Image.LANCZOS)
    about_photo = ImageTk.PhotoImage(resized_img)
    # MAGIC APPEND
    photo_list.append(about_photo)  # add photo object to the photo list
    # Show photo in a label widget
    about_label = tk.Label(about_window, image=about_photo)
    about_label.place(x=380, y=165, anchor="n")

    # Set the font of the label to Supersonic Rocketship with a size of 20
    modal_label.config(font=("Supersonic Rocketship", 64))

    # This code is for displaying the copyright
    ver_label = tk.Label(about_window, text='Copyright © 2023, PicTales',
                         font=custom_font, fg='white', bg='#F8BC3B')
    ver_label.place(relx=0.25, rely=0.75)
    ver_label.config(font=("Supersonic Rocketship", 24))

    # This code is for displaying the version of the app
    copy_label = tk.Label(about_window, text='VER. 1.0',
                          font=custom_font, fg='white', bg='#F8BC3B')
    copy_label.pack(pady=190)
    copy_label.config(font=("Supersonic Rocketship", 24))

    # Disables the resizing of the about window
    about_window.resizable(False, False)
# ________________________________________________________________________________


def funct_howTo_window():     # How to button will show this window playing the video about pictales

    # Show instructions:
    show_message("Instructions", "- Must have 8gb+ GPU ram\n- In the fonts folder, install supersonic rocketship\n- Must have wifi constantly on\n- Text Inputs must only be in english and has a maximum of 120 characters\n- Change Display scale and layout from 125% to 100%\n- Close buttons are disabled, the only exit is from the main menu", app)

    global howTo_window  # Globalize to be destroyed later

    # Initiate how to window's tk GUI
    howTo_window = tk.Toplevel()
    howTo_window.title('How to use Pictales')

    # This code will pop up the window how to in top level
    howTo_window.grab_set()

    # The geometry with app winfo width and height will center the window modal in main screen
    howTo_window.geometry("1028x700+{}+{}".format(
        app.winfo_width()//2 - 480 + app.winfo_rootx(),
        app.winfo_height()//2 - 380 + app.winfo_rooty()
    ))
    howTo_window.configure(bg='#F8BC3B')  # set background color

    # Video Player on playing the tutorial video in howTo_window
    videoplayer = TkinterVideo(howTo_window, scaled=True)
    # Path of video file
    videoplayer.load("./Assets/sample.mp4")
    videoplayer.pack(expand=True, fill="both")
    videoplayer.play()  # play the video

    howTo_window.resizable(False, False)

    # Back button of the How To
    back_photo_howTo_window = ImageTk.PhotoImage(
        Image.open('./Assets/inverted_backbutton.png'))
    # add photo object to the photo list
    photo_list.append(back_photo_howTo_window)
    back_label_howTo_window = Button(howTo_window, borderwidth=0, highlightthickness=0,
                                     image=back_photo_howTo_window, command=howTo_window.destroy, bg='#F8BC3B', activebackground='#F8BC3B')
    back_label_howTo_window.place(x=85, y=20, anchor="n")
# ________________________________________________________________________________


def main_screen_deposit():  # Function called when pressing back button or generating a save page in generate window

    global update_value  # Recall the update value from generate window
    # Reset update value
    update_value = None

    # Show the hidden main screen again
    main_screen.deiconify()

    # Hide window 1
    app.withdraw()

    # Destroy the generate window
    generate_window.destroy()
# ________________________________________________________________________________


def funct_generate_window():    # This window is for getting the text prompt and image generated result from that prompt

    # Hide main screen when in generate window
    main_screen.withdraw()

    # Globalized to be destroyed at the click of the save button in edit_content_page function
    global generate_window

    # Initiate generate window's tk GUI
    generate_window = tk.Toplevel()
    generate_window.title("Generate Page")

    # This code will pop up the window how to in top level
    generate_window.grab_set()

    center_window(generate_window, 1228, 800)
    generate_window.configure(bg='#F8BC3B')  # set background color

    # Disable the Close Window Control Icon in generate window
    generate_window.protocol("WM_DELETE_WINDOW", disable_event)

    # Back button to generate_window
    back_photo_generate_window = ImageTk.PhotoImage(
        Image.open('./Assets/inverted_backbutton.png'))
    # add photo object to the photo list
    photo_list.append(back_photo_generate_window)
    back_label_generate_window = Button(generate_window, borderwidth=0, highlightthickness=0,
                                        image=back_photo_generate_window, command=main_screen_deposit, bg='#F8BC3B', activebackground='#F8BC3B')
    back_label_generate_window.place(x=85, y=20, anchor="n")

    # Label for prompt in generate window
    text_title = Label(
        generate_window, text="Enter prompt here (120 characters max)", bg='#F8BC3B')
    text_title.place(x=598, y=67)
    text_title.config(font=("Supersonic Rocketship", 18))

    global text_area  # Globalize the widget containing the text input from the user

    # Textbox widget for getting USER TEXT INPUT FOR GENERATING IMAGE
    text_area = tk.Text(generate_window, height=13, width=38,
                        bg='#F8BC3B',  bd=1, relief="solid", font=("Supersonic Rocketship", 20))
    text_area.place(x=600, y=100)

    # Label for image generated
    generate_title = Label(
        generate_window, text="Image generated", bg='#F8BC3B')
    generate_title.place(x=55, y=67)
    generate_title.config(font=("Supersonic Rocketship", 18))

    # This code is to generate the border of the generated image
    generate_border = Label(generate_window, height=34, width=72,
                            bd=1, relief="solid", bg='#F8BC3B')
    generate_border.place(x=58, y=100)

    global lmain  # Globalize to pass on generate image function

    # Show the image in a container
    lmain = tk.Label(generate_window, bg='#F8BC3B')
    lmain.place(x=50, y=100)

    # global ltext  # Globalize to pass on generate image function
    # ltext = ctk.CTkLabel(generate_window, height=15, width=46, text="Image Title", font=(
    #     "Supersonic Rocketship", 20), text_color="black")
    # ltext.place(x=60, y=635)

    # Generate button
    trigger_photo = ImageTk.PhotoImage(
        Image.open('./Assets/frame0/Generate Button.png'))
    photo_list.append(trigger_photo)  # add photo object to the photo list
    trigger_label = Button(generate_window, image=trigger_photo, borderwidth=0,
                           highlightthickness=0, bg='#F8BC3B', activebackground='#F8BC3B', command=generate_image)
    trigger_label.place(x=110, y=660)

    # Globalize this so it can be disabled when no image is generated in generate image function
    global save_label

    # Save content button (SAVES THE IMAGE WITH NO CHARACTER AND NO CONTENT)
    save_photo = ImageTk.PhotoImage(Image.open('./Assets/frame0/save.png'))
    photo_list.append(save_photo)  # add photo object to the photo list
    save_label = Button(generate_window, image=save_photo, borderwidth=0, highlightthickness=0,
                        bg='#F8BC3B', activebackground='#F8BC3B', command=generate_save, state="disabled")
    save_label.place(x=600, y=665)

    # Globalize this so it can be disabled when no image is generated in generate image function
    global edit_content_label
    # Edit content photo // add character button
    edit_content_photo = ImageTk.PhotoImage(
        Image.open('./Assets/addStory_Button.png'))
    photo_list.append(edit_content_photo)  # add photo object to the photo list
    edit_content_label = Button(generate_window, image=edit_content_photo, borderwidth=0, highlightthickness=0,
                                bg='#F8BC3B', activebackground='#F8BC3B', command=edit_content_page, state="disabled")
    edit_content_label.place(x=900, y=665)

    # Disable generate window resizing
    generate_window.resizable(False, False)
# ________________________________________________________________________________


def funct_toggle_start_button():  # Function for toggling start button

    global start_button  # Retrieve start button

    # Bring back window 1
    app.deiconify()

    def on_button_click():
        # First command
        start_window.deiconify()

        # Second command
        app.withdraw()

    # Assign the new function as the button's command
    start_button.config(state="normal", command=on_button_click)

    start_window.withdraw()  # Hide start window
# ________________________________________________________________________________


def title_window():  # Window to get author and title data // Window 2

    # Hide window 1
    app.withdraw()

    global start_window  # Globalize to be destroyed at the opening of the main operating window

    # Window 2 config start / ctk window / Initiate generate window's tk GUI
    start_window = tk.Toplevel(app)
    start_window.title("Generate Cover Page")

    # This code will pop up the window how to in top level
    start_window.geometry("1832x932")
    center_window(start_window, 1832, 932)
    start_window.configure(bg="#F9F4F1")

    # Disable the Close Window Control Icon in start window
    start_window.protocol("WM_DELETE_WINDOW", disable_event)

    global start_button  # Recall start button
    if start_window.winfo_exists():  # Check if start window is open
        # Disable the start button
        start_button.config(state="disabled")

    # The variable that stores the textbox object for naming the storybook
    global prompt_pdf

    # Variable that stores the author's name
    global author_name

    # Tkinter UI for the textbox prompts for the storybook file
    # For Title Label
    ltext_title = ctk.CTkLabel(start_window, height=20, width=20, text="Title", font=(
        "Supersonic Rocketship", 38 * -1), text_color="#AB7A11")
    ltext_title.place(x=218, y=125)

    # For Title Textbox
    prompt_pdf = ctk.CTkEntry(start_window, height=85, width=729, font=(
        "Supersonic Rocketship", 20), text_color="black", fg_color="white", border_width=10, border_color="#DDC8A0")
    prompt_pdf.place(x=201.0, y=180.0)

    # For Author Label
    ltext_authname = ctk.CTkLabel(start_window, height=20, width=20, text="Author Name", font=(
        "Supersonic Rocketship", 38 * -1), text_color="#AB7A11")
    ltext_authname.place(x=218, y=295)

    # For Author Textbox
    author_name = ctk.CTkEntry(start_window, width=729.0, height=85.0, bg_color="#F9F4F1", font=(
        "Supersonic Rocketship", 20), text_color="black", fg_color="white", border_width=10, border_color="#DDC8A0")
    author_name.place(x=201.0, y=350.0)

    # Generate button for Cover img generator
    covergen_photo = ImageTk.PhotoImage(
        Image.open('./Assets/frame0/Generate Button.png'))
    photo_list.append(covergen_photo)  # add photo object to the list
    covergen_label = Button(start_window, image=covergen_photo, borderwidth=0,
                            highlightthickness=0, command=generate_cover_image)
    covergen_label.place(x=201, y=750)  # y=750

    global lmain_cover  # Globalize cover label frame holder
    global ltext_cover  # Globalize text label frame holder

    # For prompt Title Label for cover image
    prompt_title = ctk.CTkLabel(start_window, height=20, width=20, text="Enter prompt for Cover Image", font=(
        "Supersonic Rocketship", 38 * -1), text_color="#AB7A11")
    prompt_title.place(x=218, y=465)

    # For prompt Title Label for cover image
    prompt_title_max = ctk.CTkLabel(start_window, height=20, width=20, text="(120 characters max)", font=(
        "Supersonic Rocketship", 18 * -1), text_color="#AB7A11")
    prompt_title_max.place(x=765, y=490)

    # Tkinter UI for the textbox prompt for the cover img
    # cover_prompt = ctk.CTkEntry(start_window, width=729.0, height=185.0, bg_color="#F9F4F1", font=(
    #     "Supersonic Rocketship", 20), text_color="black", fg_color="white", border_width=10, border_color="#DDC8A0")
    # cover_prompt.place(x=201.0, y=520.0)

    global prompt_area  # Globalize the widget containing the text input from the user

    # Create a Frame widget with the desired border color
    border_frame = tk.Frame(start_window, bg="#DDC8A0", bd=10)
    border_frame.place(x=201, y=520)

    # Tkinter UI for the textbox prompt for the cover img
    prompt_area = tk.Text(border_frame, height=5, width=52,
                          bg='white', font=("Supersonic Rocketship", 20))
    # Use pack() to fill the available space within the Frame
    prompt_area.pack(fill='both', expand=True)

    # For Cover image generated Label
    coverimglab = ctk.CTkLabel(start_window, height=20, width=20, text="Cover Image", font=(
        "Supersonic Rocketship", 48 * -1), text_color="#AB7A11")
    coverimglab.place(x=1185, y=115)

    # Placeholder frame for image result generated for cover image
    lmain_cover = tk.Label(start_window)
    lmain_cover.place(x=1180, y=183)

    # Placeholder frame for the text input for cover image
    ltext_cover = ctk.CTkLabel(start_window, height=100, width=512, text=" \n".join(textwrap.wrap(
        glob_title, width=10)), font=(
        "Supersonic Rocketship", 20), text_color="#AB7A11", fg_color=None, wraplength=500)
    ltext_cover.place(x=1182, y=650)

    # Back button in window 2 // Start Window
    # Globalize this back button to call it to a function
    global back_label_start_window
    back_photo_start_window = ImageTk.PhotoImage(
        Image.open('./Assets/backbutton.png'))
    photo_list.append(back_photo_start_window)  # add photo object to the list
    back_label_start_window = Button(start_window, borderwidth=0, highlightthickness=0,
                                     image=back_photo_start_window, command=funct_toggle_start_button)
    back_label_start_window.place(x=100, y=50, anchor="n")

    # called the 2 different icon which is on and off
    realisticOn_icon = ImageTk.PhotoImage(
        Image.open('./Assets/realisticOn.png'))
    realisticOff_icon = ImageTk.PhotoImage(
        Image.open('./Assets/realisticOff.png'))

    photo_list.extend([realisticOn_icon, realisticOff_icon]
                      )  # add photo objects to the list

    # Switch function to check if on and off
    def funct_realistic_switch():

        global enable_realistic  # Recall global variable enable_realistic

        if enable_realistic == 0:  # To check if button state is off

            funct_realistic_on()    # Enable realistic content

            # change the image to on (teddy with slash)
            realistic_button['image'] = realisticOn_icon

        else:   # Check the button state is on

            funct_realistic_off()    # Disable realistic content

            # change the image to off (teddy with no slash)
            realistic_button['image'] = realisticOff_icon

    # Button for realisitc
    realistic_button = Button(start_window, image=realisticOff_icon, borderwidth=0,
                              highlightthickness=0, command=funct_realistic_switch)  # Called the funct_realistic_switch
    realistic_button.place(x=70, y=200)

    global okay_label  # global to be called in generate_cover image function
    # Ok button to accepts the data and goes to window 3
    okay_photo = ImageTk.PhotoImage(Image.open('./Assets/OkButton.png'))
    photo_list.append(okay_photo)  # add photo object to the list
    okay_label = Button(start_window, borderwidth=0, highlightthickness=0,
                        image=okay_photo, command=funct_get_cover_data, state="disabled")  # disable if theres no cover image
    okay_label.place(x=1600, y=750, anchor="n")  # y=750

    # Disable title window resizing
    start_window.resizable(False, False)

    # Loop this window so its data can be passed later on for pdf generation
    start_window.mainloop()
# ________________________________________________________________________________


def start_window_deposit():  # Function called when pressing back button in main operating window

    # Show the hidden start window again
    start_window.deiconify()

    # Destroy the edit content page
    main_screen.withdraw()
# ________________________________________________________________________________


def main_operating_screen():  # Main Operating Screen where the text and image pages generated by the user are displayed like a cart // Window 3

    start_window.withdraw()  # Hide start window

    global main_screen  # Globalize the value of main_screen

    # Initiate main operating screen window's tk GUI
    main_screen = tk.Toplevel(start_window)
    main_screen.title("Main Operating Screen")

    # This code will pop up the window how to in top level
    main_screen.geometry("1832x932")
    center_window(main_screen, 1832, 932)
    main_screen.configure(bg='#F9F4F1')

    # Disable the Close Window Control Icon in main operating screen
    main_screen.protocol("WM_DELETE_WINDOW", disable_event)

    # First declaration of global update value
    global update_value

    # First instance of update value to have the value None to define it in generate save function
    update_value = None

    ################################################# SCROLL BAR CODE #####################################################

    # create a new frame to hold the canvas and scrollbar
    main_frame = Frame(main_screen)
    # make the frame fill the entire main_screen window
    main_frame.pack(fill='both', expand=1)

    global canvas  # Globalize canvas to pass to Main operating window

    # create a new canvas widget and add it to the main_frame
    canvas = Canvas(main_frame)
    # set the background color of the canvas
    canvas.configure(bg="#F9F4F1")
    # make the canvas fill the entire main_frame
    canvas.pack(side='top', fill='both', expand=1)

    scrollbar = ttk.Scrollbar(     # create a new vertical scrollbar widget
        main_frame, orient='horizontal', command=canvas.xview)
    # place the scrollbar on the right side of the main_frame
    scrollbar.pack(side='bottom', fill='x')

    # configure the canvas to scroll using the scrollbar
    canvas.configure(xscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(  # bind the <Configure> event to the canvas and update the scroll region when the canvas is resized
        scrollregion=canvas.bbox('all')))

    # create a new frame to hold the widgets inside the canvas
    global inner_frame
    inner_frame = Frame(canvas)
    # set the background color of the inner frame
    inner_frame.configure(bg="#F9F4F1")
    canvas.create_window((0, 0), window=inner_frame, anchor='center')

    # Update the widgets
    funct_inner_frame()

    #########################################################################################################################

    # Back button in Window 3 / Main Operating Screen
    back_photo_main_screen = ImageTk.PhotoImage(
        Image.open('./Assets/backbutton.png'))
    photo_list.append(back_photo_main_screen)  # add photo object to the list
    back_label_main_screen = Button(main_screen, borderwidth=0, highlightthickness=0,
                                    image=back_photo_main_screen, command=start_window_deposit)
    back_label_main_screen.place(x=100, y=50, anchor="n")

    # Get the prompt text in title window that contains the storybook title
    pictales_title = tk.Label(main_screen, text="\n".join(textwrap.wrap(
        glob_title, width=70)), font=custom_font, fg='#F8BC3B', bg='#F9F4F1', justify='right')
    pictales_title.place(x=200, y=60)
    pictales_title.config(font=("Supersonic Rocketship", 28))

    # Add page button
    addpage_photo = ImageTk.PhotoImage(Image.open('./Assets/addpage.png'))
    photo_list.append(addpage_photo)  # add photo object to the list
    addpage_label = Button(main_screen, borderwidth=0,
                           highlightthickness=0, image=addpage_photo, command=funct_generate_window, bg='#F9F4F1', activebackground='#F9F4F1')
    addpage_label.place(x=100, y=780)

    # Redirecting to modal window for Generating image // Create Pictales button in window 3
    createpictales_photo = ImageTk.PhotoImage(
        Image.open('./Assets/createpictales.png'))
    photo_list.append(createpictales_photo)  # add photo object to the list
    createpictales_label = Button(main_screen, borderwidth=0,
                                  highlightthickness=0, image=createpictales_photo, command=funct_clarification_window)  # show the prompt creation of pdf
    createpictales_label.place(x=375, y=780)

    # Disable main operating screen window resizing
    main_screen.resizable(False, False)
# ________________________________________________________________________________


def funct_clarification_window():  # Clarification Window pops up before creating the pictales pdf window 5

    global clarification_window  # globallize the value of clarification

    # Initiate clarification window's tk GUI
    clarification_window = tk.Toplevel()
    clarification_window.title('Are you sure?')

    # This code will pop up the window how to in top level
    clarification_window.grab_set()

    center_window(clarification_window, 690, 603)
    clarification_window.configure(bg='#F8BC3B')  # set background color

    # Set the clarification label on the window
    clear_label = tk.Label(clarification_window, text='ARE YOU SURE TO \n REDISCOVER YOUR STORY AND \n CREATE YOUR OWN PICTALES?',
                           font=custom_font, fg='white', bg='#F8BC3B')
    clear_label.place(x=40, y=50)

    # set the font of the label to Supersonic Rocketship with a size of 20
    clear_label.config(font=("Supersonic Rocketship", 34))

    # X Button // Close the clarification window
    close_photo = ImageTk.PhotoImage(
        Image.open('./Assets/window2/x Button.png'))
    photo_list.append(close_photo)  # add photo object to the list
    no_button = Button(clarification_window, image=close_photo, command=clarification_window.destroy,
                       background='#F8BC3B', borderwidth=0, highlightthickness=0, activebackground='#F8BC3B')
    no_button.place(x=200, y=400)

    # Check Button // Generate PDF File
    open_photo = ImageTk.PhotoImage(
        Image.open('./Assets/window2/check button.png'))
    photo_list.append(open_photo)  # add photo object to the list
    yes_button = Button(clarification_window, image=open_photo, command=generate_pdf,
                        background='#F8BC3B', borderwidth=0, highlightthickness=0, activebackground='#F8BC3B')
    yes_button.place(x=400, y=400)

    # Disable clarification window resizing
    clarification_window.resizable(False, False)
# ________________________________________________________________________________


def on_enter_main(e, hover_photo, char_key):  # For main on hover effect
    if (char_key == 1):
        boy_label['image'] = hover_photo
    elif (char_key == 2):
        girl_label['image'] = hover_photo
    elif (char_key == 3):
        dog_label['image'] = hover_photo
# ________________________________________________________________________________


def on_leave_main(e, photo, char_key):  # For main off hover effect
    if (char_key == 1):
        boy_label['image'] = photo
    elif (char_key == 2):
        girl_label['image'] = photo
    elif (char_key == 3):
        dog_label['image'] = photo
# ________________________________________________________________________________


def funct_char_select(char_value):  # Function for getting the character selected

    global char_select  # Globalize the value of character selection

    char_select = char_value    # Get the value passed from addcharacter screen

    # Call the character expression window to select the selected character's expressions
    character_expression_window()
# ________________________________________________________________________________


def generate_window_deposit():  # Function called when pressing back button or generating a save page in generate window

    # Show the hidden generate window again
    generate_window.deiconify()

    # Destroy the edit content page
    addcharacter_screen.destroy()
# ________________________________________________________________________________


def edit_content_page():  # Add edit the page content window 5.1 // ADD STORY WINDOW

    # Hide generate window when in edit content page
    generate_window.withdraw()

    # Globalize edit content page to destroy it later in generate save function
    global addcharacter_screen

    # Globalize Flag for main_char_select to detect if add story button was clicked
    global main_char_select

    # Set the flag to 9 since there is no designated character at value 9 to mimic the button being clicked
    main_char_select = 9

    # Initiate edit content page window's tk GUI
    addcharacter_screen = tk.Toplevel()
    addcharacter_screen.title("Edit Content Page")

    # This code will pop up the window how to in top level
    addcharacter_screen.grab_set()
    addcharacter_screen.geometry("1832x932")
    center_window(addcharacter_screen, 1832, 932)
    addcharacter_screen.configure(bg='#F8BC3B')

    # Disable the Close Window Control Icon in edit content page
    addcharacter_screen.protocol("WM_DELETE_WINDOW", disable_event)

    # Back button for add character window 5.1
    back_photo_edit_content = ImageTk.PhotoImage(
        Image.open('./Assets/backbutton.png'))
    photo_list.append(back_photo_edit_content)  # add photo object to the list
    back_label_edit_content = Button(addcharacter_screen, borderwidth=0, highlightthickness=0, image=back_photo_edit_content,
                                     command=generate_window_deposit, bg='#F8BC3B', activebackground='#F8BC3B')
    back_label_edit_content.place(x=100, y=50, anchor="n")

    ############################## Preview Code ##############################
    # Show the selected character from the 8 expressions:
    preview_label = tk.Label(
        addcharacter_screen, text='Preview:', font=custom_font, fg='white', bg='#F8BC3B')
    preview_label.place(x=600, y=500)
    # Set the font of the label to Supersonic Rocketship with a size of 15
    preview_label.config(font=("Supersonic Rocketship", 15))

    # This block of code show the logo PICTALES and resize it, and append the image to be seen coz of resizing
    preview_img = Image.open('./GeneratedImages/Preview.png')
    resized_preview_img = preview_img.resize(
        (350, 350), resample=Image.LANCZOS)
    preview_photo = ImageTk.PhotoImage(resized_preview_img)
    # MAGIC APPEND
    photo_list.append(preview_photo)  # add photo object to the photo list

    # Show the image preview in a container
    preview_label_photo = tk.Label(
        addcharacter_screen, bg='#F8BC3B', image=preview_photo)
    preview_label_photo.place(x=500, y=550)
    ##############################              ##############################

    # Show the selected character from the 8 expressions:
    selected_character_label = tk.Label(
        addcharacter_screen, text='Selected Character:', font=custom_font, fg='white', bg='#F8BC3B')
    selected_character_label.place(x=200, y=500)

    # Set the font of the label to Supersonic Rocketship with a size of 15
    selected_character_label.config(font=("Supersonic Rocketship", 15))

    # Globalize the container for the selected character that will appear in the edit content page
    global selected_character_photo

    # Show the image in a container
    selected_character_photo = tk.Label(addcharacter_screen, bg='#F8BC3B')
    selected_character_photo.place(x=230, y=600)

    # Character label to choose charcter
    character_label = tk.Label(
        addcharacter_screen, text='CHOOSE YOUR CHARACTER: CLICK ON THE \n CHARACTER YOU WANT', font=custom_font, fg='white', bg='#F8BC3B')
    character_label.place(x=180, y=50)

    # Set the font of the character label to Supersonic Rocketship with a size of 25
    character_label.config(font=("Supersonic Rocketship", 25))

    # Label for edit page content
    edit_prompt = Label(addcharacter_screen,
                        text="Enter your story here (120 characters max): ", bg='#F8BC3B', fg='white')
    edit_prompt.place(x=900, y=110)
    edit_prompt.config(font=("Supersonic Rocketship", 18))

    global edit_textcontent_area  # Globalize to pass to generate save with get() method

    # Edit textbox widget for editing the content of the story page
    edit_textcontent_area = tk.Text(addcharacter_screen, height=16, width=62,
                                    bg='#F8BC3B',  bd=1, relief="solid", font=("Supersonic Rocketship", 20))
    edit_textcontent_area.place(x=900, y=150)

    # BOY character Screen window 5.1
    boy_photo = ImageTk.PhotoImage(Image.open('./Assets/boy_normal_small.png'))
    photo_list.append(boy_photo)  # add photo object to the list

    # Boy hover img config
    boy_hover_img = Image.open('./Assets/boy_happy_small.png')
    boy_hover_photo = ImageTk.PhotoImage(boy_hover_img)

    # Button configs
    # .bind binds an event on the button
    global boy_label
    boy_label = Button(addcharacter_screen, borderwidth=0, highlightthickness=0,
                       image=boy_photo, command=lambda: funct_char_select(1), bg='#F8BC3B', activebackground='#F8BC3B')
    boy_label.place(x=500, y=200, anchor="n")

    # Hovering effect on boy button/image
    boy_label.bind("<Enter>", lambda e: on_enter_main(e, boy_hover_photo, 1))
    boy_label.bind("<Leave>", lambda e: on_leave_main(e, boy_photo, 1))

    # Girl character Screen window 5.1
    girl_photo = ImageTk.PhotoImage(
        Image.open('./Assets/girl_normal_small.png'))
    photo_list.append(girl_photo)  # add photo object to the list
    # Girl hover img config
    girl_hover_photo = ImageTk.PhotoImage(
        Image.open('./Assets/girl_happy_small.png'))

    # Button configs
    # .bind binds an event on the button
    global girl_label
    girl_label = Button(addcharacter_screen, borderwidth=0, highlightthickness=0,
                        image=girl_photo, command=lambda: funct_char_select(2), bg='#F8BC3B', activebackground='#F8BC3B')
    girl_label.place(x=300, y=200, anchor="n")

    # Hovering effect on girl button/image
    girl_label.bind("<Enter>", lambda e: on_enter_main(e, girl_hover_photo, 2))
    girl_label.bind("<Leave>", lambda e: on_leave_main(e, girl_photo, 2))

    # DOG character Screen window 5.1
    dog_photo = ImageTk.PhotoImage(Image.open('./Assets/dog_normal_small.png'))
    photo_list.append(dog_photo)  # add photo object to the list
    # Dog hover img config
    dog_hover_img = Image.open('./Assets/dog_happy_small.png')
    dog_hover_photo = ImageTk.PhotoImage(dog_hover_img)

    # Button configs
    # .bind binds an event on the button
    global dog_label
    dog_label = Button(addcharacter_screen, borderwidth=0, highlightthickness=0,
                       image=dog_photo, command=lambda: funct_char_select(3), bg='#F8BC3B', activebackground='#F8BC3B')
    dog_label.place(x=700, y=220, anchor="n")

    # Hovering effect on dog button/image
    dog_label.bind("<Enter>", lambda e: on_enter_main(e, dog_hover_photo, 3))
    dog_label.bind("<Leave>", lambda e: on_leave_main(e, dog_photo, 3))

    # Save content button (SAVES THE IMAGE WITH THE CHARACTER AND THE CONTENT)
    save_photo_with_char = ImageTk.PhotoImage(
        Image.open('./Assets/frame0/save.png'))
    photo_list.append(save_photo_with_char)  # add photo object to the list
    save_label = Button(addcharacter_screen, image=save_photo_with_char, borderwidth=0, highlightthickness=0,
                        bg='#F8BC3B', activebackground='#F8BC3B', command=generate_save)
    save_label.place(x=1250, y=800)

    addcharacter_screen.resizable(False, False)
# ________________________________________________________________________________


def addcharacter_screen_deposit():  # Function called when pressing back button or selecting a character in character expression window

    # Show the hidden edit content page again
    addcharacter_screen.deiconify()

    # Destroy the character expression window
    character_screen.destroy()
# ________________________________________________________________________________


def character_expression_window():  # Choosing expression window

    # Hide edit content page when in expression window
    addcharacter_screen.withdraw()

    # Globalize the screen to destroy it later on selection in funct_main_char_select
    global character_screen

    # Initiate character expression window's tk GUI
    character_screen = tk.Toplevel()
    character_screen.title("Character Expressions")

    # This code will pop up the window how to in top level
    character_screen.grab_set()
    character_screen.geometry("1228x600")
    center_window(character_screen, 1228, 600)
    character_screen.configure(bg='#F8BC3B')

    # Disable the Close Window Control Icon in edit character expression window
    character_screen.protocol("WM_DELETE_WINDOW", disable_event)

    # Get the character data from the global variable and function
    if (char_select == 1):
        char_name = "boy"
    elif (char_select == 2):
        char_name = "girl"
    elif (char_select == 3):
        char_name = "dog"

    # Back button on character_screen
    back_photo_character_screen = ImageTk.PhotoImage(
        Image.open('./Assets/backbutton.png'))
    # add photo object to the list
    photo_list.append(back_photo_character_screen)
    back_label_character_screen = Button(character_screen, borderwidth=0, highlightthickness=0, image=back_photo_character_screen,
                                         command=addcharacter_screen_deposit, bg='#F8BC3B', activebackground='#F8BC3B')
    back_label_character_screen.place(x=100, y=50, anchor="n")

    # Label to choose which emotion to include in the generated image
    character1_label = tk.Label(
        character_screen, text='WHAT DOES YOUR CHARACTER FEEL?', font=custom_font, fg='white', bg='#F8BC3B')
    character1_label.place(x=350, y=50)
    # set the font of the label to Supersonic Rocketship with a size of 35
    character1_label.config(font=("Supersonic Rocketship", 35))

    def on_enter(e, bg_color):  # Mouse on button hover effect
        e.widget['background'] = bg_color

    def on_leave(e):           # Mouse off button hover effect
        e.widget['background'] = '#F8BC3B'

    # Character expression 1 widget
    char1_photo = ImageTk.PhotoImage(Image.open(
        './Assets/{}_happy_small.png'.format(char_name)))  # Happy emotion option
    photo_list.append(char1_photo)
    char1_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char1_photo,
                         command=lambda: funct_main_char_select(1, char1_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char1_label.place(x=400, y=150, anchor="n")
    char1_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char1_label.bind("<Leave>", on_leave)

    # Character expression 2 widget
    char2_photo = ImageTk.PhotoImage(Image.open(
        './Assets/{}_sad_small.png'.format(char_name)))  # Sad emotion option
    photo_list.append(char2_photo)
    char2_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char2_photo,
                         command=lambda: funct_main_char_select(2, char2_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char2_label.place(x=600, y=150, anchor="n")
    char2_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char2_label.bind("<Leave>", on_leave)

    # Character expression 3 widget
    char3_photo = ImageTk.PhotoImage(Image.open(
        './Assets/{}_angry_small.png'.format(char_name)))  # Angry emotion option
    photo_list.append(char3_photo)  # add photo object to the list
    char3_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char3_photo,
                         command=lambda: funct_main_char_select(3, char3_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char3_label.place(x=800, y=150, anchor="n")
    char3_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char3_label.bind("<Leave>", on_leave)

    # Character expression 4 widget
    char4_photo = ImageTk.PhotoImage(
        Image.open('./Assets/{}_surprised_small.png'.format(char_name)))  # Surprised emotion option
    photo_list.append(char4_photo)  # add photo object to the list
    char4_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char4_photo,
                         command=lambda: funct_main_char_select(4, char4_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char4_label.place(x=1000, y=150, anchor="n")
    char4_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char4_label.bind("<Leave>", on_leave)

    # Character expression 5 widget
    char5_photo = ImageTk.PhotoImage(Image.open(
        './Assets/{}_normal_small.png'.format(char_name)))  # Smile emotion option
    photo_list.append(char5_photo)  # add photo object to the list
    char5_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char5_photo,
                         command=lambda: funct_main_char_select(5, char5_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char5_label.place(x=400, y=350, anchor="n")
    char5_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char5_label.bind("<Leave>", on_leave)

    # Character expression 6 widget
    char6_photo = ImageTk.PhotoImage(Image.open(
        './Assets/{}_confused_small.png'.format(char_name)))  # Confused emotion option
    photo_list.append(char6_photo)  # add photo object to the list
    char6_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char6_photo,
                         command=lambda: funct_main_char_select(6, char6_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char6_label.place(x=600, y=350, anchor="n")
    char6_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char6_label.bind("<Leave>", on_leave)

    # Character expression 7 widget
    char7_photo = ImageTk.PhotoImage(Image.open(
        './Assets/{}_disgust_small.png'.format(char_name)))  # Disgust emotion option
    photo_list.append(char7_photo)  # add photo object to the list
    char7_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char7_photo,
                         command=lambda: funct_main_char_select(7, char7_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char7_label.place(x=800, y=350, anchor="n")
    char7_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char7_label.bind("<Leave>", on_leave)

    # Character expression 8 widget
    char8_photo = ImageTk.PhotoImage(Image.open(
        './Assets/{}_fear_small.png'.format(char_name)))  # Fear emotion option
    photo_list.append(char8_photo)  # add photo object to the list
    char8_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char8_photo,
                         command=lambda: funct_main_char_select(8, char8_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char8_label.place(x=1000, y=350, anchor="n")
    char8_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char8_label.bind("<Leave>", on_leave)

    # Disable character screen resizing
    character_screen.resizable(False, False)


# ___________________________________________________________________________ MAIN TKINTER UI ___________________________________________________________________________
# Create the app
app = ctk.CTk()
app.title("PicTales")
app.geometry("1832x932")
center_window(app, 1832, 932)
ctk.set_appearance_mode("F9F4F1")


def disable_event():  # Functionn for disabling the command close window for specific tk windows
    pass
# ________________________________________________________________________________


# Play background music
funct_play_music()

# Globalize the value of character selection WITH the expressions
main_char_select = 0

# Store the character in a photo image variable
character = ImageTk.PhotoImage(blank)  # Set no character as default

# Set background of window 1
bg_img_photo = ImageTk.PhotoImage(Image.open('./Assets/AppBG.png'))
bg_img_label = Label(app, image=bg_img_photo)
bg_img_label.place(x=0, y=0)

# Load and display the logo image on the canvas in window 1
logo_photo = ImageTk.PhotoImage(Image.open('./Assets/frame0/image_1.png'))
logo_label = Label(app, image=logo_photo, bg='#F9F4F1')
logo_label.place(x=800, y=90)

# load and display start button
start_photo = ImageTk.PhotoImage(
    Image.open('./Assets/frame0/button_3.png'))
start_button = Button(app, image=start_photo, borderwidth=0,
                      highlightthickness=0, command=title_window)
start_button.place(x=770, y=530)

# load and display howto button
howTo_photo = ImageTk.PhotoImage(Image.open('./Assets/frame0/button_2.png'))
howTo_button = Button(app, image=howTo_photo, borderwidth=0,
                      highlightthickness=0, command=funct_howTo_window)
howTo_button.place(x=770, y=690)

# Question Mark in Window 1 / Main Window
about_icon = ImageTk.PhotoImage(Image.open('./Assets/frame0/button_1.png'))
photo_list.append(about_icon)  # add photo object to the list
about_button = Button(app, image=about_icon, borderwidth=0,
                      highlightthickness=0, command=funct_about_window)
about_button.place(x=50, y=50)

# Toggle Sound button in Window 1 / Main Window
musicOn_icon = ImageTk.PhotoImage(Image.open('./Assets/ButtonmusicOn.png'))
musicOff_icon = ImageTk.PhotoImage(Image.open('./Assets/ButtonmusicOff.png'))
# add photo objects to the list
photo_list.append([musicOn_icon, musicOff_icon])

# Play Sound button in Window 1 / Main Window
music_button = Button(app, image=musicOn_icon, borderwidth=0,
                      highlightthickness=0, command=toggle_music)
music_button.place(x=50, y=180)

# Disable the main widget's resizing
app.resizable(False, False)
# ___________________________________________________________________________ DRIVER CODE ___________________________________________________________________________
# Get text input prompts again by automatically restarting the app
app.mainloop()
