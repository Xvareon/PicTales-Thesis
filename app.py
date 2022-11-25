# Python packages and dependencies are needed for the application to run. Installed through PIP in VSCode terminal (Todo: automatically install these with the app with PyInstaller)

# ___________________________________________________________________________ DEPENDENCIES ___________________________________________________________________________
# Import Tkinter for Python UI
import tkinter as tk

# Import CustomTkinter for additional Tkinter configurations
import customtkinter as ctk

# Import Pillow or PIL for image configurations in Tkinter
from PIL import ImageTk

# Import auth_token for Token authentication that will be mostly used from tokens in Huggingface website account
from authtoken import auth_token

# Import Pytorch for the neural networks used in machine learning and AI
import torch
from torch import autocast

# Import StableDiffusionPipeline for the stable diffusion methods that are used in the local GPU.
from diffusers import StableDiffusionPipeline

# ___________________________________________________________________________ GLOBAL VARIABLES ___________________________________________________________________________
# Globalized some of the variables to avoid parameter mishap
global device
global pipe
global prompt
global lmain
global ltext

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


def generate():  # Function to generate the images from the text prompt

    global img  # For storing the image to avoid garbage collection

    global text_input  # For storing the text input to transfer to the Picture Book PDF

    # Uses the GPU to process the dataset through the model and get the image result
    with autocast(device):

        image = pipe(prompt.get(), guidance_scale=10)[
            "images"][0]  # Variable that contains the image result. ("images" was previously labeled as "sample")
        text_input = prompt.get()

    # Displays the text input in the Tkinter UI after generation
    img = ImageTk.PhotoImage(image)
    ltext.configure(text=text_input)
    ltext.update()

    # Displays the image in the Tkinter UI after generation
    lmain.configure(image=img)
    lmain.update()

    # Saves the image
    image.save('generatedimage.png')


# ___________________________________________________________________________ TKINTER UI ___________________________________________________________________________
# Create the app
app = tk.Tk()
app.title("Pictales")
app.geometry("532x732")
ctk.set_appearance_mode("dark")

# Button for submitting the text input prompts and its configurations via position
trigger = ctk.CTkButton(height=40, width=120, text_font=(
    "Arial", 20), text_color="white", fg_color="blue", command=generate)
trigger.configure(text="Generate")
trigger.place(x=206, y=60)

# Tkinter UI for the prompt textbox
prompt = ctk.CTkEntry(height=40, width=512, text_font=(
    "Arial", 20), text_color="black", fg_color="white")
prompt.place(x=10, y=10)

# Placeholder frame for image result generated
lmain = ctk.CTkLabel(height=512, width=512)
lmain.place(x=10, y=110)

# Placeholder frame for the text input
ltext = ctk.CTkLabel(height=100, width=512, text="TEST", text_font=(
    "Arial", 20), text_color="black", fg_color="red")
ltext.place(x=10, y=600)

# ___________________________________________________________________________ DRIVER CODE ___________________________________________________________________________
# Get text input prompts again by automatically restarting the app after the image was generated (If another image gets generated,
# it replaces the previous image in the directory!!!)
app.mainloop()
