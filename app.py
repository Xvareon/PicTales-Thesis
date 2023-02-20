# Python packages and dependencies are needed for the application to run. Installed through PIP in VSCode terminal (Todo: automatically install these with the app with PyInstaller)

#########################################################
# TO-DO LIST FOR THE BREAK:

# Paragraph input chop chop
# Put watercolor, children's storybook, Drawing
# PicTales options basic and advanced
# Inject authentication entry in main code, also combine the authtoken.py with the main app
# Update storyboard with the characters (images = base)
# TITLE PAGE WITH TITLE AND AUTHOR
# Upload self created character
# PDF MUST BE AUTOMATICALLY 2 PAGE
# NEEDS UI that shows storybook has been created and exit the program
# UI OVERHAUL
#########################################################

# ___________________________________________________________________________ DEPENDENCIES ___________________________________________________________________________
# Import Tkinter for Python UI
import tkinter as tk

# Import CustomTkinter for additional Tkinter configurations
import customtkinter as ctk

# Import Pillow or PIL for image configurations in Tkinter
from PIL import ImageTk, Image, ImageDraw, ImageFont, ImageFilter

# Import auth_token for Token authentication that will be mostly used from tokens in Huggingface website account
from authtoken import auth_token

# Import Pytorch for the neural networks used in machine learning and AI
import torch
from torch import autocast

# Import StableDiffusionPipeline for the stable diffusion methods that are used in the local GPU.
from diffusers import StableDiffusionPipeline

# Provides functions for interacting with the operating system
import os
import sys

# ___________________________________________________________________________ GLOBAL VARIABLES ___________________________________________________________________________

image_list = []  # ARRAY OF IMAGES
text_list = []  # ARRAY OF TEXT INPUTS
content_list = []  # ARRAY OF PAGE CONTENT (mostly the text)
pdf_list = []  # ARRAY OF PDF PAGES

# ___________________________________________________________________________ MODEL ___________________________________________________________________________

# Loads the model
model = torch.load('./results/model-1.pt')
# print(model)
# model.eval()

# ___________________________________________________________________________ FUNCTIONS ___________________________________________________________________________


def generate_image():  # Function to generate the images from the text prompt

    global img  # For storing the image to avoid garbage collection

    global text_input  # For storing the text input to transfer to the Picture Book PDF

    global image  # For storing image to be saved if save image button is clicked

    # Uses the GPU to process the dataset through the model and get the image result
    with autocast(device):

        # Note: ADD A CATCH ERROR IF THE INPUT IS BLANK
        text_input = prompt.get()  # Store text input in a variable

        image = pipe(text_input, guidance_scale=10)[
            "images"][0]  # Variable that contains the image result. ("images" was previously labeled as "sample")

    # Store image in a variable
    img = ImageTk.PhotoImage(image)

    # Displays the text input in the Tkinter UI after generation
    ltext.configure(text=text_input)
    ltext.update()

    # Displays the image in the Tkinter UI after generation
    lmain.configure(image=img)
    lmain.update()


def save_window():

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

    global char_select    # Declare value for radio selection

    # Window object for the text prompt for naming the book
    app_save = ctk.CTkToplevel(app)
    app_save.title("Edit Content Page")
    app_save.geometry("1832x932")
    ctk.set_appearance_mode("dark")

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
    char_one = ImageTk.PhotoImage(Image.open('./Characters/char_one.png'))
    char_two = ImageTk.PhotoImage(Image.open('./Characters/char_two.png'))
    char_three = ImageTk.PhotoImage(Image.open('./Characters/char_three.png'))

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


def generate_save():  # Saves the image in the current directory and displays the current images selected for the picture book

    # Check if user has already generated an image first before saving.
    try:
        image
    except NameError:  # If variable image is empty, return false
        is_generated = False
    else:  # If image variable is defined
        is_generated = True

    # If an image has been generated
    if is_generated:

        # Globalize content variable that stores the edited content
        global content

        global character  # Store the character in a variable

        global base  # Store the base image on which the character would be pasted on

        # Save image file name as PNG based on text input
        image.save('./GeneratedImages/{}.png'.format(text_input))

        if char_select.get() == 1:  # If character one was selected

            base = Image.open('./GeneratedImages/{}.png'.format(text_input))
            # Select the character image from the folder pathfile
            character = Image.open('./Characters/char_one.png')
            # Location where the character image will be pasted into which then pastes it.
            base.paste(character, (0, 360), character.convert('RGBA'))
            base.save('./GeneratedImages/{}.png'.format(text_input))

        if char_select.get() == 2:  # If character two was selected

            base = Image.open('./GeneratedImages/{}.png'.format(text_input))
            # Select the character image from the folder pathfile
            character = Image.open('./Characters/char_two.png')
            # Location where the character image will be pasted into which then pastes it.
            base.paste(character, (0, 360), character.convert('RGBA'))
            base.save('./GeneratedImages/{}.png'.format(text_input))

        if char_select.get() == 3:  # If character three was selected

            base = Image.open('./GeneratedImages/{}.png'.format(text_input))
            # Select the character image from the folder pathfile
            character = Image.open('./Characters/char_three.png')
            # Location where the character image will be pasted into which then pastes it.
            base.paste(character, (0, 360), character.convert('RGBA'))
            base.save('./GeneratedImages/{}.png'.format(text_input))

        i = 0  # Instantiate i for loops
        j = 0  # Instantiate j for loops

        content = prompt_save.get("0.0", "end")

        # Makes the text input as a default content input if the user did not enter anything at the content textbox.
        if (content == ''):
            content = text_input

        # Add the content to the list
        content_list.append(content)

        # Add the previously stored text in a list
        text_list.append(text_input)

        # Store image in a variable
        # img = ImageTk.PhotoImage(image)
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
            # Placeholder frame for the text input LISTS
            # pic = pic.resize((200, 200))
            limg_list = ctk.CTkLabel(app, height=200, width=200, image=pic)
            limg_list.place(x=1200, y=-100 + (200*i))

        app_save.destroy()  # Destroy the edit content window


def pdf_window():  # Show a text prompt

    global app_pdf  # Globalize the window object that pops up for pdf creation
    global prompt_pdf  # The variable that stores the textbox object for naming the storybook

    # Window object for the text prompt for naming the book
    app_pdf = ctk.CTkToplevel(app)
    app_pdf.title("Set Storybook Name")
    app_pdf.geometry("512x512")
    ctk.set_appearance_mode("dark")

    # Tkinter UI for the textbox prompt
    prompt_pdf = ctk.CTkEntry(app_pdf, height=40, width=400, font=(
        "Arial", 20), text_color="black", fg_color="white")
    prompt_pdf.place(x=6, y=10)

    # Tkinter Widget for the button
    create_pdf = ctk.CTkButton(app_pdf, height=40, width=120, font=(
        "Arial", 20), text_color="white", fg_color="blue", command=generate_pdf)
    create_pdf.configure(text="Generate {}".format('Storybook'))
    create_pdf.place(x=140, y=60)


def generate_pdf():  # Generate PicTale Story book

    pdf_name = prompt_pdf.get()  # Store text input in a variable, from the pdf window

    # Store the pdf file name into a variable, sets this as default for errors and etc like if the title name is not set.
    if (pdf_name == ''):
        pdf_name = 'PicTales'

    # Specifies the directory where the pdf will generate
    pdf_path = "./StoryBooks/{}.pdf".format(pdf_name)

    # # Create template page
    # blank = Image.new('RGB', (512, 512))

    # # Save template in generated images folder
    # blank.save('./GeneratedImages/TextTemplate.png')

    i = 0  # Pointer/Flag for content for content list access later

    # For each image file that has been written with the text list names, the text list names their files itself based on order.
    for file in text_list:

        # # Store blank image in a variable
        # photo = Image.open('./GeneratedImages/TextTemplate.png')

        # Store Generated image in a variable to be used as the text background
        photo = Image.open('./GeneratedImages/{}.png'.format(file))

        photo = photo.filter(ImageFilter.GaussianBlur(20)
                             )  # Blur the stored image

        # Invoke draw function to the blank image
        phototext = ImageDraw.Draw(photo)

        # Choose font
        font = ImageFont.truetype('arial.ttf', 16)

        bbox = phototext.textbbox(  # Make a rectangle background for the text
            (10, 10), content_list[i], font=font)
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

    if pdf_list:  # Check if storybook has content
        # Generate the PDF
        pdf_list[0].save(
            pdf_path, "PDF", resolution=100.0, save_all=True, append_images=pdf_list[1:]
        )

    app_pdf.destroy()  # Destroy the rename window


# ___________________________________________________________________________ CONFIGURATIONS ___________________________________________________________________________
isExist = os.path.exists('./results/model-1.pt')

if (isExist == False):
    sys.exit(0)

# loads the model used to a pre-defined library online
modelid = "CompVis/stable-diffusion-v1-4"

# Specifies the graphics driver to be used
device = "cuda"

# Loads the model into torch
torch.load('./results/model-1.pt')

# Uses the pipe from the online library for model translation to produce the image.
pipe = StableDiffusionPipeline.from_pretrained(
    modelid, revision="fp16", torch_dtype=torch.float16, use_auth_token=auth_token)

# Uses the graphics driver (Must atleast be 4GB ram)
pipe.to(device)

# ___________________________________________________________________________ MAIN TKINTER UI ___________________________________________________________________________
# Create the app
app = ctk.CTk()
app.title("Pictales")
app.geometry("1832x932")
ctk.set_appearance_mode("dark")

# Button for submitting the text input prompts and its configurations via position
trigger = ctk.CTkButton(app, height=40, width=120, font=(
    "Arial", 20), text_color="white", fg_color="blue", command=generate_image)
trigger.configure(text="Generate")
trigger.place(x=206, y=60)

# Tkinter UI for the textbox prompt
prompt = ctk.CTkEntry(app, height=40, width=512, font=(
    "Arial", 20), text_color="black", fg_color="white")
prompt.place(x=10, y=10)

# Placeholder frame for image result generated
lmain = ctk.CTkLabel(app, height=512, width=512)
lmain.place(x=10, y=110)

# Placeholder frame for the text input
ltext = ctk.CTkLabel(app, height=100, width=512, text="TEST", font=(
    "Arial", 20), text_color="white", fg_color="blue")
ltext.place(x=10, y=600)

# Button for creating pdf
create = ctk.CTkButton(app, height=40, width=120, font=(
    "Arial", 20), text_color="white", fg_color="blue", command=pdf_window)
create.configure(text="Create PicTales")
create.place(x=206, y=800)

# Button for saving image
# save_image = ctk.CTkButton(height=40, width=120, text_font=(
#     "Arial", 20), text_color="white", fg_color="blue", command=generate_save)
save_image = ctk.CTkButton(app, height=40, width=120, font=(
    "Arial", 20), text_color="white", fg_color="blue", command=save_window)
save_image.configure(text="Save Image")
save_image.place(x=206, y=725)

# ___________________________________________________________________________ DRIVER CODE ___________________________________________________________________________
# Get text input prompts again by automatically restarting the app
app.mainloop()
