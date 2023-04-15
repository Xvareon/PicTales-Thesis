# Python packages and dependencies are needed for the application to run. Installed through PIP in VSCode terminal (Todo: automatically install these with the app with PyInstaller)

#########################################################
# TO-DO LIST FOR THE BREAK:

# Auto Install # PRIORITY
# PicTales options basic and advanced
# Edit Pages?
# Character Expressions detector
# Paragraph input chop chop (to avoid cutoff text)
# Upload self created character
# PDF MUST BE AUTOMATICALLY 2 PAGE
# NEEDS UI that shows storybook has been created and exit the program
# Video needs to have proper closing
#########################################################

# ___________________________________________________________________________ DEPENDENCIES ___________________________________________________________________________
# Import Tkinter for Python UI
import tkinter as tk

# Import Tkinter modules for buttons, labels, additional GUI
from tkinter import Label, Button, Canvas

# Import Tkinter module for video
import tkvideo

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
# model = torch.load('./results/model-1.pt')

# ___________________________________________________________________________ FUNCTIONS ___________________________________________________________________________


def generate_image():   # Function to generate the images from the text prompt

    global img          # For storing the image to avoid garbage collection

    global text_input   # For storing the text input to transfer to the Picture Book PDF

    global image        # For storing image to be saved if save image button is clicked

    # Uses the GPU to process the dataset through the model and get the image result
    with autocast(device):

        # Store text input in a variable
        # text_input = text_area.get()
        text_input = text_area.get('1.0', tk.END)

        # Catch error if no text input is given
        if len(text_input) == 0 or text_input.isspace() == True:
            image = blank
        else:
            image = blank   # (COMMENT OUT THIS LINE) FOR USING GUI WITHOUT AI TESTING ONLY!
            cartoon_input = "cartoonish " + text_input
            # Variable that contains the image result
            # image = pipe(cartoon_input, guidance_scale=10)[
            #     "images"][0]

    # Store image in a variable
    img = ImageTk.PhotoImage(image)

    # Displays the text input in the Tkinter UI after generation
    # ltext.configure(text=text_input)
    # ltext.update()

    # # Displays the image in the Tkinter UI after generation
    # lmain.configure(image=img)
    # lmain.update()


def save_window():  # Function that saves the image to the directory with the modifications

    # Globalize the window object that pops up for save creation
    global app_save

    # The variable that stores the textbox object for editing the text of a page
    global prompt_save

    # Declares the variables that will store the characters
    global char_one
    global char_two
    global char_three

    # Declare the variables that store the labels/position of the character image selection
    global lchar_one
    global lchar_two
    global lchar_three

    # Declare the variables that store the labels/position of the text label of character selection
    global lchar_one_text
    global lchar_two_text
    global lchar_three_text

    # Declare value for radio selection
    global char_select

    # Window object for the text prompt for naming the book
    app_save = ctk.CTkToplevel(app)
    app_save.title("Edit Content Page")
    app_save.geometry("1832x932")
    ctk.set_appearance_mode("dark")

    # Background for the save image window
    SaveBGimg = ctk.CTkLabel(app_save, image=ImageTk.PhotoImage(
        Image.open('./Assets/AppBG.png')))
    SaveBGimg.pack()

    # Tkinter UI for the textbox prompt
    prompt_save = ctk.CTkTextbox(app_save, height=400, width=400, font=(
        "Arial", 12), text_color="black", fg_color="white")
    prompt_save.place(x=6, y=6)

    # Tkinter Widget for the button
    create_save = ctk.CTkButton(app_save, height=40, width=120, font=(
        "Arial", 20), text_color="white", fg_color="blue", command=generate_save)
    create_save.configure(text="Save Image and Page")
    create_save.place(x=230, y=725)

    # Translate image details and transform them to a variables which stores each character
    char_one = ImageTk.PhotoImage(Image.open('./Assets/char_one.png'))
    char_two = ImageTk.PhotoImage(Image.open('./Assets/char_two.png'))
    char_three = ImageTk.PhotoImage(Image.open('./Assets/char_three.png'))

    # Placeholder frame and text label for image result generated:

    # For character one
    lchar_one = ctk.CTkLabel(app_save, height=150, width=150)
    lchar_one.place(x=900, y=80)
    lchar_one.configure(image=char_one)
    lchar_one.update()
    lchar_one_text = ctk.CTkLabel(app_save, height=75, width=150, text="Character 1", font=(
        "Arial", 16), text_color="white", fg_color="blue")
    lchar_one_text.place(x=900, y=260)

    # For character two
    lchar_two = ctk.CTkLabel(app_save, height=150, width=150)
    lchar_two.place(x=1200, y=80)
    lchar_two.configure(image=char_two)
    lchar_two.update()
    lchar_two_text = ctk.CTkLabel(app_save, height=75, width=150, text="Character 2", font=(
        "Arial", 16), text_color="white", fg_color="blue")
    lchar_two_text.place(x=1200, y=260)

    # For character three
    lchar_three = ctk.CTkLabel(app_save, height=150, width=150)
    lchar_three.place(x=1500, y=80)
    lchar_three.configure(image=char_three)
    lchar_three.update()
    lchar_three_text = ctk.CTkLabel(app_save, height=75, width=150, text="Character 3", font=(
        "Arial", 16), text_color="white", fg_color="blue")
    lchar_three_text.place(x=1500, y=260)

    # Instantiate 0 as base value and default
    char_select = tk.IntVar(app_save, 0)

    # Selection/Radio buttons for character
    rchar_one = ctk.CTkRadioButton(app_save, text="Choose Character One",
                                   command=radiobutton_char_select, variable=char_select, value=1)
    rchar_one.place(x=900, y=360)

    rchar_two = ctk.CTkRadioButton(app_save, text="Choose Character Two",
                                   command=radiobutton_char_select, variable=char_select, value=2)
    rchar_two.place(x=1200, y=360)

    rchar_three = ctk.CTkRadioButton(app_save, text="Choose Character Three",
                                     command=radiobutton_char_select, variable=char_select, value=3)
    rchar_three.place(x=1500, y=360)


def radiobutton_char_select():  # Function for getting the character selected
    print("radiobutton toggled, current value:",
          char_select.get())  # PLACEHOLDER LINE


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

        # Store the character in a variable
        global character

        # Store the base image on which the character would be pasted on
        global base

        # Save image file name as PNG based on text input
        image.save('./GeneratedImages/{}.png'.format(text_input.strip()))  # Strip the text input to remove the newline at the end of the data.

        if char_select.get() == 1:  # If character one was selected

            base = Image.open('./GeneratedImages/{}.png'.format(text_input))
            # Select the character image from the folder pathfile
            character = Image.open('./Assets/char_one.png')
            # Location where the character image will be pasted into which then pastes it.
            base.paste(character, (0, 360), character.convert('RGBA'))
            base.save('./GeneratedImages/{}.png'.format(text_input))

        if char_select.get() == 2:  # If character two was selected

            base = Image.open('./GeneratedImages/{}.png'.format(text_input))
            # Select the character image from the folder pathfile
            character = Image.open('./Assets/char_two.png')
            # Location where the character image will be pasted into which then pastes it.
            base.paste(character, (0, 360), character.convert('RGBA'))
            base.save('./GeneratedImages/{}.png'.format(text_input))

        if char_select.get() == 3:  # If character three was selected

            base = Image.open('./GeneratedImages/{}.png'.format(text_input))
            # Select the character image from the folder pathfile
            character = Image.open('./Assets/char_three.png')
            # Location where the character image will be pasted into which then pastes it.
            base.paste(character, (0, 360), character.convert('RGBA'))
            base.save('./GeneratedImages/{}.png'.format(text_input))

        i = 0  # Instantiate i for loops (text item positioning)
        j = 0  # Instantiate j for loops (pic positioning)

        content = prompt_save.get("0.0", "end")

        # Makes the text input as a default content input if the user did not enter anything at the content textbox.
        if (content == ''):
            content = text_input

        # Add the content to the list
        content_list.append(content)

        # Add the previously stored text in a list
        text_list.append(text_input)

        # Store image in image variable if no character is selected and store it in base variable if a character is selected (For previews)
        if char_select.get() == 0:
            img = ImageTk.PhotoImage(image)
        else:
            img = ImageTk.PhotoImage(base)

        # Store previous image in a list
        image_list.append(img)

        # Displays the text list
        for text_item in content_list:
            j = j+1
            # Placeholder frame for the text input LISTS
            ltext_list = ctk.CTkLabel(app, height=512, width=512, text=text_item, font=(
                "Arial", 12), text_color="white", fg_color="blue")
            ltext_list.place(x=600, y=-100 + (200*j))

        # Displays the image list
        for pic in image_list:
            i = i+1
            limg_list = ctk.CTkLabel(app, height=200, width=200, image=pic)
            limg_list.place(x=1200, y=-100 + (200*i))

        # Destroy the edit content window
        app_save.destroy()


def pdf_window():           # Show a text prompt

    # Globalize the window object that pops up for pdf creation
    global app_pdf

    # The variable that stores the textbox object for naming the storybook
    global prompt_pdf

    # Variable that stores the author's name
    global author_name

    # Window object for the text prompt for naming the book
    app_pdf = ctk.CTkToplevel(app)
    app_pdf.title("Set Storybook Name")
    app_pdf.geometry("1832x932")
    ctk.set_appearance_mode("dark")

    # Background for the create pdf window
    PDFBGimg = ctk.CTkLabel(app_pdf, image=ImageTk.PhotoImage(
        Image.open('./Assets/AppBG.png')))
    PDFBGimg.pack()

    # Tkinter UI for the textbox prompts for the storybook file
    # For Title Label
    ltext_title = ctk.CTkLabel(app_pdf, height=20, width=20, text="Title", font=(
        "Arial", 12), text_color="white", fg_color="blue")
    ltext_title.place(x=60, y=70)
    # For Title Textbox
    prompt_pdf = ctk.CTkEntry(app_pdf, height=40, width=400, font=(
        "Arial", 20), text_color="black", fg_color="white")
    prompt_pdf.place(x=60, y=120)

    # For Author Label
    ltext_authname = ctk.CTkLabel(app_pdf, height=20, width=20, text="Author Name", font=(
        "Arial", 12), text_color="white", fg_color="blue")
    ltext_authname.place(x=60, y=170)
    # For Author Textbox
    author_name = ctk.CTkEntry(app_pdf, height=40, width=400, font=(
        "Arial", 20), text_color="black", fg_color="white")
    author_name.place(x=60, y=220)

    # Generate image for coverpage
    cover_trigger = ctk.CTkButton(app_pdf, height=40, width=120, font=(
        "Arial", 20), text_color="white", fg_color="blue", command=generate_cover_image)
    cover_trigger.configure(text="Generate")
    cover_trigger.place(x=1000, y=800)

    global lmain_cover  # Globalize cover label frame holder
    global ltext_cover  # Globalize text label frame holder
    global cover_prompt  # Globalize the prompt for cover text input

    # Tkinter UI for the textbox prompt
    cover_prompt = ctk.CTkEntry(app_pdf, height=40, width=512, font=(
        "Arial", 20), text_color="black", fg_color="white")
    cover_prompt.place(x=610, y=60)

    # Placeholder frame for image result generated
    lmain_cover = ctk.CTkLabel(app_pdf, height=512, width=512)
    lmain_cover.place(x=610, y=110)

    # Placeholder frame for the text input
    ltext_cover = ctk.CTkLabel(app_pdf, height=100, width=512, text="COVERPAGE", font=(
        "Arial", 20), text_color="white", fg_color="blue")
    ltext_cover.place(x=610, y=600)

    # Tkinter Widget for the button
    create_pdf = ctk.CTkButton(app_pdf, height=40, width=120, font=(
        "Arial", 20), text_color="white", fg_color="blue", command=generate_pdf)
    create_pdf.configure(text="Generate {}".format('Storybook'))
    create_pdf.place(x=140, y=370)


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
        else:
            cartoon_input = "cartoonish " + cover_input
            # Variable that contains the image result
            # image_cover = pipe(cartoon_input, guidance_scale=10)[
            #     "images"][0]

    # Store image in a variable
    img_cover = ImageTk.PhotoImage(image_cover)

    # Displays the text input in the Tkinter UI after generation
    ltext_cover.configure(text=cover_input)
    ltext_cover.update()

    # Displays the image in the Tkinter UI after generation
    lmain_cover.configure(image=img_cover)
    lmain_cover.update()


def generate_pdf():                 # Generate PicTale Story book

    pdf_name = prompt_pdf.get()     # Store text input in a variable, from the pdf window

    # Store current time in a variable
    now = datetime.datetime.now()

    # Store the pdf file name into a variable, sets this as default for errors and etc like if the title name is not set.
    if (pdf_name == ''):
        pdf_name = 'PicTales'

    # Specifies the directory where the pdf will generate
    pdf_path = "./StoryBooks/{}.pdf".format(pdf_name)

    # Save image file name as PNG based on text input
    image_cover.save('./GeneratedImages/TitlePage_{}.png'.format(pdf_name))

    # Pass image cover variable for drawing/writing the page title details
    covertext = ImageDraw.Draw(image_cover)

    # Choose font
    font = ImageFont.truetype('arial.ttf', 16)

    # Write the text input based on the details provided by the user

    # For Author
    covertext.text((10, 10), author_name.get(),
                   font=font, fill=(255, 255, 255))

    # For Title
    covertext.text((10, 210), pdf_name, font=font, fill=(255, 255, 255))

    # For Date Created
    covertext.text((10, 410), now.strftime("%m-%d-%Y"),
                   font=font, fill=(255, 255, 255))

    # Save cover image to local directory
    image_cover.save('./GeneratedImages/TitlePage_{}.png'.format(pdf_name))

    # Store the coverpage into an object variable
    cover = Image.open('./Assets/CoverPage.png')
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

        # Append main image file
        pdf_list.append(Image.open(
            './GeneratedImages/{}.png'.format(file)))

        # Append the image file that has the text input drawn on a blank page
        pdf_list.append(Image.open(
            './GeneratedImages/INPUT{}.png'.format(file)))

    # Check if storybook has content
    if pdf_list:
        # Generate the PDF
        pdf_list[0].save(
            pdf_path, "PDF", resolution=100.0, save_all=True, append_images=pdf_list[1:]
        )

    # Destroy the rename window
    app_pdf.destroy()


# ___________________________________________________________________________ CONFIGURATIONS ___________________________________________________________________________
# isExist = os.path.exists('./results/model-1.pt')

# if (isExist == False):
#     sys.exit(0)

# # loads the model used to a pre-defined library online
# modelid = "CompVis/stable-diffusion-v1-4"

# # Specifies the graphics driver to be used
# device = "cuda"
device = "cpu"

# # Loads the model into torch
# torch.load('./results/model-1.pt')

# auth_token = "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"

# # Uses the pipe from the online library for model translation to produce the image.
# pipe = StableDiffusionPipeline.from_pretrained(
#     modelid, revision="fp16", torch_dtype=torch.float16, use_auth_token=auth_token)

# # # Uses the graphics driver (Must atleast be 4GB ram)
# pipe.to(device)

# Create template page for the title page image
blank = Image.new('RGB', (512, 512))

# Save template in generated images folder
blank.save('./GeneratedImages/BlankTemplate.png')

# -----------------------------------------------------------------------------------

# Define the font file path and size
font_path = "./fonts/SupersonicRockets.ttf"
font_size = 24
# Create a custom font
custom_font = (font_path, font_size, "bold")

# -----------------------------------------------------------------------------------

# ABOUT WINDOW POP UP
def about_window():     # the question mark button shows the about pictales modal 
    
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
    modal_label = tk.Label(about_window, text='ABOUT', font=custom_font, fg='white', bg='#F8BC3B')
    modal_label.pack(pady=50)

    # this block of code show the logo PICTALES and resize it, and append the image to be seen coz of resizing
    about_img = Image.open('./Assets/PICTALES LOGO Big w background.png')
    resized_img = about_img.resize((200, 200), resample=Image.LANCZOS)
    about_photo = ImageTk.PhotoImage(resized_img)
    photo_list.append(about_photo)  # add photo object to the list
    about_label = tk.Label(about_window, image=about_photo)
    about_label.place(x=380, y=165, anchor="n") 
    
    # set the font of the label to Supersonic Rocketship with a size of 20
    modal_label.config(font=("Supersonic Rocketship", 64))

    # this code is for printing the copyright
    ver_label = tk.Label(about_window, text='Copyright © 2023, PICTALES', font=custom_font, fg='white', bg='#F8BC3B')
    ver_label.place(relx=0.25, rely=0.75)
    ver_label.config(font=("Supersonic Rocketship", 24))
    
    # this code is for printing the version of the app 
    copy_label = tk.Label(about_window, text='VER. 1.0', font=custom_font, fg='white', bg='#F8BC3B')
    copy_label.pack(pady=190)
    copy_label.config(font=("Supersonic Rocketship", 24))

    about_window.resizable(False, False)

# -----------------------------------------------------------------------------------

def howTo_window():     # how to button will show this window playing the video about pictales
    # this code will pop up the window how to in top level 
    # the geometry with app winfo width and height will center the window modal in main screen
    howTo_window = tk.Toplevel(app)
    howTo_window.title('How to use Pictales')
    howTo_window.grab_set()
    howTo_window.geometry("1028x639+{}+{}".format(
        app.winfo_width()//2 - 480 + app.winfo_rootx(),
        app.winfo_height()//2 - 380 + app.winfo_rooty()
    ))
    howTo_window.configure(bg='#F8BC3B')  # set background color

    # this block of code play the video using the tkvideo library 
    my_label = Label(howTo_window)
    my_label.pack()
    player = tkvideo.tkvideo("./Assets/sample.mp4", my_label, loop = 1,  size=(820, 420)) # to change soon if video pictales is available
    player.play()                                                                         # change the function to play or stop the video
    
     # Center the label/video in the window
    my_label.place(x=520, y=300, anchor="center")

    howTo_window.resizable(False, False)



def generate_window():    # this window is start button in main page
    # this code will pop up the window how to in top level
    # the geometry with app winfo width and height will center the window modal in main screen
    generate_window = tk.Toplevel(app)
    generate_window.title("Prompt")    
    generate_window.grab_set()
    generate_window.geometry("1228x739+{}+{}".format(
        app.winfo_width()//2 - 614 + app.winfo_rootx(),
        app.winfo_height()//2 - 369 + app.winfo_rooty()
    ))
    generate_window.configure(bg='#F8BC3B')  # set background color
    
    # this code is for the title label
    text_title = Label(generate_window, text="Enter prompt", bg='#F8BC3B')
    text_title.place(x=460, y=67)
    text_title.config(font=("Supersonic Rocketship", 18))
    
    global text_area
    
    # Textbox widget for getting USER TEXT INPUT FOR GENERATING IMAGE
    text_area = tk.Text(generate_window, height=15, width=46, bg='#F8BC3B',  bd=2, relief="solid", font=("Arial", 20))
    text_area.place(x=460, y=100)
    
    # this code is for the title generate container
    generate_title = Label(generate_window, text="Image generated", bg='#F8BC3B')
    generate_title.place(x=50, y=67)
    generate_title.config(font=("Supersonic Rocketship", 18))
    
    # this code is to show the generated image on this container
    lmain = tk.Label(generate_window, height=32, width=55, bg='#F8BC3B', bd=2, relief="solid")
    lmain.place(x=50, y=100)
    
    #this code is to show the generate button 
    trigger_image = Image.open('./Assets/frame0/Generate Button.png') 
    trigger_photo = ImageTk.PhotoImage(trigger_image) 
    photo_list.append(trigger_photo)  # add photo object to the list 
    trigger_label = Button(generate_window, image=trigger_photo, borderwidth=0, highlightthickness=0, bg='#F8BC3B', activebackground='#F8BC3B', command=generate_image) 
    trigger_label.place(x=110, y=605)
    
    global ltext # Globalize to pass on generate image function
    ltext = ctk.CTkLabel(generate_window, height=15, width=46, text="Image Title", font=(
        "Supersonic Rocketship", 20), text_color="black")
    ltext.place(x=60, y=600)
    
    # this code is to show the add character button
    char_image = Image.open('./Assets/frame0/addcharacter.png') 
    char_photo = ImageTk.PhotoImage(char_image) 
    photo_list.append(char_photo)  # add photo object to the list
    char_label = Button(generate_window, image=char_photo, borderwidth=0, highlightthickness=0, bg='#F8BC3B', activebackground='#F8BC3B', command=addcharacter_screen) 
    char_label.place(x=650, y=610)
    
    # this code is to show the save button 
    save_image = Image.open('./Assets/frame0/save.png') 
    save_photo = ImageTk.PhotoImage(save_image) 
    photo_list.append(save_photo)  # add photo object to the list
    save_label = Button(generate_window, image=save_photo, borderwidth=0, highlightthickness=0, bg='#F8BC3B', activebackground='#F8BC3B', command=generate_save) 
    save_label.place(x=950, y=610)

def title_window(): # Window to get author and title data entry 

    # Window 2 config start / ctk window
    start_window = ctk.CTkToplevel(app)
    start_window.title("Title and Author")
    start_window.grab_set()
    start_window.geometry("1832x932")
    start_window.configure(bg = "#F9F4F1")
     
    # Create a canvas widget
    canvas = Canvas(start_window, bg = "#F9F4F1", height = 932, width = 1832, bd = 0, highlightthickness = 0, relief = "ridge")
    canvas.place(x = 0, y = 0)
    
    # Author TextBox
    entry_1 = ctk.CTkEntry(start_window, width=1029.0, height=85.0, bg_color="#F9F4F1", font=("Arial", 20), text_color="black", border_width=10, border_color="#DDC8A0")
    entry_1.place(x=401.0, y=200.0)

    # Author label on top of the text box
    canvas.create_text(
        418.0,
        99.0,
        anchor="nw",
        text="Title",
        fill="#AB7A11",
        font=("Montserrat", 48 * -1)
    )
    
    # Title Textbox
    entry_2 =ctk.CTkEntry(start_window, width=1029.0, height=85.0, bg_color="#F9F4F1", font=("Arial", 20), text_color="black", border_width=10, border_color="#DDC8A0")
    entry_2.place(x=401.0, y=441.0)
                        
    # Title label on top of the text box
    canvas.create_text(
        418.0,
        373.0,
        anchor="nw",
        text="Author",
        fill="#AB7A11",
        font=("Montserrat", 48 * -1)
    )

    # X Red button
    button1_photo = ImageTk.PhotoImage(Image.open('./Assets/window2/button_1.png'))
    button_1 = Button(
        start_window,
        image = button1_photo,
        borderwidth=0,
        command = start_window.destroy,
        highlightthickness=0,
        relief="flat"
    )
    button_1.place(
        x=765.0,
        y=465.0,
        width=93.0,
        height=103.0
    )
    
    # Check Green Button
    button2_photo = ImageTk.PhotoImage(Image.open('./Assets/window2/button_2.png'))
    button_2= Button(
        start_window,
        image = button2_photo,
        borderwidth=0,
        highlightthickness=0,
        command=main_operating_screen,
        relief="flat"
    )
    button_2.place(   
        x=957.0,
        y=465.0,
        width=93.0,
        height=103.0
    )

    # Handle the window's screen updates
    start_window.resizable(False, False)
    start_window.mainloop()

# ==============================

# Main Operating Screen
def main_operating_screen ():
    main_operating_screen = tk.Toplevel(app)
    main_operating_screen.title("Main Operating Screen")
    main_operating_screen.grab_set()
    main_operating_screen.geometry("1832x932")
    main_operating_screen.configure(bg='#F9F4F1')
    
    # Back button to title and author
    back_img = Image.open('./Assets/backbutton.png')
    back_photo = ImageTk.PhotoImage(back_img)
    photo_list.append(back_photo)  # add photo object to the list
    back_label = Button(main_operating_screen, borderwidth=0, highlightthickness=0, image=back_photo, command = main_operating_screen.destroy)
    back_label.place(x=100, y=50, anchor="n")

    # Will be the title based on the output of the user
    pictales_title = tk.Label(main_operating_screen, text='Title of Pictales', font=custom_font, fg='#F8BC3B', bg='#F9F4F1')
    pictales_title.place(x=200, y=50)
    pictales_title.config(font=("Supersonic Rocketship", 60))

    # Add page button 
    addpage_img = Image.open('./Assets/addpage.png')
    addpage_photo = ImageTk.PhotoImage(addpage_img)
    photo_list.append(addpage_photo)  # add photo object to the list
    addpage_label = Button(main_operating_screen, borderwidth=0, highlightthickness=0, image=addpage_photo, command=generate_window)
    addpage_label.place(x=1160, y=450, anchor="n")

    # Redirecting to modal window for Generating image 
    createpictales_img = Image.open('./Assets/createpictales.png')
    createpictales_photo = ImageTk.PhotoImage(createpictales_img)
    photo_list.append(createpictales_photo)  # add photo object to the list
    createpictales_label = Button(main_operating_screen, borderwidth=0, highlightthickness=0, image=createpictales_photo, command=clarification_window)
    createpictales_label.place(x=1050, y=440, anchor="n")

# Clarification Window pops up before creating the pictales
def clarification_window(): 
    clarification_window = tk.Toplevel(app)
    clarification_window.title('Are you sure?')
    clarification_window.grab_set()
    clarification_window.geometry("690x603+{}+{}".format(
        app.winfo_width()//2 - 378 + app.winfo_rootx(),
        app.winfo_height()//2 - 372 + app.winfo_rooty()
    ))
    clarification_window.configure(bg='#F8BC3B')  # set background color
    
    # Set the clarification label on the window
    clear_label = tk.Label(clarification_window, text='ARE YOU SURE TO \n REDISCOVER YOUR STORY AND \n CREATE YOUR OWN PICTALES?', font=custom_font, fg='white', bg='#F8BC3B')
    clear_label.place(x=40, y=50)

    #set the font of the label to Supersonic Rocketship with a size of 20
    clear_label.config(font=("Supersonic Rocketship", 34))

    # X Button
    no_button = Image.open('./Assets/window2/button_1.png')
    close_photo = ImageTk.PhotoImage(no_button)
    photo_list.append(close_photo)  # add photo object to the list
    no_button = Button(clarification_window,image=close_photo, command=lambda: print(" x  button clicked"), background='#F8BC3B', borderwidth=0, highlightthickness=0, activebackground='#F8BC3B')
    no_button.place(x=200, y=400) 

    # v/ Button  
    yes_button = Image.open('./Assets/window2/button_2.png')
    open_photo = ImageTk.PhotoImage(yes_button)
    photo_list.append(open_photo)  # add photo object to the list
    yes_button = Button(clarification_window,image=open_photo, command=lambda: print(" v/  button clicked"), background='#F8BC3B', borderwidth=0, highlightthickness=0, activebackground='#F8BC3B')
    yes_button.place(x=400, y=400)

# Add Screen
def addcharacter_screen ():
    addcharacter_screen = tk.Toplevel(app)
    addcharacter_screen.title("Characters")
    addcharacter_screen.grab_set()
    addcharacter_screen.geometry("1832x932")
    addcharacter_screen.configure(bg='#F8BC3B')

    #Chacter label to choose charcter
    character_label = tk.Label(addcharacter_screen, text='CHOOSE YOUR CAHARCTER: CLICK ON THE CHARACTER YOU WANT', font=custom_font, fg='white', bg='#F8BC3B')
    character_label.place(x=40, y=50)
    #set the font of the label to Supersonic Rocketship with a size of 20
    character_label.config(font=("Supersonic Rocketship", 34))

    #========================================Character Buttons========================================
    # GIRL
    girl_img = Image.open('./Assets/char_two.png')
    girl_photo = ImageTk.PhotoImage(girl_img)
    photo_list.append(girl_photo)  # add photo object to the list
    girl_label = Button(addcharacter_screen, borderwidth=0, highlightthickness=0, image=girl_photo, command=girlharacter_screen , bg='#F8BC3B', activebackground='#F8BC3B')
    girl_label.place(x=300, y=150, anchor="n")

    # BOY
    girl_img = Image.open('./Assets/char_one.png')
    girl_photo = ImageTk.PhotoImage(girl_img)
    photo_list.append(girl_photo)  # add photo object to the list
    girl_label = Button(addcharacter_screen, borderwidth=0, highlightthickness=0, image=girl_photo, command=boyharacter_screen , bg='#F8BC3B', activebackground='#F8BC3B')
    girl_label.place(x=500, y=150, anchor="n")

    # DOG
    dog_img = Image.open('./Assets/char_three.png')
    dog_photo = ImageTk.PhotoImage(dog_img)
    photo_list.append(dog_photo)  # add photo object to the list
    dog_label = Button(addcharacter_screen, borderwidth=0, highlightthickness=0, image=dog_photo, command=dogharacter_screen, bg='#F8BC3B', activebackground='#F8BC3B')
    dog_label.place(x=700, y=150, anchor="n")
    #=================================================================================================

# Girl Character
def girlharacter_screen ():
    girlharacter_screen = tk.Toplevel(app)
    girlharacter_screen.title("Characters")
    girlharacter_screen.grab_set()
    girlharacter_screen.geometry("1832x932")
    girlharacter_screen.configure(bg='#F8BC3B')
    
    # GIRL HAPPY
    girl1_img = Image.open('./Assets/girl_happy_small.png')
    girl1_photo = ImageTk.PhotoImage(girl1_img)
    photo_list.append(girl1_photo)  # add photo object to the list
    girl1_label = Button(girlharacter_screen, borderwidth=0, highlightthickness=0, image=girl1_photo, command=lambda: print("Girl 1"),bg='#F8BC3B', activebackground='#F8BC3B')
    girl1_label.place(x=300, y=100, anchor="n")

    # GIRL SAD
    girl2_img = Image.open('./Assets/girl_sad_small.png')
    girl2_photo = ImageTk.PhotoImage(girl2_img)
    photo_list.append(girl2_photo)  # add photo object to the list
    girl2_label = Button(girlharacter_screen, borderwidth=0, highlightthickness=0, image=girl2_photo, command=lambda: print("Girl 2"), bg='#F8BC3B', activebackground='#F8BC3B')
    girl2_label.place(x=500, y=100, anchor="n")

    # GIRL ANGRY
    girl3_img = Image.open('./Assets/girl_angry_small.png')
    girl3_photo = ImageTk.PhotoImage(girl3_img)
    photo_list.append(girl3_photo)  # add photo object to the list
    girl3_label = Button(girlharacter_screen, borderwidth=0, highlightthickness=0, image=girl3_photo, command=lambda: print("Girl 2"), bg='#F8BC3B', activebackground='#F8BC3B')
    girl3_label.place(x=700, y=100, anchor="n")

    # GIRL SURRPISED
    girl4_img = Image.open('./Assets/girl_surprised_small.png')
    girl4_photo = ImageTk.PhotoImage(girl4_img)
    photo_list.append(girl4_photo)  # add photo object to the list
    girl4_label = Button(girlharacter_screen, borderwidth=0, highlightthickness=0, image=girl4_photo, command=lambda: print("Girl 4"), bg='#F8BC3B', activebackground='#F8BC3B')
    girl4_label.place(x=900, y=100, anchor="n")

    # GIRL 5
    girl5_img = Image.open('./Assets/backbutton.png')
    girl5_photo = ImageTk.PhotoImage(girl5_img)
    photo_list.append(girl5_photo)  # add photo object to the list
    girl5_label = Button(girlharacter_screen, borderwidth=0, highlightthickness=0, image=girl5_photo, command=lambda: print("Girl 5"), bg='#F8BC3B', activebackground='#F8BC3B')
    girl5_label.place(x=300, y=500, anchor="n")

    # GIRL 6
    girl6_img = Image.open('./Assets/backbutton.png')
    girl6_photo = ImageTk.PhotoImage(girl6_img)
    photo_list.append(girl6_photo)  # add photo object to the list
    girl6_label = Button(girlharacter_screen, borderwidth=0, highlightthickness=0, image=girl6_photo, command=lambda: print("Girl 6"), bg='#F8BC3B', activebackground='#F8BC3B')
    girl6_label.place(x=500, y=500, anchor="n")

    # GIRL 7
    girl7_img = Image.open('./Assets/backbutton.png')
    girl7_photo = ImageTk.PhotoImage(girl7_img)
    photo_list.append(girl7_photo)  # add photo object to the list
    girl7_label = Button(girlharacter_screen, borderwidth=0, highlightthickness=0, image=girl7_photo, command=lambda: print("Girl 7"), bg='#F8BC3B', activebackground='#F8BC3B')
    girl7_label.place(x=700, y=500, anchor="n")

    # GIRL 8
    girl8_img = Image.open('./Assets/backbutton.png')
    girl8_photo = ImageTk.PhotoImage(girl8_img)
    photo_list.append(girl8_photo)  # add photo object to the list
    girl8_label = Button(girlharacter_screen, borderwidth=0, highlightthickness=0, image=girl8_photo, command=lambda: print("Girl 8"), bg='#F8BC3B', activebackground='#F8BC3B')
    girl8_label.place(x=900, y=500, anchor="n")


# Boy Character
def boyharacter_screen ():
    boyharacter_screen = tk.Toplevel(app)
    boyharacter_screen.title("Characters")
    boyharacter_screen.grab_set()
    boyharacter_screen.geometry("1832x932")
    boyharacter_screen.configure(bg='#F8BC3B')
    
    # boy happy
    boy1_img = Image.open('./Assets/boy_happy_small.png')
    boy1_photo = ImageTk.PhotoImage(boy1_img)
    photo_list.append(boy1_photo)  # add photo object to the list
    boy1_label = Button(boyharacter_screen, borderwidth=0, highlightthickness=0, image=boy1_photo, command=lambda: print("boy 1"),bg='#F8BC3B', activebackground='#F8BC3B')
    boy1_label.place(x=300, y=100, anchor="n")

    # boy sad
    boy2_img = Image.open('./Assets/boy_sad_small.png')
    boy2_photo = ImageTk.PhotoImage(boy2_img)
    photo_list.append(boy2_photo)  # add photo object to the list
    boy2_label = Button(boyharacter_screen, borderwidth=0, highlightthickness=0, image=boy2_photo, command=lambda: print("boy 2"),bg='#F8BC3B', activebackground='#F8BC3B')
    boy2_label.place(x=500, y=100, anchor="n")

    # boy angry
    boy3_img = Image.open('./Assets/boy_angry_small.png')
    boy3_photo = ImageTk.PhotoImage(boy3_img)
    photo_list.append(boy3_photo)  # add photo object to the list
    boy3_label = Button(boyharacter_screen, borderwidth=0, highlightthickness=0, image=boy3_photo, command=lambda: print("boy 2"),bg='#F8BC3B', activebackground='#F8BC3B')
    boy3_label.place(x=700, y=100, anchor="n")

    # boy surprised
    boy4_img = Image.open('./Assets/boy_surprised_small.png')
    boy4_photo = ImageTk.PhotoImage(boy4_img)
    photo_list.append(boy4_photo)  # add photo object to the list
    boy4_label = Button(boyharacter_screen, borderwidth=0, highlightthickness=0, image=boy4_photo, command=lambda: print("boy 4"),bg='#F8BC3B', activebackground='#F8BC3B')
    boy4_label.place(x=900, y=100, anchor="n")

    # boy 5
    boy5_img = Image.open('./Assets/backbutton.png')
    boy5_photo = ImageTk.PhotoImage(boy5_img)
    photo_list.append(boy5_photo)  # add photo object to the list
    boy5_label = Button(boyharacter_screen, borderwidth=0, highlightthickness=0, image=boy5_photo, command=lambda: print("boy 5"), bg='#F8BC3B', activebackground='#F8BC3B')
    boy5_label.place(x=300, y=500, anchor="n")

    # boy 6
    boy6_img = Image.open('./Assets/backbutton.png')
    boy6_photo = ImageTk.PhotoImage(boy6_img)
    photo_list.append(boy6_photo)  # add photo object to the list
    boy6_label = Button(boyharacter_screen, borderwidth=0, highlightthickness=0, image=boy6_photo, command=lambda: print("boy 6"), bg='#F8BC3B', activebackground='#F8BC3B')
    boy6_label.place(x=500, y=500, anchor="n")

    # boy 7
    boy7_img = Image.open('./Assets/backbutton.png')
    boy7_photo = ImageTk.PhotoImage(boy7_img)
    photo_list.append(boy7_photo)  # add photo object to the list
    boy7_label = Button(boyharacter_screen, borderwidth=0, highlightthickness=0, image=boy7_photo, command=lambda: print("boy 7"), bg='#F8BC3B', activebackground='#F8BC3B')
    boy7_label.place(x=700, y=500, anchor="n")

    # boy 8
    boy8_img = Image.open('./Assets/backbutton.png')
    boy8_photo = ImageTk.PhotoImage(boy8_img)
    photo_list.append(boy8_photo)  # add photo object to the list
    boy8_label = Button(boyharacter_screen, borderwidth=0, highlightthickness=0, image=boy8_photo, command=lambda: print("boy 8"), bg='#F8BC3B', activebackground='#F8BC3B')
    boy8_label.place(x=900, y=500, anchor="n")


# Dog Character  
def dogharacter_screen ():
    dogharacter_screen = tk.Toplevel(app)
    dogharacter_screen.title("Characters")
    dogharacter_screen.grab_set()
    dogharacter_screen.geometry("1832x932")
    dogharacter_screen.configure(bg='#F8BC3B')
    
    # dog happy
    dog1_img = Image.open('./Assets/dog_happy_small.png')
    dog1_photo = ImageTk.PhotoImage(dog1_img)
    photo_list.append(dog1_photo)  # add photo object to the list
    dog1_label = Button(dogharacter_screen, borderwidth=0, highlightthickness=0, image=dog1_photo, command=lambda: print("dog_happy_small"), bg='#F8BC3B', activebackground='#F8BC3B')
    dog1_label.place(x=300, y=100, anchor="n")

    # dog sad
    dog2_img = Image.open('./Assets/dog_sad_small.png')
    dog2_photo = ImageTk.PhotoImage(dog2_img)
    photo_list.append(dog2_photo)  # add photo object to the list
    dog2_label = Button(dogharacter_screen, borderwidth=0, highlightthickness=0, image=dog2_photo, command=lambda: print("dog 2"), bg='#F8BC3B', activebackground='#F8BC3B')
    dog2_label.place(x=500, y=100, anchor="n")

    # dog angry
    dog3_img = Image.open('./Assets/dog_angry_small.png')
    dog3_photo = ImageTk.PhotoImage(dog3_img)
    photo_list.append(dog3_photo)  # add photo object to the list
    dog3_label = Button(dogharacter_screen, borderwidth=0, highlightthickness=0, image=dog3_photo, command=lambda: print("dog 2"), bg='#F8BC3B', activebackground='#F8BC3B')
    dog3_label.place(x=700, y=100, anchor="n")
    
    # dog surprised
    dog4_img = Image.open('./Assets/dog_surprised_small.png')
    dog4_photo = ImageTk.PhotoImage(dog4_img)
    photo_list.append(dog4_photo)  # add photo object to the list
    dog4_label = Button(dogharacter_screen, borderwidth=0, highlightthickness=0, image=dog4_photo, command=lambda: print("dog 4"), bg='#F8BC3B', activebackground='#F8BC3B')
    dog4_label.place(x=900, y=100, anchor="n")

    # dog 5
    dog5_img = Image.open('./Assets/backbutton.png')
    dog5_photo = ImageTk.PhotoImage(dog5_img)
    photo_list.append(dog5_photo)  # add photo object to the list
    dog5_label = Button(dogharacter_screen, borderwidth=0, highlightthickness=0, image=dog5_photo, command=lambda: print("dog 5"), bg='#F8BC3B', activebackground='#F8BC3B')
    dog5_label.place(x=300, y=500, anchor="n")

    # dog 6
    dog6_img = Image.open('./Assets/backbutton.png')
    dog6_photo = ImageTk.PhotoImage(dog6_img)
    photo_list.append(dog6_photo)  # add photo object to the list
    dog6_label = Button(dogharacter_screen, borderwidth=0, highlightthickness=0, image=dog6_photo, command=lambda: print("dog 6"), bg='#F8BC3B', activebackground='#F8BC3B')
    dog6_label.place(x=500, y=500, anchor="n")

    # dog 7
    dog7_img = Image.open('./Assets/backbutton.png')
    dog7_photo = ImageTk.PhotoImage(dog7_img)
    photo_list.append(dog7_photo)  # add photo object to the list
    dog7_label = Button(dogharacter_screen, borderwidth=0, highlightthickness=0, image=dog7_photo, command=lambda: print("dog 7"), bg='#F8BC3B', activebackground='#F8BC3B')
    dog7_label.place(x=700, y=500, anchor="n")

    # dog 8
    dog8_img = Image.open('./Assets/backbutton.png')
    dog8_photo = ImageTk.PhotoImage(dog8_img)
    photo_list.append(dog8_photo)  # add photo object to the list
    dog8_label = Button(dogharacter_screen, borderwidth=0, highlightthickness=0, image=dog8_photo, command=lambda: print("dog 8"), bg='#F8BC3B', activebackground='#F8BC3B')
    dog8_label.place(x=900, y=500, anchor="n")




# ___________________________________________________________________________ MAIN TKINTER UI ___________________________________________________________________________
# Create the app
app = ctk.CTk()
app.title("Pictales")
app.geometry("1832x932")
ctk.set_appearance_mode("F9F4F1")

# ___________________________________________________________________________
# Set background of window 1
bg_img = Image.open('./Assets/AppBG.png')
bg_img_photo = ImageTk.PhotoImage(bg_img)
bg_img_label = Label (app,image = bg_img_photo)
bg_img_label.place(x=0, y=0)

# Load and display the logo image on the canvas 
logo_image = Image.open('./Assets/frame0/image_1.png') 
logo_photo = ImageTk.PhotoImage(logo_image) 
logo_label = Label(app, image=logo_photo) 
logo_label.place(x=800, y=90) 

# load and display start button
start_button = Image.open('./Assets/frame0/button_3.png')
start_photo = ImageTk.PhotoImage(start_button)
start_button = Button(app, image=start_photo, borderwidth=0, highlightthickness=0, command=title_window)
start_button.place(x=770, y=530)

# load and display howto button
howTo_button = Image.open('./Assets/frame0/button_2.png')
howTo_photo = ImageTk.PhotoImage(howTo_button)
howTo_button = Button(app, image=howTo_photo, borderwidth=0, highlightthickness=0, command=howTo_window)
howTo_button.place(x=770, y=690)

# load about button 
about_button = Image.open('./Assets/frame0/button_1.png')
about_photo = ImageTk.PhotoImage(about_button)
photo_list.append(about_photo)  # add photo object to the list
about_button = Button(app, image=about_photo, borderwidth=0, highlightthickness=0, command=about_window)
about_button.place(x=50, y=50) 

# ___________________________________________________________________________ DRIVER CODE ___________________________________________________________________________
# Get text input prompts again by automatically restarting the app
app.mainloop()




