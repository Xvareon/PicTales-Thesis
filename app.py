# Python packages and dependencies are needed for the application to run. Installed through PIP in VSCode terminal (Todo: automatically install these with the app with PyInstaller)

#########################################################
# TO-DO LIST FOR THE BREAK:

# Auto Install # !!!PRIORITY!!!
# Checks for same image names
# Loading window when generating image/cover image
# PicTales for adults which disables cartoon input but still filters out bad data/harmful inputs/outputs
# Cute size some windows
# Check for grabbing windows, will break the program
#########################################################

# ___________________________________________________________________________ DEPENDENCIES ___________________________________________________________________________
# Import Tkinter for Python UI
import tkinter as tk
from tkinter import ttk
from tkVideoPlayer import TkinterVideo
# Import Tkinter modules for buttons, labels, additional GUI
from tkinter import Label, Button, Canvas, Frame, messagebox

# Import Tkinter module for video
import pygame
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

image_list = []     # ARRAY OF IMAGES
text_list = []      # ARRAY OF TEXT INPUTS
content_list = []   # ARRAY OF PAGE CONTENT (mostly the text)
pdf_list = []       # ARRAY OF PDF PAGES

photo_list = []     # create a global list to store photo objects for GUI

# ___________________________________________________________________________ MODEL ___________________________________________________________________________

# Loads the model
model = torch.load('./results/model-1.pt')

# ___________________________________________________________________________ FUNCTIONS ___________________________________________________________________________


def funct_play_music():
    # Initialize sound player
    pygame.mixer.init()
    # Play sound (converted mp4 to mp3 video of to video)
    pygame.mixer.music.load("./Assets/PicTalesBGsound.mp3")
    # Loop it indefinitely
    pygame.mixer.music.play(loops=-1)


def funct_stop_music():
    pygame.mixer.music.stop()


def generate_image():   # Function to generate the images from the text prompt

    global img          # For storing the image to avoid garbage collection

    global text_input   # For storing the text input to transfer to the Picture Book PDF

    global image        # For storing image to be saved if save image button is clicked

    # Uses the GPU to process the dataset through the model and get the image result
    with autocast(device):

        # Store text input in a variable
        # text_input = text_area.get()
        text_input = text_area.get('1.0', tk.END)
        text_input = text_input.strip()

        # Catch error if no text input is given
        if len(text_input) == 0 or text_input.isspace() == True:
            image = blank
            # Disable the add character button if no input is given
            edit_content_label.config(state="disabled")
            # Disable the save button if no input is given
            save_label.config(state="disabled")
        else:
            # (COMMENT OUT THIS LINE) FOR USING GUI WITHOUT AI TESTING ONLY!
            # image = blank
            cartoon_input = "cartoonish " + text_input
            # Variable that contains the image result
            image = pipe(cartoon_input, guidance_scale=10)[
                "images"][0]
            # Enable the add character button if the image is generated successfully
            edit_content_label.config(state="normal")
            # Enable the save button in generate window if the image is generated successfully
            save_label.config(state="normal")

    # Store image in a variable
    img = ImageTk.PhotoImage(image)

    # Displays the text input in the Tkinter UI after generation
    # ltext.configure(text=text_input)
    # ltext.update()

    # # Displays the image in the Tkinter UI after generation
    lmain.configure(image=img)
    lmain.update()

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

    print("main value (1-8):", main_char_select)  # PLACEHOLDER LINE

    # Update the image for the select character window (1-3)
    selected_character_photo.configure(image=character)
    selected_character_photo.update()

    # Destroy the character expression screen
    character_screen.destroy()


def generate_save():    # Saves the image in the current directory and displays the current images selected for the picture book

    # Check if user has already generated an image first before saving.
    try:
        image
    except NameError:   # If variable image is empty, return false
        is_generated = False
    else:               # If image variable is defined
        is_generated = True

    # If an image has been generated
    if is_generated:

        # Globalize content variable that stores the edited content
        global content

        # Store the base image on which the character would be pasted on
        global base

        # Save image file name as PNG based on text input
        # Strip the text input to remove the newline at the end of the data.
        image.save('./GeneratedImages/{}.png'.format(text_input))

        ##################################################################
        # If a character has been chosen
        if main_char_select > 0:
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

            # Save the result image to disk
            result.save('./GeneratedImages/{}.png'.format(text_input))

            img = ImageTk.PhotoImage(result)
            content = edit_textcontent_area.get('1.0', tk.END)

        ##################################################################

        i = 0  # Instantiate i for loops (text item positioning)
        j = 0  # Instantiate j for loops (pic positioning)

        # Store image in image variable if no character is selected and store it in base variable if a character is selected (For previews)
        if main_char_select == 0:
            img = ImageTk.PhotoImage(image)
            content = text_input

        # Makes the text input as a default content input if the user did not enter anything at the content textbox.
        if (content == '' or len(content) == 0 or content.isspace() == True):
            content = text_input

        # Add the content to the list
        content_list.append(content)

        # Add the previously stored text in a list
        text_list.append(text_input)

        # Store previous image in a list
        image_list.append(img)

        ############# MAIN OPERATING SCREEN IMAGES ADDED SO FAR IN FOR LOOP #############

        # create a list to hold the labels for each item
        label_list = []

        # Displays the text and image list in the main operating window
        counter = 0

        for text_item, pic in zip(content_list, image_list):

            counter += 1

            # remove the previous labels from the window
            for label in label_list:
                label.pack_forget()
            label_list = []

            ltext_list = Label(inner_frame, height=10, width=50, text="\n".join(textwrap.wrap(text_item, width=50)), font=(
                "Arial", 16), fg="#AB7A11", bg="#F9F4F1")
            # ltext_list = Label(inner_frame, height=10, width=70, text=text_item, font=(
            #     "Arial", 12), fg="#AB7A11", bg="#F9F4F1")
            # ltext_list.pack(side = 'right')
            ltext_list.grid(row=counter-1, column=0, padx=20,
                            pady=10, ipadx=10, ipady=150, sticky='n')
            label_list.append(ltext_list)

            limg_list = Label(inner_frame, image=pic, bg="#F9F4F1")
            # limg_list.pack(side = 'right')
            limg_list.grid(row=counter-1, column=1, padx=20,
                           pady=10, ipadx=10, ipady=80, sticky='n')
            label_list.append(limg_list)

            # update the scroll region of the canvas
            canvas.update_idletasks()
            canvas.config(scrollregion=canvas.bbox('all'))

        ###########################################################################################

        # Destroy the edit content window and generate window
        # Check if there is a widget named addcharacter_screen.
        try:
            addcharacter_screen
        except NameError:   # If variable addcharacter_screen is empty, return false
            is_window_open = False
        else:               # If addcharacter_screen variable is defined
            is_window_open = True

        # If an image has been generated
        if is_window_open:
            addcharacter_screen.destroy()
        generate_window.destroy()


def generate_cover_image():   # Function to generate the images from the text prompt

    global img_cover          # For storing the image to avoid garbage collection

    global cover_input   # For storing the text input to transfer to the Picture Book PDF

    global image_cover  # Globalizes cover image variable

    # Uses the GPU to process the dataset through the model and get the image result
    with autocast(device):

        # Store text input in a variable
        cover_input = cover_prompt.get()

        # Catch error if no text input is given
        if len(cover_input) == 0 or cover_input.isspace() == True:
            image_cover = blank
            # Disable the button if no input is given
            okay_label.config(state="disabled")
        else:
            # image_cover = blank
            cartoon_input = "cartoonish " + cover_input
            # Variable that contains the image result
            image_cover = pipe(cartoon_input, guidance_scale=10)[
                "images"][0]
            # Enable the button if the image is generated successfully
            okay_label.config(state="normal")
    # Store image in a variable
    img_cover = ImageTk.PhotoImage(image_cover)

    # Displays the text input in the Tkinter UI after generation
    ltext_cover.configure(text=cover_input)
    ltext_cover.update()

    # Displays the image in the Tkinter UI after generation
    lmain_cover.configure(image=img_cover)
    lmain_cover.update()


def generate_pdf():                 # Generate PicTale Story book

    pdf_name = prompt_pdf.get()    # Store text input in a variable, from the pdf window

    # Store current time in a variable
    now = datetime.datetime.now()

    # Store the pdf file name into a variable, sets this as default for errors and etc like if the title name is not set.
    if (pdf_name == '' or len(pdf_name) == 0 or pdf_name.isspace() == True):
        pdf_name = 'PicTales'

    # Specifies the directory where the pdf will generate
    pdf_path = "./StoryBooks/{}.pdf".format(pdf_name)

    #######################################################################################

    # Save image file name as PNG based on text input
    image_cover.save('./GeneratedImages/TitlePage_{}.png'.format(pdf_name))

    # Pass image cover variable for drawing/writing the page title details
    covertext = ImageDraw.Draw(image_cover)

    # Choose font
    font = ImageFont.truetype('arial.ttf', 16)
    titlefont = ImageFont.truetype('comic.ttf', 30)

    # Set the maximum width for each line
    max_width = 15

    # Wrap the text into multiple lines based on the maximum width
    wrapped_text = textwrap.wrap(pdf_name, width=max_width)

    # Calculate the y-coordinate for the second line of text
    y_coord = 95

    # Draw each line of text with white color and increment the y-coordinate
    for line in wrapped_text:
        # Black background for anti camo in title name / pdf name
        text_width, text_height = titlefont.getsize(line)
        bbox = (150, y_coord, 150 + text_width, y_coord + text_height)
        covertext.rectangle(bbox, fill=(0, 0, 0))
        # For writing title page / pdf name input in cover page
        covertext.text((150, y_coord), line,
                       font=titlefont, fill=(255, 255, 255))
        y_coord += titlefont.getsize(line)[1] + 10

    # Black background for anti camo in author name
    bbox = covertext.textbbox((50, 380), author_name.get(), font=font)
    covertext.rectangle(bbox, fill=(0, 0, 0))
    # For writing author input in cover page
    covertext.text((50, 380), author_name.get(),
                   font=font, fill=(255, 255, 255))

    # Black background for anti camo in date created
    bbox = covertext.textbbox((50, 410), now.strftime("%m-%d-%Y"), font=font)
    covertext.rectangle(bbox, fill=(0, 0, 0))
    # For writing date created in cover page
    covertext.text((50, 410), now.strftime("%m-%d-%Y"),
                   font=font, fill=(255, 255, 255))

    # Save cover image to local directory // This has the Generated Cover Image // Page 1
    image_cover.save('./GeneratedImages/TitlePage_{}.png'.format(pdf_name))

    # Store the coverpage into an object variable // Static Image Page 2
    cover = Image.open('./Assets/CoverPage.png')

    #######################################################################################

    # Safely convert the rogue image into a pdf page
    if cover.mode == 'RGBA':
        cover = cover.convert('RGB')

    # Add the title page to page 2 of storybook
    pdf_list.append(Image.open(
        './GeneratedImages/TitlePage_{}.png'.format(pdf_name)))

    # Add the PicTales cover page (Page 2) to page 1 of storybook
    pdf_list.append(cover)

    # Pointer/Flag for content for content list access later and start at 1 so index 0 can store title page
    i = 0

    # For each image file that has been written with the text list names, the text list names their files itself based on order.
    for file in text_list:

        # Store Generated image in a variable to be used as the text background
        photo = Image.open('./GeneratedImages/{}.png'.format(file))

        # Blur the stored image
        photo = photo.filter(ImageFilter.GaussianBlur(20))

        # Invoke draw function to the blank image
        phototext = ImageDraw.Draw(photo)

        # Choose font
        font = ImageFont.truetype('arial.ttf', 16)

        # Make a rectangle background for the text
        bbox = phototext.textbbox((10, 10), content_list[i], font=font)
        phototext.rectangle(bbox, fill=(0, 0, 0))

        # Write the text input based on the designated text image
        phototext.text(
            (10, 10), content_list[i], font=font, fill=(255, 255, 255))

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
    messagebox.showinfo("Pictales", "Your PDF has been generated!")

    # Close the app when storybook is made
    app.destroy()


# ___________________________________________________________________________ CONFIGURATIONS ___________________________________________________________________________
isExist = os.path.exists('./results/model-1.pt')

if (isExist == False):
    sys.exit(0)

# loads the model used to a pre-defined library online
modelid = "CompVis/stable-diffusion-v1-4"

# # Specifies the graphics driver to be used
device = "cuda"
# device = "cpu"

# # Loads the model into torch
torch.load('./results/model-1.pt')

auth_token = "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"

# # Uses the pipe from the online library for model translation to produce the image.
pipe = StableDiffusionPipeline.from_pretrained(
    modelid, revision="fp16", torch_dtype=torch.float16, use_auth_token=auth_token)

# # # Uses the graphics driver (Must atleast be 4GB ram)
pipe.to(device)

# -----------------------------------------------------------------------------------
# Create template page for the title page image
blank = Image.new('RGB', (512, 512))
# Save template in generated images folder
blank.save('./GeneratedImages/BlankTemplate.png')
# Define the font file path and size
font_path = "./fonts/SupersonicRockets.ttf"
font_size = 24
# Create a custom font
custom_font = (font_path, font_size, "bold")
# -----------------------------------------------------------------------------------

# ABOUT WINDOW POP UP


def funct_about_window():     # the question mark button shows the about pictales modal

    # this code will pop up the window about in top level
    # the geometry with app winfo width and height will center the window modal in main screen
    about_window = tk.Toplevel(app)
    about_window.title('About Pictales')
    about_window.grab_set()
    about_window.geometry("756x653+{}+{}".format(
        app.winfo_width()//2 - 378 + app.winfo_rootx(),
        app.winfo_height()//2 - 372 + app.winfo_rooty()
    ))

    about_window.configure(bg='#F8BC3B')  # set background color

    # to show the about title
    modal_label = tk.Label(about_window, text='ABOUT',
                           font=custom_font, fg='white', bg='#F8BC3B')
    modal_label.pack(pady=50)

    # this block of code show the logo PICTALES and resize it, and append the image to be seen coz of resizing
    about_img = Image.open('./Assets/PICTALES LOGO Big w background.png')
    # resized_img = about_img.resize(
    #     (200, 200), resample=Image.LANCZOS)
    resized_img = about_img.resize(
        (200, 200), resample=Image.Resampling.LANCZOS)
    about_photo = ImageTk.PhotoImage(resized_img)

    # MAGIC APPEND
    photo_list.append(about_photo)  # add photo object to the list

    about_label = tk.Label(about_window, image=about_photo)
    about_label.place(x=380, y=165, anchor="n")

    # set the font of the label to Supersonic Rocketship with a size of 20
    modal_label.config(font=("Supersonic Rocketship", 64))

    # this code is for printing the copyright
    ver_label = tk.Label(about_window, text='Copyright © 2023, PICTALES',
                         font=custom_font, fg='white', bg='#F8BC3B')
    ver_label.place(relx=0.25, rely=0.75)
    ver_label.config(font=("Supersonic Rocketship", 24))

    # this code is for printing the version of the app
    copy_label = tk.Label(about_window, text='VER. 1.0',
                          font=custom_font, fg='white', bg='#F8BC3B')
    copy_label.pack(pady=190)
    copy_label.config(font=("Supersonic Rocketship", 24))

    about_window.resizable(False, False)

# -----------------------------------------------------------------------------------


def funct_howTo_window():     # how to button will show this window playing the video about pictales
    # this code will pop up the window how to in top level
    # the geometry with app winfo width and height will center the window modal in main screen
    global howTo_window  # Globalize to be destroyed later
    howTo_window = tk.Toplevel(app)
    howTo_window.title('How to use Pictales')
    howTo_window.grab_set()
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

    # back button of the How To
    back_photo = ImageTk.PhotoImage(
        Image.open('./Assets/inverted_backbutton.png'))
    photo_list.append(back_photo)  # add photo object to the list
    back_label = Button(howTo_window, borderwidth=0, highlightthickness=0,
                        image=back_photo, command=howTo_window.destroy, bg='#F8BC3B', activebackground='#F8BC3B')
    back_label.place(x=85, y=20, anchor="n")


def funct_generate_window():    # This window is for getting the text prompt and image generated result from that prompt

    # Globalized to be destroyed at the click of the save button in edit_content_page function
    global generate_window
    generate_window = tk.Toplevel(app)  # pop up the window how to in top level
    generate_window.title("Prompt")
    generate_window.grab_set()
    # the geometry with app winfo width and height will center the window modal in main screen
    generate_window.geometry("1228x800+{}+{}".format(
        app.winfo_width()//2 - 614 + app.winfo_rootx(),
        app.winfo_height()//2 - 369 + app.winfo_rooty()
    ))
    generate_window.configure(bg='#F8BC3B')  # set background color

    # Back button to main_operation_window
    back_photo = ImageTk.PhotoImage(
        Image.open('./Assets/inverted_backbutton.png'))
    photo_list.append(back_photo)  # add photo object to the list
    back_label = Button(generate_window, borderwidth=0, highlightthickness=0,
                        image=back_photo, command=generate_window.destroy, bg='#F8BC3B', activebackground='#F8BC3B')
    back_label.place(x=85, y=20, anchor="n")

    # Label for prompt
    text_title = Label(generate_window, text="Enter prompt here", bg='#F8BC3B')
    text_title.place(x=598, y=67)
    text_title.config(font=("Supersonic Rocketship", 18))

    global text_area  # Globalize the widget containing the text input from the user

    # Textbox widget for getting USER TEXT INPUT FOR GENERATING IMAGE
    text_area = tk.Text(generate_window, height=16, width=38,
                        bg='#F8BC3B',  bd=1, relief="solid", font=("Arial", 20))
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
    photo_list.append(trigger_photo)  # add photo object to the list
    trigger_label = Button(generate_window, image=trigger_photo, borderwidth=0,
                           highlightthickness=0, bg='#F8BC3B', activebackground='#F8BC3B', command=generate_image)
    trigger_label.place(x=110, y=660)

    global save_label
    # Save content button (SAVES THE IMAGE WITH NO CHARACTER AND NO CONTENT)
    save_photo = ImageTk.PhotoImage(Image.open('./Assets/frame0/save.png'))
    photo_list.append(save_photo)  # add photo object to the list
    save_label = Button(generate_window, image=save_photo, borderwidth=0, highlightthickness=0,
                        bg='#F8BC3B', activebackground='#F8BC3B', command=generate_save, state="disabled")
    save_label.place(x=600, y=665)

    global edit_content_label
    # EDIT CONTENT PHOTO // ADD STORY BUTTON
    edit_content_photo = ImageTk.PhotoImage(
        Image.open('./Assets/addStory_Button.png'))
    photo_list.append(edit_content_photo)  # add photo object to the list
    edit_content_label = Button(generate_window, image=edit_content_photo, borderwidth=0, highlightthickness=0,
                                bg='#F8BC3B', activebackground='#F8BC3B', command=edit_content_page, state="disabled")
    edit_content_label.place(x=900, y=665)
    generate_window.resizable(False, False)


def title_window():  # Window to get author and title data in entry window 2

    global start_window  # Globalize to be destroyed at the opening of the main operating window
    # Window 2 config start / ctk window
    start_window = tk.Toplevel(app)
    start_window.title("Title and Author")
    start_window.grab_set()
    start_window.geometry("1832x932")
    start_window.configure(bg="#F9F4F1")

    # The variable that stores the textbox object for naming the storybook
    global prompt_pdf

    # Variable that stores the author's name
    global author_name
    # Tkinter UI for the textbox prompts for the storybook file

    # For Title Label
    ltext_title = ctk.CTkLabel(start_window, height=20, width=20, text="Title", font=(
        "Montserrat", 48 * -1), text_color="#AB7A11")
    ltext_title.place(x=218, y=125)

    # For Title Textbox
    prompt_pdf = ctk.CTkEntry(start_window, height=85, width=729, font=(
        "Arial", 20), text_color="black", fg_color="white", border_width=10, border_color="#DDC8A0")
    prompt_pdf.place(x=201.0, y=180.0)

    # For Author Label
    ltext_authname = ctk.CTkLabel(start_window, height=20, width=20, text="Author Name", font=(
        "Montserrat", 48 * -1), text_color="#AB7A11")
    ltext_authname.place(x=218, y=295)
    # For Author Textbox
    author_name = ctk.CTkEntry(start_window, width=729.0, height=85.0, bg_color="#F9F4F1", font=(
        "Arial", 20), text_color="black", fg_color="white", border_width=10, border_color="#DDC8A0")
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
    global cover_prompt  # Globalize the prompt for cover text input

    # For prompt Title Label
    prompt_title = ctk.CTkLabel(start_window, height=20, width=20, text="Enter prompt for Cover Image", font=(
        "Montserrat", 48 * -1), text_color="#AB7A11")
    prompt_title.place(x=218, y=465)

    # Tkinter UI for the textbox prompt for the cover img
    cover_prompt = ctk.CTkEntry(start_window, width=729.0, height=185.0, bg_color="#F9F4F1", font=(
        "Arial", 20), text_color="black", fg_color="white", border_width=10, border_color="#DDC8A0")
    cover_prompt.place(x=201.0, y=520.0)

    # For Cover image generated Label
    coverimglab = ctk.CTkLabel(start_window, height=20, width=20, text="Cover Image", font=(
        "Montserrat", 48 * -1), text_color="#AB7A11")
    coverimglab.place(x=1185, y=115)

    # Placeholder frame for image result generated
    lmain_cover = tk.Label(start_window)
    lmain_cover.place(x=1180, y=183)

    # Placeholder frame for the text input
    ltext_cover = ctk.CTkLabel(start_window, height=100, width=512, text=" ", font=(
        "Arial", 20), text_color="#AB7A11", fg_color=None)
    ltext_cover.place(x=1182, y=650)

    # Back button to window 2
    back_photo = ImageTk.PhotoImage(Image.open('./Assets/backbutton.png'))
    photo_list.append(back_photo)  # add photo object to the list
    back_label = Button(start_window, borderwidth=0, highlightthickness=0,
                        image=back_photo, command=start_window.destroy)
    back_label.place(x=100, y=50, anchor="n")
    # Mute Sound button in Window 2 / start Window
    musicOff_icon = ImageTk.PhotoImage(
        Image.open('./Assets/ButtonmusicOff.png'))
    photo_list.append(musicOff_icon)  # add photo object to the list
    music_button = Button(start_window, image=musicOff_icon, borderwidth=0,
                          highlightthickness=0, command=funct_stop_music)
    music_button.place(x=50, y=180)
    # Play Sound button in Window 2 / start Window
    musicOn_icon = ImageTk.PhotoImage(Image.open('./Assets/ButtonmusicOn.png'))
    photo_list.append(musicOn_icon)  # add photo object to the list
    music_button = Button(start_window, image=musicOn_icon, borderwidth=0,
                          highlightthickness=0, command=funct_play_music)
    music_button.place(x=50, y=310)

    global okay_label  # global to be called in generate_cover image function
    # Ok button to accepts the data and goes to window 3
    okay_photo = ImageTk.PhotoImage(Image.open('./Assets/OkButton.png'))
    photo_list.append(okay_photo)  # add photo object to the list
    okay_label = Button(start_window, borderwidth=0, highlightthickness=0,
                        image=okay_photo, command=main_operating_screen, state="disabled")  # disable if theres no cover image
    okay_label.place(x=1600, y=750, anchor="n")  # y=750

    # Handle the window's screen updates
    start_window.resizable(False, False)
    start_window.mainloop()

# ==============================


def main_operating_screen():  # Main Operating Screen window 3

    # start_window.destroy()  # Destroy the start window (with the author and title data entry)

    global main_screen  # Globalize the value of main_screen

    main_screen = tk.Toplevel(app)
    main_screen.title("Main Operating Screen")
    main_screen.grab_set()
    main_screen.geometry("1832x932")
    main_screen.configure(bg='#F9F4F1')

    ################################################# MESSY SCROLL BAR CODE #####################################################

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
    canvas.pack(side='left', fill='both', expand=1)

    scrollbar = ttk.Scrollbar(     # create a new vertical scrollbar widget
        main_frame, orient='vertical', command=canvas.yview)
    # place the scrollbar on the right side of the main_frame
    scrollbar.pack(side='right', fill='y')

    # configure the canvas to scroll using the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(  # bind the <Configure> event to the canvas and update the scroll region when the canvas is resized
        scrollregion=canvas.bbox('all')))

    # create a new frame to hold the widgets inside the canvas
    global inner_frame
    inner_frame = Frame(canvas)
    # set the background color of the inner frame
    inner_frame.configure(bg="#F9F4F1")
    canvas.create_window((0, 0), window=inner_frame, anchor='center')

    ######################################################################################################

    # Back button to title and author
    back_photo = ImageTk.PhotoImage(Image.open('./Assets/backbutton.png'))
    photo_list.append(back_photo)  # add photo object to the list
    back_label = Button(main_screen, borderwidth=0, highlightthickness=0,
                        image=back_photo, command=main_screen.destroy)
    back_label.place(x=100, y=50, anchor="n")
    # Mute Sound button in Window 3 / Main Operating Screen
    musicOff_icon = ImageTk.PhotoImage(
        Image.open('./Assets/ButtonmusicOff.png'))
    photo_list.append(musicOff_icon)  # add photo object to the list
    music_button = Button(main_screen, image=musicOff_icon, borderwidth=0,
                          highlightthickness=0, command=funct_stop_music)
    music_button.place(x=50, y=180)
    # Play Sound button in Window 3 / Main Operating Screen
    musicOn_icon = ImageTk.PhotoImage(Image.open('./Assets/ButtonmusicOn.png'))
    photo_list.append(musicOn_icon)  # add photo object to the list
    music_button = Button(main_screen, image=musicOn_icon, borderwidth=0,
                          highlightthickness=0, command=funct_play_music)
    music_button.place(x=50, y=310)

    text = prompt_pdf.get()
    if len(text) >= 40 or 25 <= len(text):
        wrapped_text = '\n'.join(text[i:i+40] for i in range(0, len(text), 40))
        pictales_title = tk.Label(main_screen, text=wrapped_text, font=custom_font,
                                  fg='#F8BC3B', bg='#F9F4F1', wraplength=500, justify='right')
        pictales_title.place(x=1325, y=78)
        pictales_title.config(font=("Supersonic Rocketship", 28))
    else:
        pictales_title = tk.Label(main_screen, text=text, font=custom_font,
                                  fg='#F8BC3B', bg='#F9F4F1', justify='right')
        pictales_title.place(x=1275, y=78)
        pictales_title.config(font=("Supersonic Rocketship", 28))

    # Add page button // Cross Photo
    addpage_photo = ImageTk.PhotoImage(Image.open('./Assets/addpage.png'))
    photo_list.append(addpage_photo)  # add photo object to the list
    addpage_label = Button(main_screen, borderwidth=0,
                           highlightthickness=0, image=addpage_photo, command=funct_generate_window, bg='#F9F4F1', activebackground='#F9F4F1')
    addpage_label.place(x=1450, y=625)

    # Redirecting to modal window for Generating image // Create Pictales button in window 3
    createpictales_photo = ImageTk.PhotoImage(
        Image.open('./Assets/createpictales.png'))
    photo_list.append(createpictales_photo)  # add photo object to the list
    createpictales_label = Button(main_screen, borderwidth=0,
                                  highlightthickness=0, image=createpictales_photo, command=clarification_window)  # show the prompt creation of pdf
    createpictales_label.place(x=1300, y=750)


def clarification_window():  # Clarification Window pops up before creating the pictales pdf window 5
    global clarification  # globallize the value of clarification

    clarification = tk.Toplevel(app)
    clarification.title('Are you sure?')
    clarification.grab_set()
    clarification.geometry("690x603+{}+{}".format(
        app.winfo_width()//2 - 378 + app.winfo_rootx(),
        app.winfo_height()//2 - 372 + app.winfo_rooty()
    ))
    clarification.configure(bg='#F8BC3B')  # set background color

    # Set the clarification label on the window
    clear_label = tk.Label(clarification, text='ARE YOU SURE TO \n REDISCOVER YOUR STORY AND \n CREATE YOUR OWN PICTALES?',
                           font=custom_font, fg='white', bg='#F8BC3B')
    clear_label.place(x=40, y=50)

    # set the font of the label to Supersonic Rocketship with a size of 20
    clear_label.config(font=("Supersonic Rocketship", 34))

    # X Button // Close the clarification window
    close_photo = ImageTk.PhotoImage(
        Image.open('./Assets/window2/x Button.png'))
    photo_list.append(close_photo)  # add photo object to the list
    no_button = Button(clarification, image=close_photo, command=clarification.destroy,
                       background='#F8BC3B', borderwidth=0, highlightthickness=0, activebackground='#F8BC3B')
    no_button.place(x=200, y=400)

    # v/ Button // Generate PDF File
    open_photo = ImageTk.PhotoImage(
        Image.open('./Assets/window2/check button.png'))
    photo_list.append(open_photo)  # add photo object to the list
    yes_button = Button(clarification, image=open_photo, command=generate_pdf,
                        background='#F8BC3B', borderwidth=0, highlightthickness=0, activebackground='#F8BC3B')
    yes_button.place(x=400, y=400)

    clarification.resizable(False, False)


def on_enter_main(e, hover_photo, char_key):  # For main on hover effect
    if (char_key == 1):
        boy_label['image'] = hover_photo
    elif (char_key == 2):
        girl_label['image'] = hover_photo
    elif (char_key == 3):
        dog_label['image'] = hover_photo


def on_leave_main(e, photo, char_key):  # For main off hover effect
    if (char_key == 1):
        boy_label['image'] = photo
    elif (char_key == 2):
        girl_label['image'] = photo
    elif (char_key == 3):
        dog_label['image'] = photo


def funct_char_select(char_value):  # Function for getting the character selected

    global char_select  # Globalize the value of character selection

    # char_select = 0 # Instantiate to zero
    char_select = char_value    # Get the value passed from addcharacter screen
    print("current value (1-3):", char_select)  # PLACEHOLDER LINE

    # Call the character expression window to select the selected character's expressions
    character_expression_window()


def edit_content_page():  # Add edit the page content window 5.1 // ADD STORY WINDOW

    # Globalize edit content page to destroy it later in generate save function
    global addcharacter_screen

    addcharacter_screen = tk.Toplevel(app)
    addcharacter_screen.title("Characters and Story")
    addcharacter_screen.grab_set()
    addcharacter_screen.geometry("1832x932")
    addcharacter_screen.configure(bg='#F8BC3B')

    # Back button for add character window 5.1
    back_photo = ImageTk.PhotoImage(Image.open('./Assets/backbutton.png'))
    photo_list.append(back_photo)  # add photo object to the list
    back_label = Button(addcharacter_screen, borderwidth=0, highlightthickness=0, image=back_photo,
                        command=addcharacter_screen.destroy, bg='#F8BC3B', activebackground='#F8BC3B')
    back_label.place(x=100, y=50, anchor="n")
    # Mute Sound button in Window 5.1 / Edit Content Window
    musicOff_icon = ImageTk.PhotoImage(
        Image.open('./Assets/ButtonmusicOff.png'))
    photo_list.append(musicOff_icon)  # add photo object to the list
    music_button = Button(addcharacter_screen, image=musicOff_icon, borderwidth=0,
                          highlightthickness=0, command=funct_stop_music,  bg='#F8BC3B', activebackground='#F8BC3B')
    music_button.place(x=50, y=180)
    # Play Sound button in Window 5.1 / Edit Content Window
    musicOn_icon = ImageTk.PhotoImage(Image.open('./Assets/ButtonmusicOn.png'))
    photo_list.append(musicOn_icon)  # add photo object to the list
    music_button = Button(addcharacter_screen, image=musicOn_icon, borderwidth=0,
                          highlightthickness=0, command=funct_play_music,  bg='#F8BC3B', activebackground='#F8BC3B')
    music_button.place(x=50, y=310)

    # Show the selected character from the 8 expressions:
    selected_character_label = tk.Label(
        addcharacter_screen, text='Selected Character:', font=custom_font, fg='white', bg='#F8BC3B')
    selected_character_label.place(x=200, y=500)
    # set the font of the label to Supersonic Rocketship with a size of 20
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
    # set the font of the label to Supersonic Rocketship with a size of 20
    character_label.config(font=("Supersonic Rocketship", 25))

    # Label for edit page content
    edit_prompt = Label(addcharacter_screen,
                        text="Enter your story here: ", bg='#F8BC3B', fg='white')
    edit_prompt.place(x=900, y=110)
    edit_prompt.config(font=("Supersonic Rocketship", 18))

    global edit_textcontent_area  # Globalize to pass to generate save with get() method
    # Edit textbox widget for editing the content of the story page
    edit_textcontent_area = tk.Text(addcharacter_screen, height=20, width=45,
                                    bg='#F8BC3B',  bd=1, relief="solid", font=("Arial", 20))
    edit_textcontent_area.place(x=900, y=150)

    # ========================================Character Buttons========================================
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


def character_expression_window():  # Choosing expression window
    # Globalize the screen to destroy it later on selection in funct_main_char_select
    global character_screen
    character_screen = tk.Toplevel(app)
    character_screen.title("Character's Emotion Selection")
    character_screen.grab_set()
    character_screen.geometry("1832x932")
    character_screen.configure(bg='#F8BC3B')

    # Get the character data from the global variable and function
    if (char_select == 1):
        char_name = "boy"
    elif (char_select == 2):
        char_name = "girl"
    elif (char_select == 3):
        char_name = "dog"

    # Back button on boycharacter_screen
    back_photo = ImageTk.PhotoImage(Image.open('./Assets/backbutton.png'))
    photo_list.append(back_photo)  # add photo object to the list
    back_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=back_photo,
                        command=character_screen.destroy, bg='#F8BC3B', activebackground='#F8BC3B')
    back_label.place(x=100, y=50, anchor="n")
    # Mute Sound button in Expression Window
    musicOff_icon = ImageTk.PhotoImage(
        Image.open('./Assets/ButtonmusicOff.png'))
    photo_list.append(musicOff_icon)  # add photo object to the list
    music_button = Button(character_screen, image=musicOff_icon, borderwidth=0,
                          highlightthickness=0, command=funct_stop_music, bg='#F8BC3B', activebackground='#F8BC3B')
    music_button.place(x=50, y=180)

    # Play Sound button in Expression Window
    musicOn_icon = ImageTk.PhotoImage(Image.open('./Assets/ButtonmusicOn.png'))
    photo_list.append(musicOn_icon)  # add photo object to the list
    music_button = Button(character_screen, image=musicOn_icon, borderwidth=0,
                          highlightthickness=0, command=funct_play_music, bg='#F8BC3B', activebackground='#F8BC3B')
    music_button.place(x=50, y=310)

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

    char1_photo = ImageTk.PhotoImage(Image.open(
        './Assets/{}_happy_small.png'.format(char_name)))  # Happy emotion option
    photo_list.append(char1_photo)
    char1_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char1_photo,
                         command=lambda: funct_main_char_select(1, char1_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char1_label.place(x=400, y=150, anchor="n")
    char1_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char1_label.bind("<Leave>", on_leave)

    char2_photo = ImageTk.PhotoImage(Image.open(
        './Assets/{}_sad_small.png'.format(char_name)))  # Sad emotion option
    photo_list.append(char2_photo)
    char2_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char2_photo,
                         command=lambda: funct_main_char_select(2, char2_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char2_label.place(x=600, y=150, anchor="n")
    char2_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char2_label.bind("<Leave>", on_leave)

    char3_photo = ImageTk.PhotoImage(Image.open(
        './Assets/{}_angry_small.png'.format(char_name)))  # Angry emotion option
    photo_list.append(char3_photo)  # add photo object to the list
    char3_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char3_photo,
                         command=lambda: funct_main_char_select(3, char3_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char3_label.place(x=800, y=150, anchor="n")
    char3_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char3_label.bind("<Leave>", on_leave)

    char4_photo = ImageTk.PhotoImage(
        Image.open('./Assets/{}_surprised_small.png'.format(char_name)))  # Surprised emotion option
    photo_list.append(char4_photo)  # add photo object to the list
    char4_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char4_photo,
                         command=lambda: funct_main_char_select(4, char4_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char4_label.place(x=1000, y=150, anchor="n")
    char4_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char4_label.bind("<Leave>", on_leave)

    char5_photo = ImageTk.PhotoImage(Image.open(
        './Assets/{}_normal_small.png'.format(char_name)))  # Smile emotion option
    photo_list.append(char5_photo)  # add photo object to the list
    char5_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char5_photo,
                         command=lambda: funct_main_char_select(5, char5_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char5_label.place(x=400, y=350, anchor="n")
    char5_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char5_label.bind("<Leave>", on_leave)

    char6_photo = ImageTk.PhotoImage(Image.open(
        './Assets/{}_confused_small.png'.format(char_name)))  # Confused emotion option
    photo_list.append(char6_photo)  # add photo object to the list
    char6_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char6_photo,
                         command=lambda: funct_main_char_select(6, char6_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char6_label.place(x=600, y=350, anchor="n")
    char6_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char6_label.bind("<Leave>", on_leave)

    char7_photo = ImageTk.PhotoImage(Image.open(
        './Assets/{}_disgust_small.png'.format(char_name)))  # Disgust emotion option
    photo_list.append(char7_photo)  # add photo object to the list
    char7_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char7_photo,
                         command=lambda: funct_main_char_select(7, char7_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char7_label.place(x=800, y=350, anchor="n")
    char7_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char7_label.bind("<Leave>", on_leave)

    char8_photo = ImageTk.PhotoImage(Image.open(
        './Assets/{}_fear_small.png'.format(char_name)))  # Fear emotion option
    photo_list.append(char8_photo)  # add photo object to the list
    char8_label = Button(character_screen, borderwidth=0, highlightthickness=0, image=char8_photo,
                         command=lambda: funct_main_char_select(8, char8_photo), bg='#F8BC3B', activebackground='#F8BC3B')
    char8_label.place(x=1000, y=350, anchor="n")
    char8_label.bind("<Enter>", lambda e: on_enter(e, "#fad689"))
    char8_label.bind("<Leave>", on_leave)

    character_screen.resizable(False, False)


# ___________________________________________________________________________ MAIN TKINTER UI ___________________________________________________________________________
# Create the app
app = ctk.CTk()
app.title("Pictales")
app.geometry("1832x932")
ctk.set_appearance_mode("F9F4F1")

# Play background music
funct_play_music()

# Globalize the value of character selection WITH the expressions
main_char_select = 0

# Store the character in a photo image variable
character = ImageTk.PhotoImage(blank)  # Set no character as default

# ___________________________________________________________________________
# Set background of window 1
bg_img_photo = ImageTk.PhotoImage(Image.open('./Assets/AppBG.png'))
bg_img_label = Label(app, image=bg_img_photo)
bg_img_label.place(x=0, y=0)

# Load and display the logo image on the canvas in window 1
logo_photo = ImageTk.PhotoImage(Image.open('./Assets/frame0/image_1.png'))
logo_label = Label(app, image=logo_photo, bg='#F9F4F1')
logo_label.place(x=800, y=90)

# load and display start button
start_photo = ImageTk.PhotoImage(Image.open('./Assets/frame0/button_3.png'))
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

# Mute Sound button in Window 1 / Main Window
musicOff_icon = ImageTk.PhotoImage(Image.open('./Assets/ButtonmusicOff.png'))
photo_list.append(musicOff_icon)  # add photo object to the list
music_button = Button(app, image=musicOff_icon, borderwidth=0,
                      highlightthickness=0, command=funct_stop_music)
music_button.place(x=50, y=180)
# Play Sound button in Window 1 / Main Window
musicOn_icon = ImageTk.PhotoImage(Image.open('./Assets/ButtonmusicOn.png'))
photo_list.append(musicOn_icon)  # add photo object to the list
music_button = Button(app, image=musicOn_icon, borderwidth=0,
                      highlightthickness=0, command=funct_play_music)
music_button.place(x=50, y=310)

app.resizable(False, False)
# ___________________________________________________________________________ DRIVER CODE ___________________________________________________________________________
# Get text input prompts again by automatically restarting the app
app.mainloop()
