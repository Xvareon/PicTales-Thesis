# Python packages and dependencies are needed for the application to run. Installed through PIP in VSCode terminal (Todo: automatically install these with the app with PyInstaller)

# ___________________________________________________________________________ DEPENDENCIES ___________________________________________________________________________
# Import Tkinter for Python UI
import tkinter as tk

# Import CustomTkinter for additional Tkinter configurations
import customtkinter as ctk

# Import Pillow or PIL for image configurations in Tkinter
from PIL import ImageTk, Image, ImageDraw, ImageFont

# Import auth_token for Token authentication that will be mostly used from tokens in Huggingface website account
from authtoken import auth_token

# Import Pytorch for the neural networks used in machine learning and AI
import torch
from torch import autocast

# Import StableDiffusionPipeline for the stable diffusion methods that are used in the local GPU.
from diffusers import StableDiffusionPipeline

# ___________________________________________________________________________ GLOBAL VARIABLES ___________________________________________________________________________

image_list = []  # ARRAY OF IMAGES
text_list = []  # ARRAY OF TEXT INPUTS
pdf_list = []  # ARRAY OF PDF PAGES

# ___________________________________________________________________________ CONFIGURATIONS ___________________________________________________________________________
# Specifies the model used, can be changed and configured
modelid = "CompVis/stable-diffusion-v1-4"

# Specifies the graphics driver to be used
device = "cuda"

# Uses the dataset from the huggingface website. User can add their own provided they have data and money.
pipe = StableDiffusionPipeline.from_pretrained(
    modelid, revision="fp16", torch_dtype=torch.float16, use_auth_token=auth_token)

# Uses the graphics driver to be used (Must atleast be 4GB ram)
pipe.to(device)

# ___________________________________________________________________________ FUNCTIONS ___________________________________________________________________________


def generate_image():  # Function to generate the images from the text prompt

    global img  # For storing the image to avoid garbage collection

    global text_input  # For storing the text input to transfer to the Picture Book PDF

    global image  # For storing image to be saved if save image button is clicked

    # Uses the GPU to process the dataset through the model and get the image result
    with autocast(device):

        image = pipe(prompt.get(), guidance_scale=10)[
            "images"][0]  # Variable that contains the image result. ("images" was previously labeled as "sample")

        text_input = prompt.get()  # Store text input in a variable

    # Store image in a variable
    img = ImageTk.PhotoImage(image)

    # Displays the text input in the Tkinter UI after generation
    ltext.configure(text=text_input)
    ltext.update()

    # Displays the image in the Tkinter UI after generation
    lmain.configure(image=img)
    lmain.update()


def generate_save():  # Saves the image in the current directory and displays the current images selected for the picture book

    # Save image file name as PNG based on text input
    image.save('./GeneratedImages/{}.png'.format(text_input))

    i = 0  # Instantiate i for loops
    j = 0  # Instantiate j for loops

    # Add the previously stored text in a list
    text_list.append(text_input)

    # Store image in a variable
    img = ImageTk.PhotoImage(image)

    # Store previous image in a list
    image_list.append(img)

    # Displays the text list
    for text_item in text_list:
        j = j+1
        # Placeholder frame for the text input LISTS
        ltext_list = ctk.CTkLabel(height=512, width=512, text=text_item, text_font=(
            "Arial", 12), text_color="white", fg_color="blue")
        ltext_list.place(x=600, y=-100 + (200*j))

    # Displays the image list
    for pic in image_list:
        i = i+1
        # Placeholder frame for the text input LISTS
        # pic = pic.resize((200, 200))
        limg_list = ctk.CTkLabel(height=200, width=200, image=pic)
        limg_list.place(x=1200, y=-100 + (200*i))


def generate_pdf():  # Generate PicTale Story book

    # Specifies the directory where the pdf will generate
    pdf_path = "./StoryBooks/PicTales.pdf"

    # Create template page
    blank = Image.new('RGB', (512, 512))

    # Save template in generated images folder
    blank.save('./GeneratedImages/TextTemplate.png')

    for file in text_list:

        # Store blank image in a variable
        photo = Image.open('./GeneratedImages/TextTemplate.png')

        # Invoke draw function to the blank image
        phototext = ImageDraw.Draw(photo)

        # Choose font
        font = ImageFont.truetype('arial.ttf', 16)

        # Write the text input based on the designated text image
        phototext.text((10, 10), file, font=font, fill=(255, 0, 0))

        # Save the drawn page that contains the text input in the local directory
        photo.save('./GeneratedImages/INPUT{}.png'.format(file))

    # Convert each PhotoImage object files into normal files
    for file in text_list:

        # Append main image file
        pdf_list.append(Image.open(
            './GeneratedImages/{}.png'.format(file)))

        # Append the image file that has the text input drawn on a blank page
        pdf_list.append(Image.open(
            './GeneratedImages/INPUT{}.png'.format(file)))

    # Generate the PDF
    pdf_list[0].save(
        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=pdf_list[1:]
    )

    # NEEDS TO HIDE SAVE BUTTON FOR IMAGE AND PDF
    # NEEDS TO SHOW THE PROGRESS IN THE TKINTER
    # TO DO: MAKE THE TITLE OF THE PDF A VARIABLE


# ___________________________________________________________________________ TKINTER UI ___________________________________________________________________________
# Create the app
app = tk.Tk()
app.title("Pictales")
app.geometry("1832x932")
ctk.set_appearance_mode("dark")

# Button for submitting the text input prompts and its configurations via position
trigger = ctk.CTkButton(height=40, width=120, text_font=(
    "Arial", 20), text_color="white", fg_color="blue", command=generate_image)
trigger.configure(text="Generate")
trigger.place(x=206, y=60)

# Tkinter UI for the textbox prompt
prompt = ctk.CTkEntry(height=40, width=512, text_font=(
    "Arial", 20), text_color="black", fg_color="white")
prompt.place(x=10, y=10)

# Placeholder frame for image result generated
lmain = ctk.CTkLabel(height=512, width=512)
lmain.place(x=10, y=110)

# Placeholder frame for the text input
ltext = ctk.CTkLabel(height=100, width=512, text="TEST", text_font=(
    "Arial", 20), text_color="white", fg_color="blue")
ltext.place(x=10, y=600)

# Button for creating pdf
create = ctk.CTkButton(height=40, width=120, text_font=(
    "Arial", 20), text_color="white", fg_color="blue", command=generate_pdf)
create.configure(text="Create PicTales")
create.place(x=206, y=800)

# Button for saving image
save_image = ctk.CTkButton(height=40, width=120, text_font=(
    "Arial", 20), text_color="white", fg_color="blue", command=generate_save)
save_image.configure(text="Save Image")
save_image.place(x=206, y=725)

# ___________________________________________________________________________ DRIVER CODE ___________________________________________________________________________
# Get text input prompts again by automatically restarting the app
app.mainloop()
