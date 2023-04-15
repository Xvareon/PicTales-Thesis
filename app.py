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
            # (COMMENT OUT THIS LINE) FOR USING GUI WITHOUT AI TESTING ONLY!
            image = blank
            cartoon_input = "cartoonish " + text_input
            # Variable that contains the image result
            # image = pipe(cartoon_input, guidance_scale=10)[
            #     "images"][0]

    # Store image in a variable
    img = ImageTk.PhotoImage(image)

    # Displays the text input in the Tkinter UI after generation
    ltext.configure(text=text_input)
    ltext.update()

    # # Displays the image in the Tkinter UI after generation
    lmain.configure(image=img)
    lmain.update()


# Function for getting the character selected WITH the expressions, essentially the image we pass for saving a page.
def funct_main_char_select(main_char_value, main_char_image):

    # Globalize the value of character selection WITH the expressions
    global main_char_select

    # Store the character in a variable
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
        image.save('./GeneratedImages/{}.png'.format(text_input.strip()))

        ##################################################################
        # base = Image.open(
        #     './GeneratedImages/{}.png'.format(text_input.strip()))
        # # Select the character image from the folder pathfile
        # # Location where the character image will be pasted into which then pastes it.
        # base.paste(character, (0, 360), character.convert('RGBA'))
        # base.save('./GeneratedImages/{}.png'.format(text_input.strip()))

        # Load the base image on which the character will be pasted
        base = Image.open(
            './GeneratedImages/{}.png'.format(text_input.strip())).convert('RGBA')

        # Convert the PhotoImage object to a PIL Image object and convert to RGBA mode
        character_image = ImageTk.getimage(character).convert('RGBA')

        # Create a new transparent image of the same size as the base image
        result = Image.new('RGBA', base.size, (0, 0, 0, 0))

        # Paste the base image onto the new image
        result.paste(base, (0, 0))

        # Paste the character image onto the new image using alpha_composite
        result.alpha_composite(character_image, dest=(0, 360))

        # Save the result image to disk
        result.save('./GeneratedImages/{}.png'.format(text_input.strip()))

        ##################################################################

        i = 0  # Instantiate i for loops (text item positioning)
        j = 0  # Instantiate j for loops (pic positioning)

        content = edit_textcontent_area.get('1.0', tk.END)

        # Makes the text input as a default content input if the user did not enter anything at the content textbox.
        if (content == ''):
            content = text_input

        # Add the content to the list
        content_list.append(content)

        # Add the previously stored text in a list
        text_list.append(text_input)

        # Store image in image variable if no character is selected and store it in base variable if a character is selected (For previews)
        if char_select == 0:
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

        # Destroy the edit content window and generate window
        # app_save.destroy()
        addcharacter_screen.destroy()
        generate_window.destroy()


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
    modal_label = tk.Label(about_window, text='ABOUT',
                           font=custom_font, fg='white', bg='#F8BC3B')
    modal_label.pack(pady=50)

    # this block of code show the logo PICTALES and resize it, and append the image to be seen coz of resizing
    about_img = Image.open('./Assets/PICTALES LOGO Big w background.png')
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
    # to change soon if video pictales is available
    player = tkvideo.tkvideo("./Assets/sample.mp4",
                             my_label, loop=1,  size=(820, 420))
    # change the function to play or stop the video
    player.play()

    # Center the label/video in the window
    my_label.place(x=520, y=300, anchor="center")

    howTo_window.resizable(False, False)


def funct_generate_window():    # This window is for getting the text prompt and image generated result from that prompt

    # Globalized to be destroyed at the click of the save button in edit_content_page function
    global generate_window
    generate_window = tk.Toplevel(app)  # pop up the window how to in top level
    generate_window.title("Prompt")
    generate_window.grab_set()
    # the geometry with app winfo width and height will center the window modal in main screen
    generate_window.geometry("1228x739+{}+{}".format(
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

    # Generate button
    trigger_photo = ImageTk.PhotoImage(
        Image.open('./Assets/frame0/Generate Button.png'))
    photo_list.append(trigger_photo)  # add photo object to the list
    trigger_label = Button(generate_window, image=trigger_photo, borderwidth=0,
                           highlightthickness=0, bg='#F8BC3B', activebackground='#F8BC3B', command=generate_image)
    trigger_label.place(x=110, y=620)

    global ltext  # Globalize to pass on generate image function
    ltext = ctk.CTkLabel(generate_window, height=15, width=46, text="Image Title", font=(
        "Supersonic Rocketship", 20), text_color="black")
    ltext.place(x=60, y=600)

    # EDIT CONTENT PHOTO
    edit_content_photo = ImageTk.PhotoImage(
        Image.open('./Assets/addStory_Button.png'))
    photo_list.append(edit_content_photo)  # add photo object to the list
    edit_content_label = Button(generate_window, image=edit_content_photo, borderwidth=0, highlightthickness=0,
                                bg='#F8BC3B', activebackground='#F8BC3B', command=edit_content_page)
    edit_content_label.place(x=900, y=623)


def title_window():  # Window to get author and title data in entry window 2

    global start_window  # Globalize to be destroyed at the opening of the main operating window
    # Window 2 config start / ctk window
    start_window = ctk.CTkToplevel(app)
    start_window.title("Title and Author")
    start_window.grab_set()
    start_window.geometry("1832x932")
    start_window.configure(bg="#F9F4F1")

    # Create a canvas widget
    canvas = Canvas(start_window, bg="#F9F4F1", height=932,
                    width=1832, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    # Author Textbox
    entry_1 = ctk.CTkEntry(start_window, width=1029.0, height=85.0, bg_color="#F9F4F1", font=(
        "Arial", 20), text_color="black", border_width=10, border_color="#DDC8A0")
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
    entry_2 = ctk.CTkEntry(start_window, width=1029.0, height=85.0, bg_color="#F9F4F1", font=(
        "Arial", 20), text_color="black", border_width=10, border_color="#DDC8A0")
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
    button1_photo = ImageTk.PhotoImage(
        Image.open('./Assets/window2/button_1.png'))
    button_1 = Button(
        start_window,
        image=button1_photo,
        borderwidth=0,
        command=start_window.destroy,
        highlightthickness=0,
        relief="flat"
    )
    button_1.place(
        x=765.0,
        y=765.0,
        width=93.0,
        height=103.0
    )

    # Check Green Button
    button2_photo = ImageTk.PhotoImage(
        Image.open('./Assets/window2/button_2.png'))
    button_2 = Button(
        start_window,
        image=button2_photo,
        borderwidth=0,
        highlightthickness=0,
        command=main_operating_screen,
        relief="flat",
    )
    button_2.place(
        x=957.0,
        y=765.0,
        width=93.0,
        height=103.0
    )

    # Handle the window's screen updates
    start_window.resizable(False, False)
    start_window.mainloop()

# ==============================


def main_operating_screen():  # Main Operating Screen window 3

    start_window.destroy()  # Destroy the start window (with the author and title data entry)

    main_operating_screen = tk.Toplevel(app)
    main_operating_screen.title("Main Operating Screen")
    main_operating_screen.grab_set()
    main_operating_screen.geometry("1832x932")
    main_operating_screen.configure(bg='#F9F4F1')

    # Back button to title and author
    back_photo = ImageTk.PhotoImage(Image.open('./Assets/backbutton.png'))
    photo_list.append(back_photo)  # add photo object to the list
    back_label = Button(main_operating_screen, borderwidth=0, highlightthickness=0,
                        image=back_photo, command=main_operating_screen.destroy)
    back_label.place(x=100, y=50, anchor="n")

    # Will be the title based on the output of the user
    pictales_title = tk.Label(main_operating_screen, text='Title of Pictales',
                              font=custom_font, fg='#F8BC3B', bg='#F9F4F1')
    pictales_title.place(x=200, y=50)
    pictales_title.config(font=("Supersonic Rocketship", 60))

    # Add page button
    addpage_photo = ImageTk.PhotoImage(Image.open('./Assets/addbutton.png'))
    photo_list.append(addpage_photo)  # add photo object to the list
    addpage_label = Button(main_operating_screen, borderwidth=0,
                           highlightthickness=0, image=addpage_photo, command=funct_generate_window, bg='#F9F4F1', activebackground='#F8BC3B')
    addpage_label.place(x=300, y=250, anchor="n")

    # Redirecting to modal window for Generating image // Create Pictales button in window 3
    createpictales_photo = ImageTk.PhotoImage(
        Image.open('./Assets/createpictales.png'))
    photo_list.append(createpictales_photo)  # add photo object to the list
    createpictales_label = Button(main_operating_screen, borderwidth=0,
                                  highlightthickness=0, image=createpictales_photo, command=clarification_window)
    # createpictales_label = Button(main_operating_screen, borderwidth=0,
    #                               highlightthickness=0, image=createpictales_photo, command=pdf_window)
    createpictales_label.place(x=1450, y=50, anchor="n")


def clarification_window():  # Clarification Window pops up before creating the pictales pdf window 5
    clarification_window = tk.Toplevel(app)
    clarification_window.title('Are you sure?')
    clarification_window.grab_set()
    clarification_window.geometry("690x603+{}+{}".format(
        app.winfo_width()//2 - 378 + app.winfo_rootx(),
        app.winfo_height()//2 - 372 + app.winfo_rooty()
    ))
    clarification_window.configure(bg='#F8BC3B')  # set background color

    # Set the clarification label on the window
    clear_label = tk.Label(clarification_window, text='ARE YOU SURE TO \n REDISCOVER YOUR STORY AND \n CREATE YOUR OWN PICTALES?',
                           font=custom_font, fg='white', bg='#F8BC3B')
    clear_label.place(x=40, y=50)

    # set the font of the label to Supersonic Rocketship with a size of 20
    clear_label.config(font=("Supersonic Rocketship", 34))

    # X Button // Close the clarification window
    close_photo = ImageTk.PhotoImage(
        Image.open('./Assets/window2/button_1.png'))
    photo_list.append(close_photo)  # add photo object to the list
    no_button = Button(clarification_window, image=close_photo, command=clarification_window.destroy,
                       background='#F8BC3B', borderwidth=0, highlightthickness=0, activebackground='#F8BC3B')
    no_button.place(x=200, y=400)

    # v/ Button // Generate PDF File
    open_photo = ImageTk.PhotoImage(
        Image.open('./Assets/window2/button_2.png'))
    photo_list.append(open_photo)  # add photo object to the list
    yes_button = Button(clarification_window, image=open_photo, command=lambda: generate_pdf,
                        background='#F8BC3B', borderwidth=0, highlightthickness=0, activebackground='#F8BC3B')
    yes_button.place(x=400, y=400)


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


def edit_content_page():  # Add edit the page content window 5.1

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
    save_photo = ImageTk.PhotoImage(Image.open('./Assets/frame0/save.png'))
    photo_list.append(save_photo)  # add photo object to the list
    save_label = Button(addcharacter_screen, image=save_photo, borderwidth=0, highlightthickness=0,
                        bg='#F8BC3B', activebackground='#F8BC3B', command=generate_save)
    save_label.place(x=1250, y=800)


def character_expression_window():  # Boy Character
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


# ___________________________________________________________________________ MAIN TKINTER UI ___________________________________________________________________________
# Create the app
app = ctk.CTk()
app.title("Pictales")
app.geometry("1832x932")
ctk.set_appearance_mode("F9F4F1")
# Set the app geometry to fit the screen
# app.update_idletasks()
# w = app.winfo_screenwidth()
# h = app.winfo_screenheight()
# app.geometry("%dx%d+0+0" % (w, h))
# ___________________________________________________________________________
# Set background of window 1
bg_img_photo = ImageTk.PhotoImage(Image.open('./Assets/AppBG.png'))
bg_img_label = Label(app, image=bg_img_photo)
bg_img_label.place(x=0, y=0)

# Load and display the logo image on the canvas in window 1
logo_photo = ImageTk.PhotoImage(Image.open('./Assets/frame0/image_1.png'))
logo_label = Label(app, image=logo_photo)
logo_label.place(x=800, y=90)

# load and display start button
start_photo = ImageTk.PhotoImage(Image.open('./Assets/frame0/button_3.png'))
start_button = Button(app, image=start_photo, borderwidth=0,
                      highlightthickness=0, command=title_window)
start_button.place(x=770, y=530)

# load and display howto button
howTo_photo = ImageTk.PhotoImage(Image.open('./Assets/frame0/button_2.png'))
howTo_button = Button(app, image=howTo_photo, borderwidth=0,
                      highlightthickness=0, command=howTo_window)
howTo_button.place(x=770, y=690)

# Question Mark in Window 1/ Main Window
about_icon = ImageTk.PhotoImage(Image.open('./Assets/frame0/button_1.png'))
photo_list.append(about_icon)  # add photo object to the list
about_button = Button(app, image=about_icon, borderwidth=0,
                      highlightthickness=0, command=about_window)
about_button.place(x=50, y=50)

# Testing Phase - Background transparency window 1
# ___________________________________________________________________________ DRIVER CODE ___________________________________________________________________________
# Get text input prompts again by automatically restarting the app
app.mainloop()
